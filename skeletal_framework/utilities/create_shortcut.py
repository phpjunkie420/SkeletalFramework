import ctypes
import os
import sys
import time
from collections.abc import Callable
from ctypes import wintypes
from os import startfile
from pathlib import Path
from threading import Thread
from typing import Any, TYPE_CHECKING


from comtypes.client import CreateObject

from skeletal_framework.win32_bindings.wsh_interfaces import CLSID_WScriptShell, IWshShell3, IWshShortcut

# --- 1. COM Constants ---
COINIT_APARTMENTTHREADED = 0x2
COINIT_DISABLE_OLE1DDE = 0x4

# --- 2. ShellExecute Constants ---
SEE_MASK_INVOKEIDLIST = 0x0000000C
SW_SHOW = 5

IN = 1

SHELL32 = ctypes.WinDLL('Shell32', use_last_error = True)
USER32 = ctypes.WinDLL('User32', use_last_error = True)


def main():
    basepath = Path(__file__).parent.parent.resolve()
    output_folder = basepath / 'scratches'

    if not output_folder.exists():
        output_folder.mkdir(parents = True, exist_ok = True)

    filename = output_folder / 'hello_world.lnk'
    filename.unlink(missing_ok = True)

    icon_file = basepath / 'images' / 'Python.ico'

    script = output_folder / 'hello_world.py'
    script.write_text("print('Hello World')")

    shell = CreateObject(CLSID_WScriptShell, interface = IWshShell3)

    terminal = r'%LocalAppData%\Microsoft\WindowsApps\wt.exe'
    arguments = f'-d "{output_folder}" --title "Command Prompt" cmd.exe /k "{sys.executable}" {script}'

    shortcut: IWshShortcut = shell.CreateShortcut(str(filename))
    shortcut.TargetPath = terminal
    shortcut.Arguments = arguments
    shortcut.WorkingDirectory = str(output_folder)
    shortcut.IconLocation = str(icon_file)
    shortcut.Save()

    show_file_properties(filename)
    startfile(filepath = filename, operation = 'open', cwd = output_folder)

    thread = Thread(target = wait_for_properties_to_close)
    thread.start()
    thread.join()


def show_file_properties(file_path: Path):
    success = ShellExecuteEx(
        pExecInfo = SHELLEXECUTEINFO(
            fMask = SEE_MASK_INVOKEIDLIST,
            lpFile = str(file_path),
            lpVerb = "properties",
            nShow = SW_SHOW,
        )
    )

    if not success:
        print(f"Failed to open properties. Error: {ctypes.GetLastError()}")


def wait_for_properties_to_close(timeout = 5):
    my_pid = os.getpid()
    target_hwnd = None
    start_time = time.monotonic()

    print(f"Scanning for Properties dialog in PID {my_pid}...")

    # --- Phase 1: Hunt for the Window ---
    # We retry for a few seconds because the window takes time to animate/appear
    while time.monotonic() - start_time < timeout:
        @WNDENUMPROC
        def find_window_callback(hwnd, lParam):  # noqa
            def get_pid(hwnd: int) -> tuple[int, int]:
                pid = wintypes.DWORD()
                tid = GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

                return tid, pid.value

            # 1. Check if this window belongs to our Python process
            _, pid = get_pid(
                hwnd = hwnd
            )

            if pid != my_pid:
                return True  # Not ours, keep looking

            # 2. Check if it is visible (optimization)
            if not IsWindowVisible(hwnd):
                return True

            # 3. Check the Class Name
            class_name = GetClassName(hwnd)

            if class_name == "#32770":
                nonlocal target_hwnd
                target_hwnd = hwnd
                return False  # Stop enumerating, we found it!

            return True

        # Run the search
        EnumWindows(find_window_callback, 0)

        if target_hwnd:
            break

        time.sleep(0.1)

    if not target_hwnd:
        print("Could not find the Properties window (Did it open?). Exiting.")
        return

    # --- Phase 2: The Wait Loop ---
    print("Properties dialog found! Waiting for you to close it...")

    # While the window handle is still valid, we sleep
    while IsWindow(target_hwnd):
        time.sleep(0.1)

    print("Dialog closed detected.")


_WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)


def WNDENUMPROC(func: Callable[..., Any]) -> Any:
    return _WNDENUMPROC(func)


class SHELLEXECUTEINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("fMask", wintypes.ULONG),
        ("hwnd", wintypes.HANDLE),
        ("lpVerb", wintypes.LPCWSTR),
        ("lpFile", wintypes.LPCWSTR),
        ("lpParameters", wintypes.LPCWSTR),
        ("lpDirectory", wintypes.LPCWSTR),
        ("nShow", ctypes.c_int),
        ("hInstApp", wintypes.HINSTANCE),
        ("lpIDList", ctypes.c_void_p),
        ("lpClass", wintypes.LPCWSTR),
        ("hkeyClass", wintypes.HKEY),
        ("dwHotKey", wintypes.DWORD),
        ("hIcon", wintypes.HANDLE),
        ("hProcess", wintypes.HANDLE),
    ]

    def __init__(
            self,
            fMask: int = 0,
            hwnd: int = 0,
            lpVerb: str = None,
            lpFile: str = None,
            lpParameters: str = None,
            lpDirectory: str = None,
            nShow: int = 0,
            hInstApp: int = 0,
            lpIDList: int = 0,
            lpClass: str = None,
            hkeyClass: int = 0,
            dwHotKey: int = 0,
            hIcon: int = 0,
            hProcess: int = 0,
    ):
        super().__init__()
        self.cbSize = ctypes.sizeof(self)
        self.fMask = fMask
        self.hwnd = hwnd
        self.lpVerb = lpVerb
        self.lpFile = lpFile
        self.lpParameters = lpParameters
        self.lpDirectory = lpDirectory
        self.nShow = nShow
        self.hInstApp = hInstApp
        self.lpIDList = lpIDList
        self.lpClass = lpClass
        self.hkeyClass = hkeyClass
        self.dwHotKey = dwHotKey
        self.hIcon = hIcon
        self.hProcess = hProcess


if TYPE_CHECKING:
    # @formatter:off
    def GetClassNameW(hWnd: int, lpClassName: Any, nMaxCount: int) -> int: ...  # noqa
    def IsWindow(hWnd: int) -> bool: ...                                        # noqa
    def EnumWindows(lpEnumFunc: _WNDENUMPROC, lParam) -> bool: ...              # noqa
    def GetWindowThreadProcessId(hWnd: int, lpdwProcessId: Any) -> int: ...     # noqa
    def IsWindowVisible(hWnd: int) -> bool: ...                                 # noqa
    # @formatter:on

else:
    GetClassNameW = ctypes.WINFUNCTYPE(
        ctypes.c_int,
        wintypes.HWND,
        wintypes.LPWSTR,
        ctypes.c_int
    )(
        ('GetClassNameW', USER32),
        (
            (IN, 'hWnd'),
            (IN, 'lpClassName'),
            (IN, 'nMaxCount')
        )
    )

    IsWindow = ctypes.WINFUNCTYPE(
        wintypes.BOOL,
        wintypes.HWND
    )(
        ('IsWindow', USER32),
        (
            (IN, 'hWnd'),
        )
    )

    # Note: WNDENUMPROC is a callback function
    EnumWindows = ctypes.WINFUNCTYPE(
        # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumwindows
        # BOOL EnumWindows(
        #   [in] WNDENUMPROC lpEnumFunc,
        #   [in] LPARAM      lParam
        # );
        wintypes.BOOL,
        _WNDENUMPROC,
        wintypes.LPARAM
    )(
        ('EnumWindows', USER32),
        (
            (IN, 'lpEnumFunc'),
            (IN, 'lParam')
        )
    )

    GetWindowThreadProcessId = ctypes.WINFUNCTYPE(
        # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowthreadprocessid
        # DWORD GetWindowThreadProcessId(
        #   [in]            HWND    hWnd,
        #   [out, optional] LPDWORD lpdwProcessId
        # );
        wintypes.DWORD,
        wintypes.HWND,
        ctypes.POINTER(wintypes.DWORD)
    )(
        ('GetWindowThreadProcessId', USER32),
        (
            (IN, 'hWnd'),
            (IN, 'lpdwProcessId')
        )
    )

    IsWindowVisible = ctypes.WINFUNCTYPE(
        # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-iswindowvisible
        # BOOL IsWindowVisible(
        #   [in] HWND hWnd
        # );
        wintypes.BOOL,
        wintypes.HWND
    )(
        ('IsWindowVisible', USER32),
        (
            (IN, 'hWnd'),
        )
    )

_ShellExecuteEx = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    ctypes.POINTER(SHELLEXECUTEINFO)
)(
    ("ShellExecuteExW", SHELL32),
    (
        (IN, 'pExecInfo'),
    )
)


def GetClassName(hWnd: int) -> str:
    buff = ctypes.create_unicode_buffer(256)
    GetClassNameW(hWnd, buff, 256)
    return buff.value


def ShellExecuteEx(pExecInfo: SHELLEXECUTEINFO) -> bool:
    return bool(_ShellExecuteEx(ctypes.byref(pExecInfo)))


if __name__ == '__main__':
    main()
