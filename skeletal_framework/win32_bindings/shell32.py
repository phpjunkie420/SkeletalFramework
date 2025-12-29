import ctypes
from ctypes import wintypes

__all__ = [
    'IsUserAnAdmin',
    'ShellExecute'
]

IN = 1
OUT = 2
INOUT = 3

# region Win32 Bindings
shell32 = ctypes.WinDLL('shell32', use_last_error = True)

# https://learn.microsoft.com/en-us/windows/win32/api/shlobj_core/nf-shlobj_core-isuseranadmin
# BOOL IsUserAnAdmin();
_IsUserAnAdmin = ctypes.WINFUNCTYPE(
    wintypes.BOOL
)(
    ('IsUserAnAdmin', shell32),
    ()
)


# https://learn.microsoft.com/en-us/windows/win32/api/shellapi/nf-shellapi-shellexecutew
# HINSTANCE ShellExecuteW(
#   [in, optional] HWND    hwnd,
#   [in, optional] LPCWSTR lpOperation,
#   [in]           LPCWSTR lpFile,
#   [in, optional] LPCWSTR lpParameters,
#   [in, optional] LPCWSTR lpDirectory,
#   [in]           INT     nShowCmd
# );
ShellExecuteW = ctypes.WINFUNCTYPE(
    wintypes.HINSTANCE,
    wintypes.HWND,
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.INT
)(
    ('ShellExecuteW', shell32),
    (
        (IN, "hwnd"),
        (IN, "lpOperation"),
        (IN, "lpFile"),
        (IN, "lpParameters"),
        (IN, "lpDirectory"),
        (IN, "nShowCmd"),
    )
)
# endregion


def IsUserAnAdmin() -> bool:
    try:
        return _IsUserAnAdmin() > 0
    except AttributeError:
        return False


def ShellExecute(
    *,
    hwnd: int | None = None,
    lpOperation: str | None = None,
    lpFile: str,
    lpParameters: str | None = None,
    lpDirectory: str | None = None,
    nShowCmd: int
) -> int:
    ret = ShellExecuteW(hwnd, lpOperation, lpFile, lpParameters, lpDirectory, nShowCmd)
    if ret <= 32:
        raise ctypes.WinError(ctypes.get_last_error())
    return ret
