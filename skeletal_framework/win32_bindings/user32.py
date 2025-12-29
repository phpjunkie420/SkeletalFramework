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


# BOOL AppendMenuW(
#   [in]           HMENU    hMenu,
#   [in]           UINT     uFlags,
#   [in]           UINT_PTR uIDNewItem,
#   [in, optional] LPCWSTR  lpNewItem
# );
_AppendMenu = user32.AppendMenuW
_AppendMenu.argtypes = [wintypes.HMENU, wintypes.UINT, ctypes.c_void_p, ctypes.c_void_p]
_AppendMenu.restype = wintypes.BOOL


def AppendMenu(hMenu: int, uFlags: int, uIDNewItem: int, lpNewItem: str | None) -> bool:
    return _AppendMenu(hMenu, uFlags, uIDNewItem, lpNewItem) > 0


# HDC BeginPaint(
#   [in]  HWND          hWnd,
#   [out] LPPAINTSTRUCT lpPaint
# );
_BeginPaint = user32.BeginPaint
# noinspection PyDeprecation
_BeginPaint.argtypes = [wintypes.HWND, ctypes.POINTER(PAINTSTRUCT)]
_BeginPaint.restype = wintypes.HDC


def BeginPaint(hwnd: int) -> tuple[PAINTSTRUCT, int]:
    ps = PAINTSTRUCT()
    hdc = _BeginPaint(hwnd, ctypes.byref(ps))

    return ps, hdc


# LRESULT CallWindowProcW(
#   [in] WNDPROC lpPrevWndFunc,
#   [in] HWND    hWnd,
#   [in] UINT    Msg,
#   [in] WPARAM  wParam,
#   [in] LPARAM  lParam
# );
_CallWindowProc = user32.CallWindowProcW
_CallWindowProc.argtypes = [LONG_PTR, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
_CallWindowProc.restype = LRESULT


def CallWindowProc(lpPrevWndFunc: int, hWnd: int, Msg: int, wParam: int, lParam: int) -> int:
    return _CallWindowProc(lpPrevWndFunc, hWnd, Msg, wParam, lParam)


# HMENU CreateMenu();
CreateMenu = user32.CreateMenu
CreateMenu.restype = wintypes.HMENU

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
_CreateWindowEx = ctypes.WINFUNCTYPE(
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
        _CreateWindowEx,
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
_DefWindowProcW = user32.DefWindowProcW
_DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
_DefWindowProcW.restype = wintypes.LPARAM


def DefWindowProc(hWnd: int, Msg: int, wParam: int, lParam: int) -> int:
    return _DefWindowProcW(hWnd, Msg, wParam, lParam)


# BOOL DestroyIcon(
#   [in] HICON hIcon
# );
_DestroyIcon = user32.DestroyIcon
_DestroyIcon.argtypes = [wintypes.HICON]
_DestroyIcon.restype = wintypes.BOOL


def DestroyIcon(hIcon: int) -> bool:
    return _DestroyIcon(hIcon) > 0


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-destroywindow
# BOOL DestroyWindow(
#   [in] HWND hWnd
# );
_DestroyWindow = user32.DestroyWindow
_DestroyWindow.argtypes = [wintypes.HWND]
_DestroyWindow.restype = wintypes.BOOL
_DestroyWindow.errcheck = errcheck_bool


def DestroyWindow(hWnd: int) -> bool:
    return _DestroyWindow(hWnd)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-dispatchmessagew
# LRESULT DispatchMessageW(
#   [in] const MSG *lpMsg
# );
_DispatchMessage = user32.DispatchMessageW
_DispatchMessage.argtypes = [wintypes.LPMSG]
_DispatchMessage.restype = ctypes.c_ssize_t


def DispatchMessage(lpMsg: Any) -> int:
    return _DispatchMessage(lpMsg)


# BOOL DrawFocusRect(
#   [in] HDC        hDC,
#   [in] const RECT *lprc  # noqa
# );
DrawFocusRect = user32.DrawFocusRect
DrawFocusRect.argtypes = [wintypes.HDC, wintypes.LPRECT]
DrawFocusRect.restype = wintypes.BOOL

# BOOL DrawFrameControl(
#   [in] HDC    hdc,
#   [in] LPRECT lprc,  # noqa
#   [in] UINT   uType,
#   [in] UINT   uState
# );
DrawFrameControl = user32.DrawFrameControl
DrawFrameControl.argtypes = [wintypes.HDC, wintypes.LPRECT, wintypes.UINT, wintypes.UINT]
DrawFrameControl.restype = wintypes.BOOL

DrawText = user32.DrawTextW
DrawText.argtypes = [
    wintypes.HDC,
    wintypes.LPCWSTR,
    ctypes.c_int,
    wintypes.LPRECT,
    wintypes.UINT
]
# noinspection DuplicatedCode
DrawText.restype = ctypes.c_int

# BOOL EnableMenuItem(
#   [in] HMENU hMenu,
#   [in] UINT  uIDEnableItem,
#   [in] UINT  uEnable
# );
EnableMenuItem = user32.EnableMenuItem
EnableMenuItem.argtypes = [wintypes.HMENU, wintypes.UINT, wintypes.UINT]
EnableMenuItem.restype = wintypes.BOOL


# BOOL EnableWindow(
#   [in] HWND hWnd,
#   [in] BOOL bEnable
# );
EnableWindow = user32.EnableWindow
EnableWindow.argtypes = [wintypes.HWND, wintypes.BOOL]
EnableWindow.restype = wintypes.BOOL

# BOOL EndPaint(
#   [in] HWND              hWnd,
#   [in] const PAINTSTRUCT *lpPaint
# );
_EndPaint = user32.EndPaint
_EndPaint.argtypes = [wintypes.HWND, ctypes.POINTER(PAINTSTRUCT)]
_EndPaint.restype = wintypes.BOOL


def EndPaint(hwnd: int, ps: PAINTSTRUCT):
    _EndPaint(hwnd, ctypes.byref(ps))


FillRect = user32.FillRect
FillRect.argtypes = [wintypes.HDC, wintypes.LPRECT, wintypes.HBRUSH]
FillRect.restype = wintypes.INT

FrameRect = user32.FrameRect
FrameRect.argtypes = [wintypes.HDC, wintypes.LPRECT, wintypes.HBRUSH]
FrameRect.restype = wintypes.INT


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getclientrect
# BOOL GetClientRect(
#   [in]  HWND   hWnd,
#   [out] LPRECT lpRect
# );
_GetClientRect = user32.GetClientRect
_GetClientRect.argtypes = [wintypes.HWND, wintypes.LPRECT]
_GetClientRect.restype = wintypes.BOOL
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


# BOOL GetCursorPos(
#   [out] LPPOINT lpPoint
# );
GetCursorPos = user32.GetCursorPos
GetCursorPos.argtypes = [wintypes.LPPOINT]
# noinspection DuplicatedCode
GetCursorPos.restype = wintypes.BOOL

# HDC GetDC(
#   [in] HWND hWnd
# );
GetDC = user32.GetDC
GetDC.argtypes = [wintypes.HWND]
GetDC.restype = wintypes.HDC


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getmessagew
# BOOL GetMessageW(
#   [out]          LPMSG lpMsg,
#   [in, optional] HWND  hWnd,
#   [in]           UINT  wMsgFilterMin,
#   [in]           UINT  wMsgFilterMax
# );
_GetMessage = user32.GetMessageW
_GetMessage.argtypes = [wintypes.LPMSG, wintypes.HWND, wintypes.UINT, wintypes.UINT]
_GetMessage.restype = wintypes.BOOL


def GetMessage(lpMsg: Any, hWnd: int | None, wMsgFilterMin: int, wMsgFilterMax: int) -> int:
    # GetMessage can return -1 on error, 0 on WM_QUIT, and >0 on success.
    # It's a bit special, so standard errcheck might not be perfect, but let's wrap it.
    # However, GetMessage returning 0 is NOT an error (it means quit), so we shouldn't use _errcheck_bool
    # which raises on 0.
    # We'll just return the result directly as it's tri-state.
    return _GetMessage(lpMsg, hWnd, wMsgFilterMin, wMsgFilterMax)


GetSysColor = user32.GetSysColor
# noinspection DuplicatedCode
GetSysColor.argtypes = [ctypes.c_int]
GetSysColor.restype = wintypes.COLORREF

GetSysColorBrush = user32.GetSysColorBrush
GetSysColorBrush.argtypes = [ctypes.c_int]
GetSysColorBrush.restype = wintypes.HBRUSH

# int GetSystemMetrics(
#   [in] int nIndex
# );
GetSystemMetrics = user32.GetSystemMetrics
GetSystemMetrics.argtypes = [wintypes.INT]
GetSystemMetrics.restype = wintypes.INT

# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowlongptrw
# LONG_PTR GetWindowLongPtrW(
#   [in] HWND hWnd,
#   [in] int  nIndex
# );
_GetWindowLongPtrW = user32.GetWindowLongPtrW
_GetWindowLongPtrW.argtypes = [wintypes.HWND, wintypes.INT]
_GetWindowLongPtrW.restype = LONG_PTR


def GetWindowLong(hWnd: int, nIndex: int) -> int:
    # GetWindowLongPtr can return 0 as a valid value (e.g. if the style is 0).
    # To check for error, we must clear last error, call it, then check last error.
    return call_with_last_error_check(_GetWindowLongPtrW, hWnd, nIndex)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowrect
# BOOL GetWindowRect(
#   [in]  HWND   hWnd,
#   [out] LPRECT lpRect
# );
_GetWindowRect = user32.GetWindowRect
_GetWindowRect.argtypes = [wintypes.HWND, wintypes.LPRECT]
_GetWindowRect.restype = wintypes.BOOL
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


# int GetWindowTextW(
#   [in]  HWND   hWnd,
#   [out] LPWSTR lpString,
#   [in]  int    nMaxCount
# );
GetWindowText = user32.GetWindowTextW
GetWindowText.argtypes = [wintypes.HWND, wintypes.LPWSTR, wintypes.INT]
GetWindowText.restype = wintypes.INT

# int GetWindowTextLengthW(
#   [in] HWND hWnd
# );
GetWindowTextLength = user32.GetWindowTextLengthW
GetWindowTextLength.argtypes = [wintypes.HWND]
GetWindowTextLength.restype = wintypes.INT

# DWORD GetWindowThreadProcessId(
#   [in]            HWND    hWnd,
#   [out, optional] LPDWORD lpdwProcessId
# );
GetWindowThreadProcessId = user32.GetWindowThreadProcessId
GetWindowThreadProcessId.argtypes = [wintypes.HWND, wintypes.LPDWORD]
GetWindowThreadProcessId.restype = wintypes.DWORD

# BOOL InvalidateRect(
#   [in] HWND       hWnd,
#   [in] const RECT *lpRect,
#   [in] BOOL       bErase
# );
InvalidateRect = user32.InvalidateRect
InvalidateRect.argtypes = [wintypes.HWND, wintypes.LPRECT, wintypes.BOOL]
InvalidateRect.restype = wintypes.BOOL

# BOOL IsDialogMessageW(
#   [in] HWND  hDlg,
#   [in] LPMSG lpMsg
# );
IsDialogMessage = user32.IsDialogMessageW
IsDialogMessage.argtypes = [wintypes.HWND, wintypes.LPMSG]
IsDialogMessage.restype = wintypes.BOOL

# BOOL IsWindowEnabled(
#   [in] HWND hWnd
# );
IsWindowEnabled = user32.IsWindowEnabled
IsWindowEnabled.argtypes = [wintypes.HWND]
IsWindowEnabled.restype = wintypes.BOOL

# BOOL KillTimer(
#   [in, optional] HWND     hWnd,
#   [in]           UINT_PTR uIDEvent
# );
KillTimer = user32.KillTimer
KillTimer.argtypes = [wintypes.HWND, ULONG_PTR]
# noinspection DuplicatedCode
KillTimer.restype = wintypes.BOOL


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-loadcursorw
# HCURSOR LoadCursorW(
#   [in, optional] HINSTANCE hInstance,
#   [in]           LPCWSTR   lpCursorName
# );
_LoadCursor = user32.LoadCursorW
_LoadCursor.argtypes = [wintypes.HINSTANCE, wintypes.LPVOID]
_LoadCursor.restype = wintypes.HANDLE


def LoadCursor(hInstance: int | None, lpCursorName: int | str) -> int:
    return call_with_last_error_check(_LoadCursor, hInstance, lpCursorName)


# HICON LoadIconW(
#   [in, optional] HINSTANCE hInstance,
#   [in]           LPCWSTR   lpIconName
# );
LoadIcon = user32.LoadIconW
LoadIcon.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR]
LoadIcon.restype = wintypes.HICON

# HANDLE LoadImageW(
#   [in, optional] HINSTANCE hInst,
#   [in]           LPCWSTR   name,
#   [in]           UINT      type,
#   [in]           int       cx,
#   [in]           int       cy,
#   [in]           UINT      fuLoad
# );
LoadImage = user32.LoadImageW
LoadImage.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR, wintypes.UINT, ctypes.c_int, ctypes.c_int, wintypes.UINT]
LoadImage.restype = wintypes.HANDLE

# int MapWindowPoints(
#   [in]      HWND    hWndFrom,
#   [in]      HWND    hWndTo,
#   [in, out] LPPOINT lpPoints,
#   [in]      UINT    cPoints
# );
MapWindowPoints = user32.MapWindowPoints
MapWindowPoints.argtypes = [wintypes.HWND, wintypes.HWND, wintypes.LPRECT, wintypes.UINT]
MapWindowPoints.restype = wintypes.UINT


# int MessageBox(
#   [in, optional] HWND    hWnd,
#   [in, optional] LPCTSTR lpText,
#   [in, optional] LPCTSTR lpCaption,
#   [in]           UINT    uType
# );
MessageBox = ctypes.WINFUNCTYPE(
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

# BOOL MoveWindow(
#   [in] HWND hWnd,
#   [in] int  X,
#   [in] int  Y,
#   [in] int  nWidth,
#   [in] int  nHeight,
#   [in] BOOL bRepaint
# );
MoveWindow = user32.MoveWindow
MoveWindow.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.BOOL]
MoveWindow.restype = wintypes.BOOL

# BOOL PostMessageW(
#   [in, optional] HWND   hWnd,
#   [in]           UINT   Msg,
#   [in]           WPARAM wParam,
#   [in]           LPARAM lParam
# );
PostMessage = user32.PostMessageW
PostMessage.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
PostMessage.restype = wintypes.BOOL


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-postquitmessage
# void PostQuitMessage(
#   [in] int nExitCode
# );
_PostQuitMessage = user32.PostQuitMessage
_PostQuitMessage.argtypes = [wintypes.INT]


def PostQuitMessage(nExitCode: int) -> None:
    _PostQuitMessage(nExitCode)


# BOOL PtInRect(
#   [in] const RECT *lprc,  # noqa
#   [in] POINT      pt
# );
PtInRect = user32.PtInRect
PtInRect.argtypes = [wintypes.LPRECT, wintypes.POINT]
PtInRect.restype = wintypes.BOOL

# BOOL RedrawWindow(
#   [in] HWND       hWnd,
#   [in] const RECT *lprcUpdate,
#   [in] HRGN       hrgnUpdate,
#   [in] UINT       flags
# );
RedrawWindow = user32.RedrawWindow
RedrawWindow.argtypes = [wintypes.HWND, wintypes.LPRECT, wintypes.HRGN, wintypes.UINT]
RedrawWindow.restype = wintypes.BOOL


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-registerclassw
# ATOM RegisterClassW(
#   [in] const WNDCLASSW *lpWndClass
# );
_RegisterClass = user32.RegisterClassW
_RegisterClass.argtypes = [ctypes.POINTER(WNDCLASS)]
_RegisterClass.restype = wintypes.ATOM
_RegisterClass.errcheck = errcheck_zero


def RegisterClass(lpWndClass: WNDCLASS) -> int:
    return _RegisterClass(
        ctypes.byref(lpWndClass)
    )


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-registerclassexw
# ATOM RegisterClassExW(
#   [in] const WNDCLASSEXW *unnamedParam1
# );
_RegisterClassEx = user32.RegisterClassExW
_RegisterClassEx.argtypes = [ctypes.POINTER(WNDCLASSEX)]
_RegisterClassEx.restype = wintypes.ATOM
_RegisterClassEx.errcheck = errcheck_zero


def RegisterClassEx(lpWndClassEx: WNDCLASSEX) -> int:
    return _RegisterClassEx(
        ctypes.byref(lpWndClassEx)
    )


# int ReleaseDC(
#   [in] HWND hWnd,
#   [in] HDC  hDC
# );
ReleaseDC = user32.ReleaseDC
ReleaseDC.argtypes = [wintypes.HWND, wintypes.HDC]
ReleaseDC.restype = wintypes.INT

# BOOL ScreenToClient(
#   [in] HWND    hWnd,
#        LPPOINT lpPoint
# );
ScreenToClient = user32.ScreenToClient
ScreenToClient.argtypes = [wintypes.HWND, wintypes.LPPOINT]
ScreenToClient.restype = wintypes.BOOL

SendMessage = user32.SendMessageW
# noinspection DuplicatedCode
SendMessage.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPVOID]
SendMessage.restype = wintypes.LPARAM

# HWND SetActiveWindow(
#   [in] HWND hWnd
# );
SetActiveWindow = user32.SetActiveWindow
SetActiveWindow.argtypes = [wintypes.HWND]
SetActiveWindow.restype = wintypes.HWND

# HWND SetFocus(
#   [in, optional] HWND hWnd
# );
SetFocus = user32.SetFocus
SetFocus.argtypes = [wintypes.HWND]
SetFocus.restype = wintypes.HWND

# BOOL SetProcessDPIAware();
SetProcessDPIAware = user32.SetProcessDPIAware
SetProcessDPIAware.restype = wintypes.BOOL

# int SetScrollInfo(
#   [in] HWND          hwnd,
#   [in] int           nBar,
#   [in] LPCSCROLLINFO lpsi,  # noqa
#   [in] BOOL          redraw
# );
SetScrollInfo = user32.SetScrollInfo
SetScrollInfo.argtypes = [wintypes.HWND, wintypes.INT, ctypes.POINTER(SCROLLINFO), wintypes.BOOL]
SetScrollInfo.restype = wintypes.INT

# UINT_PTR SetTimer(
#   [in, optional] HWND      hWnd,
#   [in]           UINT_PTR  nIDEvent,
#   [in]           UINT      uElapse,
#   [in, optional] TIMERPROC lpTimerFunc
# );
SetTimer = user32.SetTimer
SetTimer.argtypes = [wintypes.HWND, ULONG_PTR, wintypes.UINT, wintypes.LPVOID]
SetTimer.restype = ULONG_PTR


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowlongw
# LONG SetWindowLongW(
#   [in] HWND hWnd,
#   [in] int  nIndex,
#   [in] LONG dwNewLong
# );
_SetWindowLongW = user32.SetWindowLongW
_SetWindowLongW.argtypes = [wintypes.HWND, wintypes.INT, wintypes.LPVOID]
_SetWindowLongW.restype = wintypes.LONG

# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowlongptrw
# LONG_PTR SetWindowLongPtrW(
#   [in] HWND     hWnd,
#   [in] int      nIndex,
#   [in] LONG_PTR dwNewLong
# );
if ctypes.sizeof(ctypes.c_void_p) == 8:
    _SetWindowLongPtrW = user32.SetWindowLongPtrW
    _SetWindowLongPtrW.argtypes = [wintypes.HWND, wintypes.INT, wintypes.LPVOID]
    _SetWindowLongPtrW.restype = LONG_PTR
else:
    _SetWindowLongPtrW = _SetWindowLongW


def SetWindowLong(hWnd: int, nIndex: int, dwNewLong: int) -> int:
    return call_with_last_error_check(_SetWindowLongPtrW, hWnd, nIndex, dwNewLong)


# BOOL SetWindowPos(
#   [in]           HWND hWnd,
#   [in, optional] HWND hWndInsertAfter,
#   [in]           int  X,
#   [in]           int  Y,
#   [in]           int  cx,
#   [in]           int  cy,
#   [in]           UINT uFlags
# );
_SetWindowPos = user32.SetWindowPos
_SetWindowPos.argtypes = [
    wintypes.HWND,
    wintypes.HWND,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    wintypes.UINT
]
_SetWindowPos.restype = wintypes.BOOL
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


# int SetWindowRgn(
#   [in] HWND hWnd,
#   [in] HRGN hRgn,
#   [in] BOOL bRedraw
# );
SetWindowRgn = user32.SetWindowRgn
SetWindowRgn.argtypes = [wintypes.HWND, wintypes.HRGN, wintypes.BOOL]
SetWindowRgn.restype = wintypes.INT


# BOOL SetWindowTextW(
#   [in]           HWND    hWnd,
#   [in, optional] LPCWSTR lpString
# );
SetWindowText = user32.SetWindowTextW
SetWindowText.argtypes = [wintypes.HWND, wintypes.LPCWSTR]
SetWindowText.restype = wintypes.BOOL


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow
# BOOL ShowWindow(
#   [in] HWND hWnd,
#   [in] int  nCmdShow
# );
_ShowWindow = user32.ShowWindow
_ShowWindow.argtypes = [wintypes.HWND, wintypes.UINT]
_ShowWindow.restype = wintypes.BOOL


def ShowWindow(hWnd: int, nCmdShow: int) -> bool:
    return _ShowWindow(hWnd, nCmdShow)


# BOOL TrackMouseEvent(
#   [in, out] LPTRACKMOUSEEVENT lpEventTrack
# );
TrackMouseEvent = user32.TrackMouseEvent
TrackMouseEvent.argtypes = [ctypes.POINTER(TRACKMOUSEEVENT)]
TrackMouseEvent.restype = wintypes.BOOL


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-translatemessage
# BOOL TranslateMessage(
#   [in] const MSG *lpMsg
# );
_TranslateMessage = user32.TranslateMessage
_TranslateMessage.argtypes = [wintypes.LPMSG]
_TranslateMessage.restype = wintypes.BOOL


def TranslateMessage(lpMsg: Any) -> bool:
    return _TranslateMessage(lpMsg)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-updatewindow
# BOOL UpdateWindow(
#   [in] HWND hWnd
# );
_UpdateWindow = user32.UpdateWindow
_UpdateWindow.argtypes = [wintypes.HWND]
_UpdateWindow.restype = wintypes.BOOL
_UpdateWindow.errcheck = errcheck_bool


def UpdateWindow(hWnd: int) -> bool:
    return _UpdateWindow(hWnd)


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-unregisterclassw
# BOOL UnregisterClassW(
#   [in]           LPCWSTR   lpClassName,
#   [in, optional] HINSTANCE hInstance
# );
_UnregisterClass = user32.UnregisterClassW
_UnregisterClass.argtypes = [wintypes.LPCWSTR, wintypes.HINSTANCE]
_UnregisterClass.restype = wintypes.BOOL
_UnregisterClass.errcheck = errcheck_bool


def UnregisterClass(lpClassName: str, hInstance: int) -> bool:
    return _UnregisterClass(lpClassName, hInstance)
