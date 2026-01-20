import ctypes
from ctypes import wintypes
from typing import TYPE_CHECKING

from pyvda import AppView

IN = 1
OUT = 2
INOUT = 3

user32 = ctypes.WinDLL('user32', use_last_error = True)

if TYPE_CHECKING:
    class PAINTSTRUCT(ctypes.Structure):
        hdc: int
        fErase: bool
        rcPaint: wintypes.RECT
        fRestore: bool
        fIncUpdate: bool
        rgbReserved: ctypes.Array[ctypes.c_byte]
else:
    class PAINTSTRUCT(ctypes.Structure):
        _fields_ = [
            ("hdc", wintypes.HDC),
            ("fErase", wintypes.BOOL),
            ("rcPaint", wintypes.RECT),
            ("fRestore", wintypes.BOOL),
            ("fIncUpdate", wintypes.BOOL),
            ("rgbReserved", (ctypes.c_byte * 32))
        ]

if TYPE_CHECKING:
    # noinspection PyUnusedLocal
    def BeginPaint(hWnd: int) -> PAINTSTRUCT: ...
else:
    BeginPaint = ctypes.WINFUNCTYPE(
        wintypes.HDC,
        wintypes.HWND,
        ctypes.POINTER(PAINTSTRUCT)
    )(
        ('BeginPaint', user32),
        (
            (IN, "hWnd"),
            (OUT, "lpPaint"),
        )
    )


ps = BeginPaint(AppView.current().hwnd)
print(ps.hdc)
