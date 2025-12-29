import ctypes
from ctypes import wintypes

from skeletal_framework.win32_bindings.errcheck import errcheck_hresult

__all__ = [
    'SetWindowTheme'
]

IN = 1
OUT = 2
INOUT = 3

uxtheme = ctypes.WinDLL('uxtheme', use_last_error=True)

# https://learn.microsoft.com/en-us/windows/win32/api/uxtheme/nf-uxtheme-setwindowtheme
# HRESULT SetWindowTheme(
#   [in] HWND    hwnd,
#   [in] LPCWSTR pszSubAppName,
#   [in] LPCWSTR pszSubIdList
# );
_SetWindowTheme = ctypes.WINFUNCTYPE(
    ctypes.HRESULT,
    wintypes.HWND,
    wintypes.LPCWSTR,
    wintypes.LPCWSTR
)(
    ('SetWindowTheme', uxtheme),
    (
        (IN, "hwnd"),
        (IN, "pszSubAppName"),
        (IN, "pszSubIdList"),
    )
)
_SetWindowTheme.errcheck = errcheck_hresult


def SetWindowTheme(hwnd: int, pszSubAppName: str | None, pszSubIdList: str | None) -> int:
    return _SetWindowTheme(hwnd, pszSubAppName, pszSubIdList)
