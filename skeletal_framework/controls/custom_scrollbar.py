from ctypes import wintypes
import win32con

from skeletal_framework.win32_bindings.gdi32 import (
    CreateSolidBrush, DeleteObject, SelectObject, GetStockObject, RoundRect, Polygon
)
from skeletal_framework.win32_bindings.user32 import (
    CreateWindowEx, DefWindowProc, RegisterClass, WNDCLASS,
    LoadCursor, BeginPaint, EndPaint, InvalidateRect, GetClientRect,
    PostMessage, TrackMouseEvent, TRACKMOUSEEVENT, PtInRect,
    SetCapture, ReleaseCapture, FillRect,
    SetTimer, KillTimer, ScreenToClient
)
from skeletal_framework.win32_bindings.kernel32 import GetModuleHandle
from skeletal_framework.dispatcher import Dispatcher
from skeletal_framework.win32_bindings.macros import hiword, loword, MAKEWPARAM


class CustomScrollBar:
    _CLASS_NAME = "CustomScrollBarClass"
    _ATOM = None

    _TIMER_ID = 1
    _INITIAL_DELAY_MS = 400
    _REPEAT_DELAY_MS = 60

    _NULL_PEN = 8

    def __init__(
            self,
            parent_hwnd: int,
            x: int, y: int, width: int, height: int,
            *,
            bg_color: int = wintypes.RGB(25, 25, 25),
            thumb_color: int = wintypes.RGB(80, 80, 80),
            thumb_hover_color: int = wintypes.RGB(100, 100, 100),
            thumb_press_color: int = wintypes.RGB(120, 120, 120),
            button_color: int = wintypes.RGB(75, 75, 75),
            arrow_color: int = wintypes.RGB(25, 25, 25)
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
        self.button_color = button_color
        self.arrow_color = arrow_color

        self._h_instance = GetModuleHandle(None)
        self._register_class()

        self._scroll_pos = 0
        self._page_size = 1.0
        self._is_hovering = False
        self._is_dragging = False
        self._drag_start_y = 0
        self._drag_start_pos = 0.0

        self._auto_scroll_action = None
        self._timer_active = False

        self._btn_size = width

        self._bg_brush = CreateSolidBrush(self.bg_color)
        self._thumb_brush = CreateSolidBrush(self.thumb_color)
        self._thumb_hover_brush = CreateSolidBrush(self.thumb_hover_color)
        self._thumb_press_brush = CreateSolidBrush(self.thumb_press_color)
        self._button_brush = CreateSolidBrush(self.button_color)
        self._arrow_brush = CreateSolidBrush(self.arrow_color)

        self._hwnd = self._create_window()

    def _register_class(self):
        if CustomScrollBar._ATOM is None:
            wnd_class = WNDCLASS(
                style = win32con.CS_HREDRAW | win32con.CS_VREDRAW,
                lpfnWndProc = Dispatcher,
                hInstance = self._h_instance,
                hCursor = LoadCursor(0, win32con.IDC_ARROW),
                lpszClassName = self._CLASS_NAME,
                hbrBackground = None
            )
            CustomScrollBar._ATOM = RegisterClass(wnd_class)

    def _create_window(self):
        return CreateWindowEx(
            dwExStyle = 0,
            lpClassName = self._CLASS_NAME,
            lpWindowName = "",
            dwStyle = win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.WS_CLIPSIBLINGS,
            x = self.x, y = self.y,
            nWidth = self.width, nHeight = self.height,
            hWndParent = self._parent_hwnd,
            hMenu = None,
            hInstance = self._h_instance,
            lpParam = id(self)
        )

    @property
    def hwnd(self):
        return self._hwnd

    def set_scroll_params(self, pos: float, page_size: float):
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

        elif msg == win32con.WM_TIMER:
            self._on_timer(hwnd, wparam)
            return 0

        elif msg == win32con.WM_MOUSELEAVE:
            self._is_hovering = False
            InvalidateRect(hwnd, None, False)
            return 0

        elif msg == win32con.WM_NCDESTROY:
            self._cleanup()
            return 0

        return DefWindowProc(hwnd, msg, wparam, lparam)

    def _get_layout(self, client_rect):
        w = client_rect.right - client_rect.left
        h = client_rect.bottom - client_rect.top

        # Standard size based on width
        std_size = self._btn_size

        # Shrink the physical button height by 2 pixels to create the gap
        btn_h = std_size - 2

        if h < 2 * std_size:
            return None, None, None

        # Top button: 0 to btn_h
        top_btn = wintypes.RECT(0, 0, w, btn_h)

        # Bottom button: h - btn_h to h
        bot_btn = wintypes.RECT(0, h - btn_h, w, h)

        # Track: Starts at std_size, Ends at h - std_size
        # The track preserves the gap area (showing background color)
        track_top = std_size
        track_bottom = h - std_size
        track_rect = wintypes.RECT(0, track_top, w, track_bottom)

        return top_btn, bot_btn, track_rect

    def _calculate_thumb_rect(self, track_rect):
        if not track_rect: return wintypes.RECT(0, 0, 0, 0), 0
        track_h = track_rect.bottom - track_rect.top
        if track_h <= 0: return wintypes.RECT(0, 0, 0, 0), 0

        min_thumb_height = 20
        thumb_height = max(min_thumb_height, int(track_h * self._page_size))
        thumb_height = min(thumb_height, track_h)

        travel_range = track_h - thumb_height

        if travel_range <= 0:
            thumb_y = track_rect.top
            travel_range = 0

        else:
            thumb_y = track_rect.top + int(travel_range * self._scroll_pos)

        return wintypes.RECT(
            track_rect.left, thumb_y,
            track_rect.right, thumb_y + thumb_height
        ), travel_range

    def _draw_arrow(self, hdc, rect, direction = 'up'):
        """Draws a simple triangle arrow in the center of rect."""
        cx = (rect.left + rect.right) // 2
        cy = (rect.top + rect.bottom) // 2

        # Arrow radius
        r = 5

        if direction == 'up':
            points = [
                wintypes.POINT(cx, cy - r),  # Top
                wintypes.POINT(cx - r, cy + r),  # Bottom Left
                wintypes.POINT(cx + r, cy + r)  # Bottom Right
            ]

        else:
            points = [
                wintypes.POINT(cx - r, cy - r),  # Top Left
                wintypes.POINT(cx + r, cy - r),  # Top Right
                wintypes.POINT(cx, cy + r)  # Bottom
            ]

        old_brush = SelectObject(hdc, self._arrow_brush)
        # NULL_PEN ensures no outline
        null_pen = GetStockObject(self._NULL_PEN)
        old_pen = SelectObject(hdc, null_pen)

        Polygon(hdc, points)

        SelectObject(hdc, old_pen)
        SelectObject(hdc, old_brush)

    def _on_paint(self, hwnd):
        ps, hdc = BeginPaint(hwnd)
        try:
            client_rect = wintypes.RECT()
            GetClientRect(hwnd, client_rect)
            FillRect(hdc, client_rect, self._bg_brush)

            top_btn, bot_btn, track_rect = self._get_layout(client_rect)

            if top_btn:
                # 1. Draw Buttons
                FillRect(hdc, top_btn, self._button_brush)
                FillRect(hdc, bot_btn, self._button_brush)

                # 2. Draw Arrows
                self._draw_arrow(hdc, top_btn, 'up')
                self._draw_arrow(hdc, bot_btn, 'down')

                # 3. Draw Thumb
                if self._page_size < 1.0:
                    thumb_rect, _ = self._calculate_thumb_rect(track_rect)

                    brush = self._thumb_brush
                    if self._is_dragging:
                        brush = self._thumb_press_brush

                    elif self._is_hovering:
                        brush = self._thumb_hover_brush

                    # Rounded Thumb Logic with Nudge
                    rect_width = thumb_rect.right - thumb_rect.left
                    desired_width = 8
                    if desired_width > rect_width: desired_width = rect_width

                    margin = (rect_width - desired_width) // 2
                    thumb_offset_x = 1

                    visual_left = thumb_rect.left + margin + thumb_offset_x
                    visual_right = visual_left + desired_width
                    visual_top = thumb_rect.top
                    visual_bottom = thumb_rect.bottom

                    if visual_right > thumb_rect.right:
                        diff = visual_right - thumb_rect.right
                        visual_right -= diff
                        visual_left -= diff

                    null_pen = GetStockObject(self._NULL_PEN)
                    old_pen = SelectObject(hdc, null_pen)
                    old_brush = SelectObject(hdc, brush)

                    RoundRect(hdc, visual_left, visual_top, visual_right, visual_bottom, desired_width, desired_width)

                    SelectObject(hdc, old_brush)
                    SelectObject(hdc, old_pen)

        finally:
            EndPaint(hwnd, ps)

    def _on_mouse_move(self, hwnd, lparam):
        if not self._is_hovering:
            self._is_hovering = True
            tme = TRACKMOUSEEVENT(dwFlags = win32con.TME_LEAVE, hwndTrack = hwnd, dwHoverTime = 0)
            TrackMouseEvent(tme)
            InvalidateRect(hwnd, None, False)

        if self._is_dragging:
            y = hiword(lparam)
            if y > 32767: y -= 65536

            client_rect = wintypes.RECT()
            GetClientRect(hwnd, client_rect)
            _, _, track_rect = self._get_layout(client_rect)

            if track_rect:
                _, travel_range = self._calculate_thumb_rect(track_rect)
                if travel_range > 0:
                    delta_y = y - self._drag_start_y
                    delta_pos = delta_y / travel_range
                    new_pos = self._drag_start_pos + delta_pos
                    self._scroll_pos = max(0.0, min(1.0, new_pos))
                    self._notify_parent(win32con.SB_THUMBTRACK)
                    InvalidateRect(hwnd, None, False)

    def _on_left_button_down(self, hwnd, lparam):
        x = loword(lparam)
        y = hiword(lparam)
        if y > 32767: y -= 65536
        pt = wintypes.POINT(x, y)

        client_rect = wintypes.RECT()
        GetClientRect(hwnd, client_rect)
        top_btn, bot_btn, track_rect = self._get_layout(client_rect)
        if not top_btn: return

        action = None
        if PtInRect(top_btn, pt):
            action = win32con.SB_LINEUP

        elif PtInRect(bot_btn, pt):
            action = win32con.SB_LINEDOWN

        elif PtInRect(track_rect, pt):
            thumb_rect, _ = self._calculate_thumb_rect(track_rect)
            if PtInRect(thumb_rect, pt):
                self._is_dragging = True
                self._drag_start_y = y
                self._drag_start_pos = self._scroll_pos
                SetCapture(hwnd)
                InvalidateRect(hwnd, None, False)
                return

            elif y < thumb_rect.top:
                action = win32con.SB_PAGEUP

            elif y > thumb_rect.bottom:
                action = win32con.SB_PAGEDOWN

        if action is not None:
            self._auto_scroll_action = action
            self._notify_parent(action)
            SetTimer(hwnd, self._TIMER_ID, self._INITIAL_DELAY_MS, None)
            self._timer_active = True
            SetCapture(hwnd)

    def _on_left_button_up(self, hwnd):
        if self._is_dragging:
            self._is_dragging = False
            ReleaseCapture()
            InvalidateRect(hwnd, None, False)

        if self._timer_active:
            KillTimer(hwnd, self._TIMER_ID)
            self._timer_active = False
            self._auto_scroll_action = None
            ReleaseCapture()

    def _on_timer(self, hwnd, timer_id):
        if timer_id == self._TIMER_ID and self._auto_scroll_action is not None:
            KillTimer(hwnd, self._TIMER_ID)
            SetTimer(hwnd, self._TIMER_ID, self._REPEAT_DELAY_MS, None)

            pt = wintypes.POINT()
            ScreenToClient(hwnd, pt)

            rect = wintypes.RECT()
            GetClientRect(hwnd, rect)
            top_btn, bot_btn, track_rect = self._get_layout(rect)

            should_scroll = False
            if self._auto_scroll_action == win32con.SB_LINEUP:
                should_scroll = PtInRect(top_btn, pt)

            elif self._auto_scroll_action == win32con.SB_LINEDOWN:
                should_scroll = PtInRect(bot_btn, pt)

            elif self._auto_scroll_action in (win32con.SB_PAGEUP, win32con.SB_PAGEDOWN):
                thumb_rect, _ = self._calculate_thumb_rect(track_rect)
                if PtInRect(thumb_rect, pt):
                    should_scroll = False

                elif self._auto_scroll_action == win32con.SB_PAGEUP and pt.y < thumb_rect.top:
                    should_scroll = True

                elif self._auto_scroll_action == win32con.SB_PAGEDOWN and pt.y > thumb_rect.bottom:
                    should_scroll = True

            if should_scroll:
                self._notify_parent(self._auto_scroll_action)

    def _notify_parent(self, code):
        if code == win32con.SB_THUMBTRACK:
            pos_int = int(self._scroll_pos * 65535)
            wparam = MAKEWPARAM(code, pos_int)

        else:
            wparam = MAKEWPARAM(code, 0)

        PostMessage(self._parent_hwnd, win32con.WM_VSCROLL, wparam, self._hwnd)

    def _cleanup(self):
        if self._timer_active:
            KillTimer(self._hwnd, self._TIMER_ID)

        DeleteObject(self._bg_brush)
        DeleteObject(self._thumb_brush)
        DeleteObject(self._thumb_hover_brush)
        DeleteObject(self._thumb_press_brush)
        DeleteObject(self._button_brush)
        DeleteObject(self._arrow_brush)
