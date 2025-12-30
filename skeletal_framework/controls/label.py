from ctypes import wintypes
from enum import IntEnum

import win32con

from skeletal_framework.core_context import CoreContext
from skeletal_framework.dispatcher import Dispatcher
from skeletal_framework.win32_bindings.gdi32 import *
from skeletal_framework.win32_bindings.user32 import *

__all__ = ['Style', 'Label']


class Style(IntEnum):
    Left = 0
    Center = 1
    Right = 2


class Label:

    _class_registered = False
    _class_name = "LabelClass"

    @property
    def hwnd(self) -> int: return self._hwnd

    def __init__(self, text: str, x: int, y: int, width: int, height: int, ctrl_id: int, /, *, parent_hwnd: int | None = None, style: Style = Style.Left, font_name: str = 'Segoe UI', font_size: int = 10):
        self._context = CoreContext()
        self._parent_hwnd = parent_hwnd or self._context.main_window

        self._font = self._create_font(font_name, font_size)
        self._style = style

        self._register_class(self._context.h_instance)
        self._hwnd = self._create_window(text, x, y, width, height, style, ctrl_id)

    def _create_window(self, text: str, x: int, y: int, width: int, height: int, style: Style, ctrl_id: int):
        return CreateWindowEx(
            dwExStyle = 0,
            lpClassName = self._class_name,
            lpWindowName = text,
            dwStyle = win32con.WS_CHILD | win32con.WS_VISIBLE | style,
            x = x, y = y, nWidth = width, nHeight = height,
            hWndParent = self._parent_hwnd,
            hMenu = ctrl_id,
            hInstance = self._context.h_instance,
            lpParam = id(self)
        )

    @classmethod
    def _register_class(cls, h_instance) -> None:
        """Register the window class for the image panel."""
        if cls._class_registered:
            return

        RegisterClassEx(
            WNDCLASSEX(
                style = win32con.CS_HREDRAW | win32con.CS_VREDRAW,
                lpfnWndProc = Dispatcher,
                hInstance = h_instance,
                hCursor = LoadCursor(0, win32con.IDC_ARROW),
                hbrBackground = 0,
                lpszClassName = cls._class_name
            )
        )
        cls._class_registered = True

    @staticmethod
    def _create_font(font_name: str, font_size: int) -> int:
        """Helper method to create a LOGFONT structure."""
        return CreateFontIndirect(
            LOGFONT(
                height = -int(font_size * 1.333),
                weight = win32con.FW_NORMAL,
                charset = win32con.DEFAULT_CHARSET,
                out_precision = win32con.OUT_DEFAULT_PRECIS,
                clip_precision = win32con.CLIP_DEFAULT_PRECIS,
                quality = win32con.DEFAULT_QUALITY,
                pitch_and_family = win32con.DEFAULT_PITCH | win32con.FF_DONTCARE,
                face_name = font_name,
            )
        )

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_SETTEXT:
            result = DefWindowProc(hwnd, msg, wparam, lparam)
            InvalidateRect(hwnd, None, False)
            return result

        elif msg == win32con.WM_ERASEBKGND:
            return 1

        elif msg == win32con.WM_PAINT:
            ps, hdc = BeginPaint(hwnd)
            *_, rect = GetClientRect(hwnd)

            text = GetWindowText(hwnd)

            bg_brush = CreateSolidBrush(
                wintypes.RGB(
                    red = 75, green = 75, blue = 75
                )
            )
            FillRect(hdc, rect, bg_brush)

            SetBkMode(hdc, win32con.TRANSPARENT)

            old_font = SelectObject(hdc, self._font)
            SetTextColor(hdc, wintypes.RGB(255, 255, 255))
            DrawText(
                hdc, text, -1, rect,
                win32con.DT_SINGLELINE | win32con.DT_VCENTER | self._style
            )

            SelectObject(hdc, old_font)
            EndPaint(hwnd, ps)
            return 0

        return DefWindowProc(hwnd, msg, wparam, lparam)
