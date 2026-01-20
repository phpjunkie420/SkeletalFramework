# win32_bindings\user32.py

import ctypes
from ctypes import wintypes
from typing import TYPE_CHECKING

IN = 1
OUT = 2
INOUT = 3

USER32 = ctypes.WinDLL('user32', use_last_error = True)

# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowtextw
# int GetWindowTextW(
#   [in]  HWND   hWnd,
#   [out] LPWSTR lpString,
#   [in]  int    nMaxCount
# );
GetWindowTextW = ctypes.WINFUNCTYPE(
    wintypes.INT,
    wintypes.HWND,
    wintypes.LPWSTR,
    wintypes.INT
)(
    ('GetWindowTextW', USER32),
    (
        (IN, "hWnd"),
        (IN, "lpString"),
        (IN, "nMaxCount"),
    )
)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowtextlengthw
# int GetWindowTextLengthW(
#   [in] HWND hWnd
# );
GetWindowTextLengthW = ctypes.WINFUNCTYPE(
    wintypes.INT,
    wintypes.HWND
)(
    ('GetWindowTextLengthW', USER32),
    (
        (IN, "hWnd"),
    )
)


def GetWindowText(hWnd: int) -> str:
    text_len = GetWindowTextLengthW(hWnd) + 1
    text_buffer = ctypes.create_unicode_buffer(text_len)

    GetWindowTextW(hWnd, text_buffer, text_len)
    return text_buffer.value


# --- Static Analysis Stubs (What the IDE sees) ---
# These are only seen by the IDE, not at runtime
if TYPE_CHECKING:
    def GetWindowTextW(hWind: int, lpString: ctypes.Array[ctypes.c_wchar] | None, nMaxCount: int) -> str: ...  # noqa E501
    def GetWindowTextLengthW(hWnd: int) -> int: ...  # noqa E501

__all__ = [
    'GetWindowText', 'GetWindowTextW', 'GetWindowTextLengthW'
]
