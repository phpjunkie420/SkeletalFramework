import ctypes
from ctypes import wintypes

from pyvda import AppView

IN = 1
OUT = 2
INOUT = 3

user32 = ctypes.WinDLL('user32', use_last_error = True)


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
    ('GetWindowTextW', user32),
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
    ('GetWindowTextLengthW', user32),
    (
        (IN, "hWnd"),
    )
)


def GetWindowText(hWnd: int) -> str:
    text_len = GetWindowTextLengthW(hWnd) + 1
    text_buffer = ctypes.create_unicode_buffer(text_len)

    GetWindowTextW(hWnd, text_buffer, text_len)
    return text_buffer.value


print(GetWindowText(AppView.current().hwnd))
