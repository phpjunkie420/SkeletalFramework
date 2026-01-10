import inspect
import textwrap
from typing import TypedDict, Unpack,overload

from skeletal_framework.utilities.terminal import Terminal


class _X(TypedDict):
    x: int


class _Y(TypedDict):
    y: int


class _Position(_X, _Y): ...


class _RequiredAttributes(TypedDict):
    width: int
    text: str
    ctrl_id: int


class _OptionalAttributes(TypedDict, total = False):
    font_size: int


class _Kwargs(_Position, _RequiredAttributes, _OptionalAttributes): ...


class Checkbox:
    def __init__(self, **kwargs: Unpack[_Kwargs]):
        # REQUIRED Fields
        self._class_name = self.__class__.__name__
        self._x = kwargs['x']
        self._y = kwargs['y']
        self._width = kwargs['width']
        self._text = kwargs['text']
        self._ctrl_id = kwargs['ctrl_id']

        # OPTIONAL Fields
        self._font_size = kwargs.get('font_size', 10)

        # --- Console Output Setup ---
        self._mro_chain_source: str | None = None

        keys = list(self.__dict__)
        self._max_length = max(len(key) for key in keys) + 2
        self._mro_chain_source = self._build_mro_report()

        self._terminal = Terminal()

        labels = {}
        for key in keys:
            styled_text = f"[bold sand]{key}[/] [red]:[/]"
            formatted_label = self._terminal.format(styled_text, width = self._max_length, justify = 'right')
            labels[key] = formatted_label

        # Print properties
        for k, v in self.__dict__.items():
            if k in labels:
                if k == '_mro_chain_source':
                    self._terminal.print(f'{labels[k]} {v}')
                else:
                    self._terminal.print(f'{labels[k]} [bold white]{v}[/]')

        self._terminal.print('\n', f'[sand]{'─' * 100}[/]', '\n', sep = '')

    def _build_mro_report(self) -> str:
        report_lines = []

        mro = [cls for cls in inspect.getmro(self.__class__) if cls is not object]

        indent = " " * (self._max_length + 1)
        for i, cls in enumerate(mro):
            source = self.get_class_source(cls)
            if source:
                source_lines = source.splitlines()
                for line in source_lines:
                    if 'self._class_name' in line:
                        continue

                    report_lines.append(f'[bold white]{line}[/]')

                report_lines.append(f'[sand]{'─' * 52}[/]')

        for index, line in enumerate(report_lines):
            if index:
                report_lines[index] = f'{indent}{line}'

        return "\n".join(report_lines[:-1])

    @staticmethod
    def get_class_source(cls: type) -> str:
        try:
            lines, _ = inspect.getsourcelines(cls)
        except (OSError, TypeError):
            return ""

        has_super_call = False
        for line in lines:
            stripped = line.strip()
            if 'super().__init__' in stripped and 'if' not in stripped:
                has_super_call = True
                break

        if not has_super_call:
            lines = lines[:2]
            lines.append(f'{' ' * 8}...')

        return textwrap.dedent(''.join(lines))


class _KwargsX(_X, _RequiredAttributes, _OptionalAttributes): ...
class _KwargsY(_Y, _RequiredAttributes, _OptionalAttributes): ...


# --- Parent Classes ---
class _ShowDesktopIcon(Checkbox):
    def __init__(self, **kwargs: Unpack[_Kwargs]):
        super().__init__(**kwargs)


class _LeftColumnIcon(_ShowDesktopIcon):
    @overload
    def __init__(self, y: int, width: int, text: str, ctrl_id: int): ...

    def __init__(self, **kwargs: Unpack[_Kwargs]):
        super().__init__(x = 20, **kwargs)


class _RightColumnIcon(_ShowDesktopIcon):
    def __init__(self, **kwargs: Unpack[_KwargsY]):
        super().__init__(x = 230, **kwargs)


# --- Child Classes ---
class ShowComputerIcon(_LeftColumnIcon):
    def __init__(self):
        super().__init__(
            y = 25,
            width = 150,
            text = "Show Computer Icon",
            ctrl_id = 300
        )


class ShowUserFolderIcon(_LeftColumnIcon):
    def __init__(self):
        super().__init__(
            y = 45,
            width = 170,
            text = "Show User's Folder Icon",
            ctrl_id = 301
        )


class ShowNetworkIcon(_RightColumnIcon):
    def __init__(self):
        super().__init__(
            y = 25,
            width = 150,
            text = "Show Network Icon",
            ctrl_id = 302
        )


class ShowRecycleBinIcon(_RightColumnIcon):
    def __init__(self):
        super().__init__(
            y = 45,
            width = 170,
            text = "Show Recycle Bin Icon",
            ctrl_id = 303
        )


# --- Parent Class ---
class _ThemeChangesOption(Checkbox):
    def __init__(self, **kwargs: Unpack[_KwargsX]):
        super().__init__(y = 395, **kwargs)


# --- Child Classes ---
class ThemeChangesDesktopIcons(_ThemeChangesOption):
    def __init__(self):
        super().__init__(
            x = 10,
            width = 200,
            text = "Allow themes to change desktop icons",
            ctrl_id = 304,
        )


class ThemeChangesMousePointers(_ThemeChangesOption):
    def __init__(self):
        super().__init__(
            x = 218,
            width = 205,
            text = "Allow themes to change mouse pointers",
            ctrl_id = 305,
        )


if __name__ == '__main__':
    ShowComputerIcon()
    ShowComputerIcon()
    ShowUserFolderIcon()
    ShowNetworkIcon()
    ShowRecycleBinIcon()
    ThemeChangesDesktopIcons()
    ThemeChangesMousePointers()
