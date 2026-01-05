import ctypes
from ctypes import wintypes

import win32con

from skeletal_framework.win32_bindings.gdi32 import (
    # Structures
    LOGFONT,

    # Functions
    CreateFontIndirect, CreatePen, CreateSolidBrush,
    DeleteObject,
    ExtTextOut,
    GetTextExtentPoint32,
    RoundRect,
    SelectObject, SetBkMode, SetTextColor
)
from skeletal_framework.win32_bindings.user32 import FillRect, GetDC, GetSysColor, ReleaseDC


class GroupBox:
    """
    A class to draw a group box with rounded corners and a label across the top line.
    """

    @property
    def hwnd(self) -> int: return self._parent_hwnd

    def __init__(
        self,
        parent_hwnd: int,
        x: int, y: int, width: int, height: int,
        *,
        title: str = "",
        corner_radius: int = 10,
        line_color = None,
        title_padding: int = 10,
        font_name = "Segoe UI", font_size: int = 9
    ):
        self._parent_hwnd = parent_hwnd
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.corner_radius = corner_radius
        self.line_color = line_color or wintypes.RGB(180, 180, 180)  # Light gray default
        self.title_padding = title_padding
        self._font = self._create_log_font(font_name, font_size)

    @staticmethod
    def _create_log_font(font_name: str, font_size: int) -> LOGFONT:
        """Helper method to create a LOGFONT structure."""
        return LOGFONT(
            height = -int(font_size * 1.333),
            charset = win32con.DEFAULT_CHARSET,
            out_precision = win32con.OUT_DEFAULT_PRECIS,
            clip_precision = win32con.CLIP_DEFAULT_PRECIS,
            quality = win32con.DEFAULT_QUALITY,
            pitch_and_family = win32con.DEFAULT_PITCH | win32con.FF_DONTCARE,
            face_name = font_name,
        )

    def draw(self, hdc: int):
        release_dc = False
        if hdc is None:
            hdc = GetDC(self._parent_hwnd)
            release_dc = True

        pen = CreatePen(win32con.PS_SOLID, 1, self.line_color)
        old_pen = SelectObject(hdc, pen)

        old_bk_mode = SetBkMode(hdc, win32con.TRANSPARENT)

        hfont = CreateFontIndirect(ctypes.byref(self._font))
        old_font = SelectObject(hdc, hfont)

        try:
            title_size = wintypes.SIZE()
            GetTextExtentPoint32(hdc, self.title, len(self.title), ctypes.byref(title_size))

            self._draw_rounded_rect_with_title_gap(hdc, title_size)

            if self.title:
                SetTextColor(hdc, wintypes.RGB(100, 100, 100))
                ExtTextOut(
                    hdc,
                    self.x + self.corner_radius + self.title_padding,
                    self.y - title_size.cy // 2 - 2,
                    0,
                    None,
                    self.title,
                    len(self.title),
                    None
                )

        finally:
            SelectObject(hdc, old_font)
            DeleteObject(hfont)
            SetBkMode(hdc, old_bk_mode)
            SelectObject(hdc, old_pen)
            DeleteObject(pen)

            if release_dc:
                ReleaseDC(self._parent_hwnd, hdc)

    def _draw_rounded_rect_with_title_gap(self, hdc, title_size: wintypes.SIZE):
        """Draw a rounded rectangle with a gap for the title text."""
        if self.title:
            # Calculate the gap for the title using title_padding
            gap_start = self.x + self.title_padding - 10
            gap_width = gap_start + 10 + title_size.cx + 20

            bg_color = GetSysColor(win32con.COLOR_BTNFACE)
            bg_brush = CreateSolidBrush(bg_color)
            old_brush = SelectObject(hdc, bg_brush)

            try:
                # Draw the main rounded rectangle
                RoundRect(
                    hdc, self.x, self.y, self.x + self.width, self.y + self.height,
                    self.corner_radius, self.corner_radius
                )

                # "Erase" the part of the top border where the title will go
                fill_rect = wintypes.RECT(
                    gap_start, self.y - 1,
                    gap_width, self.y + 1
                )
                FillRect(hdc, fill_rect, bg_brush)

            finally:
                SelectObject(hdc, old_brush)
                DeleteObject(bg_brush)

        else:
            RoundRect(
                hdc, self.x, self.y, self.x + self.width, self.y + self.height,
                self.corner_radius, self.corner_radius
            )

    def destroy(self):
        pass
