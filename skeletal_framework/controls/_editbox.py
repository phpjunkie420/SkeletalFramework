import ctypes
from ctypes import wintypes

import win32con

from skeletal_framework.core_context import CoreContext
from skeletal_framework.win32_bindings.gdi32 import (
    CreateFontIndirect, LOGFONT, CreateSolidBrush, DeleteObject, SetTextColor, SetBkColor
)
from skeletal_framework.win32_bindings.kernel32 import GetModuleHandle
from skeletal_framework.win32_bindings.user32 import (
    CreateWindowEx, DefWindowProc, DestroyWindow, SetWindowLong, GetWindowLong, CallWindowProc, WNDPROC, HideCaret, SendMessage, SetWindowText
)


class EditBox:
    """
    A self-contained, customizable Edit control wrapper for the Win32 API.

    This class encapsulates the creation and management of a Win32 EDIT control,
    allowing for easy customization of font, colors, and behavior like read-only state.
    It uses window subclassing to handle its own focus messages (to hide the caret)
    and provides a handler for the parent to delegate color messages.
    """

    def __init__(
            self,
            x: int, y: int, width: int, height: int,
            /, *,
            text: str = "",
            font_name: str = "Segoe UI",
            font_size: int = 12,
            text_color: int = wintypes.RGB(255, 0, 0),
            bg_color: int = wintypes.RGB(75, 75, 75),
            read_only: bool = False,
            parent_hwnd: int | None = None
    ):
        self._core_context = CoreContext()

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color
        self.bg_color = bg_color
        self.read_only = read_only

        self._parent_hwnd = parent_hwnd
        if parent_hwnd is None:
            self._parent_hwnd = self._core_context.main_window

        self._h_instance = GetModuleHandle(None)
        self._font = self._create_font(font_name, font_size)
        self._bg_brush = CreateSolidBrush(self.bg_color)

        self._hwnd = self._create_window()
        self._original_wnd_proc = 0

        SetWindowLong(self._hwnd, win32con.GWL_USERDATA, id(self))
        self._parent_proc = SetWindowLong(self._hwnd, win32con.GWL_WNDPROC, _subclass_wnd_proc)

    @staticmethod
    def _create_font(font_name, font_size):
        return CreateFontIndirect(
            LOGFONT(
                height = -int(font_size * 1.333),
                face_name = font_name,
                quality = win32con.CLEARTYPE_QUALITY,
            )
        )

    def _create_window(self):
        style = (
                win32con.WS_CHILD |
                win32con.WS_VISIBLE |
                win32con.WS_BORDER |
                win32con.ES_MULTILINE |
                win32con.ES_AUTOVSCROLL |
                win32con.WS_VSCROLL
        )
        if self.read_only:
            style |= win32con.ES_READONLY

        hwnd = CreateWindowEx(
            dwExStyle = win32con.WS_EX_CLIENTEDGE,
            lpClassName = 'EDIT',
            lpWindowName = self.text,
            dwStyle = style,
            x = self.x, y = self.y,
            nWidth = self.width, nHeight = self.height,
            hWndParent = self._parent_hwnd,
            hMenu = None,
            hInstance = self._h_instance,
            lpParam = id(self)
        )
        SendMessage(hwnd, win32con.WM_SETFONT, self._font, True)
        return hwnd

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        """Handles messages for this specific EditBox instance."""
        if msg == win32con.WM_SETFOCUS and self.read_only:
            HideCaret(hwnd)

        if msg == win32con.WM_NCDESTROY:
            # Clean up GDI objects and unsubclass
            SetWindowLong(self._hwnd, win32con.GWL_WNDPROC, self._parent_proc)
            if self._font:
                DeleteObject(self._font)
            if self._bg_brush:
                DeleteObject(self._bg_brush)
            SetWindowLong(self._hwnd, win32con.GWL_USERDATA, 0)

        return CallWindowProc(self._parent_proc, hwnd, msg, wparam, lparam)

    def handle_color(self, hdc: int) -> int:
        """
        To be called by the parent window from its WM_CTLCOLORSTATIC handler.
        Sets the text and background colors and returns the background brush.
        """
        SetTextColor(hdc, self.text_color)
        SetBkColor(hdc, self.bg_color)
        return self._bg_brush

    @property
    def hwnd(self) -> int:
        return self._hwnd

    def set_text(self, text: str):
        """Sets the text of the edit control."""
        self.text = text
        SetWindowText(self._hwnd, self.text)

    def destroy(self):
        """Destroys the window handle."""
        if self._hwnd:
            DestroyWindow(self._hwnd)
            self._hwnd = None


# Global subclass procedure
@WNDPROC
def _subclass_wnd_proc(hwnd, msg, wparam, lparam):
    """
    A global window procedure to intercept messages for our EditBox instances.
    It retrieves the Python object associated with the hwnd and calls its instance-specific message handler.
    """
    instance_id = GetWindowLong(hwnd, win32con.GWL_USERDATA)
    if instance_id == 0:
        # This can happen if messages are received after we've started to unsubclass.
        return DefWindowProc(hwnd, msg, wparam, lparam)

    try:
        instance = ctypes.cast(instance_id, ctypes.py_object).value
        return instance.wnd_proc(hwnd, msg, wparam, lparam)
    except (ValueError, ctypes.ArgumentError):
        # This can happen if the window is being destroyed and the object is already gone.
        return DefWindowProc(hwnd, msg, wparam, lparam)
