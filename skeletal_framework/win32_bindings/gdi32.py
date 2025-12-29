import ctypes
from ctypes import wintypes

from win32_bindings.errcheck import errcheck_bool

__all__ = [
    'CreateSolidBrush',
    'DeleteObject',
    'SetBkColor', 'SetTextColor'
]

gdi32 = ctypes.WinDLL('gdi32', use_last_error = True)

# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createsolidbrush
# HBRUSH CreateSolidBrush(
#   [in] COLORREF color
# );
_CreateSolidBrush = gdi32.CreateSolidBrush
_CreateSolidBrush.argtypes = [wintypes.COLORREF]
_CreateSolidBrush.restype = wintypes.HBRUSH


def CreateSolidBrush(color: int) -> int:
    return _CreateSolidBrush(color)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-deleteobject
# BOOL DeleteObject(
#   [in] HGDIOBJ ho
# );
_DeleteObject = gdi32.DeleteObject
_DeleteObject.argtypes = [wintypes.HGDIOBJ]
_DeleteObject.restype = wintypes.BOOL
_DeleteObject.errcheck = errcheck_bool


def DeleteObject(ho: int) -> bool:
    return _DeleteObject(ho)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-setbkcolor
# COLORREF SetBkColor(
#   [in] HDC      hdc,
#   [in] COLORREF color
# );
_SetBkColor = gdi32.SetBkColor
_SetBkColor.argtypes = [wintypes.HDC, wintypes.COLORREF]
_SetBkColor.restype = wintypes.COLORREF


def SetBkColor(hdc: int, color: int) -> int:
    return _SetBkColor(hdc, color)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-settextcolor
# COLORREF SetTextColor(
#   [in] HDC      hdc,
#   [in] COLORREF color
# );
_SetTextColor = gdi32.SetTextColor
_SetTextColor.argtypes = [wintypes.HDC, wintypes.COLORREF]
_SetTextColor.restype = wintypes.COLORREF


def SetTextColor(hdc: int, color: int) -> int:
    return _SetTextColor(hdc, color)
