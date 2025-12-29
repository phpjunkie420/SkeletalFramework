import ctypes
from ctypes import wintypes

import win32con

from skeletal_framework.win32_bindings.dispatcher import Dispatcher
from skeletal_framework.win32_bindings.dwmapi import DwmSetWindowAttribute, DWMWINDOWATTRIBUTE
from skeletal_framework.win32_bindings.gdi32 import *
from skeletal_framework.win32_bindings.kernel32 import GetModuleHandle
from skeletal_framework.win32_bindings.monitor_info import GetMonitorInfo, MonitorFromPoint
from skeletal_framework.win32_bindings.user32 import *


class ExceptionHandlerDialog:
    def __init__(self):
        self._hwnd: int | None = None
        self._class_name = 'ExceptionHandlerDialogClass'
        self._window_name = 'Exception Handler'
        self._dark_mode = False

        self._hbr_background = 0
        if self._dark_mode:
            self._hbr_background = CreateSolidBrush(
                color = wintypes.RGB(
                    red = 75, green = 75, blue = 75
                )
            )

        self._width = 800
        self._height = 600

        self._h_instance = GetModuleHandle(None)

        self._atom = self._register_class()
        self._create_window()

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_NCCREATE:
            self._hwnd = hwnd

        elif msg == win32con.WM_CREATE:
            self.invalidate_geometry()
            self.create_controls()
            return 0

        # elif msg == win32con.WM_CTLCOLORSTATIC:
        #     hdc = wparam
        #     # Set text color to white
        #     SetTextColor(hdc, wintypes.RGB(200, 0, 0))
        #     # Set background color of the text to dark gray
        #     SetBkColor(hdc, wintypes.RGB(255, 255, 255))
        #     # Return the brush handle for the control background
        #     return self._hbr_edit_background

        elif msg == win32con.WM_CLOSE:
            pass

        elif msg == win32con.WM_DESTROY:
            self.destroy()
            PostQuitMessage(0)
            return 0

        return DefWindowProc(hwnd, msg, wparam, lparam)

    def _use_immersive_dark_mode(self):
        DwmSetWindowAttribute(
            hwnd = self._hwnd,
            dwAttribute = DWMWINDOWATTRIBUTE.DWMWA_USE_IMMERSIVE_DARK_MODE,
            pvAttribute = True
        )

    def create_controls(self):
        hwnd_edit = CreateWindowEx(  # noqa
            dwExStyle = 0,
            lpClassName = 'EDIT',
            lpWindowName = 'This is a read-only info box.\r\nIt has custom colors.',
            dwStyle = (
                    win32con.WS_CHILD
                    | win32con.WS_VISIBLE
                    | win32con.WS_BORDER
                    | win32con.ES_MULTILINE
                    | win32con.ES_AUTOVSCROLL
                    | win32con.WS_VSCROLL
                    | win32con.ES_READONLY
            ),
            x = 10, y = 10,
            nWidth = self._width - 20, nHeight = self._height - 20,
            hWndParent = self._hwnd,
            hMenu = None,
            hInstance = self._h_instance,
            lpParam = None
        )

        # SetWindowTheme(hwnd_edit, "DarkMode_Explorer", None)

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
        *_, width, height = GetClientRect(self._hwnd)

        width_adjustment = self._width - width
        height_adjustment = self._height - height

        if width_adjustment > 0 or height_adjustment > 0:
            *_, width, height = GetWindowRect(self._hwnd)
            current_width, current_height = width, height

            width, height = current_width + width_adjustment, current_height + height_adjustment

            monitor = GetMonitorInfo(MonitorFromPoint(0, 0))
            SetWindowPos(
                self._hwnd, 0,
                (monitor.width - width) // 2, (monitor.height - height) // 2,
                width, height,
                win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE
            )

    def destroy(self):
        if self._hwnd is not None and self._hwnd:
            DestroyWindow(self._hwnd)
            try:
                UnregisterClass(self._class_name, self._h_instance)
            except:  # noqa
                pass

    def show_window(self):
        if self._dark_mode:
            self._use_immersive_dark_mode()

        DwmSetWindowAttribute(
            hwnd = self._hwnd,
            dwAttribute = DWMWINDOWATTRIBUTE.DWMWA_CAPTION_COLOR,
            pvAttribute = wintypes.RGB(50, 50, 50)
        )

        ShowWindow(self._hwnd, win32con.SW_SHOW)
        UpdateWindow(self._hwnd)

        msg = ctypes.byref(wintypes.MSG())
        while GetMessage(msg, None, 0, 0) > 0:
            TranslateMessage(msg)
            DispatchMessage(msg)


if __name__ == '__main__':
    dialog = ExceptionHandlerDialog()
    dialog.show_window()
