import ctypes
from ctypes import wintypes
import weakref

import win32con

from skeletal_framework.win32_bindings.errcheck import errcheck_bool, call_with_last_error_check

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


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-bitblt
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
_BitBlt = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HDC,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    wintypes.HDC,
    ctypes.c_int,
    ctypes.c_int,
    wintypes.DWORD
)(
    ('BitBlt', gdi32),
    (
        (IN, "hdc"),
        (IN, "x"),
        (IN, "y"),
        (IN, "cx"),
        (IN, "cy"),
        (IN, "hdcSrc"),
        (IN, "x1"),
        (IN, "y1"),
        (IN, "rop"),
    )
)
_BitBlt.errcheck = errcheck_bool


def BitBlt(hdc: int, x: int, y: int, cx: int, cy: int, hdcSrc: int, x1: int, y1: int, rop: int) -> bool:
    return _BitBlt(hdc, x, y, cx, cy, hdcSrc, x1, y1, rop)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createbitmap
# HBITMAP CreateBitmap(
#   [in] int        nWidth,
#   [in] int        nHeight,
#   [in] UINT       nPlanes,
#   [in] UINT       nBitCount,
#   [in] const VOID *lpBits
# );
_CreateBitmap = ctypes.WINFUNCTYPE(
    wintypes.HBITMAP,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_uint,
    ctypes.c_uint,
    ctypes.c_void_p
)(
    ('CreateBitmap', gdi32),
    (
        (IN, "nWidth"),
        (IN, "nHeight"),
        (IN, "nPlanes"),
        (IN, "nBitCount"),
        (IN, "lpBits"),
    )
)


def CreateBitmap(nWidth: int, nHeight: int, nPlanes: int, nBitCount: int, lpBits: int | None) -> int:
    return call_with_last_error_check(_CreateBitmap, nWidth, nHeight, nPlanes, nBitCount, lpBits)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createcompatiblebitmap
# HBITMAP CreateCompatibleBitmap(
#   [in] HDC hdc,
#   [in] int cx,
#   [in] int cy
# );
_CreateCompatibleBitmap = ctypes.WINFUNCTYPE(
    wintypes.HBITMAP,
    wintypes.HDC,
    ctypes.c_int,
    ctypes.c_int
)(
    ('CreateCompatibleBitmap', gdi32),
    (
        (IN, "hdc"),
        (IN, "cx"),
        (IN, "cy"),
    )
)


def CreateCompatibleBitmap(hdc: int, cx: int, cy: int) -> int:
    return call_with_last_error_check(_CreateCompatibleBitmap, hdc, cx, cy)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createcompatibledc
# HDC CreateCompatibleDC(
#   [in] HDC hdc
# );
_CreateCompatibleDC = ctypes.WINFUNCTYPE(
    wintypes.HDC,
    wintypes.HDC
)(
    ('CreateCompatibleDC', gdi32),
    (
        (IN, "hdc"),
    )
)


def CreateCompatibleDC(hdc: int) -> int:
    return call_with_last_error_check(_CreateCompatibleDC, hdc)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createdibsection
# HBITMAP CreateDIBSection(
#   [in]  HDC              hdc,
#   [in]  const BITMAPINFO *pbmi,
#   [in]  UINT             usage,
#   [out] VOID             **ppvBits,
#   [in]  HANDLE           hSection,
#   [in]  DWORD            offset
# );
_CreateDIBSection = ctypes.WINFUNCTYPE(
    wintypes.HBITMAP,
    wintypes.HDC,
    ctypes.POINTER(BITMAPINFO),
    wintypes.UINT,
    ctypes.POINTER(wintypes.LPVOID),
    wintypes.HANDLE,
    wintypes.DWORD
)(
    ('CreateDIBSection', gdi32),
    (
        (IN, "hdc"),
        (IN, "pbmi"),
        (IN, "usage"),
        (OUT, "ppvBits"),
        (IN, "hSection"),
        (IN, "offset"),
    )
)


def CreateDIBSection(hdc: int, pbmi: BITMAPINFO, usage: int, ppvBits: ctypes.POINTER(wintypes.LPVOID), hSection: int, offset: int) -> int:
    return call_with_last_error_check(_CreateDIBSection, hdc, ctypes.byref(pbmi), usage, ppvBits, hSection, offset)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createfontw
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
CreateFontW = ctypes.WINFUNCTYPE(
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


def CreateFont(cHeight, cWidth, cEscapement, cOrientation, cWeight, bItalic, bUnderline, bStrikeOut, iCharSet, iOutPrecision, iClipPrecision, iQuality, iPitchAndFamily, pszFaceName) -> int:
    return call_with_last_error_check(CreateFontW, cHeight, cWidth, cEscapement, cOrientation, cWeight, bItalic, bUnderline, bStrikeOut, iCharSet, iOutPrecision, iClipPrecision, iQuality, iPitchAndFamily, pszFaceName)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createfontindirectw
# HFONT CreateFontIndirectW(
#   [in] const LOGFONTW *lplf
# );
CreateFontIndirectW = ctypes.WINFUNCTYPE(
    wintypes.HFONT,
    ctypes.POINTER(LOGFONT)
)(
    ('CreateFontIndirectW', gdi32),
    (
        (IN, "lplf"),
    )
)


def CreateFontIndirect(plf: LOGFONT) -> int:
    return call_with_last_error_check(CreateFontIndirectW, ctypes.byref(plf))


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createpen
# HPEN CreatePen(
#   [in] int      iStyle,
#   [in] int      cWidth,
#   [in] COLORREF color
# );
_CreatePen = ctypes.WINFUNCTYPE(
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


def CreatePen(iStyle: int, cWidth: int, color: int) -> int:
    return call_with_last_error_check(_CreatePen, iStyle, cWidth, color)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createsolidbrush
# HBRUSH CreateSolidBrush(
#   [in] COLORREF color
# );
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
    return call_with_last_error_check(_CreateSolidBrush, color)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-deletedc
# BOOL DeleteDC(
#   [in] HDC hdc
# );
_DeleteDC = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HDC
)(
    ('DeleteDC', gdi32),
    (
        (IN, "hdc"),
    )
)
_DeleteDC.errcheck = errcheck_bool


def DeleteDC(hdc: int) -> bool:
    return _DeleteDC(hdc)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-deleteobject
# BOOL DeleteObject(
#   [in] HGDIOBJ ho
# );
_DeleteObject = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HGDIOBJ
)(
    ('DeleteObject', gdi32),
    (
        (IN, "ho"),
    )
)
_DeleteObject.errcheck = errcheck_bool


def DeleteObject(ho: int) -> bool:
    return _DeleteObject(ho)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-ellipse
# BOOL Ellipse(
#   [in] HDC hdc,
#   [in] int left,
#   [in] int top,
#   [in] int right,
#   [in] int bottom
# );
_Ellipse = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HDC,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int
)(
    ('Ellipse', gdi32),
    (
        (IN, "hdc"),
        (IN, "left"),
        (IN, "top"),
        (IN, "right"),
        (IN, "bottom"),
    )
)
_Ellipse.errcheck = errcheck_bool


def Ellipse(hdc: int, left: int, top: int, right: int, bottom: int) -> bool:
    return _Ellipse(hdc, left, top, right, bottom)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getstockobject
# HGDIOBJ GetStockObject(
#   [in] int i
# );
_GetStockObject = ctypes.WINFUNCTYPE(
    wintypes.HGDIOBJ,
    wintypes.INT
)(
    ('GetStockObject', gdi32),
    (
        (IN, "i"),
    )
)


def GetStockObject(i: int) -> int:
    return call_with_last_error_check(_GetStockObject, i)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-gettextextentpoint32w
# BOOL GetTextExtentPoint32W(
#   [in]  HDC     hdc,
#   [in]  LPCWSTR lpString,
#   [in]  int     c,
#   [out] LPSIZE  psizl
# );
GetTextExtentPoint32W = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HDC,
    wintypes.LPCWSTR,
    ctypes.c_int,
    wintypes.LPSIZE
)(
    ('GetTextExtentPoint32W', gdi32),
    (
        (IN, "hdc"),
        (IN, "lpString"),
        (IN, "c"),
        (OUT, "psizl"),
    )
)
GetTextExtentPoint32W.errcheck = errcheck_bool


def GetTextExtentPoint32(hdc: int, lpString: str, c: int, psizl: wintypes.SIZE) -> bool:
    return GetTextExtentPoint32W(hdc, lpString, c, psizl)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-exttextoutw
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
ExtTextOutW = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HDC,
    wintypes.INT,
    wintypes.INT,
    wintypes.UINT,
    ctypes.POINTER(wintypes.RECT),
    wintypes.LPCWSTR,
    ctypes.c_int,
    ctypes.POINTER(wintypes.INT)
)(
    ('ExtTextOutW', gdi32),
    (
        (IN, "hdc"),
        (IN, "x"),
        (IN, "y"),
        (IN, "options"),
        (IN, "lprect"),
        (IN, "lpString"),
        (IN, "c"),
        (IN, "lpDx"),
    )
)
ExtTextOutW.errcheck = errcheck_bool


def ExtTextOut(hdc: int, x: int, y: int, options: int, lprect: wintypes.RECT | None, lpString: str, c: int, lpDx: ctypes.POINTER(wintypes.INT) | None) -> bool:
    return ExtTextOutW(hdc, x, y, options, lprect, lpString, c, lpDx)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-framergn
# BOOL FrameRgn(
#   [in] HDC    hdc,
#   [in] HRGN   hrgn,
#   [in] HBRUSH hbr,
#   [in] int    w,
#   [in] int    h
# );
_FrameRgn = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HDC,
    wintypes.HRGN,
    wintypes.HBRUSH,
    ctypes.c_int,
    ctypes.c_int
)(
    ('FrameRgn', gdi32),
    (
        (IN, "hdc"),
        (IN, "hrgn"),
        (IN, "hbr"),
        (IN, "w"),
        (IN, "h"),
    )
)
_FrameRgn.errcheck = errcheck_bool


def FrameRgn(hdc: int, hrgn: int, hbr: int, w: int, h: int) -> bool:
    return _FrameRgn(hdc, hrgn, hbr, w, h)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-lineto
# BOOL LineTo(
#   [in] HDC hdc,
#   [in] int x,
#   [in] int y
# );
_LineTo = ctypes.WINFUNCTYPE(
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


def LineTo(hdc: int, x: int, y: int) -> bool:
    if not _LineTo(hdc, x, y):
        raise ctypes.WinError(ctypes.get_last_error())
    return True


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-movetoex
# BOOL MoveToEx(
#   [in]  HDC     hdc,
#   [in]  int     x,
#   [in]  int     y,
#   [out] LPPOINT lppt
# );
_MoveToEx = ctypes.WINFUNCTYPE(
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
        (IN, "lppt"),
    )
)


def MoveToEx(hdc: int, x: int, y: int, lppt: wintypes.POINT | None) -> bool:
    if not _MoveToEx(hdc, x, y, lppt):
        raise ctypes.WinError(ctypes.get_last_error())
    return True


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-rectangle
# BOOL Rectangle(
#   [in] HDC hdc,
#   [in] int left,
#   [in] int top,
#   [in] int right,
#   [in] int bottom
# );
_Rectangle = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HDC,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int
)(
    ('Rectangle', gdi32),
    (
        (IN, "hdc"),
        (IN, "left"),
        (IN, "top"),
        (IN, "right"),
        (IN, "bottom"),
    )
)
_Rectangle.errcheck = errcheck_bool


def Rectangle(hdc: int, left: int, top: int, right: int, bottom: int) -> bool:
    return _Rectangle(hdc, left, top, right, bottom)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-roundrect
# BOOL RoundRect(
#   [in] HDC hdc,
#   [in] int left,
#   [in] int top,
#   [in] int right,
#   [in] int bottom,
#   [in] int width,
#   [in] int height
# );
_RoundRect = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HDC,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int
)(
    ('RoundRect', gdi32),
    (
        (IN, "hdc"),
        (IN, "left"),
        (IN, "top"),
        (IN, "right"),
        (IN, "bottom"),
        (IN, "width"),
        (IN, "height"),
    )
)
_RoundRect.errcheck = errcheck_bool


def RoundRect(hdc: int, left: int, top: int, right: int, bottom: int, width: int, height: int) -> bool:
    return _RoundRect(hdc, left, top, right, bottom, width, height)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createroundrectrgn
# HRGN CreateRoundRectRgn(
#   [in] int x1,
#   [in] int y1,
#   [in] int x2,
#   [in] int y2,
#   [in] int w,
#   [in] int h
# );
_CreateRoundRectRgn = ctypes.WINFUNCTYPE(
    wintypes.HRGN,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int
)(
    ('CreateRoundRectRgn', gdi32),
    (
        (IN, "x1"),
        (IN, "y1"),
        (IN, "x2"),
        (IN, "y2"),
        (IN, "w"),
        (IN, "h"),
    )
)


def CreateRoundRectRgn(x1: int, y1: int, x2: int, y2: int, w: int, h: int) -> int:
    return call_with_last_error_check(_CreateRoundRectRgn, x1, y1, x2, y2, w, h)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-selectcliprgn
# int SelectClipRgn(
#   [in] HDC  hdc,
#   [in] HRGN hrgn
# );
_SelectClipRgn = ctypes.WINFUNCTYPE(
    wintypes.INT,
    wintypes.HDC,
    wintypes.HRGN
)(
    ('SelectClipRgn', gdi32),
    (
        (IN, "hdc"),
        (IN, "hrgn"),
    )
)


def SelectClipRgn(hdc: int, hrgn: int) -> int:
    ret = _SelectClipRgn(hdc, hrgn)
    if ret == 0: # ERROR
        raise ctypes.WinError(ctypes.get_last_error())
    return ret


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-selectobject
# HGDIOBJ SelectObject(
#   [in] HDC     hdc,
#   [in] HGDIOBJ h
# );
_SelectObject = ctypes.WINFUNCTYPE(
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


def SelectObject(hdc: int, h: int) -> int:
    # SelectObject returns NULL on error for some objects, or HGDI_ERROR for others.
    # However, it returns the previous object on success.
    # We'll use call_with_last_error_check which checks for NULL/0 return and GetLastError.
    # Note: HGDI_ERROR is defined as (HGDIOBJ)-1 or 0xFFFFFFFF.
    # call_with_last_error_check handles 0 return.
    # Let's handle HGDI_ERROR explicitly if needed, but standard check is a good start.
    return call_with_last_error_check(_SelectObject, hdc, h)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-setbkcolor
# COLORREF SetBkColor(
#   [in] HDC      hdc,
#   [in] COLORREF color
# );
_SetBkColor = ctypes.WINFUNCTYPE(
    wintypes.COLORREF,
    wintypes.HDC,
    wintypes.COLORREF
)(
    ('SetBkColor', gdi32),
    (
        (IN, "hdc"),
        (IN, "color"),
    )
)


def SetBkColor(hdc: int, color: int) -> int:
    # Returns CLR_INVALID on failure
    ret = _SetBkColor(hdc, color)
    if ret == 0xFFFFFFFF:
        raise ctypes.WinError(ctypes.get_last_error())
    return ret


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-setbkmode
# int SetBkMode(
#   [in] HDC hdc,
#   [in] int mode
# );
_SetBkMode = ctypes.WINFUNCTYPE(
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


def SetBkMode(hdc: int, mode: int) -> int:
    return call_with_last_error_check(_SetBkMode, hdc, mode)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-setdibits
# int SetDIBits(
#   [in] HDC              hdc,
#   [in] HBITMAP          hbm,
#   [in] UINT             start,
#   [in] UINT             cLines,
#   [in] const VOID       *lpBits,
#   [in] const BITMAPINFO *lpbmi,
#   [in] UINT             ColorUse
# );
_SetDIBits = ctypes.WINFUNCTYPE(
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


def SetDIBits(hdc: int, hbm: int, start: int, cLines: int, lpBits: int, lpbmi: BITMAPINFO, ColorUse: int) -> int:
    # Returns 0 on failure
    return call_with_last_error_check(_SetDIBits, hdc, hbm, start, cLines, lpBits, ctypes.byref(lpbmi), ColorUse)


# https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-setpixel
# COLORREF SetPixel(
#   [in] HDC      hdc,
#   [in] int      x,
#   [in] int      y,
#   [in] COLORREF color
# );
_SetPixel = ctypes.WINFUNCTYPE(
    wintypes.COLORREF,
    wintypes.HDC,
    ctypes.c_int,
    ctypes.c_int,
    wintypes.COLORREF
)(
    ('SetPixel', gdi32),
    (
        (IN, "hdc"),
        (IN, "x"),
        (IN, "y"),
        (IN, "color"),
    )
)


def SetPixel(hdc: int, x: int, y: int, color: int) -> int:
    ret = _SetPixel(hdc, x, y, color)
    if ret == -1:
        raise ctypes.WinError(ctypes.get_last_error())
    return ret


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
    ret = _SetTextColor(hdc, color)
    if ret == 0xFFFFFFFF: # CLR_INVALID
        raise ctypes.WinError(ctypes.get_last_error())
    return ret
