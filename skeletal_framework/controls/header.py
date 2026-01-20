from functools import cached_property
from ctypes import wintypes

import win32con
from PIL import Image as PilImage, ImageWin
from PIL.Image import Image

from skeletal_framework.core_context import CoreContext
from skeletal_framework.dispatcher import Dispatcher
from skeletal_framework.win32_bindings.gdi32 import CreateSolidBrush, CreatePen, DeleteObject, SelectObject, MoveToEx, LineTo, SetBkMode, SetTextColor, LOGFONT, CreateFontIndirect
from skeletal_framework.win32_bindings.user32 import GetClientRect, CreateWindowEx, ShowWindow, UpdateWindow, RegisterClassEx, WNDCLASSEX, LoadCursor, BeginPaint, EndPaint, FillRect, DestroyWindow, GetSysColorBrush, DefWindowProc, DrawText
from skeletal_framework.win32_bindings.macros import adjust_rgb, get_rgb

_image_panels = {}


class Header:
    _class_registered = False
    _class_name = "TitlePanelClass"

    @cached_property
    def _width(self) -> int:
        rect = wintypes.RECT()
        GetClientRect(self._core_context.main_window, rect)

        return rect.right - rect.left

    def __init__(
            self, text: str,
            *,
            side_image: Image,
            center_image: Image | None = None,
            edge_length: int = 60,
            text_color: int = wintypes.RGB(0, 0, 0),
            bg_color: int = wintypes.RGB(255, 255, 255),
            scale_factors: tuple[float, float, float, float] = (0.60, 0.40, 1.076, 1.091),
            flip_left_image: bool = False,
            flip_right_image: bool = False,
    ):
        self._core_context: CoreContext = CoreContext()

        self._edge_length = edge_length
        self._text_color = text_color
        self._bg_color = bg_color
        self._scale_factors = scale_factors
        self._flip_left_image = flip_left_image
        self._flip_right_image = flip_right_image
        self._text = text
        self._side_image = side_image

        self._register_window_class(h_instance = self._core_context.h_instance)
        self.hwnd = self._create_window()

        self._side_canvas = self._create_fitted_canvas(
            image = side_image,
            width = self._edge_length,
            height = self._edge_length,
            bg_color = self._bg_color
        )

        self._center_canvas: Image | None = None
        if center_image:
            center_canvas_width = self._width - (self._edge_length * 2) - 6
            self._center_canvas = self._create_fitted_canvas(
                image = center_image,
                width = center_canvas_width,
                height = self._edge_length,
                bg_color = self._bg_color
            )

        _image_panels[self.hwnd] = self

        UpdateWindow(self.hwnd)
        ShowWindow(self.hwnd, win32con.SW_SHOW)

    @staticmethod
    def _create_fitted_canvas(image: Image, width: int, height: int, bg_color: int) -> Image:
        ratio = min(width / image.width, height / image.height)
        new_size = (int(image.width * ratio), int(image.height * ratio))
        resized_image = image.resize(new_size, PilImage.Resampling.LANCZOS)
        mask = resized_image.split()[3] if 'A' in resized_image.getbands() else None

        paste_x = (width - new_size[0]) // 2
        paste_y = (height - new_size[1]) // 2

        canvas = PilImage.new("RGB", (width, height), get_rgb(bg_color))
        canvas.paste(resized_image, (paste_x, paste_y), mask)

        return canvas

    def _create_window(self) -> int:
        return CreateWindowEx(
            dwExStyle = 0,
            lpClassName = self._class_name,
            lpWindowName = "Title Panel",
            dwStyle = win32con.WS_CHILD,
            x = 0, y = 0, nWidth = self._width, nHeight = self._edge_length + 6,
            hWndParent = self._core_context.main_window,
            hMenu = None,
            hInstance = self._core_context.h_instance,
            lpParam = id(self)
        )

    @classmethod
    def _register_window_class(cls, h_instance) -> None:
        """Register the window class for the image panel."""

        if cls._class_registered:
            return

        RegisterClassEx(
            WNDCLASSEX(
                style = win32con.CS_HREDRAW | win32con.CS_VREDRAW,
                lpfnWndProc = Dispatcher,
                hInstance = h_instance,
                hCursor = LoadCursor(0, win32con.IDC_ARROW),
                hbrBackground = GetSysColorBrush(win32con.BLACK_BRUSH),
                lpszClassName = cls._class_name
            )
        )
        cls._class_registered = True

    @staticmethod
    def wnd_proc(hwnd, msg, wparam, lparam):
        """Window procedure for handling window messages."""
        # Get the instance associated with this window
        header: Header = _image_panels.get(hwnd)

        if msg == win32con.WM_PAINT:
            if header:
                ps, hdc = BeginPaint(hwnd)

                header._draw_sunken_area(hdc, 0, 0, header._width, header._edge_length + 6)
                header._draw_left_image(hdc, 3, 3, header._flip_left_image)
                header._draw_right_image(hdc, header._width - header._edge_length - 3, 3, header._flip_right_image)
                header._draw_center_image(hdc, header._edge_length + 3, 3)
                header._draw_text(hdc, ps.rcPaint)

                EndPaint(hwnd, ps)
            return 0

        elif msg == win32con.WM_DESTROY:
            # Clean up when the window is destroyed
            if header:
                header._side_canvas.close()
                header._side_canvas = None

                header._side_image.close()
                header._side_image = None

                # Remove from dictionary
                if hwnd in _image_panels:
                    del _image_panels[hwnd]
            return 0

        return DefWindowProc(hwnd, msg, wparam, lparam)

    def _draw_sunken_area(self, hdc, x, y, width, height):
        def create_pen(base_color_rgb: tuple[int, int, int], scale_factor: float) -> int:
            r, g, b = base_color_rgb

            new_r, new_g, new_b = adjust_rgb(r, g, b, scale_factor)

            return CreatePen(win32con.PS_SOLID, 1, wintypes.RGB(new_r, new_g, new_b))

        sunken_area_rect = wintypes.RECT(x + 2, y + 2, x + width - 2, y + height - 2)
        white_brush = CreateSolidBrush(self._bg_color)

        FillRect(hdc, sunken_area_rect, white_brush)
        DeleteObject(white_brush)

        dark_factor, darker_factor, light_factor, lighter_factor = self._scale_factors
        # Use the new helper to create 1-pixel-wide pens
        base_color = get_rgb(self._bg_color)
        dark_pen = create_pen(base_color, scale_factor = dark_factor)
        darker_pen = create_pen(base_color, scale_factor = darker_factor)
        light_pen = create_pen(base_color, scale_factor = light_factor)
        lighter_pen = create_pen(base_color, scale_factor = lighter_factor)

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
        LineTo(hdc, x + width - 2, y + height - 1)

        SelectObject(hdc, old_pen)

        # Cleanup
        DeleteObject(dark_pen)
        DeleteObject(darker_pen)
        DeleteObject(lighter_pen)
        DeleteObject(light_pen)

    def _draw_left_image(self, hdc, x, y, flip) -> None:
        if self._side_canvas:
            self._draw_image(hdc, self._side_canvas, x, y, flip)

    def _draw_right_image(self, hdc, x, y, flip) -> None:
        if self._side_canvas:
            self._draw_image(hdc, self._side_canvas, x, y, flip)

    def _draw_center_image(self, hdc, x, y):
        if hasattr(self, '_center_canvas') and self._center_canvas:
            self._draw_image(hdc, self._center_canvas, x, y)

    @staticmethod
    def _draw_image(hdc, image, x, y, flip = False) -> None:
        if image:
            try:
                img_width, img_height = image.size

                if flip:
                    image = image.transpose(PilImage.Transpose.FLIP_LEFT_RIGHT)

                dib = ImageWin.Dib(image)
                dib.draw(hdc, (x, y, x + img_width, y + img_height))

            except Exception as e:
                print(f"Error drawing image: {e}")

    def _draw_text(self, hdc, rect: wintypes.RECT) -> None:
        text_rect = wintypes.RECT(
            rect.left + self._edge_length + 3,
            rect.top,
            rect.right - self._edge_length - 3,
            rect.bottom
        )

        font = LOGFONT(
            height = -75,
            weight = win32con.FW_BOLD,
            face_name = 'Microsoft Sans Serif',
            charset = win32con.DEFAULT_CHARSET,  # Important for character encoding
            quality = win32con.CLEARTYPE_QUALITY  # Better text rendering
        )
        h_font = CreateFontIndirect(font)
        old_font = SelectObject(hdc, h_font)

        SetBkMode(hdc, win32con.TRANSPARENT)
        SetTextColor(hdc, self._text_color)

        DrawText(
            hdc,
            self._text,
            -1,
            text_rect,
            win32con.DT_VCENTER | win32con.DT_CENTER | win32con.DT_SINGLELINE  # Added SINGLELINE
        )

        SelectObject(hdc, old_font)
        DeleteObject(h_font)

    def destroy(self) -> None:
        """Destroy the panel window."""
        if self.hwnd:
            # DeleteObject(self.background_brush)
            DestroyWindow(self.hwnd)
            self.hwnd = None
