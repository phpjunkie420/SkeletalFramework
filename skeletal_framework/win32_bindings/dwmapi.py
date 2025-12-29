import ctypes
from ctypes import wintypes
from enum import IntEnum

from skeletal_framework.win32_bindings.errcheck import errcheck_hresult

__all__ = [
    'DwmSetWindowAttribute',
    'DWMWINDOWATTRIBUTE',
    'DWM_WINDOW_CORNER_PREFERENCE'
]

IN = 1
OUT = 2
INOUT = 3

dwmapi = ctypes.WinDLL('dwmapi', use_last_error=True)


class DWMWINDOWATTRIBUTE(IntEnum):
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    DWMWA_WINDOW_CORNER_PREFERENCE = 33
    DWMWA_BORDER_COLOR = 34
    DWMWA_CAPTION_COLOR = 35
    DWMWA_TEXT_COLOR = 36


class DWM_WINDOW_CORNER_PREFERENCE(IntEnum):
    DWMWCP_DEFAULT = 0,
    DWMWCP_DONOTROUND = 1,
    DWMWCP_ROUND = 2,
    DWMWCP_ROUNDSMALL = 3


# https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/nf-dwmapi-dwmsetwindowattribute
# HRESULT DwmSetWindowAttribute(
#   [in] HWND    hwnd,
#   [in] DWORD   dwAttribute,
#   [in] LPCVOID pvAttribute,
#   [in] DWORD   cbAttribute
# );
_DwmSetWindowAttribute = ctypes.WINFUNCTYPE(
    ctypes.HRESULT,
    wintypes.HWND,
    wintypes.DWORD,
    wintypes.LPCVOID,
    wintypes.DWORD
)(
    ('DwmSetWindowAttribute', dwmapi),
    (
        (IN, "hwnd"),
        (IN, "dwAttribute"),
        (IN, "pvAttribute"),
        (IN, "cbAttribute"),
    )
)
_DwmSetWindowAttribute.errcheck = errcheck_hresult


def DwmSetWindowAttribute(hwnd: int, dwAttribute: DWMWINDOWATTRIBUTE, pvAttribute: int | bool = True) -> int:
    """
    Sets the value of a Desktop Window Manager (DWM) non-client rendering attribute for a window.

    Args:
        hwnd (int): The handle to the window for which the attribute value is to be set.
        dwAttribute (int): A flag describing which value to set, specified as a value of the DWMWINDOWATTRIBUTE enumeration.
                           Defaults to DWMWA_USE_IMMERSIVE_DARK_MODE (20).
        pvAttribute (int | bool): The value to set. For DWMWA_USE_IMMERSIVE_DARK_MODE, this is a BOOL (True/1 or False/0).
                                  Defaults to True.

    Returns:
        int: If the function succeeds, it returns S_OK. Otherwise, it returns an HRESULT error code.
    """
    val = ctypes.c_int(pvAttribute)
    return _DwmSetWindowAttribute(hwnd, dwAttribute, ctypes.byref(val), ctypes.sizeof(val))
