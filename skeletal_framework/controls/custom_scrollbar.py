import ctypes
from ctypes import wintypes
import win32con

from skeletal_framework.win32_bindings.gdi32 import (
    CreateSolidBrush, DeleteObject, SelectObject
)
from skeletal_framework.win32_bindings.user32 import (
    CreateWindowEx, DefWindowProc, DestroyWindow, RegisterClass, WNDCLASS,
    LoadCursor, BeginPaint, EndPaint, InvalidateRect, GetClientRect,
    SetWindowPos, PostMessage, GetWindowLong, SetWindowLong, CallWindowProc,
    TrackMouseEvent, TRACKMOUSEEVENT, PtInRect, SetCapture, ReleaseCapture, FillRect
)
from skeletal_framework.win32_bindings.kernel32 import GetModuleHandle
from skeletal_framework.dispatcher import Dispatcher
from skeletal_framework.win32_bindings.macros import hiword, loword, MAKEWPARAM


class CustomScrollBar:
    _CLASS_NAME = "CustomScrollBarClass"
    _ATOM = None

    def __init__(
        self,
        parent_hwnd: int,
        x: int, y: int, width: int, height: int,
        *,
        bg_color: int = wintypes.RGB(50, 50, 50),
        thumb_color: int = wintypes.RGB(80, 80, 80),
        thumb_hover_color: int = wintypes.RGB(100, 100, 100),
        thumb_press_color: int = wintypes.RGB(120, 120, 120),
    ):
        self._parent_hwnd = parent_hwnd
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.bg_color = bg_color
        self.thumb_color = thumb_color
        self.thumb_hover_color = thumb_hover_color
        self.thumb_press_color = thumb_press_color

        self._h_instance = GetModuleHandle(None)
        self._register_class()

        # State
        self._scroll_pos = 0  # 0.0 to 1.0
        self._page_size = 1.0  # Start with full page size (no scroll)
        self._is_hovering = False
        self._is_dragging = False
        self._drag_start_y = 0
        self._drag_start_pos = 0.0

        # GDI Objects
        self._bg_brush = CreateSolidBrush(self.bg_color)
        self._thumb_brush = CreateSolidBrush(self.thumb_color)
        self._thumb_hover_brush = CreateSolidBrush(self.thumb_hover_color)
        self._thumb_press_brush = CreateSolidBrush(self.thumb_press_color)

        self._hwnd = self._create_window()

    def _register_class(self):
        if CustomScrollBar._ATOM is None:
            wnd_class = WNDCLASS(
                style=win32con.CS_HREDRAW | win32con.CS_VREDRAW,
                lpfnWndProc=Dispatcher,
                hInstance=self._h_instance,
                hCursor=LoadCursor(0, win32con.IDC_ARROW),
                lpszClassName=self._CLASS_NAME,
                hbrBackground=None  # We paint background ourselves
            )
            CustomScrollBar._ATOM = RegisterClass(wnd_class)

    def _create_window(self):
        return CreateWindowEx(
            dwExStyle=0,
            lpClassName=self._CLASS_NAME,
            lpWindowName="",
            dwStyle=win32con.WS_CHILD | win32con.WS_VISIBLE,
            x=self.x, y=self.y,
            nWidth=self.width, nHeight=self.height,
            hWndParent=self._parent_hwnd,
            hMenu=None,
            hInstance=self._h_instance,
            lpParam=id(self)
        )

    @property
    def hwnd(self):
        return self._hwnd

    def set_scroll_params(self, pos: float, page_size: float):
        """
        Updates the scrollbar state.
        pos: 0.0 to 1.0 (top to bottom)
        page_size: 0.0 to 1.0 (fraction of content visible)
        """
        self._scroll_pos = max(0.0, min(1.0, pos))
        self._page_size = max(0.0, min(1.0, page_size))
        InvalidateRect(self._hwnd, None, False)

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_PAINT:
            self._on_paint(hwnd)
            return 0

        elif msg == win32con.WM_MOUSEMOVE:
            self._on_mouse_move(hwnd, lparam)
            return 0

        elif msg == win32con.WM_LBUTTONDOWN:
            self._on_left_button_down(hwnd, lparam)
            return 0

        elif msg == win32con.WM_LBUTTONUP:
            self._on_left_button_up(hwnd)
            return 0

        elif msg == win32con.WM_MOUSELEAVE:
            self._is_hovering = False
            InvalidateRect(hwnd, None, False)
            return 0

        elif msg == win32con.WM_NCDESTROY:
            self._cleanup()
            return 0

        return DefWindowProc(hwnd, msg, wparam, lparam)

    def _on_paint(self, hwnd):
        ps, hdc = BeginPaint(hwnd)
        try:
            # Get tuple: (left, top, right, bottom, width, height)
            client_tuple = GetClientRect(hwnd)
            if not client_tuple: return
            
            # Reconstruct RECT for FillRect
            rc_width = client_tuple[4]
            rc_height = client_tuple[5]
            rect = wintypes.RECT(0, 0, rc_width, rc_height)

            # Draw Track
            FillRect(hdc, rect, self._bg_brush)

            # Only draw thumb if needed
            if self._page_size < 1.0:
                # Calculate Thumb Rect
                thumb_rect = self._calculate_thumb_rect(rect)

                # Draw Thumb
                brush = self._thumb_brush
                if self._is_dragging:
                    brush = self._thumb_press_brush
                elif self._is_hovering:
                    brush = self._thumb_hover_brush

                FillRect(hdc, thumb_rect, brush)

        finally:
            EndPaint(hwnd, ps)

    def _calculate_thumb_rect(self, client_rect):
        height = client_rect.bottom - client_rect.top
        width = client_rect.right - client_rect.left

        min_thumb_height = 20
        thumb_height = max(min_thumb_height, int(height * self._page_size))
        travel_range = height - thumb_height
        thumb_y = int(travel_range * self._scroll_pos)

        return wintypes.RECT(
            0, thumb_y,
            width, thumb_y + thumb_height
        )

    def _on_mouse_move(self, hwnd, lparam):
        if not self._is_hovering:
            self._is_hovering = True
            tme = TRACKMOUSEEVENT(dwFlags=win32con.TME_LEAVE, hwndTrack=hwnd, dwHoverTime=0)
            TrackMouseEvent(tme)
            InvalidateRect(hwnd, None, False)

        if self._is_dragging:
            y = hiword(lparam)
            if y > 32767: y -= 65536
            
            delta_y = y - self._drag_start_y
            
            client_tuple = GetClientRect(hwnd)
            if not client_tuple: return
            height = client_tuple[5]

            min_thumb_height = 20
            thumb_height = max(min_thumb_height, int(height * self._page_size))
            travel_range = height - thumb_height
            
            if travel_range > 0:
                delta_pos = delta_y / travel_range
                new_pos = self._drag_start_pos + delta_pos
                self._scroll_pos = max(0.0, min(1.0, new_pos))
                
                self._notify_parent()
                InvalidateRect(hwnd, None, False)

    def _on_left_button_down(self, hwnd, lparam):
        x = loword(lparam)
        y = hiword(lparam)
        
        client_tuple = GetClientRect(hwnd)
        if not client_tuple: return
        
        rc_width = client_tuple[4]
        rc_height = client_tuple[5]
        rect = wintypes.RECT(0, 0, rc_width, rc_height)

        thumb_rect = self._calculate_thumb_rect(rect)
        
        pt = wintypes.POINT(x, y)
        
        if PtInRect(thumb_rect, pt):
            self._is_dragging = True
            self._drag_start_y = y
            self._drag_start_pos = self._scroll_pos
            SetCapture(hwnd)
            InvalidateRect(hwnd, None, False)

    def _on_left_button_up(self, hwnd):
        if self._is_dragging:
            self._is_dragging = False
            ReleaseCapture()
            InvalidateRect(hwnd, None, False)

    def _notify_parent(self):
        pos_int = int(self._scroll_pos * 65535)
        wparam = MAKEWPARAM(win32con.SB_THUMBTRACK, pos_int)
        PostMessage(self._parent_hwnd, win32con.WM_VSCROLL, wparam, self._hwnd)

    def _cleanup(self):
        DeleteObject(self._bg_brush)
        DeleteObject(self._thumb_brush)
        DeleteObject(self._thumb_hover_brush)
        DeleteObject(self._thumb_press_brush)
