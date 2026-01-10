import os
import sys
import winreg
from collections.abc import Generator
from dataclasses import dataclass
from enum import Enum
from typing import Any, TYPE_CHECKING

__all__ = [
    'RegistryKey',
]

RegValueType = tuple[str, str | int | bytes | list, int]


@dataclass
class RegistryValue:
    name: str
    value: Any
    type: int  # e.g., winreg.REG_SZ, winreg.REG_DWORD

    @property
    def raw(self) -> tuple[str, Any, int]:
        """Returns the legacy tuple format expected by some winreg functions."""
        return self.name, self.value, self.type

    @property
    def type_str(self) -> str:
        """Debug helper to see the type name (e.g., 'REG_SZ')."""
        # Create a reverse lookup map for winreg constants
        types = {v: k for k, v in vars(winreg).items() if k.startswith('REG_')}
        return types.get(self.type, "UNKNOWN")


class RegistryMeta(type):

    @property
    def HKEY_CURRENT_USER(cls) -> RegistryKey:
        """Factory: Returns a RegistryKey rooted in HKEY_CURRENT_USER."""
        return cls(winreg.HKEY_CURRENT_USER, '')

    @property
    def HKEY_LOCAL_MACHINE(cls) -> RegistryKey:
        """Factory: Returns a RegistryKey rooted in HKEY_LOCAL_MACHINE."""
        return cls(winreg.HKEY_LOCAL_MACHINE, '')

    @property
    def HKEY_CLASSES_ROOT(cls) -> RegistryKey:
        """Factory: Returns a RegistryKey rooted in HKEY_CLASSES_ROOT."""
        return cls(winreg.HKEY_CLASSES_ROOT, '')

    @property
    def HKEY_USERS(cls) -> RegistryKey:
        """Factory: Returns a RegistryKey rooted in HKEY_USERS."""
        return cls(winreg.HKEY_USERS, '')


class RegistryKey(metaclass = RegistryMeta):
    if TYPE_CHECKING:
        # These are "Type Stubs".
        # This block is for Static Analysis (PyCharm/VS Code) only.
        # Python ignores them at runtime (because TYPE_CHECKING is False).
        # It resolves type mismatches and suppresses false-positive IDE warnings.
        # PyCharm/VS Code reads them and overrides their inference.
        HKEY_CURRENT_USER: RegistryKey
        HKEY_LOCAL_MACHINE: RegistryKey
        HKEY_CLASSES_ROOT: RegistryKey
        HKEY_USERS: RegistryKey

    class _Scan(Enum):
        """Defines the configuration for enumerating keys vs. values."""
        Keys = (0, winreg.EnumKey)
        Values = (1, winreg.EnumValue)

    """A general-purpose class for interacting with a Windows Registry key."""
    def __init__(self, hkey: int, path: str):
        """Initializes the RegistryKey with a hive and a path."""
        cleaned_path = path.replace('/', '\\')
        cleaned_path = cleaned_path.strip('\\')

        self._hkey = hkey
        self._path = cleaned_path

    def __contains__(self, subkey: str):
        try:
            with winreg.OpenKey(self._hkey, f"{self._path}\\{subkey}"):
                return True
        except OSError:
            return False

    # 2. Modern Path Protocol (Allows usage in os.path.*)
    def __fspath__(self):
        return self._path

    # 3. Hashing (Allows use in sets/dicts)
    def __hash__(self):
        return hash((self._hkey, self._path))

    def __eq__(self, other):
        if isinstance(other, RegistryKey):
            return self._hkey == other._hkey and self._path == other._path
        return self._path == other

    # 4. Length
    def __len__(self):
        return len(self._path)

    # 5. String Representation
    def __str__(self):
        return self._path

    def __repr__(self):
        return f"<{self.__class__.__name__} path='{self._path}'>"

    def __truediv__(self, sub_path):
        """Enables using the / operator to create a new subkey path."""
        new_path = f'{self._path}\\{sub_path}'
        return RegistryKey(
            hkey = self._hkey, path = new_path
        )

    def get_value(self, value_name: str) -> RegistryValue | None:
        """Reads a value and returns a typed RegistryValue object."""
        try:
            with winreg.OpenKey(self._hkey, self._path) as key:
                # QueryValueEx returns (value_data, type_int)
                data, reg_type = winreg.QueryValueEx(key, value_name)

                # OPTIONAL: You can still choose to expand env vars here
                # or leave it raw. Usually, returning raw is safer for a wrapper class.
                if reg_type == winreg.REG_EXPAND_SZ and isinstance(data, str):
                    data = os.path.expandvars(data)

                return RegistryValue(name = value_name, value = data, type = reg_type)
        except FileNotFoundError:
            return None

    def set_value(self, name_or_obj: str | RegistryValue, value_data: Any = None, value_type: int = None):
        """
        Sets a registry value.
        Usage A (Explicit): set_value(RegistryValue("Key", 1, winreg.REG_DWORD))
        Usage B (Manual):   set_value("Key", 1, winreg.REG_DWORD)
        Usage C (Infer):    set_value("Key", 1) # Guesses REG_DWORD
        """

        # Logic to normalize inputs
        if isinstance(name_or_obj, RegistryValue):
            name = name_or_obj.name
            data = name_or_obj.value
            reg_type = name_or_obj.type
        else:
            name = name_or_obj
            data = value_data

            # If type is provided explicitly, use it. Otherwise, guess.
            if value_type is not None:
                reg_type = value_type
            else:
                # Your original guessing logic goes here
                if isinstance(data, int):
                    reg_type = winreg.REG_DWORD
                elif isinstance(data, str):
                    reg_type = winreg.REG_SZ  # Default to SZ, not EXPAND_SZ unless requested
                else:
                    raise TypeError("Cannot infer registry type. Please specify 'value_type'.")

        # Handle formatting (like your _with_env_vars) logic here
        if reg_type == winreg.REG_EXPAND_SZ and isinstance(data, str):
            data = self._with_env_vars(data)

        with winreg.CreateKeyEx(self._hkey, self._path, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, name, 0, reg_type, data)

    def delete_value(self, value_name):
        """Deletes a value from the key."""
        with winreg.OpenKey(self._hkey, self._path, 0, winreg.KEY_WRITE) as key:
            winreg.DeleteValue(key, value_name)

    def iter_keys(self) -> Generator[str, None, None]:
        """Yields subkey names."""
        yield from self._enumerate(mode = self._Scan.Keys)

    def iter_values(self) -> Generator[RegValueType, None, None]:
        """Yields value tuples."""
        yield from self._enumerate(mode = self._Scan.Values)

    def walk(self) -> Generator[tuple['RegistryKey', list[str], list[RegValueType]], None, None]:
        print_in_red = '\x1b[1;38;2;255;0;0m{text}\x1b[0m'
        try:
            subkey_names = list(self.iter_keys())
            values = list(self.iter_values())

            yield self, subkey_names, values

            for subkey_name in subkey_names:
                yield from (self / subkey_name).walk()

        except FileNotFoundError:
            return
        except PermissionError as e:
            print(print_in_red.format(text = e))
        except KeyboardInterrupt:
            print(print_in_red.format(text = 'OPERATION ABORTED BY USER'))
            sys.exit()

    def _enumerate(self, mode: _Scan) -> Generator[str | RegValueType, None, None]:
        """Internal helper to yield items based on the given mode."""
        with winreg.OpenKey(self._hkey, self._path) as key:
            # Unpack the tuple from the Enum
            index, function = mode.value

            # Use the index for QueryInfoKey
            count = winreg.QueryInfoKey(key)[index]

            for i in range(count):
                try:
                    # Use the function (EnumKey or EnumValue) stored in the Enum
                    yield function(key, i)
                except FileNotFoundError:
                    continue

    @staticmethod
    def _with_env_vars(path: str) -> str:
        PREFERRED_CASING = {
            "USERPROFILE": "UserProfile",
            "SYSTEMROOT": "SystemRoot",
            "SYSTEMDRIVE": "SystemDrive",
            "HOMEDRIVE": "HomeDrive",
            "HOMEPATH": "HomePath",
            "PROGRAMFILES": "ProgramFiles",
            "PROGRAMFILES(X86)": "ProgramFiles(x86)",
            "APPDATA": "AppData",
            "LOCALAPPDATA": "LocalAppData",
            "WINDIR": "WinDir",
            "TEMP": "Temp",
            "TMP": "Tmp",
        }

        normalized_path = os.path.normcase(path)
        env_vars = sorted(os.environ.items(), key=lambda item: len(item[1]), reverse=True)

        for name, value in env_vars:
            if not value:
                continue

            normalized_value = os.path.normcase(value)

            if normalized_path.startswith(normalized_value):
                display_name = PREFERRED_CASING.get(name.upper(), name)
                rest_of_path = path[len(value):]
                return f"%{display_name}%{rest_of_path}"

        return path


# --- EXAMPLE USAGE ---
if __name__ == '__main__':
    for subkeys in RegistryKey.HKEY_CURRENT_USER.iter_keys():
        print(subkeys)

    print('\n', '-' * 20, '\n', sep = '')

    for subkeys in RegistryKey.HKEY_CURRENT_USER.iter_values():
        print(subkeys)

    print('\n', '-' * 20, '\n', sep = '')

    basekey = RegistryKey.HKEY_LOCAL_MACHINE / 'Software/Microsoft/Windows/CurrentVersion/Explorer/DriveIcons'
    for subkey in basekey.iter_keys():
        subkey = basekey / subkey / 'DefaultIcon'
        if (value := subkey.get_value(value_name = '')) is not None:
            print(f'{subkey}', f'{value}')
