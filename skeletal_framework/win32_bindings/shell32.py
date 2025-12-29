import ctypes
from ctypes import wintypes

__all__ = [
    'IsUserAnAdmin',
    'ShellExecute'
]

# region Win32 Bindings
shell32 = ctypes.WinDLL('shell32', use_last_error = True)

# BOOL IsUserAnAdmin();
_IsUserAnAdmin = shell32.IsUserAnAdmin
_IsUserAnAdmin.argtypes = []
_IsUserAnAdmin.restype = wintypes.BOOL

# HINSTANCE ShellExecuteW(
#   [in, optional] HWND    hwnd,
#   [in, optional] LPCWSTR lpOperation,
#   [in]           LPCWSTR lpFile,
#   [in, optional] LPCWSTR lpParameters,
#   [in, optional] LPCWSTR lpDirectory,
#   [in]           INT     nShowCmd
# );
_ShellExecute = shell32.ShellExecuteW
_ShellExecute.argtypes = [wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.INT]
_ShellExecute.restype = wintypes.HINSTANCE
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
    return _ShellExecute(hwnd, lpOperation, lpFile, lpParameters, lpDirectory, nShowCmd)
