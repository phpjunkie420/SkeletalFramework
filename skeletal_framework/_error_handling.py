import ctypes
import sys
import threading
from traceback import format_exception
from ctypes import wintypes
from datetime import datetime
from pathlib import Path
from threading import Thread, ExceptHookArgs
from typing import Type
from types import TracebackType


import rich
import win32con

from skeletal_framework.controls.editbox import CustomEditBox
from skeletal_framework.controls.header import Header
from skeletal_framework.core_context import CoreContext
from skeletal_framework.dispatcher import Dispatcher
from skeletal_framework.win32_bindings.dwmapi import DwmSetWindowAttribute, DWMWINDOWATTRIBUTE  # noqa
from skeletal_framework.win32_bindings.gdi32 import *
from skeletal_framework.win32_bindings.kernel32 import GetModuleHandle
from skeletal_framework.win32_bindings.macros import hiword, loword
from skeletal_framework.win32_bindings.monitor_info import GetMonitorInfo, MonitorFromPoint
from skeletal_framework.win32_bindings.user32 import *
from skeletal_framework.resources import *


class ExceptionHandlerDialog:
    _ID_EDITBOX = 1000

    def __init__(self, exc_type: Type[BaseException], log_text: str):
        self._core_context = CoreContext()

        self._class_name = 'ExceptionHandlerDialogClass'
        self._window_name = 'Application has crashed . . .'

        self._exception_name = exc_type.__name__
        self._log_text = '\r\n'.join(log_text.splitlines())

        self._hbr_background = GetSysColorBrush(win32con.COLOR_BTNFACE)
        # self._hbr_background = CreateSolidBrush(
        #     color = wintypes.RGB(
        #         red = 50, green = 50, blue = 50
        #     )
        # )

        self._width = 800
        self._height = 600

        self.font_name = "Segoe UI"
        self.font_size = 12

        self._h_font = self._create_font()
        self._header: Header | None = None
        self._edit_box: int | None = None
        self._h_instance = GetModuleHandle(None)

        self._atom = self._register_class()
        self._create_window()

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_NCCREATE:
            self._core_context.setattr(
                key = 'main_window',
                value = hwnd
            )

        elif msg == win32con.WM_CREATE:
            self.invalidate_geometry()
            self.create_controls()
            return 0

        elif msg == win32con.WM_COMMAND:
            control_id = loword(wparam)
            if control_id == self._ID_EDITBOX:
                notification_code = hiword(wparam)
                if notification_code == win32con.EN_SETFOCUS:
                    HideCaret(lparam)

        elif msg == win32con.WM_CLOSE:
            pass

        elif msg == win32con.WM_DESTROY:
            self.destroy()
            PostQuitMessage(0)
            return 0

        return DefWindowProc(hwnd, msg, wparam, lparam)

    def create_controls(self):
        self._header = Header(
            text = self._exception_name,
            side_image = EXCEPTION_HAND,
            center_image = EXCEPTION_FACE,
            edge_length = 125,
            # scale_factors = (0.90, 0.70, 1.285, 1.3),
            text_color = wintypes.RGB(red = 255, green = 0, blue = 0),
            # bg_color = wintypes.RGB(60, 60, 60)
            flip_right_image = True,
        )

        # self._edit_box = CustomEditBox(
        #     10, 145, self._width - 20, self._height - 155,
        #     text = self._log_text,
        #     font_name = 'Helvetica',
        #     font_size = 12,
        #     bg_color = wintypes.RGB(50, 50, 50),
        #     text_color = wintypes.RGB(red = 255, green = 0, blue = 0),
        # )

        style = (
            win32con.WS_CHILD
            | win32con.WS_VISIBLE
            | win32con.WS_BORDER
            | win32con.ES_LEFT
            | win32con.ES_MULTILINE
            | win32con. ES_AUTOVSCROLL
            | win32con.WS_VSCROLL
            | win32con.ES_AUTOHSCROLL
            | win32con.WS_HSCROLL
            | win32con.ES_READONLY
            | win32con.WS_TABSTOP
        )

        self._edit_box = CreateWindowEx(
            dwExStyle = 0,
            lpClassName = "EDIT",
            lpWindowName = self._log_text,
            dwStyle = style,
            x = 10, y = 145, nWidth = self._width - 20, nHeight = self._height - 155,
            hWndParent = self._core_context.main_window,
            hMenu = self._ID_EDITBOX,
            hInstance = self._h_instance,
            lpParam = None
        )
        SendMessage(
            self._edit_box,
            win32con.WM_SETFONT,
            self._h_font,
            True
        )

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

    def _create_window(self):
        return CreateWindowEx(
            dwExStyle = win32con.WS_EX_TOPMOST,
            lpClassName = self._class_name,
            lpWindowName = self._window_name,
            dwStyle = win32con.WS_SYSMENU,
            x = win32con.CW_USEDEFAULT, y = win32con.CW_USEDEFAULT,
            nWidth = self._width, nHeight = self._height,
            hWndParent = None, hMenu = None,
            hInstance = self._h_instance, lpParam = id(self)
        )

    def _register_class(self):
        return RegisterClass(
            lpWndClass = WNDCLASS(
                style = win32con.CS_HREDRAW | win32con.CS_VREDRAW,
                lpfnWndProc = Dispatcher,
                hInstance = self._h_instance,
                hIcon = None,
                hbrBackground = self._hbr_background,
                hCursor = LoadCursor(0, win32con.IDC_ARROW),
                lpszClassName = self._class_name
            )
        )

    def invalidate_geometry(self):
        hwnd = self._core_context.main_window

        rect = wintypes.RECT()
        GetClientRect(hwnd, rect)
        width, height = rect.right - rect.left, rect.bottom - rect.top

        width_adjustment = self._width - width
        height_adjustment = self._height - height

        if width_adjustment > 0 or height_adjustment > 0:
            GetWindowRect(hwnd, rect)
            current_width, current_height = rect.right - rect.left, rect.bottom - rect.top

            width, height = current_width + width_adjustment, current_height + height_adjustment

            monitor = GetMonitorInfo(MonitorFromPoint(0, 0))
            SetWindowPos(
                hwnd, 0,
                (monitor.width - width) // 2, (monitor.height - height) // 2,
                width, height,
                win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE
            )

    def destroy(self):
        if hasattr(self, '_hbr_background'):
            if self._hbr_background:
                DeleteObject(self._hbr_background)

            del self._hbr_background

        if hasattr(self, '_bg_brush'):
            if self._bg_brush is not None:
                DeleteObject(self._bg_brush)

            del self._bg_brush

        hwnd = self._core_context.main_window

        if hwnd is not None and hwnd:
            DestroyWindow(hwnd)
            try:
                UnregisterClass(self._class_name, self._h_instance)
            except:  # noqa
                pass

    def show_window(self):
        hwnd = self._core_context.main_window

        # DwmSetWindowAttribute(
        #     hwnd = hwnd,
        #     dwAttribute = DWMWINDOWATTRIBUTE.DWMWA_CAPTION_COLOR,
        #     pvAttribute = wintypes.RGB(25, 25, 25)
        # )

        ShowWindow(hwnd, win32con.SW_SHOW)
        UpdateWindow(hwnd)

        msg = ctypes.byref(wintypes.MSG())
        while GetMessage(msg, None, 0, 0) > 0:
            TranslateMessage(msg)
            DispatchMessage(msg)

    @classmethod
    def system_exception_hook(cls, exc_type: Type[BaseException], exc_value: BaseException, exc_traceback: TracebackType) -> None:
        cls._format_exception(exc_type, exc_value, exc_traceback)

    @classmethod
    def threading_exception_hook(cls, args: ExceptHookArgs) -> None:
        exc_type, exc_value, exc_traceback, exc_thread = args

        cls._format_exception(exc_type, exc_value, exc_traceback, exc_thread)

    @classmethod
    def _format_exception(cls, exc_type: Type[BaseException], exc_value: BaseException, exc_traceback: TracebackType, exc_thread: Thread | None = None) -> None:
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        traceback = format_exception(exc_type, exc_value, exc_traceback)
        if exc_thread is not None:
            traceback.insert(0, f'Exception occurred in thread: {exc_thread.name!r}\n')
        traceback = ''.join(traceback)

        cls._log_exception(text = traceback)
        cls(
            exc_type = exc_type,
            log_text = traceback
        ).show_window()

    @staticmethod
    def _log_exception(
            text: str
    ) -> None:
        """Handle uncaught exceptions by logging to file and displaying dialog."""

        rootpath = Path(__file__).parent.parent
        crash_reports = rootpath / 'crash_reports'
        crash_reports.mkdir(parents = True, exist_ok = True)

        # Create a log file with a timestamp
        now = datetime.now()
        log_file = crash_reports / f'{now.strftime('%m-%d-%Y %H.%M.%S')}.log'
        log_file.write_text(text, encoding = 'utf-8')
        rich.console.Console(highlight = False, style = 'red').print(log_file.read_text())

    @classmethod
    def install_exception_handlers(cls, main_class_name: str = "Application"):
        """Install the custom exception handler."""
        cls._main_class_name = main_class_name
        sys.excepthook = cls.system_exception_hook
        threading.excepthook = cls.threading_exception_hook
