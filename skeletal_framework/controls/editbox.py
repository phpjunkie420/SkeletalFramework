import ctypes
from ctypes import wintypes
import win32con

from skeletal_framework.core_context import CoreContext
from skeletal_framework.controls.custom_scrollbar import CustomScrollBar
from skeletal_framework.dispatcher import Dispatcher
# Added CreateFont to imports
from skeletal_framework.win32_bindings.gdi32 import (
    CreateSolidBrush, DeleteObject, SetTextColor, SetBkColor, CreateFont
)
from skeletal_framework.win32_bindings.kernel32 import GetModuleHandle
from skeletal_framework.win32_bindings.macros import hiword, loword, MAKEWPARAM
from skeletal_framework.win32_bindings.user32 import (
    SCROLLINFO, WNDCLASS, WNDPROC, CreateWindowEx, DefWindowProc, RegisterClass,
    LoadCursor, PostMessage, SetWindowLong, CallWindowProc,
    SendMessage, SetWindowText, GetWindowLong, GetScrollInfo,
    GetSystemMetrics, SetWindowPos
)


class CustomEditBox:
    _CLASS_NAME = "CustomEditBoxContainerClass"
    _ATOM = None

    def __init__(
            self,
            x: int, y: int, width: int, height: int,
            *,
            text: str = "",
            # New Font Parameters
            font_name: str = "Segoe UI",
            font_size: int = 12,
            border_color: int = wintypes.RGB(0, 0, 0),
            bg_color: int = wintypes.RGB(75, 75, 75),
            text_color: int = wintypes.RGB(220, 220, 220),
            scrollbar_width: int = 18,
            border_size: int = 1,
            parent_hwnd: int | None = None
    ):
        self._core_context = CoreContext()

        self._parent_hwnd = parent_hwnd or self._core_context.main_window
        self.x, self.y, self.width, self.height = x, y, width, height
        self.font_name = font_name
        self.font_size = font_size
        self.border_color = border_color
        self.bg_color = bg_color
        self.text_color = text_color
        self.scrollbar_width = scrollbar_width
        self.border_size = border_size

        self._h_instance = GetModuleHandle(None)
        self._bg_brush = CreateSolidBrush(self.bg_color)
        self._border_brush = CreateSolidBrush(self.border_color)

        self._register_class()
        self._hwnd = self._create_window()

        self._hwnd_edit = self._create_edit_control()

        # Create and set font
        self._h_font = self._create_font()
        SendMessage(self._hwnd_edit, win32con.WM_SETFONT, self._h_font, True)

        self._scrollbar = self._create_scrollbar()

        SetWindowPos(
            self._scrollbar.hwnd,
            win32con.HWND_TOP,
            0, 0, 0, 0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
        )

        self._parent_proc = None
        self._subclass_edit_control()

        self.set_text(text)
        self.update_scrollbar()

    def _create_font(self):
        # Calculate height from point size.
        # Formula: -MulDiv(PointSize, GetDeviceCaps(hDC, LOGPIXELSY), 72)
        # Assuming 96 DPI for simplicity here: -int(size * 96 / 72) -> size * 1.333
        height = -int(self.font_size * 1.33333)

        return CreateFont(
            cHeight = height,
            cWidth = 0,
            cEscapement = 0,
            cOrientation = 0,
            cWeight = win32con.FW_NORMAL,
            bItalic = 0,
            bUnderline = 0,
            bStrikeOut = 0,
            iCharSet = win32con.DEFAULT_CHARSET,
            iOutPrecision = win32con.OUT_DEFAULT_PRECIS,
            iClipPrecision = win32con.CLIP_DEFAULT_PRECIS,
            iQuality = win32con.CLEARTYPE_QUALITY,
            iPitchAndFamily = win32con.DEFAULT_PITCH | win32con.FF_DONTCARE,
            pszFaceName = self.font_name
        )

    def _register_class(self):
        if CustomEditBox._ATOM is None:
            wnd_class = WNDCLASS(
                style = win32con.CS_HREDRAW | win32con.CS_VREDRAW,
                lpfnWndProc = Dispatcher,
                hInstance = self._h_instance,
                hCursor = LoadCursor(0, win32con.IDC_ARROW),
                lpszClassName = self._CLASS_NAME,
                hbrBackground = self._border_brush
            )
            CustomEditBox._ATOM = RegisterClass(wnd_class)

    def _create_window(self):
        return CreateWindowEx(
            dwExStyle = 0,
            lpClassName = self._CLASS_NAME,
            lpWindowName = "",
            dwStyle = win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.WS_CLIPCHILDREN,
            x = self.x, y = self.y,
            nWidth = self.width, nHeight = self.height,
            hWndParent = self._parent_hwnd,
            hMenu = None,
            hInstance = self._h_instance,
            lpParam = id(self)
        )

    def _create_edit_control(self):
        edit_style = (
                win32con.WS_CHILD
                | win32con.WS_VISIBLE
                | win32con.ES_MULTILINE
                | win32con.ES_AUTOVSCROLL
                | win32con.ES_READONLY
                | win32con.WS_VSCROLL
                | win32con.WS_CLIPSIBLINGS
        )

        sys_sb_width = GetSystemMetrics(win32con.SM_CXVSCROLL)

        edit_x = self.border_size
        edit_y = self.border_size

        available_width = self.width - (self.border_size * 2) - self.scrollbar_width
        edit_width = available_width + sys_sb_width

        edit_height = self.height - (self.border_size * 2)

        hwnd = CreateWindowEx(
            dwExStyle = 0, lpClassName = 'EDIT', lpWindowName = "", dwStyle = edit_style,
            x = edit_x, y = edit_y, nWidth = edit_width, nHeight = edit_height,
            hWndParent = self._hwnd, hMenu = None, hInstance = self._h_instance, lpParam = None
        )
        return hwnd

    def _create_scrollbar(self):
        sb_x = self.width - self.scrollbar_width - self.border_size
        sb_y = self.border_size
        sb_height = self.height - (self.border_size * 2)
        return CustomScrollBar(
            parent_hwnd = self._hwnd,
            x = sb_x, y = sb_y,
            width = self.scrollbar_width, height = sb_height
        )

    def _subclass_edit_control(self):
        SetWindowLong(self._hwnd_edit, win32con.GWL_USERDATA, id(self))
        self._parent_proc = SetWindowLong(self._hwnd_edit, win32con.GWL_WNDPROC, _subclass_wnd_proc)

    @property
    def hwnd(self):
        return self._hwnd

    def set_text(self, text: str):
        SetWindowText(self._hwnd_edit, text)
        self.update_scrollbar()

    def update_scrollbar(self):
        si = SCROLLINFO()
        si.cbSize = ctypes.sizeof(SCROLLINFO)
        si.fMask = win32con.SIF_ALL

        try:
            GetScrollInfo(self._hwnd_edit, win32con.SB_VERT, si)
        except OSError:
            self._scrollbar.set_scroll_params(0.0, 1.0)
            return

        content_size = si.nMax - si.nMin + 1

        if si.nMax <= 0 or si.nPage >= content_size:
            scroll_pos = 0.0
            page_size = 1.0
        else:
            max_scroll = content_size - si.nPage
            scroll_pos = si.nPos / max_scroll if max_scroll > 0 else 0
            page_size = si.nPage / content_size

        self._scrollbar.set_scroll_params(scroll_pos, page_size)

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_CTLCOLORSTATIC and lparam == self._hwnd_edit:
            SetTextColor(wparam, self.text_color)
            SetBkColor(wparam, self.bg_color)
            return self._bg_brush

        elif msg == win32con.WM_MOUSEWHEEL:
            SendMessage(self._hwnd_edit, msg, wparam, lparam)
            return 0

        elif msg == win32con.WM_VSCROLL and lparam == self._scrollbar.hwnd:
            scroll_code = loword(wparam)

            if scroll_code == win32con.SB_THUMBTRACK:
                pos_float = hiword(wparam) / 65535.0
                si = SCROLLINFO()
                si.cbSize = ctypes.sizeof(SCROLLINFO)
                si.fMask = win32con.SIF_RANGE | win32con.SIF_PAGE
                try:
                    GetScrollInfo(self._hwnd_edit, win32con.SB_VERT, si)
                    max_scroll = si.nMax - si.nPage + 1
                    new_pos = int(pos_float * max_scroll)
                    SendMessage(self._hwnd_edit, win32con.WM_VSCROLL, MAKEWPARAM(win32con.SB_THUMBTRACK, new_pos), 0)
                except OSError:
                    pass

            elif scroll_code in (win32con.SB_LINEUP, win32con.SB_LINEDOWN, win32con.SB_PAGEUP, win32con.SB_PAGEDOWN):
                SendMessage(self._hwnd_edit, win32con.WM_VSCROLL, MAKEWPARAM(scroll_code, 0), 0)

            self.update_scrollbar()
            return 0

        elif msg == win32con.WM_NCDESTROY:
            self._cleanup()
            return 0

        return DefWindowProc(hwnd, msg, wparam, lparam)

    def wnd_proc_edit(self, hwnd, msg, wparam, lparam):
        res = CallWindowProc(self._parent_proc, hwnd, msg, wparam, lparam)

        if msg in (win32con.WM_VSCROLL, win32con.WM_MOUSEWHEEL, win32con.WM_KEYDOWN, win32con.WM_KEYUP, win32con.WM_CHAR):
            self.update_scrollbar()

        return res

    def _cleanup(self):
        if self._bg_brush: DeleteObject(self._bg_brush)
        if self._border_brush: DeleteObject(self._border_brush)
        # Delete font object
        if hasattr(self, '_h_font') and self._h_font:
            DeleteObject(self._h_font)

        if self._hwnd_edit and self._parent_proc:
            SetWindowLong(self._hwnd_edit, win32con.GWL_WNDPROC, self._parent_proc)


@WNDPROC
def _subclass_wnd_proc(hwnd, msg, wparam, lparam):
    instance_id = GetWindowLong(hwnd, win32con.GWL_USERDATA)
    if instance_id == 0:
        return DefWindowProc(hwnd, msg, wparam, lparam)
    try:
        instance = ctypes.cast(instance_id, ctypes.py_object).value
        return instance.wnd_proc_edit(hwnd, msg, wparam, lparam)
    except (ValueError, ctypes.ArgumentError):
        return DefWindowProc(hwnd, msg, wparam, lparam)
