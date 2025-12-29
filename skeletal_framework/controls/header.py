import ctypes
from ctypes import wintypes

from pathlib import Path
from typing import Optional

import win32con
from PIL import Image, ImageWin

from core.core_context import CoreContext
from ui.dispatcher import dispatcher
from win32_bindings import *
from win32_bindings.macros import adjust_rgb

# Dictionary to store instances by window handle
_image_panel_instances = {}


class Header:
    """A panel control class for displaying images in a PyWin32 window.

    This panel automatically resizes the displayed image to fit the size of the panel.
    Designed to be used as a child window within a main application window.
    """
    _class_registered = False
    _class_name = "TitlePanelClass"

    def __init__(self, text: str, image_path: Path, flip_left: bool = False, flip_right: bool = False):
        self._core_context: CoreContext = CoreContext()

        self._flip_left = flip_left
        self._flip_right = flip_right

        # Register the window class if not already registered
        self._register_window_class(h_instance = self._core_context.h_instance)

        rect = wintypes.RECT()
        GetClientRect(self._core_context.main_window, ctypes.byref(rect))
        width = rect.right - rect.left

        # Create the window
        self.hwnd = CreateWindowEx(
            dwExStyle = 0,
            lpClassName = self._class_name,
            lpWindowName = "Title Panel",
            dwStyle = win32con.WS_CHILD,
            x = 0, y = 0, nWidth = width, nHeight = 66,
            hWndParent = self._core_context.main_window,
            hMenu = None,
            hInstance = self._core_context.h_instance,
            lpParam = id(self)
        )

        paste_position = (0, 0)
        self._image: Optional[Image.Image] = Image.open(image_path)
        if self._image.size != (60, 60):
            if self._image.width == self._image.height:
                width, height = (60, 60)
            elif self._image.width > self._image.height:
                width, height = (60, int(self._image.height * 60 / self._image.width))
                paste_position = (0, (60 - height) // 2)
            else:
                width, height = (int(self._image.width * 60 / self._image.height), 60)
                paste_position = ((60 - width) // 2, 0)

            self._image = self._image.resize((width, height), Image.Resampling.LANCZOS)

        self._display_image = Image.new("RGB", (60, 60), (255, 255, 255))
        self._display_image.paste(im = self._image, box = paste_position, mask = self._image.split()[3])

        self._text = text

        _image_panel_instances[self.hwnd] = self

        # Create background brush
        self.background_brush = CreateSolidBrush(wintypes.RGB(255, 255, 255))

        UpdateWindow(self.hwnd)
        ShowWindow(self.hwnd, win32con.SW_SHOW)

    @classmethod
    def _register_window_class(cls, h_instance) -> None:
        """Register the window class for the image panel."""

        if cls._class_registered:
            return

        RegisterClassEx(
            ctypes.byref(
                WNDCLASSEX(
                    style = win32con.CS_HREDRAW | win32con.CS_VREDRAW,
                    lpfnWndProc = dispatcher,
                    hInstance = h_instance,
                    hCursor = LoadCursor(0, win32con.IDC_ARROW),
                    hbrBackground = GetSysColorBrush(win32con.BLACK_BRUSH),
                    lpszClassName = cls._class_name
                )
            )
        )
        cls._class_registered = True

    @staticmethod
    def wnd_proc(hwnd, msg, wparam, lparam):
        """Window procedure for handling window messages."""
        # Get the instance associated with this window
        instance: Header = _image_panel_instances.get(hwnd)

        if msg == win32con.WM_PAINT:
            ps, hdc = BeginPaint(hwnd)

            if instance:
                # Call the instance's paint method
                # noinspection PyProtectedMember

                instance._draw_sunken_area(hdc, 0, 0, instance._core_context.width, 66)
                instance._draw_left_image(hdc, 3, 3, instance._flip_left)
                instance._draw_right_image(hdc, instance._core_context.width - 63, 3, instance._flip_right)
                instance._draw_text(hdc, ps.rcPaint)

            EndPaint(hwnd, ps)
            return 0

        elif msg == win32con.WM_DESTROY:
            # Clean up when the window is destroyed
            if instance:
                instance._display_image.close()
                instance._display_image = None

                instance._image.close()
                instance._image = None

                # Remove from dictionary
                if hwnd in _image_panel_instances:
                    del _image_panel_instances[hwnd]
            return 0

        return DefWindowProc(hwnd, msg, wparam, lparam)

    @staticmethod
    def _draw_sunken_area(hdc, x, y, width, height):
        def create_pen(base_color_rgb: tuple[int, int, int], scale_factor: float) -> wintypes.HPEN:
            r, g, b = base_color_rgb

            new_r, new_g, new_b = adjust_rgb(r, g, b, scale_factor)

            return CreatePen(win32con.PS_SOLID, 1, wintypes.RGB(new_r, new_g, new_b))

        sunken_area_rect = wintypes.RECT(x + 2, y + 2, x + width - 2, y + height - 2)
        white_brush = CreateSolidBrush(wintypes.RGB(255, 255, 255))

        FillRect(hdc, ctypes.byref(sunken_area_rect), white_brush)
        DeleteObject(white_brush)

        # Use the new helper to create 1-pixel-wide pens
        base_color = (240, 240, 240)
        dark_pen = create_pen(base_color, scale_factor = 0.70)
        darker_pen = create_pen(base_color, scale_factor = 0.50)
        light_pen = create_pen(base_color, scale_factor = 1.026)
        lighter_pen = create_pen(base_color, scale_factor = 1.041)

        # --- Outer Border ---
        old_pen = SelectObject(hdc, dark_pen)

        # Top edge
        MoveToEx(hdc, x, y, None)
        LineTo(hdc, x + width - 1, y)

        # Left edge
        MoveToEx(hdc, x, y, None)
        LineTo(hdc, x, y + height - 1)

        SelectObject(hdc, light_pen)

        # Bottom edge
        MoveToEx(hdc, x, y + height - 1, None)
        LineTo(hdc, x + width - 1, y + height - 1)

        # Right edge
        MoveToEx(hdc, x + width - 1, y, None)
        LineTo(hdc, x + width - 1, y + height)

        # --- Inner Border ---
        SelectObject(hdc, darker_pen)

        # Inner top edge
        MoveToEx(hdc, x + 1, y + 1, None)
        LineTo(hdc, x + width - 2, y + 1)

        # Inner left edge
        MoveToEx(hdc, x + 1, y + 1, None)
        LineTo(hdc, x + 1, y + height - 2)

        SelectObject(hdc, lighter_pen)

        # Inner bottom edge
        MoveToEx(hdc, x + 1, y + height - 2, None)
        LineTo(hdc, x + width - 2, y + height - 2)

        # Inner right edge
        MoveToEx(hdc, x + width - 2, y + 1, None)
        LineTo(hdc, x + width - 2, y + height - 2)

        SelectObject(hdc, old_pen)

        # Cleanup
        DeleteObject(dark_pen)
        DeleteObject(darker_pen)
        DeleteObject(lighter_pen)
        DeleteObject(light_pen)

    def _draw_left_image(self, hdc, x, y, flip) -> None:
        self._draw_image(hdc, x, y, flip)

    def _draw_right_image(self, hdc, x, y, flip) -> None:
        self._draw_image(hdc, x, y, flip)

    def _draw_image(self, hdc, x, y, flip) -> None:
        if self._display_image:
            try:
                image = self._display_image

                img_width, img_height = image.size

                if flip:
                    image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

                dib = ImageWin.Dib(image)
                dib.draw(hdc, (x, y, x + img_width, y + img_height))

            except Exception as e:
                print(f"Error drawing image: {e}")

    def _draw_text(self, hdc, rect: wintypes.RECT) -> None:
        text_rect = wintypes.RECT(
            rect.left + 63,
            rect.top,
            rect.right - 63,
            rect.bottom
        )

        font = LOGFONT(
            height = -24,
            weight = win32con.FW_NORMAL,
            face_name = 'Microsoft Sans Serif',
            charset = win32con.DEFAULT_CHARSET,  # Important for character encoding
            quality = win32con.CLEARTYPE_QUALITY  # Better text rendering
        )
        h_font = CreateFontIndirect(font)
        old_font = SelectObject(hdc, h_font)

        SetBkMode(hdc, win32con.TRANSPARENT)
        SetTextColor(hdc, wintypes.RGB(0, 0, 0))

        DrawText(
            hdc,
            self._text,
            -1,
            ctypes.byref(text_rect),
            win32con.DT_VCENTER | win32con.DT_CENTER | win32con.DT_SINGLELINE  # Added SINGLELINE
        )

        SelectObject(hdc, old_font)
        DeleteObject(h_font)

    def destroy(self) -> None:
        """Destroy the panel window."""
        if self.hwnd:
            DeleteObject(self.background_brush)
            DestroyWindow(self.hwnd)
            self.hwnd = None
