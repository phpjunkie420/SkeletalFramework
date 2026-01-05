import ctypes
from ctypes import wintypes

import win32con

from skeletal_framework.controls.label import Label, Style
from skeletal_framework.core_context import CoreContext
from skeletal_framework.dispatcher import Dispatcher
from skeletal_framework.win32_bindings.dwmapi import DwmSetWindowAttribute, DWMWINDOWATTRIBUTE
from skeletal_framework.win32_bindings.gdi32 import CreateSolidBrush, DeleteObject
from skeletal_framework.win32_bindings.monitor_info import GetMonitorInfo, MonitorFromPoint
from skeletal_framework.win32_bindings.user32 import (
    # Structures
    WNDCLASS,

    # Functions
    CreateWindowEx,
    DefWindowProc, DestroyWindow, DispatchMessage,
    GetMessage, GetClientRect, GetWindowRect,
    LoadCursor,
    PostQuitMessage,
    RegisterClass,
    SetWindowPos, ShowWindow,
    UpdateWindow, UnregisterClass,
    TranslateMessage
)


class ExampleWindow:
    _CLASS_NAME = 'ExampleWindowClass'
    _WINDOW_NAME = 'Example Window'

    def __init__(self):
        self._core_context = CoreContext()

        self._hbr_background: int | None = CreateSolidBrush(
            color = wintypes.RGB(
                red = 75, green = 75, blue = 75
            )
        )

        self._width = 800
        self._height = 600

        self._label: Label | None = None

        self._atom = self._register_class()
        self._create_window()

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_NCCREATE:
            self._core_context.setattr(
                'main_window',
                hwnd
            )

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
            hwnd = self._core_context.main_window,
            dwAttribute = DWMWINDOWATTRIBUTE.DWMWA_USE_IMMERSIVE_DARK_MODE,
            pvAttribute = True
        )

    def create_controls(self):
        self._label = Label(
            'Hello World!',
            10, 10, self._width - 20, 20,
            1000

        )

    def _create_window(self):
        return CreateWindowEx(
            dwExStyle = win32con.WS_EX_TOPMOST,
            lpClassName = self._CLASS_NAME,
            lpWindowName = self._WINDOW_NAME,
            dwStyle = win32con.WS_SYSMENU,
            x = win32con.CW_USEDEFAULT, y = win32con.CW_USEDEFAULT,
            nWidth = self._width, nHeight = self._height,
            hWndParent = None, hMenu = None,
            hInstance = self._core_context.h_instance, lpParam = id(self)
        )

    def _register_class(self):
        return RegisterClass(
            lpWndClass = WNDCLASS(
                style = win32con.CS_HREDRAW | win32con.CS_VREDRAW,
                lpfnWndProc = Dispatcher,
                hInstance = self._core_context.h_instance,
                hIcon = None,
                hbrBackground = self._hbr_background,
                hCursor = LoadCursor(0, win32con.IDC_ARROW),
                lpszClassName = self._CLASS_NAME
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
            DeleteObject(self._hbr_background)
            del self._hbr_background

        hwnd = self._core_context.main_window
        if hwnd is not None and hwnd:
            DestroyWindow(hwnd)
            try:
                UnregisterClass(self._CLASS_NAME, self._core_context.h_instance)
            except:  # noqa
                pass

    def show_window(self):
        hwnd = self._core_context.main_window

        DwmSetWindowAttribute(
            hwnd = hwnd,
            dwAttribute = DWMWINDOWATTRIBUTE.DWMWA_CAPTION_COLOR,
            pvAttribute = wintypes.RGB(50, 50, 50)
        )

        ShowWindow(hwnd, win32con.SW_SHOW)
        UpdateWindow(hwnd)

        msg = ctypes.byref(wintypes.MSG())
        while GetMessage(msg, None, 0, 0) > 0:
            TranslateMessage(msg)
            DispatchMessage(msg)


if __name__ == '__main__':
    dialog = ExampleWindow()
    dialog.show_window()
