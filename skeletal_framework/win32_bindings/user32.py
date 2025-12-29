import ctypes
from ctypes import wintypes
from collections.abc import Callable
from typing import Any

from win32_bindings.errcheck import errcheck_bool, errcheck_zero, call_with_last_error_check

__all__ = [
    'CREATESTRUCT',
    'WNDPROC', 'WNDCLASS', 'WNDCLASSEX',
    'CreateWindowEx',
    'DefWindowProc', 'DestroyWindow', 'DispatchMessage',
    'GetClientRect', 'GetMessage', 'GetWindowLong', 'GetWindowRect',
    'LoadCursor',
    'PostQuitMessage',
    'RegisterClass', 'RegisterClassEx',
    'SetWindowLong', 'SetWindowPos', 'ShowWindow',
    'TranslateMessage',
    'UnregisterClass', 'UpdateWindow'
]


if ctypes.sizeof(ctypes.c_void_p) == 8:  # 64-bit
    ULONG_PTR = LONG_PTR = LRESULT = ctypes.c_longlong
else:                                    # 32-bit
    ULONG_PTR = LONG_PTR = LRESULT = ctypes.c_long

IN = 1
OUT = 3
INOUT = 3

user32 = ctypes.WinDLL('user32', use_last_error = True)

_WNDPROC = ctypes.WINFUNCTYPE(
    ctypes.HRESULT,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM
)


def WNDPROC(func: Callable[..., Any]) -> Any:
    return _WNDPROC(func)


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


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-postquitmessage
# void PostQuitMessage(
#   [in] int nExitCode
# );
_PostQuitMessage = user32.PostQuitMessage
_PostQuitMessage.argtypes = [wintypes.INT]


def PostQuitMessage(nExitCode: int) -> None:
    _PostQuitMessage(nExitCode)


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
