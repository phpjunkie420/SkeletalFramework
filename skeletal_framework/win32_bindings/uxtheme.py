import ctypes
from ctypes import wintypes

from win32_bindings.errcheck import errcheck_bool, call_with_last_error_check

__all__ = [
    'SetWindowTheme'
]

uxtheme = ctypes.WinDLL('uxtheme', use_last_error=True)

# https://learn.microsoft.com/en-us/windows/win32/api/uxtheme/nf-uxtheme-setwindowtheme
# HRESULT SetWindowTheme(
#   [in] HWND    hwnd,
#   [in] LPCWSTR pszSubAppName,
#   [in] LPCWSTR pszSubIdList
# );
_SetWindowTheme = uxtheme.SetWindowTheme
_SetWindowTheme.argtypes = [wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR]
_SetWindowTheme.restype = ctypes.HRESULT


def SetWindowTheme(hwnd: int, pszSubAppName: str | None, pszSubIdList: str | None) -> int:
    return _SetWindowTheme(hwnd, pszSubAppName, pszSubIdList)
