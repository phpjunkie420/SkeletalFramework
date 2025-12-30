import ctypes
from ctypes import wintypes
from typing import Any

import win32con

from core.core_context import CoreContext
from ui.controls.control import *
from win32 import *

__all__ = ['Button']


class Button(Control):

    @property
    def hwnd(self) -> bool: return self._hwnd

    @property
    def is_enabled(self) -> bool: return IsWindowEnabled(self._hwnd)

    @is_enabled.setter
    def is_enabled(self, value: bool): EnableWindow(self._hwnd, value)

    def __init__(
        self,
        parent_hwnd: int,
        ctrl_id: int,
        text: str,
        x: int, y: int, width: int, height: int,
        weight: int = win32con.FW_NORMAL,
        font_name: str = 'Segoe UI',
        font_size: int = 12,
        parent_bckgnd: Any = None,
        corner_radius: int = 5,
        enabled: bool = True,
    ):
        self._context = CoreContext()

        self._parent_hwnd = parent_hwnd
        self._ctrl_id = ctrl_id
        self._parent_bckgnd = parent_bckgnd or CreateSolidBrush(GetSysColor(win32con.COLOR_BTNFACE))
        self._corner_radius = corner_radius
        self._is_pressed = False
        self._is_hover = False
        self._tracking_mouse = False

        self._hwnd = self._create_window(x, y, width, height, ctrl_id, text)
        self._font = self._create_logfont(font_name, font_size, weight)
        self._create_gdi_resources()

        SetWindowLong(self._hwnd, win32con.GWL_USERDATA, id(self))
        self._original_wnd_proc = SetWindowLong(self._hwnd, win32con.GWL_WNDPROC, button_subclass_proc)

        if not enabled:
            EnableWindow(self._hwnd, False)

        self._context.controls[ctrl_id] = self

    def _create_window(self, x, y, width, height, ctrl_id, text: str = ''):
        style = (
            win32con.WS_CHILD
            | win32con.WS_VISIBLE
            | win32con.BS_PUSHBUTTON
            | win32con.WM_DRAWITEM
            # | win32con.SS_NOTIFY
        )

        return CreateWindowEx(
            dwExStyle = 0,
            lpClassName = 'BUTTON',
            lpWindowName = text,
            dwStyle = style,
            x = x, y = y,
            nWidth = width, nHeight = height,
            hWndParent = self._parent_hwnd,
            hMenu = ctrl_id,
            hInstance = self._context.h_instance,
            lpParam = id(self)
        )

    @staticmethod
    def _create_logfont(font_name, font_size, weight):
        return CreateFontIndirect(
            LOGFONT(
                height = -int(font_size * 1.333),
                weight = weight,
                quality = win32con.CLEARTYPE_QUALITY,
                face_name = font_name
            )
        )

    def _create_gdi_resources(self):
        """Create GDI resources that will be used for drawing the button."""
        self._default_brush = CreateSolidBrush(wintypes.RGB(255, 255, 255))
        self._hover_brush = CreateSolidBrush(wintypes.RGB(225, 225, 225))
        self._pressed_brush = CreateSolidBrush(wintypes.RGB(200, 200, 200))
        self._disabled_brush = CreateSolidBrush(wintypes.RGB(240, 240, 240))
        self._border_pen_hover = CreatePen(win32con.PS_SOLID, 1, wintypes.RGB(0, 0, 0))
        self._border_pen_default = CreatePen(win32con.PS_SOLID, 1, wintypes.RGB(200, 200, 200))
        self._border_pen_hover = CreatePen(win32con.PS_SOLID, 1, wintypes.RGB(100, 100, 100))
        self._border_pen_default = CreatePen(win32con.PS_SOLID, 1, wintypes.RGB(200, 200, 200))

    def redraw(self):
        """Forces the button to redraw."""
        if self._hwnd:
            InvalidateRect(self._hwnd, None, True)

    def on_draw_item(self, event: DrawItemEvent):
        hdc, rect, state = event.astuple()

        FillRect(hdc, ctypes.byref(rect), self._parent_bckgnd)

        rgn = CreateRoundRectRgn(rect.left, rect.top, rect.right, rect.bottom, self._corner_radius, self._corner_radius)
        SelectClipRgn(hdc, rgn)

        if not self.is_enabled:
            FillRect(hdc, ctypes.byref(rect), self._disabled_brush)
        elif self._is_pressed:
            vtx = (TRIVERTEX * 2)(
                TRIVERTEX(rect.left, rect.top, 210 << 8, 210 << 8, 210 << 8, 255 << 8),
                TRIVERTEX(rect.right, rect.bottom, 240 << 8, 240 << 8, 240 << 8, 255 << 8)
            )
            g_rect = GRADIENT_RECT(0, 1)
            GradientFill(hdc, vtx, 2, ctypes.byref(g_rect), 1, win32con.GRADIENT_FILL_RECT_V)
        elif self._is_hover:
            vtx = (TRIVERTEX * 2)(
                TRIVERTEX(rect.left, rect.top, 240 << 8, 240 << 8, 240 << 8, 255 << 8),
                TRIVERTEX(rect.right, rect.bottom, 210 << 8, 210 << 8, 210 << 8, 255 << 8)
            )
            g_rect = GRADIENT_RECT(0, 1)
            GradientFill(hdc, vtx, 2, ctypes.byref(g_rect), 1, win32con.GRADIENT_FILL_RECT_V)
        else:
            FillRect(hdc, ctypes.byref(rect), self._default_brush)

        SelectClipRgn(hdc, None)
        DeleteObject(rgn)

        if self._is_hover:
            old_pen = SelectObject(hdc, self._border_pen_hover)
        else:
            old_pen = SelectObject(hdc, self._border_pen_default)

        old_brush = SelectObject(hdc, GetStockObject(win32con.NULL_BRUSH))
        RoundRect(hdc, rect.left, rect.top, rect.right, rect.bottom, self._corner_radius, self._corner_radius)
        SelectObject(hdc, old_pen)
        SelectObject(hdc, old_brush)
        SelectClipRgn(hdc, None)
        DeleteObject(rgn)

        # --- Draw Text ---
        old_font = SelectObject(hdc, self._font)
        SetBkMode(hdc, win32con.TRANSPARENT)
        if self.is_enabled:
            SetTextColor(hdc, wintypes.RGB(0, 0, 0))
        else:
            SetTextColor(hdc, wintypes.RGB(150, 150, 150))

        if self._is_pressed:
            rect.top += 1
            rect.bottom += 1

        length = GetWindowTextLength(self._hwnd)
        if length > 0:
            buffer = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(self._hwnd, buffer, length + 1)
            DrawText(hdc, buffer.value, -1, ctypes.byref(rect), win32con.DT_CENTER | win32con.DT_VCENTER | win32con.DT_SINGLELINE)

        SelectObject(hdc, old_font)

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        """Instance-level window procedure to handle messages for this specific button."""
        if msg == win32con.WM_MOUSEMOVE:
            if not self._tracking_mouse:
                TrackMouseEvent(
                    ctypes.byref(
                        TRACKMOUSEEVENT(
                            dwFlags = win32con.TME_LEAVE,
                            hwndTrack = self._hwnd,
                            dwHoverTime = 0
                        )
                    )
                )
                self._tracking_mouse = True
                self._is_hover = True
                self.redraw()
            return 0

        elif msg == win32con.WM_MOUSELEAVE:
            self._tracking_mouse = False
            self._is_hover = False
            self._is_pressed = False
            self.redraw()
            return 0

        elif msg == win32con.WM_LBUTTONDBLCLK:
            self._is_pressed = True
            self.redraw()
            return 0

        elif msg == win32con.WM_LBUTTONDOWN:
            self._is_pressed = True
            self.redraw()
            return 0

        elif msg == win32con.WM_LBUTTONUP:
            if self._is_pressed:
                self._is_pressed = False
                self.redraw()
                # Notify the parent window that a click occurred
                SendMessage(self._parent_hwnd, win32con.WM_COMMAND, self._ctrl_id, self._hwnd)
            return 0

        elif msg == win32con.WM_DESTROY:
            SetWindowLong(hwnd, win32con.GWL_WNDPROC, self._original_wnd_proc)
            SetWindowLong(hwnd, win32con.GWL_USERDATA, 0)
            return 0

        # For all other messages, call the original default procedure
        return CallWindowProc(self._original_wnd_proc, hwnd, msg, wparam, lparam)

    def destroy(self):
        if self._hwnd:
            DestroyWindow(self._hwnd)
            self._hwnd = None

        DeleteObject(self._font)
        DeleteObject(self._default_brush)
        DeleteObject(self._hover_brush)
        DeleteObject(self._pressed_brush)
        DeleteObject(self._disabled_brush)
        DeleteObject(self._border_pen_hover)
        DeleteObject(self._border_pen_default)


@WNDPROC
def button_subclass_proc(hwnd, msg, wparam, lparam):
    instance_id = GetWindowLong(hwnd, win32con.GWL_USERDATA)
    if instance_id:
        instance = ctypes.cast(instance_id, ctypes.py_object).value
        return instance.wnd_proc(hwnd, msg, wparam, lparam)
    else:
        return DefWindowProc(hwnd, msg, wparam, lparam)
