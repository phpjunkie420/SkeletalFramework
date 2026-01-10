import ctypes
import operator
from abc import ABC, abstractmethod
from ctypes import wintypes
from typing import Any, TypedDict, Unpack

import win32con

from skeletal_framework.core_context import CoreContext
from skeletal_framework.win32_bindings.gdi32 import *
from skeletal_framework.win32_bindings.user32 import *

__all__ = ['Checkbox']


class _X(TypedDict):
    x: int


class _Y(TypedDict):
    y: int


class _Position(_X, _Y): ...


class _RequiredAttributes(TypedDict):
    width: int
    text: str
    ctrl_id: int


class _OptionalAttributes(TypedDict, total = False):
    font_size: int


class _Kwargs(_Position, _RequiredAttributes, _OptionalAttributes): ...


def build_class(*types): ...


class Checkbox(ABC):

    @property
    def hwnd(self) -> int: return self._hwnd

    @property
    def control_id(self) -> int: return self._ctrl_id

    @property
    def context(self) -> CoreContext: return self._context

    @property
    def is_checked(self) -> bool: return self._is_checked

    @is_checked.setter
    def is_checked(self, value: bool):
        if self._is_checked != value:
            self._is_checked = value
            self._on_check_changed(value)
            InvalidateRect(self._hwnd, None, True)

    def __init__(self, **kwargs: Unpack[_Position , _RequiredAttributes]):
        self._context = CoreContext()

        x, y, width, text, ctrl_id = operator.itemgetter('x', 'y', 'width', 'text', 'ctrl_id')(kwargs)  # type: int, int, int, str, int
        font_size = kwargs.get('font_size', 10)

        self._parent_hwnd = self._context.main_window
        self._ctrl_id = ctrl_id
        self._text = text
        self._hwnd = self._crete_window(x, y, width, 20, text)
        self._font, self._checkmark_font = self._create_logfonts(font_size)

        if not hasattr(self, '_is_checked'):
            self._is_checked = False

        SetWindowLong(self._hwnd, win32con.GWL_USERDATA, id(self))
        self._original_wnd_proc = SetWindowLong(self._hwnd, win32con.GWL_WNDPROC, _subclass_proc)

    @abstractmethod
    def _on_check_changed(self, value: bool): ...

    def _crete_window(self, x, y, width, height, text: str = ""):
        style = (
                win32con.WS_CHILD
                | win32con.WS_VISIBLE
                | win32con.BS_OWNERDRAW
        )

        # Create the window using our custom class name.
        # We pass id(self) so the dispatcher can link this HWND to this Python object instance.
        return CreateWindowEx(
            dwExStyle = 0,
            lpClassName = 'BUTTON', lpWindowName = text,
            dwStyle = style,
            x = x, y = y, nWidth = width, nHeight = height,
            hWndParent = self._parent_hwnd,
            hMenu = self._ctrl_id,
            hInstance = self._context.h_instance,
            lpParam = id(self)
        )

    @staticmethod
    def _create_logfonts(font_size) -> tuple[Any, Any]:
        return (
            CreateFontIndirect(
                LOGFONT(
                    height = -int(font_size * 1.333),  # Negative for character height in pixels
                    charset = win32con.DEFAULT_CHARSET,
                    out_precision = win32con.OUT_DEFAULT_PRECIS,
                    clip_precision = win32con.CLIP_DEFAULT_PRECIS,
                    quality = win32con.CLEARTYPE_QUALITY,
                    pitch_and_family = win32con.DEFAULT_PITCH | win32con.FF_DONTCARE,
                    face_name = "Microsoft Sans Serif"
                )
            ),
            CreateFontIndirect(
                LOGFONT(
                    height = -26,
                    charset = win32con.DEFAULT_CHARSET,
                    out_precision = win32con.OUT_DEFAULT_PRECIS,
                    clip_precision = win32con.CLIP_DEFAULT_PRECIS,
                    quality = win32con.CLEARTYPE_QUALITY,
                    face_name = "Microsoft Sans Serif"
                )
            )
        )

    def wnd_proc(self, hwnd: int, msg: int, wparam: int, lparam: int) -> int:
        if msg == win32con.WM_PAINT:
            self.on_paint_item(hwnd = hwnd)

        elif msg == win32con.WM_LBUTTONDOWN:
            return 0

        elif msg == win32con.WM_LBUTTONUP:
            SendMessage(self._context.main_window, win32con.WM_COMMAND, self._ctrl_id, self._hwnd)
            return 0

        return CallWindowProc(self._original_wnd_proc, hwnd, msg, wparam, lparam)

    def on_paint_item(self, hwnd: int) -> None:
        ps, hdc = BeginPaint(hwnd)
        ps.fErase = True

        rect = wintypes.RECT()
        GetClientRect(self._hwnd, rect)

        old_font = SelectObject(hdc, self._font)

        box_size = 12
        box_top = (rect.bottom - rect.top - box_size) // 2
        box_left = 0
        box_rect = wintypes.RECT(box_left, box_top, box_left + box_size, box_top + box_size)
        corner_radius = 3

        SetBkMode(hdc, win32con.TRANSPARENT)

        # --- Start of Modified Drawing Logic ---

        # 1. Get a black pen for the border and a white brush for the fill.
        border_pen = CreatePen(win32con.PS_SOLID, 1, GetSysColor(win32con.COLOR_WINDOWTEXT))
        white_brush = GetStockObject(win32con.WHITE_BRUSH)

        # 2. Select the new GDI objects and save the old ones.
        old_pen = SelectObject(hdc, border_pen)
        old_brush = SelectObject(hdc, white_brush)

        # 3. Draw the rounded rectangle. It will be filled with the selected brush (white)
        #    and outlined with the selected pen (black).
        RoundRect(hdc, box_rect.left, box_rect.top, box_rect.right, box_rect.bottom, corner_radius, corner_radius)

        # 4. Clean up GDI objects by restoring the originals and deleting the new ones.
        SelectObject(hdc, old_pen)
        SelectObject(hdc, old_brush)
        DeleteObject(border_pen)

        # --- End of Modified Drawing Logic ---

        if self.is_checked:
            check_rect = wintypes.RECT(box_rect.left, box_rect.top - 5, box_rect.right + 5, box_rect.bottom)

            old_checkmark_font = SelectObject(hdc, self._checkmark_font)

            old_text_color = SetTextColor(hdc, wintypes.RGB(0, 0, 0))
            DrawText(hdc, "🗸", -1, check_rect, win32con.DT_CENTER | win32con.DT_VCENTER | win32con.DT_SINGLELINE)

            # 4. Clean up resources.
            SetTextColor(hdc, old_text_color)
            SelectObject(hdc, old_checkmark_font)

            # --- End of Simplified Checkmark Logic ---

        # Draw the label text (e.g., "Show Computer Icon")
        text_rect = wintypes.RECT(box_rect.right + 5, rect.top - 1, rect.right, rect.bottom)
        SetTextColor(hdc, GetSysColor(win32con.COLOR_WINDOWTEXT))
        DrawText(hdc, self._text, -1, text_rect, win32con.DT_LEFT | win32con.DT_VCENTER | win32con.DT_SINGLELINE)

        SelectObject(hdc, old_font)

        EndPaint(hwnd, ps)

    def destroy(self):
        pass


@WNDPROC
def _subclass_proc(hwnd, msg, wparam, lparam):
    instance_id = GetWindowLong(hwnd, win32con.GWL_USERDATA)
    if instance_id:
        instance = ctypes.cast(instance_id, ctypes.py_object).value
        instance._hwnd = hwnd
        return instance.wnd_proc(hwnd, msg, wparam, lparam)
    else:
        return DefWindowProc(hwnd, msg, wparam, lparam)
