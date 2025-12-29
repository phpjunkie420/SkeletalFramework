import ctypes
from ctypes import wintypes
import weakref

import win32con

from skeletal_framework.win32_bindings.errcheck import errcheck_bool

__all__ = [
    'BitBlt',
    'CreateBitmap', 'CreateCompatibleBitmap', 'CreateCompatibleDC', 'CreateDIBSection', 'CreateFont', 'CreateFontIndirect',
    'CreatePen', 'CreateRoundRectRgn', 'CreateSolidBrush',
    'DeleteDC', 'DeleteObject',
    'Ellipse', 'ExtTextOut',
    'GetStockObject', 'GetTextExtentPoint32',
    'FrameRgn',
    'LineTo',
    'MoveToEx',
    'Rectangle', 'RoundRect',
    'SelectClipRgn', 'SelectObject', 'SetBkColor', 'SetBkMode', 'SetDIBits', 'SetPixel', 'SetTextColor',
    'BITMAPINFOHEADER', 'BITMAPINFO', 'GRADIENT_RECT', 'LOGFONT', 'TRIVERTEX',
]

IN = 1
OUT = 2
INOUT = 3

gdi32 = ctypes.WinDLL('gdi32', use_last_error = True)
_dc_objects = weakref.WeakValueDictionary()


class TRIVERTEX(ctypes.Structure):
    _fields_ = [
        ('x', wintypes.LONG),
        ('y', wintypes.LONG),
        ('Red', wintypes.USHORT),
        ('Green', wintypes.USHORT),
        ('Blue', wintypes.USHORT),
        ('Alpha', wintypes.USHORT),
    ]


class GRADIENT_RECT(ctypes.Structure):
    _fields_ = [
        ('UpperLeft', wintypes.ULONG),
        ('LowerRight', wintypes.ULONG),
    ]


class RGBQUAD(ctypes.Structure):
    _fields_ = [
        ("rgbBlue", wintypes.BYTE),
        ("rgbGreen", wintypes.BYTE),
        ("rgbRed", wintypes.BYTE),
        ("rgbReserved", wintypes.BYTE),
    ]


# typedef struct tagBITMAPINFOHEADER {
#   DWORD biSize;
#   LONG  biWidth;
#   LONG  biHeight;
#   WORD  biPlanes;
#   WORD  biBitCount;
#   DWORD biCompression;
#   DWORD biSizeImage;
#   LONG  biXPelsPerMeter;
#   LONG  biYPelsPerMeter;
#   DWORD biClrUsed;
#   DWORD biClrImportant;
# } BITMAPINFOHEADER, *LPBITMAPINFOHEADER, *PBITMAPINFOHEADER;
class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", wintypes.DWORD),
        ("biWidth", wintypes.LONG),
        ("biHeight", wintypes.LONG),
        ("biPlanes", wintypes.WORD),
        ("biBitCount", wintypes.WORD),
        ("biCompression", wintypes.DWORD),
        ("biSizeImage", wintypes.DWORD),
        ("biXPelsPerMeter", wintypes.LONG),
        ("biYPelsPerMeter", wintypes.LONG),
        ("biClrUsed", wintypes.DWORD),
        ("biClrImportant", wintypes.DWORD),
    ]


class LOGFONT(ctypes.Structure):
    _fields_ = [
        ("lfHeight",         wintypes.LONG),
        ("lfWidth",          wintypes.LONG),
        ("lfEscapement",     wintypes.LONG),
        ("lfOrientation",    wintypes.LONG),
        ("lfWeight",         wintypes.LONG),
        ("lfItalic",         wintypes.BYTE),
        ("lfUnderline",      wintypes.BYTE),
        ("lfStrikeOut",      wintypes.BYTE),
        ("lfCharSet",        wintypes.BYTE),
        ("lfOutPrecision",   wintypes.BYTE),
        ("lfClipPrecision",  wintypes.BYTE),
        ("lfQuality",        wintypes.BYTE),
        ("lfPitchAndFamily", wintypes.BYTE),
        ("lfFaceName",       wintypes.WCHAR * win32con.LF_FACESIZE)
    ]

    def __init__(
        self,
        height = -12,
        width = 0,
        escapement = 0,
        orientation = 0,
        weight = win32con.FW_NORMAL,
        italic = False,
        underline = False,
        strikeout = False,
        charset = win32con.DEFAULT_CHARSET,
        out_precision = win32con.OUT_DEFAULT_PRECIS,
        clip_precision = win32con.CLIP_DEFAULT_PRECIS,
        quality = win32con.CLEARTYPE_QUALITY,
        pitch_and_family = (win32con.DEFAULT_PITCH | win32con.FF_DONTCARE),
        face_name = "Segoe UI"
    ):
        """
        win32con.ANTIALIASED_QUALITY
        win32con.CLEARTYPE_QUALITY
        win32con.CLEARTYPE_NATURAL_QUALITY
        win32con.DEFAULT_QUALITY
        win32con.DRAFT_QUALITY
        win32con.NONANTIALIASED_QUALITY
        win32con.PROOF_QUALITY
        """

        super().__init__()

        self.lfHeight = height
        self.lfWidth = width
        self.lfEscapement = escapement
        self.lfOrientation = orientation
        self.lfWeight = weight

        self.lfItalic = 1 if italic else 0
        self.lfUnderline = 1 if underline else 0
        self.lfStrikeOut = 1 if strikeout else 0

        self.lfCharSet = charset
        self.lfOutPrecision = out_precision
        self.lfClipPrecision = clip_precision
        self.lfQuality = quality
        self.lfPitchAndFamily = pitch_and_family

        self.lfFaceName = face_name


# typedef struct tagBITMAPINFO {
#   BITMAPINFOHEADER bmiHeader;
#   RGBQUAD          bmiColors[1];
# } BITMAPINFO, *LPBITMAPINFO, *PBITMAPINFO;
class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ("bmiHeader", BITMAPINFOHEADER),
        ("bmiColors", RGBQUAD * 1)
    ]


# BOOL BitBlt(
#   [in] HDC   hdc,
#   [in] int   x,
#   [in] int   y,
#   [in] int   cx,
#   [in] int   cy,
#   [in] HDC   hdcSrc,
#   [in] int   x1,
#   [in] int   y1,
#   [in] DWORD rop
# );
BitBlt = gdi32.BitBlt
BitBlt.argtypes = [
    wintypes.HDC,    # hdcDest
    ctypes.c_int,    # xDest
    ctypes.c_int,    # yDest
    ctypes.c_int,    # width
    ctypes.c_int,    # height
    wintypes.HDC,    # hdcSrc
    ctypes.c_int,    # xSrc
    ctypes.c_int,    # ySrc
    wintypes.DWORD   # rop
]
BitBlt.restype = wintypes.BOOL

# HBITMAP CreateBitmap(
#   [in] int        nWidth,
#   [in] int        nHeight,
#   [in] UINT       nPlanes,
#   [in] UINT       nBitCount,
#   [in] const VOID *lpBits
# );
CreateBitmap = gdi32.CreateBitmap
CreateBitmap.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p]
CreateBitmap.restype = wintypes.HBITMAP

# HBITMAP CreateCompatibleBitmap(
#   [in] HDC hdc,
#   [in] int cx,
#   [in] int cy
# );
CreateCompatibleBitmap = gdi32.CreateCompatibleBitmap
CreateCompatibleBitmap.argtypes = [wintypes.HDC, ctypes.c_int, ctypes.c_int]
CreateCompatibleBitmap.restype = wintypes.HBITMAP

# HDC CreateCompatibleDC(
#   [in] HDC hdc
# );
CreateCompatibleDC = gdi32.CreateCompatibleDC
CreateCompatibleDC.argtypes = [wintypes.HDC]
CreateCompatibleDC.restype = wintypes.HDC

# HBITMAP CreateDIBSection(
#   [in]  HDC              hdc,
#   [in]  const BITMAPINFO *pbmi,
#   [in]  UINT             usage,
#   [out] VOID             **ppvBits,
#   [in]  HANDLE           hSection,
#   [in]  DWORD            offset
# );
CreateDIBSection = gdi32.CreateDIBSection
CreateDIBSection.argtypes = [
    wintypes.HDC,
    ctypes.POINTER(BITMAPINFO),
    wintypes.UINT,
    ctypes.POINTER(wintypes.LPVOID),  # Correct type for VOID**
    wintypes.HANDLE,
    wintypes.DWORD
]
CreateDIBSection.restype = wintypes.HBITMAP

# HFONT CreateFontW(
#   [in] int     cHeight,
#   [in] int     cWidth,
#   [in] int     cEscapement,
#   [in] int     cOrientation,
#   [in] int     cWeight,
#   [in] DWORD   bItalic,
#   [in] DWORD   bUnderline,
#   [in] DWORD   bStrikeOut,
#   [in] DWORD   iCharSet,
#   [in] DWORD   iOutPrecision,
#   [in] DWORD   iClipPrecision,
#   [in] DWORD   iQuality,
#   [in] DWORD   iPitchAndFamily,
#   [in] LPCWSTR pszFaceName
# );
CreateFont = ctypes.WINFUNCTYPE(
    wintypes.HFONT,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.LPCWSTR,
)(
    ('CreateFontW', gdi32),
    (
        (IN, "cHeight"),
        (IN, "cWidth"),
        (IN, "cEscapement"),
        (IN, "cOrientation"),
        (IN, "cWeight"),
        (IN, "bItalic"),
        (IN, "bUnderline"),
        (IN, "bStrikeOut"),
        (IN, "iCharSet"),
        (IN, "iOutPrecision"),
        (IN, "iClipPrecision"),
        (IN, "iQuality"),
        (IN, "iPitchAndFamily"),
        (IN, "pszFaceName"),
    )
)

# HFONT CreateFontIndirectW(
#   [in] const LOGFONTW *lplf
# );
CreateFontIndirect = ctypes.WINFUNCTYPE(
    wintypes.HFONT,
    ctypes.POINTER(LOGFONT)
)(
    ('CreateFontIndirectW', gdi32),
    (
        (IN, "plf"),
    )
)
# Example: CreateFontIndirect()

# HPEN CreatePen(
#   [in] int      iStyle,
#   [in] int      cWidth,
#   [in] COLORREF color
# );
CreatePen = ctypes.WINFUNCTYPE(
    wintypes.HPEN,
    wintypes.INT,
    wintypes.INT,
    wintypes.COLORREF,
)(
    ('CreatePen', gdi32),
    (
        (IN, "iStyle"),
        (IN, "cWidth"),
        (IN, 'color')
    )
)


_CreateSolidBrush = ctypes.WINFUNCTYPE(
    wintypes.HBRUSH,
    wintypes.COLORREF,
)(
    ('CreateSolidBrush', gdi32),
    (
        (IN, "color"),
    )
)


def CreateSolidBrush(color: int) -> int:
    return _CreateSolidBrush(color)


# BOOL DeleteDC(
#   [in] HDC hdc
# );
DeleteDC = gdi32.DeleteDC
DeleteDC.argtypes = [wintypes.HDC]
DeleteDC.restype = wintypes.BOOL

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


# BOOL Ellipse(
#   [in] HDC hdc,
#   [in] int left,
#   [in] int top,
#   [in] int right,
#   [in] int bottom
# );
Ellipse = gdi32.Ellipse
Ellipse.argtypes = [wintypes.HDC, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
Ellipse.restype = wintypes.BOOL

# HGDIOBJ GetStockObject(
#   [in] int i
# );
GetStockObject = gdi32.GetStockObject
GetStockObject.argtypes = [wintypes.INT]
GetStockObject.restype = wintypes.HGDIOBJ

# BOOL GetTextExtentPoint32W(
#   [in]  HDC     hdc,
#   [in]  LPCWSTR lpString,
#   [in]  int     c,
#   [out] LPSIZE  psizl
# );
GetTextExtentPoint32 = gdi32.GetTextExtentPoint32W
GetTextExtentPoint32.argtypes = [wintypes.HDC, wintypes.LPCWSTR, ctypes.c_int, wintypes.LPSIZE]
GetTextExtentPoint32.restype = wintypes.BOOL

# BOOL ExtTextOutW(
#   [in] HDC        hdc,
#   [in] int        x,
#   [in] int        y,
#   [in] UINT       options,
#   [in] const RECT *lprect,
#   [in] LPCWSTR    lpString,
#   [in] UINT       c,
#   [in] const INT  *lpDx
# );
ExtTextOut = gdi32.ExtTextOutW
ExtTextOut.argtypes = [wintypes.HDC, wintypes.INT, wintypes.INT, wintypes.UINT, ctypes.POINTER(wintypes.RECT), wintypes.LPCWSTR, ctypes.c_int, ctypes.POINTER(wintypes.INT)]
ExtTextOut.restype = wintypes.BOOL

# BOOL FrameRgn(
#   [in] HDC    hdc,
#   [in] HRGN   hrgn,
#   [in] HBRUSH hbr,
#   [in] int    w,
#   [in] int    h
# );
FrameRgn = gdi32.FrameRgn
FrameRgn.argtypes = [wintypes.HDC, wintypes.HRGN, wintypes.HBRUSH, ctypes.c_int, ctypes.c_int]
FrameRgn.restype = wintypes.BOOL

# BOOL LineTo(
#   [in] HDC hdc,
#   [in] int x,
#   [in] int y
# );
LineTo = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HDC,
    wintypes.INT,
    wintypes.INT,
)(
    ('LineTo', gdi32),
    (
        (IN, "hdc"),
        (IN, "x"),
        (IN, "y"),
    )
)


# BOOL MoveToEx(
#   [in]  HDC     hdc,
#   [in]  int     x,
#   [in]  int     y,
#   [out] LPPOINT lppt
# );
MoveToEx = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HDC,
    wintypes.INT,
    wintypes.INT,
    ctypes.POINTER(wintypes.POINT),
)(
    ('MoveToEx', gdi32),
    (
        (IN, "hdc"),
        (IN, "x"),
        (IN, "y"),
        (INOUT, "lppt"),
    )
)

# BOOL Rectangle(
#   [in] HDC hdc,
#   [in] int left,
#   [in] int top,
#   [in] int right,
#   [in] int bottom
# );
Rectangle = gdi32.Rectangle
Rectangle.argtypes = [wintypes.HDC, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
Rectangle.restype = wintypes.BOOL

# BOOL RoundRect(
#   [in] HDC hdc,
#   [in] int left,
#   [in] int top,
#   [in] int right,
#   [in] int bottom,
#   [in] int width,
#   [in] int height
# );
RoundRect = gdi32.RoundRect
RoundRect.argtypes = [wintypes.HDC, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
RoundRect.restype = wintypes.BOOL

# HRGN CreateRoundRectRgn(
#   [in] int x1,
#   [in] int y1,
#   [in] int x2,
#   [in] int y2,
#   [in] int w,
#   [in] int h
# );
CreateRoundRectRgn = gdi32.CreateRoundRectRgn
CreateRoundRectRgn.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
CreateRoundRectRgn.restype = wintypes.HRGN

# int SelectClipRgn(
#   [in] HDC  hdc,
#   [in] HRGN hrgn
# );
SelectClipRgn = gdi32.SelectClipRgn
SelectClipRgn.argtypes = [wintypes.HDC, wintypes.HRGN]
SelectClipRgn.restype = wintypes.INT

# HGDIOBJ SelectObject(
#   [in] HDC     hdc,
#   [in] HGDIOBJ h
# );
SelectObject = ctypes.WINFUNCTYPE(
    wintypes.HGDIOBJ,
    wintypes.HDC,
    wintypes.HGDIOBJ,
)(
    ('SelectObject', gdi32),
    (
        (IN, "hdc"),
        (IN, "h"),
    )
)


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


SetBkMode = ctypes.WINFUNCTYPE(
    wintypes.INT,
    wintypes.HDC,
    ctypes.c_int,
)(
    ('SetBkMode', gdi32),
    (
        (IN, "hdc"),
        (IN, "mode"),
    )
)

# int SetDIBits(
#   [in] HDC              hdc,
#   [in] HBITMAP          hbm,
#   [in] UINT             start,
#   [in] UINT             cLines,
#   [in] const VOID       *lpBits,
#   [in] const BITMAPINFO *lpbmi,
#   [in] UINT             ColorUse
# );
SetDIBits = ctypes.WINFUNCTYPE(
    wintypes.INT,
    wintypes.HDC,
    wintypes.HBITMAP,
    wintypes.UINT,
    wintypes.UINT,
    ctypes.c_void_p,
    ctypes.POINTER(BITMAPINFO),
    wintypes.UINT
)(
    ('SetDIBits', gdi32),
    (
        (IN, "hdc"),
        (IN, "hbm"),
        (IN, "start"),
        (IN, "cLines"),
        (IN, "lpBits"),
        (IN, "lpbmi"),
        (IN, "ColorUse"),
    )
)

# COLORREF SetPixel(
#   [in] HDC      hdc,
#   [in] int      x,
#   [in] int      y,
#   [in] COLORREF color
# );
SetPixel = gdi32.SetPixel
SetPixel.argtypes = [wintypes.HDC, ctypes.c_int, ctypes.c_int, wintypes.COLORREF]
SetPixel.restype = wintypes.COLORREF


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-settextcolor
# COLORREF SetTextColor(
#   [in] HDC      hdc,
#   [in] COLORREF color
# );
_SetTextColor = ctypes.WINFUNCTYPE(
    wintypes.COLORREF,
    wintypes.HDC,
    wintypes.COLORREF,
)(
    ('SetTextColor', gdi32),
    (
        (IN, "hdc"),
        (IN, "color"),
    )
)


def SetTextColor(hdc: int, color: int) -> int:
    return _SetTextColor(hdc, color)
