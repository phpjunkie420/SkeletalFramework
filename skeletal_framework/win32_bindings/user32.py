# noinspection PyTypeChecker
"""
Provides ctypes definitions and helper functions for interacting with
the Windows User Interface API (WinUser).

This module includes structures and functions commonly found in `winuser.h`.
For comprehensive documentation on the Windows User API, refer to:
https://learn.microsoft.com/en-us/windows/win32/api/winuser/
"""
import ctypes
from ctypes import wintypes
from collections.abc import Callable
from typing import Any

from skeletal_framework.win32_bindings.errcheck import errcheck_bool, errcheck_zero, call_with_last_error_check

# noinspection DuplicatedCode
__all__ = [
    'AppendMenu',
    'BeginPaint',
    'CallWindowProc', 'CreateMenu', 'CreateWindowEx',
    'DefWindowProc', 'DestroyIcon', 'DestroyWindow', 'DispatchMessage', 'DrawFocusRect', 'DrawFrameControl', 'DrawText',
    'EnableMenuItem', 'EnableWindow', 'EndPaint',
    'FillRect', 'FrameRect',
    'GetClientRect', 'GetCursorPos', 'GetDC', 'GetMessage', 'GetSysColor', 'GetSysColorBrush',
    'GetSystemMetrics', 'GetWindowLong', 'GetWindowRect', 'GetWindowText', 'GetWindowTextLength', 'GetWindowThreadProcessId',
    'InvalidateRect', 'IsDialogMessage', 'IsWindowEnabled',
    'KillTimer',
    'LoadCursor', 'LoadIcon', 'LoadImage',
    'MapWindowPoints', 'MessageBox', 'MoveWindow',
    'PostMessage', 'PostQuitMessage', 'PtInRect',
    'RedrawWindow', 'RegisterClass', 'RegisterClassEx', 'ReleaseDC',
    'ScreenToClient', 'SetActiveWindow', 'SetFocus', 'SetProcessDPIAware', 'SetScrollInfo', 'SetTimer', 'SendMessage', 'SetWindowLong',
    'SetWindowPos', 'SetWindowRgn', 'SetWindowText', 'ShowWindow',
    'TranslateMessage', 'TrackMouseEvent',
    'UnregisterClass', 'UpdateWindow',
    'WNDPROC',
    'COMBOBOXINFO', 'CREATESTRUCT', 'DRAWITEMSTRUCT', 'ICONINFO', 'MEASUREITEMSTRUCT', 'MINMAXINFO',
    'NMHDR', 'PAINTSTRUCT', 'SCROLLINFO', 'TRACKMOUSEEVENT', 'WNDCLASS', 'WNDCLASSEX',
]

IN = 1
OUT = 2
INOUT = 3

user32 = ctypes.WinDLL('user32', use_last_error = True)

if ctypes.sizeof(ctypes.c_void_p) == 8:  # 64-bit
    ULONG_PTR = LONG_PTR = LRESULT = ctypes.c_longlong
else:                                    # 32-bit
    ULONG_PTR = LONG_PTR = LRESULT = ctypes.c_long

_WNDPROC = ctypes.WINFUNCTYPE(
    ctypes.HRESULT,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM
)


def WNDPROC(func: Callable[..., Any]) -> Any:
    return _WNDPROC(func)


class COMBOBOXINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_uint),
        ("rcItem", wintypes.RECT),
        ("rcButton", wintypes.RECT),
        ("stateButton", ctypes.c_uint),
        ("hwndCombo", ctypes.c_void_p),
        ("hwndItem", ctypes.c_void_p),
        ("hwndList", ctypes.c_void_p)
    ]


# typedef struct tagCREATESTRUCTA {
#   LPVOID    lpCreateParams;
#   HINSTANCE hInstance;
#   HMENU     hMenu;
#   HWND      hwndParent;
#   int       cy;
#   int       cx;
#   int       y;
#   int       x;
#   LONG      style;
#   LPCSTR    lpszName;   # noqa
#   LPCSTR    lpszClass;  # noqa
#   DWORD     dwExStyle;
# } CREATESTRUCTA, *LPCREATESTRUCTA;
class CREATESTRUCT(ctypes.Structure):
    # noinspection SpellCheckingInspection
    _fields_ = [
        ('lpCreateParams', wintypes.LPVOID),
        ('hInstance', wintypes.HINSTANCE),
        ('hMenu', wintypes.HMENU),
        ('hwndParent', wintypes.HWND),
        ('cy', ctypes.c_int),
        ('cx', ctypes.c_int),
        ('y', ctypes.c_int),
        ('x', ctypes.c_int),
        ('style', wintypes.DWORD),
        ('lpszName', wintypes.LPCSTR),
        ('lpszClass', wintypes.LPCSTR),
        ('dwExStyle', wintypes.DWORD),
    ]


class DRAWITEMSTRUCT(ctypes.Structure):
    _fields_ = [
        ("CtlType", ctypes.c_uint),
        ("CtlID", ctypes.c_uint),
        ("itemID", ctypes.c_uint),
        ("itemAction", ctypes.c_uint),
        ("itemState", ctypes.c_uint),
        ("hwndItem", ctypes.c_void_p),
        ("hDC", ctypes.c_void_p),
        ("rcItem", wintypes.RECT),
        ("itemData", ctypes.c_void_p)
    ]

    # noinspection PyPep8Naming
    def __init__(
        self,
        CtlType = 0,
        CtlID = 0,
        itemID = 0,
        itemAction = 0,
        itemState = 0,
        hwndItem = None,
        hDC = None,
        rcItem = wintypes.RECT(),
        itemData = None
    ) -> None:
        super().__init__()
        self.CtlType = CtlType
        self.CtlID = CtlID
        self.itemID = itemID
        self.itemAction = itemAction
        self.itemState = itemState
        self.hwndItem = hwndItem
        self.hDC = hDC
        self.rcItem = rcItem
        self.itemData = itemData


class ICONINFO(ctypes.Structure):
    _fields_ = [
        ('fIcon', wintypes.BOOL),
        ('xHotspot', wintypes.DWORD),
        ('yHotspot', wintypes.DWORD),
        ('hbmMask', wintypes.HBITMAP),
        ('hbmColor', wintypes.HBITMAP),
    ]


# typedef struct tagMEASUREITEMSTRUCT {
#   UINT      CtlType;
#   UINT      CtlID;
#   UINT      itemID;
#   UINT      itemWidth;
#   UINT      itemHeight;
#   ULONG_PTR itemData;
# } MEASUREITEMSTRUCT, *PMEASUREITEMSTRUCT, *LPMEASUREITEMSTRUCT;
class MEASUREITEMSTRUCT(ctypes.Structure):
    _fields_ = [
        ("CtlType", wintypes.UINT),
        ("CtlID", wintypes.UINT),
        ("itemID", wintypes.UINT),
        ("itemWidth", wintypes.UINT),
        ("itemHeight", wintypes.UINT),
        ("itemData", ULONG_PTR)
    ]

    # noinspection PyPep8Naming
    def __init__(
        self,
        CtlType = 0,
        CtlID = 0,
        itemID = 0,
        itemWidth = 0,
        itemHeight = 0,
        itemData = None
    ) -> None:
        super().__init__()
        self.CtlType = CtlType
        self.CtlID = CtlID
        self.itemID = itemID
        self.itemWidth = itemWidth
        self.itemHeight = itemHeight
        self.itemData = itemData


class MINMAXINFO(ctypes.Structure):
    _fields_ = [
        ("ptReserved", wintypes.POINT),
        ("ptMaxSize", wintypes.POINT),
        ("ptMaxPosition", wintypes.POINT),
        ("ptMinTrackSize", wintypes.POINT),
        ("ptMaxTrackSize", wintypes.POINT),
    ]

    # noinspection PyPep8Naming
    def __init__(
        self,
        ptReserved = wintypes.POINT(),
        ptMaxSize = wintypes.POINT(),
        ptMaxPosition = wintypes.POINT(),
        ptMinTrackSize = wintypes.POINT(),
        ptMaxTrackSize = wintypes.POINT(),
    ) -> None:
        super().__init__()
        self.ptReserved = ptReserved
        self.ptMaxSize = ptMaxSize
        self.ptMaxPosition = ptMaxPosition
        self.ptMinTrackSize = ptMinTrackSize
        self.ptMaxTrackSize = ptMaxTrackSize


# typedef struct tagNMHDR {
#   HWND     hwndFrom;
#   UINT_PTR idFrom;
#   UINT     code;
# } NMHDR;
class NMHDR(ctypes.Structure):
    _fields_ = [
        ('hwndFrom', wintypes.HWND),
        ('idFrom', ctypes.c_size_t),
        ('code', wintypes.INT),
    ]


# typedef struct tagPAINTSTRUCT {
#   HDC  hdc;
#   BOOL fErase;
#   RECT rcPaint;
#   BOOL fRestore;
#   BOOL fIncUpdate;
#   BYTE rgbReserved[32];
# } PAINTSTRUCT, *PPAINTSTRUCT, *NPPAINTSTRUCT, *LPPAINTSTRUCT;
class PAINTSTRUCT(ctypes.Structure):
    _fields_ = [
        ("hdc", wintypes.HDC),
        ("fErase", wintypes.BOOL),
        ("rcPaint", wintypes.RECT),
        ("fRestore", wintypes.BOOL),
        ("fIncUpdate", wintypes.BOOL),
        ("rgbReserved", (ctypes.c_byte * 32))
    ]


# typedef struct tagSCROLLINFO {
#   UINT cbSize;
#   UINT fMask;
#   int  nMin;
#   int  nMax;
#   UINT nPage;
#   int  nPos;
#   int  nTrackPos;
# } SCROLLINFO, *LPSCROLLINFO;
class SCROLLINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.UINT),
        ("fMask", wintypes.UINT),
        ("nMin", wintypes.INT),
        ("nMax", wintypes.INT),
        ("nPage", wintypes.UINT),
        ("nPos", wintypes.INT),
        ("nTrackPos", wintypes.INT)]

    # noinspection PyPep8Naming
    def __init__(
        self,
        fMask: int = 0,
        nMin: int = 0,
        nMax: int = 0,
        nPage: int = 0,
        nPos: int = 0,
        nTrackPos: int = 0,
    ) -> None:
        super().__init__()
        self.cbSize = ctypes.sizeof(SCROLLINFO)
        self.fMask = fMask or 0x00000007
        self.nMin = nMin
        self.nMax = nMax
        self.nPage = nPage
        self.nPos = nPos
        self.nTrackPos = nTrackPos


# typedef struct tagTRACKMOUSEEVENT {
#   DWORD cbSize;
#   DWORD dwFlags;
#   HWND  hwndTrack;
#   DWORD dwHoverTime;
# } TRACKMOUSEEVENT, *LPTRACKMOUSEEVENT;
class TRACKMOUSEEVENT(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.DWORD),
        ('dwFlags', wintypes.DWORD),
        ('hwndTrack', wintypes.HWND),
        ('dwHoverTime', wintypes.DWORD),
    ]

    # noinspection PyPep8Naming
    def __init__(self, dwFlags: int, hwndTrack = None, dwHoverTime = 0):
        super().__init__()
        self.cbSize = ctypes.sizeof(self)
        self.dwFlags = dwFlags or 0x0001
        self.hwndTrack = hwndTrack
        self.dwHoverTime = dwHoverTime


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-wndclassw
# typedef struct tagWNDCLASSW {
#   UINT      style;
#   WNDPROC   lpfnWndProc;    # noqa
#   int       cbClsExtra;
#   int       cbWndExtra;
#   HINSTANCE hInstance;
#   HICON     hIcon;
#   HCURSOR   hCursor;
#   HBRUSH    hbrBackground;
#   LPCWSTR   lpszMenuName;   # noqa
#   LPCWSTR   lpszClassName;  # noqa
# } WNDCLASSW, *PWNDCLASSW, *NPWNDCLASSW, *LPWNDCLASSW;
class WNDCLASS(ctypes.Structure):
    _fields_ = [
        ("style", wintypes.UINT),
        ("lpfnWndProc", _WNDPROC),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", wintypes.HANDLE),
        ("hIcon", wintypes.HANDLE),
        ("hCursor", wintypes.HANDLE),
        ("hbrBackground", wintypes.HANDLE),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR)
    ]

    def __init__(
        self,
        style = 0,
        lpfnWndProc = None,
        cbClsExtra = 0,
        cbWndExtra = 0,
        hInstance = None,
        hIcon = None,
        hCursor = None,
        hbrBackground = None,
        lpszMenuName = None,
        lpszClassName = None
    ):
        super().__init__()
        self.style = style
        self.lpfnWndProc = lpfnWndProc
        self.cbClsExtra = cbClsExtra
        self.cbWndExtra = cbWndExtra
        self.hInstance = hInstance
        self.hIcon = hIcon
        self.hCursor = hCursor
        self.hbrBackground = hbrBackground
        self.lpszMenuName = lpszMenuName
        self.lpszClassName = lpszClassName


class WNDCLASSEX(ctypes.Structure):
    # noinspection SpellCheckingInspection
    _fields_ = [
        ("cbSize", wintypes.UINT),
        ("style", wintypes.UINT),
        ("lpfnWndProc", _WNDPROC),
        ("cbClsExtra", wintypes.INT),
        ("cbWndExtra", wintypes.INT),
        ("hInstance", wintypes.HINSTANCE),
        ("hIcon", wintypes.HICON),
        ("hCursor", wintypes.HANDLE),
        ("hbrBackground", wintypes.HBRUSH),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
        ("hIconSm", wintypes.HICON),
    ]

    # noinspection SpellCheckingInspection
    def __init__(
        self,
        style = 0,
        lpfnWndProc = None,
        cbClsExtra = 0,
        cbWndExtra = 0,
        hInstance = None,
        hIcon = None,
        hCursor = None,
        hbrBackground = None,
        lpszMenuName = None,
        lpszClassName = None
    ):
        super().__init__()
        self.cbSize = ctypes.sizeof(WNDCLASSEX)
        self.style = style
        self.lpfnWndProc = lpfnWndProc
        self.cbClsExtra = cbClsExtra
        self.cbWndExtra = cbWndExtra
        self.hInstance = hInstance
        self.hIcon = hIcon
        self.hCursor = hCursor
        self.hbrBackground = hbrBackground
        self.lpszMenuName = lpszMenuName
        self.lpszClassName = lpszClassName


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-appendmenuw
# BOOL AppendMenuW(
#   [in]           HMENU    hMenu,
#   [in]           UINT     uFlags,
#   [in]           UINT_PTR uIDNewItem,
#   [in, optional] LPCWSTR  lpNewItem
# );
AppendMenuW = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HMENU,
    wintypes.UINT,
    ctypes.c_void_p,
    ctypes.c_void_p
)(
    ('AppendMenuW', user32),
    (
        (IN, "hMenu"),
        (IN, "uFlags"),
        (IN, "uIDNewItem"),
        (IN, "lpNewItem"),
    )
)


def AppendMenu(hMenu: int, uFlags: int, uIDNewItem: int, lpNewItem: str | None) -> bool:
    return AppendMenuW(hMenu, uFlags, uIDNewItem, lpNewItem) > 0


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-beginpaint
# HDC BeginPaint(
#   [in]  HWND          hWnd,
#   [out] LPPAINTSTRUCT lpPaint
# );
_BeginPaint = ctypes.WINFUNCTYPE(
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


def BeginPaint(hwnd: int) -> tuple[PAINTSTRUCT, int]:
    ps = PAINTSTRUCT()
    hdc = _BeginPaint(hwnd, ctypes.byref(ps))

    return ps, hdc


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-callwindowprocw
# LRESULT CallWindowProcW(
#   [in] WNDPROC lpPrevWndFunc,
#   [in] HWND    hWnd,
#   [in] UINT    Msg,
#   [in] WPARAM  wParam,
#   [in] LPARAM  lParam
# );
CallWindowProcW = ctypes.WINFUNCTYPE(
    LRESULT,
    LONG_PTR,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM
)(
    ('CallWindowProcW', user32),
    (
        (IN, "lpPrevWndFunc"),
        (IN, "hWnd"),
        (IN, "Msg"),
        (IN, "wParam"),
        (IN, "lParam"),
    )
)


def CallWindowProc(lpPrevWndFunc: int, hWnd: int, Msg: int, wParam: int, lParam: int) -> int:
    return CallWindowProcW(lpPrevWndFunc, hWnd, Msg, wParam, lParam)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createmenu
# HMENU CreateMenu();
_CreateMenu = ctypes.WINFUNCTYPE(
    wintypes.HMENU
)(
    ('CreateMenu', user32),
    ()
)


def CreateMenu() -> int:
    return call_with_last_error_check(_CreateMenu)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createwindowexw
# HWND CreateWindowExW(
#   [in]           DWORD     dwExStyle,
#   [in, optional] LPCWSTR   lpClassName,
#   [in, optional] LPCWSTR   lpWindowName,
#   [in]           DWORD     dwStyle,
#   [in]           int       X,
#   [in]           int       Y,
#   [in]           int       nWidth,
#   [in]           int       nHeight,
#   [in, optional] HWND      hWndParent,
#   [in, optional] HMENU     hMenu,
#   [in, optional] HINSTANCE hInstance,
#   [in, optional] LPVOID    lpParam
# );
CreateWindowExW = ctypes.WINFUNCTYPE(
    wintypes.HWND,
    wintypes.DWORD,
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.DWORD,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    wintypes.HWND,
    wintypes.HMENU,
    wintypes.HINSTANCE,
    wintypes.LPVOID
)(
    ("CreateWindowExW", user32),
    (
        (IN, "dwExStyle"),
        (IN, "lpClassName"),
        (IN, "lpWindowName"),
        (IN, "dwStyle"),
        (IN, "x"),
        (IN, "y"),
        (IN, "nWidth"),
        (IN, "nHeight"),
        (IN, "hWndParent"),
        (IN, "hMenu"),
        (IN, "hInstance"),
        (IN, "lpParam"),
    )
)


def CreateWindowEx(
        *,
        dwExStyle: int = 0,
        lpClassName: str | None = None,
        lpWindowName: str | None = None,
        dwStyle: int,
        x: int, y: int, nWidth: int, nHeight: int,
        hWndParent: int | None = None,
        hMenu: int | None = None,
        hInstance: int | None = None,
        lpParam: int | None = None
) -> int:
    return call_with_last_error_check(
        CreateWindowExW,
        dwExStyle,
        lpClassName,
        lpWindowName,
        dwStyle,
        x,
        y,
        nWidth,
        nHeight,
        hWndParent,
        hMenu,
        hInstance,
        lpParam
    )


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-defwindowprocw
# LRESULT DefWindowProcW(
#   [in] HWND   hWnd,
#   [in] UINT   Msg,
#   [in] WPARAM wParam,
#   [in] LPARAM lParam
# );
DefWindowProcW = ctypes.WINFUNCTYPE(
    wintypes.LPARAM,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM
)(
    ('DefWindowProcW', user32),
    (
        (IN, "hWnd"),
        (IN, "Msg"),
        (IN, "wParam"),
        (IN, "lParam"),
    )
)


def DefWindowProc(hWnd: int, Msg: int, wParam: int, lParam: int) -> int:
    return DefWindowProcW(hWnd, Msg, wParam, lParam)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-destroyicon
# BOOL DestroyIcon(
#   [in] HICON hIcon
# );
_DestroyIcon = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HICON
)(
    ('DestroyIcon', user32),
    (
        (IN, "hIcon"),
    )
)


def DestroyIcon(hIcon: int) -> bool:
    return _DestroyIcon(hIcon) > 0


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-destroywindow
# BOOL DestroyWindow(
#   [in] HWND hWnd
# );
_DestroyWindow = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND
)(
    ('DestroyWindow', user32),
    (
        (IN, "hWnd"),
    )
)
_DestroyWindow.errcheck = errcheck_bool


def DestroyWindow(hWnd: int) -> bool:
    return _DestroyWindow(hWnd)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-dispatchmessagew
# LRESULT DispatchMessageW(
#   [in] const MSG *lpMsg
# );
DispatchMessageW = ctypes.WINFUNCTYPE(
    ctypes.c_ssize_t,
    wintypes.LPMSG
)(
    ('DispatchMessageW', user32),
    (
        (IN, "lpMsg"),
    )
)


def DispatchMessage(lpMsg: Any) -> int:
    return DispatchMessageW(lpMsg)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-drawfocusrect
# BOOL DrawFocusRect(
#   [in] HDC        hDC,
#   [in] const RECT *lprc  # noqa
# );
_DrawFocusRect = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HDC,
    wintypes.LPRECT
)(
    ('DrawFocusRect', user32),
    (
        (IN, "hDC"),
        (IN, "lprc"),
    )
)
_DrawFocusRect.errcheck = errcheck_bool


def DrawFocusRect(hDC: int, lprc: wintypes.RECT) -> bool:
    return _DrawFocusRect(hDC, ctypes.byref(lprc))


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-drawframecontrol
# BOOL DrawFrameControl(
#   [in] HDC    hdc,
#   [in] LPRECT lprc,  # noqa
#   [in] UINT   uType,
#   [in] UINT   uState
# );
_DrawFrameControl = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HDC,
    wintypes.LPRECT,
    wintypes.UINT,
    wintypes.UINT
)(
    ('DrawFrameControl', user32),
    (
        (IN, "hdc"),
        (IN, "lprc"),
        (IN, "uType"),
        (IN, "uState"),
    )
)
_DrawFrameControl.errcheck = errcheck_bool


def DrawFrameControl(hdc: int, lprc: wintypes.RECT, uType: int, uState: int) -> bool:
    return _DrawFrameControl(hdc, ctypes.byref(lprc), uType, uState)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-drawtextw
# int DrawTextW(
#   [in]      HDC     hdc,
#   [in, out] LPCWSTR lpchText,
#   [in]      int     cchText,
#   [in, out] LPRECT  lprc,
#   [in]      UINT    format
# );
DrawTextW = ctypes.WINFUNCTYPE(
    ctypes.c_int,
    wintypes.HDC,
    wintypes.LPCWSTR,
    ctypes.c_int,
    wintypes.LPRECT,
    wintypes.UINT
)(
    ('DrawTextW', user32),
    (
        (IN, "hdc"),
        (IN, "lpchText"),
        (IN, "cchText"),
        (IN, "lprc"),
        (IN, "format"),
    )
)


def DrawText(hdc: int, lpString: str, nCount: int, lpRect: wintypes.RECT, uFormat: int) -> int:
    ret = DrawTextW(hdc, lpString, nCount, ctypes.byref(lpRect), uFormat)
    if ret == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return ret


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enablemenuitem
# BOOL EnableMenuItem(
#   [in] HMENU hMenu,
#   [in] UINT  uIDEnableItem,
#   [in] UINT  uEnable
# );
_EnableMenuItem = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HMENU,
    wintypes.UINT,
    wintypes.UINT
)(
    ('EnableMenuItem', user32),
    (
        (IN, "hMenu"),
        (IN, "uIDEnableItem"),
        (IN, "uEnable"),
    )
)


def EnableMenuItem(hMenu: int, uIDEnableItem: int, uEnable: int) -> bool:
    # Returns previous state or -1 on failure
    ret = _EnableMenuItem(hMenu, uIDEnableItem, uEnable)
    if ret == -1:
        raise ctypes.WinError(ctypes.get_last_error())
    return True


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enablewindow
# BOOL EnableWindow(
#   [in] HWND hWnd,
#   [in] BOOL bEnable
# );
_EnableWindow = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.BOOL
)(
    ('EnableWindow', user32),
    (
        (IN, "hWnd"),
        (IN, "bEnable"),
    )
)


def EnableWindow(hWnd: int, bEnable: bool) -> bool:
    return _EnableWindow(hWnd, bEnable)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-endpaint
# BOOL EndPaint(
#   [in] HWND              hWnd,
#   [in] const PAINTSTRUCT *lpPaint
# );
_EndPaint = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    ctypes.POINTER(PAINTSTRUCT)
)(
    ('EndPaint', user32),
    (
        (IN, "hWnd"),
        (IN, "lpPaint"),
    )
)


def EndPaint(hwnd: int, ps: PAINTSTRUCT):
    _EndPaint(hwnd, ctypes.byref(ps))


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-fillrect
# int FillRect(
#   [in] HDC        hDC,
#   [in] const RECT *lprc,
#   [in] HBRUSH     hbr
# );
_FillRect = ctypes.WINFUNCTYPE(
    wintypes.INT,
    wintypes.HDC,
    wintypes.LPRECT,
    wintypes.HBRUSH
)(
    ('FillRect', user32),
    (
        (IN, "hDC"),
        (IN, "lprc"),
        (IN, "hbr"),
    )
)


def FillRect(hDC: int, lprc: wintypes.RECT, hbr: int) -> int:
    ret = _FillRect(hDC, ctypes.byref(lprc), hbr)
    if ret == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return ret


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-framerect
# int FrameRect(
#   [in] HDC        hDC,
#   [in] const RECT *lprc,
#   [in] HBRUSH     hbr
# );
_FrameRect = ctypes.WINFUNCTYPE(
    wintypes.INT,
    wintypes.HDC,
    wintypes.LPRECT,
    wintypes.HBRUSH
)(
    ('FrameRect', user32),
    (
        (IN, "hDC"),
        (IN, "lprc"),
        (IN, "hbr"),
    )
)


def FrameRect(hDC: int, lprc: wintypes.RECT, hbr: int) -> int:
    ret = _FrameRect(hDC, ctypes.byref(lprc), hbr)
    if ret == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return ret


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getclientrect
# BOOL GetClientRect(
#   [in]  HWND   hWnd,
#   [out] LPRECT lpRect
# );
_GetClientRect = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.LPRECT
)(
    ('GetClientRect', user32),
    (
        (IN, "hWnd"),
        (INOUT, "lpRect"),
    )
)
_GetClientRect.errcheck = errcheck_bool


def GetClientRect(hWnd: int) -> tuple[int, int, int, int, int, int] | None:
    """
    Args:
        hWnd (int): A handle to the window whose client coordinates are to be retrieved.

    Returns:
        tuple[int, int, int, int, int, int] | None: A tuple containing (left, top, right, bottom, width, height)
    """
    rect = wintypes.RECT()
    if _GetClientRect(hWnd, ctypes.byref(rect)):
        return rect.left, rect.top, rect.right, rect.bottom, rect.right - rect.left, rect.bottom - rect.top

    return None


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getcursorpos
# BOOL GetCursorPos(
#   [out] LPPOINT lpPoint
# );
_GetCursorPos = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.LPPOINT
)(
    ('GetCursorPos', user32),
    (
        (INOUT, "lpPoint"),
    )
)
_GetCursorPos.errcheck = errcheck_bool


def GetCursorPos() -> tuple[int, int]:
    pt = wintypes.POINT()
    _GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getdc
# HDC GetDC(
#   [in] HWND hWnd
# );
_GetDC = ctypes.WINFUNCTYPE(
    wintypes.HDC,
    wintypes.HWND
)(
    ('GetDC', user32),
    (
        (IN, "hWnd"),
    )
)


def GetDC(hWnd: int) -> int:
    return call_with_last_error_check(_GetDC, hWnd)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getmessagew
# BOOL GetMessageW(
#   [out]          LPMSG lpMsg,
#   [in, optional] HWND  hWnd,
#   [in]           UINT  wMsgFilterMin,
#   [in]           UINT  wMsgFilterMax
# );
GetMessageW = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.LPMSG,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.UINT
)(
    ('GetMessageW', user32),
    (
        (IN, "lpMsg"),
        (IN, "hWnd"),
        (IN, "wMsgFilterMin"),
        (IN, "wMsgFilterMax"),
    )
)


def GetMessage(lpMsg: Any, hWnd: int | None, wMsgFilterMin: int, wMsgFilterMax: int) -> int:
    # GetMessage can return -1 on error, 0 on WM_QUIT, and >0 on success.
    # It's a bit special, so standard errcheck might not be perfect, but let's wrap it.
    # However, GetMessage returning 0 is NOT an error (it means quit), so we shouldn't use _errcheck_bool
    # which raises on 0.
    # We'll just return the result directly as it's tri-state.
    return GetMessageW(lpMsg, hWnd, wMsgFilterMin, wMsgFilterMax)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsyscolor
# DWORD GetSysColor(
#   [in] int nIndex
# );
_GetSysColor = ctypes.WINFUNCTYPE(
    wintypes.COLORREF,
    ctypes.c_int
)(
    ('GetSysColor', user32),
    (
        (IN, "nIndex"),
    )
)


def GetSysColor(nIndex: int) -> int:
    return _GetSysColor(nIndex)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsyscolorbrush
# HBRUSH GetSysColorBrush(
#   [in] int nIndex
# );
_GetSysColorBrush = ctypes.WINFUNCTYPE(
    wintypes.HBRUSH,
    ctypes.c_int
)(
    ('GetSysColorBrush', user32),
    (
        (IN, "nIndex"),
    )
)


def GetSysColorBrush(nIndex: int) -> int:
    return call_with_last_error_check(_GetSysColorBrush, nIndex)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsystemmetrics
# int GetSystemMetrics(
#   [in] int nIndex
# );
_GetSystemMetrics = ctypes.WINFUNCTYPE(
    wintypes.INT,
    wintypes.INT
)(
    ('GetSystemMetrics', user32),
    (
        (IN, "nIndex"),
    )
)


def GetSystemMetrics(nIndex: int) -> int:
    return _GetSystemMetrics(nIndex)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowlongptrw
# LONG_PTR GetWindowLongPtrW(
#   [in] HWND hWnd,
#   [in] int  nIndex
# );
GetWindowLongPtrW = ctypes.WINFUNCTYPE(
    LONG_PTR,
    wintypes.HWND,
    wintypes.INT
)(
    ('GetWindowLongPtrW', user32),
    (
        (IN, "hWnd"),
        (IN, "nIndex"),
    )
)


def GetWindowLong(hWnd: int, nIndex: int) -> int:
    # GetWindowLongPtr can return 0 as a valid value (e.g. if the style is 0).
    # To check for error, we must clear last error, call it, then check last error.
    return call_with_last_error_check(GetWindowLongPtrW, hWnd, nIndex)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowrect
# BOOL GetWindowRect(
#   [in]  HWND   hWnd,
#   [out] LPRECT lpRect
# );
_GetWindowRect = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.LPRECT
)(
    ('GetWindowRect', user32),
    (
        (IN, "hWnd"),
        (INOUT, "lpRect"),
    )
)
_GetWindowRect.errcheck = errcheck_bool


def GetWindowRect(hWnd: int) -> tuple[int, int, int, int, int, int] | None:
    """
    Args:
        hWnd (int): A handle to the window whose window coordinates are to be retrieved.

    Returns:
        tuple[int, int, int, int, int, int] | None: A tuple containing (left, top, right, bottom, width, height)
    """
    rect = wintypes.RECT()
    if _GetWindowRect(hWnd, ctypes.byref(rect)):
        return rect.left, rect.top, rect.right, rect.bottom, rect.right - rect.left, rect.bottom - rect.top

    return None


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
        (INOUT, "lpString"),
        (IN, "nMaxCount"),
    )
)


def GetWindowText(hWnd: int, lpString: ctypes.Array, nMaxCount: int) -> int:
    return call_with_last_error_check(GetWindowTextW, hWnd, lpString, nMaxCount)


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


def GetWindowTextLength(hWnd: int) -> int:
    return call_with_last_error_check(GetWindowTextLengthW, hWnd)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowthreadprocessid
# DWORD GetWindowThreadProcessId(
#   [in]            HWND    hWnd,
#   [out, optional] LPDWORD lpdwProcessId
# );
_GetWindowThreadProcessId = ctypes.WINFUNCTYPE(
    wintypes.DWORD,
    wintypes.HWND,
    wintypes.LPDWORD
)(
    ('GetWindowThreadProcessId', user32),
    (
        (IN, "hWnd"),
        (INOUT, "lpdwProcessId"),
    )
)


def GetWindowThreadProcessId(hWnd: int) -> tuple[int, int]:
    pid = wintypes.DWORD()
    tid = _GetWindowThreadProcessId(hWnd, ctypes.byref(pid))
    if tid == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return tid, pid.value


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-invalidaterect
# BOOL InvalidateRect(
#   [in] HWND       hWnd,
#   [in] const RECT *lpRect,
#   [in] BOOL       bErase
# );
_InvalidateRect = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.LPRECT,
    wintypes.BOOL
)(
    ('InvalidateRect', user32),
    (
        (IN, "hWnd"),
        (IN, "lpRect"),
        (IN, "bErase"),
    )
)
_InvalidateRect.errcheck = errcheck_bool


def InvalidateRect(hWnd: int, lpRect: wintypes.RECT | None, bErase: bool) -> bool:
    return _InvalidateRect(hWnd, lpRect, bErase)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-isdialogmessagew
# BOOL IsDialogMessageW(
#   [in] HWND  hDlg,
#   [in] LPMSG lpMsg
# );
IsDialogMessageW = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.LPMSG
)(
    ('IsDialogMessageW', user32),
    (
        (IN, "hDlg"),
        (IN, "lpMsg"),
    )
)


def IsDialogMessage(hDlg: int, lpMsg: Any) -> bool:
    return IsDialogMessageW(hDlg, lpMsg)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-iswindowenabled
# BOOL IsWindowEnabled(
#   [in] HWND hWnd
# );
_IsWindowEnabled = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND
)(
    ('IsWindowEnabled', user32),
    (
        (IN, "hWnd"),
    )
)


def IsWindowEnabled(hWnd: int) -> bool:
    return _IsWindowEnabled(hWnd)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-killtimer
# BOOL KillTimer(
#   [in, optional] HWND     hWnd,
#   [in]           UINT_PTR uIDEvent
# );
_KillTimer = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    ULONG_PTR
)(
    ('KillTimer', user32),
    (
        (IN, "hWnd"),
        (IN, "uIDEvent"),
    )
)
_KillTimer.errcheck = errcheck_bool


def KillTimer(hWnd: int, uIDEvent: int) -> bool:
    return _KillTimer(hWnd, uIDEvent)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-loadcursorw
# HCURSOR LoadCursorW(
#   [in, optional] HINSTANCE hInstance,
#   [in]           LPCWSTR   lpCursorName
# );
LoadCursorW = ctypes.WINFUNCTYPE(
    wintypes.HANDLE,
    wintypes.HINSTANCE,
    wintypes.LPVOID
)(
    ('LoadCursorW', user32),
    (
        (IN, "hInstance"),
        (IN, "lpCursorName"),
    )
)


def LoadCursor(hInstance: int | None, lpCursorName: int | str) -> int:
    return call_with_last_error_check(LoadCursorW, hInstance, lpCursorName)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-loadiconw
# HICON LoadIconW(
#   [in, optional] HINSTANCE hInstance,
#   [in]           LPCWSTR   lpIconName
# );
LoadIconW = ctypes.WINFUNCTYPE(
    wintypes.HICON,
    wintypes.HINSTANCE,
    wintypes.LPCWSTR
)(
    ('LoadIconW', user32),
    (
        (IN, "hInstance"),
        (IN, "lpIconName"),
    )
)


def LoadIcon(hInstance: int | None, lpIconName: str | int) -> int:
    return call_with_last_error_check(LoadIconW, hInstance, lpIconName)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-loadimagew
# HANDLE LoadImageW(
#   [in, optional] HINSTANCE hInst,
#   [in]           LPCWSTR   name,
#   [in]           UINT      type,
#   [in]           int       cx,
#   [in]           int       cy,
#   [in]           UINT      fuLoad
# );
LoadImageW = ctypes.WINFUNCTYPE(
    wintypes.HANDLE,
    wintypes.HINSTANCE,
    wintypes.LPCWSTR,
    wintypes.UINT,
    ctypes.c_int,
    ctypes.c_int,
    wintypes.UINT
)(
    ('LoadImageW', user32),
    (
        (IN, "hInst"),
        (IN, "name"),
        (IN, "type"),
        (IN, "cx"),
        (IN, "cy"),
        (IN, "fuLoad"),
    )
)


def LoadImage(hInst: int | None, name: str, _type: int, cx: int, cy: int, fuLoad: int) -> int:
    return call_with_last_error_check(LoadImageW, hInst, name, _type, cx, cy, fuLoad)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mapwindowpoints
# int MapWindowPoints(
#   [in]      HWND    hWndFrom,
#   [in]      HWND    hWndTo,
#   [in, out] LPPOINT lpPoints,
#   [in]      UINT    cPoints
# );
_MapWindowPoints = ctypes.WINFUNCTYPE(
    wintypes.UINT,
    wintypes.HWND,
    wintypes.HWND,
    wintypes.LPRECT,
    wintypes.UINT
)(
    ('MapWindowPoints', user32),
    (
        (IN, "hWndFrom"),
        (IN, "hWndTo"),
        (INOUT, "lpPoints"),
        (IN, "cPoints"),
    )
)


def MapWindowPoints(hWndFrom: int, hWndTo: int, lpPoints: wintypes.RECT, cPoints: int) -> int:
    return call_with_last_error_check(_MapWindowPoints, hWndFrom, hWndTo, ctypes.byref(lpPoints), cPoints)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messageboxw
# int MessageBoxW(
#   [in, optional] HWND    hWnd,
#   [in, optional] LPCWSTR lpText,
#   [in, optional] LPCWSTR lpCaption,
#   [in]           UINT    uType
# );
MessageBoxW = ctypes.WINFUNCTYPE(
    wintypes.INT,
    wintypes.HWND,
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.UINT
)(
    ("MessageBoxW", user32),
    (
        (IN, "hWnd"),
        (IN, "lpText"),
        (IN, "lpCaption"),
        (IN, "uType"),
    )
)


def MessageBox(hWnd: int | None, lpText: str, lpCaption: str, uType: int) -> int:
    return call_with_last_error_check(MessageBoxW, hWnd, lpText, lpCaption, uType)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-movewindow
# BOOL MoveWindow(
#   [in] HWND hWnd,
#   [in] int  X,
#   [in] int  Y,
#   [in] int  nWidth,
#   [in] int  nHeight,
#   [in] BOOL bRepaint
# );
_MoveWindow = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    wintypes.BOOL
)(
    ('MoveWindow', user32),
    (
        (IN, "hWnd"),
        (IN, "X"),
        (IN, "Y"),
        (IN, "nWidth"),
        (IN, "nHeight"),
        (IN, "bRepaint"),
    )
)
_MoveWindow.errcheck = errcheck_bool


def MoveWindow(hWnd: int, X: int, Y: int, nWidth: int, nHeight: int, bRepaint: bool) -> bool:
    return _MoveWindow(hWnd, X, Y, nWidth, nHeight, bRepaint)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-postmessagew
# BOOL PostMessageW(
#   [in, optional] HWND   hWnd,
#   [in]           UINT   Msg,
#   [in]           WPARAM wParam,
#   [in]           LPARAM lParam
# );
PostMessageW = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM
)(
    ('PostMessageW', user32),
    (
        (IN, "hWnd"),
        (IN, "Msg"),
        (IN, "wParam"),
        (IN, "lParam"),
    )
)
PostMessageW.errcheck = errcheck_bool


def PostMessage(hWnd: int, Msg: int, wParam: int, lParam: int) -> bool:
    return PostMessageW(hWnd, Msg, wParam, lParam)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-postquitmessage
# void PostQuitMessage(
#   [in] int nExitCode
# );
_PostQuitMessage = ctypes.WINFUNCTYPE(
    None,
    wintypes.INT
)(
    ('PostQuitMessage', user32),
    (
        (IN, "nExitCode"),
    )
)


def PostQuitMessage(nExitCode: int) -> None:
    _PostQuitMessage(nExitCode)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-ptinrect
# BOOL PtInRect(
#   [in] const RECT *lprc,  # noqa
#   [in] POINT      pt
# );
_PtInRect = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.LPRECT,
    wintypes.POINT
)(
    ('PtInRect', user32),
    (
        (IN, "lprc"),
        (IN, "pt"),
    )
)


def PtInRect(lprc: wintypes.RECT, pt: wintypes.POINT) -> bool:
    return _PtInRect(ctypes.byref(lprc), pt)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-redrawwindow
# BOOL RedrawWindow(
#   [in] HWND       hWnd,
#   [in] const RECT *lprcUpdate,
#   [in] HRGN       hrgnUpdate,
#   [in] UINT       flags
# );
_RedrawWindow = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.LPRECT,
    wintypes.HRGN,
    wintypes.UINT
)(
    ('RedrawWindow', user32),
    (
        (IN, "hWnd"),
        (IN, "lprcUpdate"),
        (IN, "hrgnUpdate"),
        (IN, "flags"),
    )
)
_RedrawWindow.errcheck = errcheck_bool


def RedrawWindow(hWnd: int, lprcUpdate: wintypes.RECT | None, hrgnUpdate: int | None, flags: int) -> bool:
    return _RedrawWindow(hWnd, lprcUpdate, hrgnUpdate, flags)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-registerclassw
# ATOM RegisterClassW(
#   [in] const WNDCLASSW *lpWndClass
# );
RegisterClassW = ctypes.WINFUNCTYPE(
    wintypes.ATOM,
    ctypes.POINTER(WNDCLASS)
)(
    ('RegisterClassW', user32),
    (
        (IN, "lpWndClass"),
    )
)
RegisterClassW.errcheck = errcheck_zero


def RegisterClass(lpWndClass: WNDCLASS) -> int:
    return RegisterClassW(
        ctypes.byref(lpWndClass)
    )


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-registerclassexw
# ATOM RegisterClassExW(
#   [in] const WNDCLASSEXW *unnamedParam1
# );
RegisterClassExW = ctypes.WINFUNCTYPE(
    wintypes.ATOM,
    ctypes.POINTER(WNDCLASSEX)
)(
    ('RegisterClassExW', user32),
    (
        (IN, "unnamedParam1"),
    )
)
RegisterClassExW.errcheck = errcheck_zero


def RegisterClassEx(lpWndClassEx: WNDCLASSEX) -> int:
    return RegisterClassExW(
        ctypes.byref(lpWndClassEx)
    )


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-releasedc
# int ReleaseDC(
#   [in] HWND hWnd,
#   [in] HDC  hDC
# );
_ReleaseDC = ctypes.WINFUNCTYPE(
    wintypes.INT,
    wintypes.HWND,
    wintypes.HDC
)(
    ('ReleaseDC', user32),
    (
        (IN, "hWnd"),
        (IN, "hDC"),
    )
)


def ReleaseDC(hWnd: int, hDC: int) -> int:
    return _ReleaseDC(hWnd, hDC)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-screentoclient
# BOOL ScreenToClient(
#   [in] HWND    hWnd,
#        LPPOINT lpPoint
# );
_ScreenToClient = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.LPPOINT
)(
    ('ScreenToClient', user32),
    (
        (IN, "hWnd"),
        (INOUT, "lpPoint"),
    )
)
_ScreenToClient.errcheck = errcheck_bool


def ScreenToClient(hWnd: int, lpPoint: wintypes.POINT) -> bool:
    return _ScreenToClient(hWnd, ctypes.byref(lpPoint))


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendmessagew
# LRESULT SendMessageW(
#   [in] HWND   hWnd,
#   [in] UINT   Msg,
#   [in] WPARAM wParam,
#   [in] LPARAM lParam
# );
SendMessageW = ctypes.WINFUNCTYPE(
    wintypes.LPARAM,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPVOID
)(
    ('SendMessageW', user32),
    (
        (IN, "hWnd"),
        (IN, "Msg"),
        (IN, "wParam"),
        (IN, "lParam"),
    )
)


def SendMessage(hWnd: int, Msg: int, wParam: int, lParam: Any) -> int:
    return SendMessageW(hWnd, Msg, wParam, lParam)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setactivewindow
# HWND SetActiveWindow(
#   [in] HWND hWnd
# );
_SetActiveWindow = ctypes.WINFUNCTYPE(
    wintypes.HWND,
    wintypes.HWND
)(
    ('SetActiveWindow', user32),
    (
        (IN, "hWnd"),
    )
)


def SetActiveWindow(hWnd: int) -> int:
    return call_with_last_error_check(_SetActiveWindow, hWnd)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setfocus
# HWND SetFocus(
#   [in, optional] HWND hWnd
# );
_SetFocus = ctypes.WINFUNCTYPE(
    wintypes.HWND,
    wintypes.HWND
)(
    ('SetFocus', user32),
    (
        (IN, "hWnd"),
    )
)


def SetFocus(hWnd: int) -> int:
    return call_with_last_error_check(_SetFocus, hWnd)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setprocessdpiaware
# BOOL SetProcessDPIAware();
_SetProcessDPIAware = ctypes.WINFUNCTYPE(
    wintypes.BOOL
)(
    ('SetProcessDPIAware', user32),
    ()
)
_SetProcessDPIAware.errcheck = errcheck_bool


def SetProcessDPIAware() -> bool:
    return _SetProcessDPIAware()


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setscrollinfo
# int SetScrollInfo(
#   [in] HWND          hwnd,
#   [in] int           nBar,
#   [in] LPCSCROLLINFO lpsi,  # noqa
#   [in] BOOL          redraw
# );
_SetScrollInfo = ctypes.WINFUNCTYPE(
    wintypes.INT,
    wintypes.HWND,
    wintypes.INT,
    ctypes.POINTER(SCROLLINFO),
    wintypes.BOOL
)(
    ('SetScrollInfo', user32),
    (
        (IN, "hwnd"),
        (IN, "nBar"),
        (IN, "lpsi"),
        (IN, "redraw"),
    )
)


def SetScrollInfo(hwnd: int, nBar: int, lpsi: SCROLLINFO, redraw: bool) -> int:
    return _SetScrollInfo(hwnd, nBar, ctypes.byref(lpsi), redraw)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-settimer
# UINT_PTR SetTimer(
#   [in, optional] HWND      hWnd,
#   [in]           UINT_PTR  nIDEvent,
#   [in]           UINT      uElapse,
#   [in, optional] TIMERPROC lpTimerFunc
# );
_SetTimer = ctypes.WINFUNCTYPE(
    ULONG_PTR,
    wintypes.HWND,
    ULONG_PTR,
    wintypes.UINT,
    wintypes.LPVOID
)(
    ('SetTimer', user32),
    (
        (IN, "hWnd"),
        (IN, "nIDEvent"),
        (IN, "uElapse"),
        (IN, "lpTimerFunc"),
    )
)


def SetTimer(hWnd: int, nIDEvent: int, uElapse: int, lpTimerFunc: int | None) -> int:
    return call_with_last_error_check(_SetTimer, hWnd, nIDEvent, uElapse, lpTimerFunc)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowlongw
# LONG SetWindowLongW(
#   [in] HWND hWnd,
#   [in] int  nIndex,
#   [in] LONG dwNewLong
# );
SetWindowLongW = ctypes.WINFUNCTYPE(
    wintypes.LONG,
    wintypes.HWND,
    wintypes.INT,
    wintypes.LPVOID
)(
    ('SetWindowLongW', user32),
    (
        (IN, "hWnd"),
        (IN, "nIndex"),
        (IN, "dwNewLong"),
    )
)

# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowlongptrw
# LONG_PTR SetWindowLongPtrW(
#   [in] HWND     hWnd,
#   [in] int      nIndex,
#   [in] LONG_PTR dwNewLong
# );
if ctypes.sizeof(ctypes.c_void_p) == 8:
    SetWindowLongPtrW = ctypes.WINFUNCTYPE(
        LONG_PTR,
        wintypes.HWND,
        wintypes.INT,
        wintypes.LPVOID
    )(
        ('SetWindowLongPtrW', user32),
        (
            (IN, "hWnd"),
            (IN, "nIndex"),
            (IN, "dwNewLong"),
        )
    )
else:
    SetWindowLongPtrW = SetWindowLongW


def SetWindowLong(hWnd: int, nIndex: int, dwNewLong: int) -> int:
    return call_with_last_error_check(SetWindowLongPtrW, hWnd, nIndex, dwNewLong)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowpos
# BOOL SetWindowPos(
#   [in]           HWND hWnd,
#   [in, optional] HWND hWndInsertAfter,
#   [in]           int  X,
#   [in]           int  Y,
#   [in]           int  cx,
#   [in]           int  cy,
#   [in]           UINT uFlags
# );
_SetWindowPos = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.HWND,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    wintypes.UINT
)(
    ('SetWindowPos', user32),
    (
        (IN, "hWnd"),
        (IN, "hWndInsertAfter"),
        (IN, "X"),
        (IN, "Y"),
        (IN, "cx"),
        (IN, "cy"),
        (IN, "uFlags"),
    )
)
_SetWindowPos.errcheck = errcheck_bool


def SetWindowPos(hWnd: int, hWndInsertAfter: int, X: int, Y: int, cx: int, cy: int, uFlags: int) -> bool:
    """
    Changes the size, position, and Z order of a child, pop-up, or top-level window.

    Args:
        hWnd (int): A handle to the window.
        hWndInsertAfter (int): A handle to the window to precede the positioned window in the Z order.
        X (int): The new position of the left side of the window, in client coordinates.
        Y (int): The new position of the top of the window, in client coordinates.
        cx (int): The new width of the window, in pixels.
        cy (int): The new height of the window, in pixels.
        uFlags (int): The window sizing and positioning flags.

    Returns:
        bool: True if the function succeeds.
    """
    return _SetWindowPos(hWnd, hWndInsertAfter, X, Y, cx, cy, uFlags)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowrgn
# int SetWindowRgn(
#   [in] HWND hWnd,
#   [in] HRGN hRgn,
#   [in] BOOL bRedraw
# );
_SetWindowRgn = ctypes.WINFUNCTYPE(
    wintypes.INT,
    wintypes.HWND,
    wintypes.HRGN,
    wintypes.BOOL
)(
    ('SetWindowRgn', user32),
    (
        (IN, "hWnd"),
        (IN, "hRgn"),
        (IN, "bRedraw"),
    )
)


def SetWindowRgn(hWnd: int, hRgn: int, bRedraw: bool) -> int:
    return call_with_last_error_check(_SetWindowRgn, hWnd, hRgn, bRedraw)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowtextw
# BOOL SetWindowTextW(
#   [in]           HWND    hWnd,
#   [in, optional] LPCWSTR lpString
# );
SetWindowTextW = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.LPCWSTR
)(
    ('SetWindowTextW', user32),
    (
        (IN, "hWnd"),
        (IN, "lpString"),
    )
)
SetWindowTextW.errcheck = errcheck_bool


def SetWindowText(hWnd: int, lpString: str) -> bool:
    return SetWindowTextW(hWnd, lpString)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow
# BOOL ShowWindow(
#   [in] HWND hWnd,
#   [in] int  nCmdShow
# );
_ShowWindow = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.UINT
)(
    ('ShowWindow', user32),
    (
        (IN, "hWnd"),
        (IN, "nCmdShow"),
    )
)


def ShowWindow(hWnd: int, nCmdShow: int) -> bool:
    return _ShowWindow(hWnd, nCmdShow)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-trackmouseevent
# BOOL TrackMouseEvent(
#   [in, out] LPTRACKMOUSEEVENT lpEventTrack
# );
_TrackMouseEvent = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    ctypes.POINTER(TRACKMOUSEEVENT)
)(
    ('TrackMouseEvent', user32),
    (
        (INOUT, "lpEventTrack"),
    )
)
_TrackMouseEvent.errcheck = errcheck_bool


def TrackMouseEvent(lpEventTrack: TRACKMOUSEEVENT) -> bool:
    return _TrackMouseEvent(ctypes.byref(lpEventTrack))


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-translatemessage
# BOOL TranslateMessage(
#   [in] const MSG *lpMsg
# );
_TranslateMessage = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.LPMSG
)(
    ('TranslateMessage', user32),
    (
        (IN, "lpMsg"),
    )
)


def TranslateMessage(lpMsg: Any) -> bool:
    return _TranslateMessage(lpMsg)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-updatewindow
# BOOL UpdateWindow(
#   [in] HWND hWnd
# );
_UpdateWindow = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND
)(
    ('UpdateWindow', user32),
    (
        (IN, "hWnd"),
    )
)
_UpdateWindow.errcheck = errcheck_bool


def UpdateWindow(hWnd: int) -> bool:
    return _UpdateWindow(hWnd)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-unregisterclassw
# BOOL UnregisterClassW(
#   [in]           LPCWSTR   lpClassName,
#   [in, optional] HINSTANCE hInstance
# );
UnregisterClassW = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.LPCWSTR,
    wintypes.HINSTANCE
)(
    ('UnregisterClassW', user32),
    (
        (IN, "lpClassName"),
        (IN, "hInstance"),
    )
)
UnregisterClassW.errcheck = errcheck_bool


def UnregisterClass(lpClassName: str, hInstance: int) -> bool:
    return UnregisterClassW(lpClassName, hInstance)
