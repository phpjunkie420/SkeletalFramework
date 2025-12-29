import ctypes
from ctypes import Array, wintypes

from skeletal_framework.win32_bindings.errcheck import errcheck_bool, errcheck_zero, call_with_last_error_check

# region Win32 Bindings
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
user32 = ctypes.WinDLL('user32', use_last_error=True)

IN = 1
OUT = 2
INOUT = 3

# https://learn.microsoft.com/en-us/windows/console/getconsolewindow
# HWND WINAPI GetConsoleWindow(void);
_GetConsoleWindow = ctypes.WINFUNCTYPE(
    wintypes.HWND
)(
    ('GetConsoleWindow', kernel32),
    ()
)


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
_GetWindowThreadProcessId.errcheck = errcheck_zero


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowtextw
# int GetWindowTextW(
#   [in]  HWND   hWnd,
#   [out] LPWSTR lpString,
#   [in]  int    nMaxCount
# );
GetWindowTextW = ctypes.WINFUNCTYPE(
    ctypes.c_int,
    wintypes.HWND,
    wintypes.LPWSTR,
    ctypes.c_int
)(
    ('GetWindowTextW', user32),
    (
        (IN, "hWnd"),
        (INOUT, "lpString"),
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


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowrect
# BOOL GetWindowRect(
#   [in]  HWND   hWnd,
#   [out] LPRECT lpRect
# );
_GetWindowRect = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    ctypes.POINTER(wintypes.RECT)
)(
    ('GetWindowRect', user32),
    (
        (IN, "hWnd"),
        (INOUT, "lpRect"),
    )
)
_GetWindowRect.errcheck = errcheck_bool


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
# endregion


def GetConsoleWindow() -> int:
    """
    Retrieves the window handle used by the console associated with the calling process.

    Returns:
        int: The return value is a handle to the window used by the console associated with the calling process
             or NULL if there is no such associated console.
    """
    return _GetConsoleWindow()


def GetWindowThreadProcessId(hWnd: int) -> tuple[int, int]:
    """
    Retrieves the identifier of the thread that created the specified window and, optionally, the identifier of the
    process that created the window.

    Args:
        hWnd (int): A handle to the window.

    Returns:
        tuple[int, int]: A tuple containing (thread_id, process_id).
    """
    pid = wintypes.DWORD()
    tid = _GetWindowThreadProcessId(hWnd, ctypes.byref(pid))

    return tid, pid.value


def GetWindowTextLength(hWnd: int) -> tuple[Array, int]:
    """
    Retrieves the length, in characters, of the specified window's title bar text (if the window has a title bar).

    Args:
        hWnd (int): A handle to the window or control.

    Returns:
        tuple[ctypes.Array, int]: A tuple containing the text buffer (ctypes array) and the text length.
    """
    text_len = call_with_last_error_check(GetWindowTextLengthW, hWnd) + 1
    text_buffer: Array = ctypes.create_unicode_buffer(text_len)

    return text_buffer, text_len


def GetWindowText(hWnd: int) -> str:
    """
    Copies the text of the specified window's title bar (if it has one) into a buffer.

    Args:
        hWnd (int): A handle to the window or control.

    Returns:
        str: The text of the window's title bar.
    """
    text_buffer, text_len = GetWindowTextLength(hWnd)

    call_with_last_error_check(GetWindowTextW, hWnd, text_buffer, text_len)
    return text_buffer.value


def GetWindowRect(hWnd: int) -> tuple[int, int, int, int]:
    """
    Retrieves the dimensions of the bounding rectangle of the specified window.
    The dimensions are given in screen coordinates that are relative to the upper-left corner of the screen.

    Args:
        hWnd (int): A handle to the window.

    Returns:
        tuple[int, int, int, int]: A tuple containing (left, top, right, bottom) coordinates.
    """
    rect = wintypes.RECT()
    _GetWindowRect(hWnd, ctypes.byref(rect))
    return rect.left, rect.top, rect.right, rect.bottom


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
    _SetWindowPos(hWnd, hWndInsertAfter, X, Y, cx, cy, uFlags)
    return True
