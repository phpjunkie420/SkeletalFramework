import ctypes
from ctypes import wintypes

import win32con

from skeletal_framework.win32_bindings.dispatcher import *
from skeletal_framework.win32_bindings.dwmapi import *
from skeletal_framework.win32_bindings.gdi32 import *
from skeletal_framework.win32_bindings.kernel32 import *
from skeletal_framework.win32_bindings.monitor_info import *
from skeletal_framework.win32_bindings.user32 import *


class AbstractDialogWindow:
    _CLASS_NAME = 'AbstractDialogWindowClass'
    _WINDOW_NAME = 'Abstract Dialog'

    def __init__(self):
        self._hwnd: int | None = None

        self._hbr_background = CreateSolidBrush(
            color = wintypes.RGB(
                red = 50, green = 50, blue = 50
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
        pass

    def _create_window(self):
        return CreateWindowEx(
            dwExStyle = win32con.WS_EX_TOPMOST,
            lpClassName = self._CLASS_NAME,
            lpWindowName = self._WINDOW_NAME,
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
                lpszClassName = self._CLASS_NAME
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
        try:
            DeleteObject(self._hbr_background)
        except OSError:
            pass

        if self._hwnd is not None and self._hwnd:
            DestroyWindow(self._hwnd)
            try:
                UnregisterClass(self._CLASS_NAME, self._h_instance)
            except:  # noqa
                pass

    def show_window(self):
        self._use_immersive_dark_mode()

        ShowWindow(self._hwnd, win32con.SW_SHOW)
        UpdateWindow(self._hwnd)

        msg = ctypes.byref(wintypes.MSG())
        while GetMessage(msg, None, 0, 0) > 0:
            TranslateMessage(msg)
            DispatchMessage(msg)
