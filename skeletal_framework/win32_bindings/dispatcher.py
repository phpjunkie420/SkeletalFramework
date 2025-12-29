import ctypes

import win32con

from skeletal_framework.win32_bindings.user32 import (
    # Structures
    CREATESTRUCT, WNDPROC,

    # Functions
    DefWindowProc, GetWindowLong, SetWindowLong
)

__all__ = [
    'Dispatcher'
]


@WNDPROC
def Dispatcher(hwnd, msg, wparam, lparam):
    """
    Generic dispatcher that can be used for any window class.
    Store the instance in our global dictionary.
    """
    if msg == win32con.WM_NCCREATE:
        cs = ctypes.cast(lparam, ctypes.POINTER(CREATESTRUCT)).contents

        instance_id = cs.lpCreateParams
        SetWindowLong(hwnd, win32con.GWL_USERDATA, instance_id)

        instance = ctypes.cast(instance_id, ctypes.py_object).value
        instance._hwnd = hwnd

        return instance.wnd_proc(hwnd, msg, wparam, lparam)

    instance_id = GetWindowLong(hwnd, win32con.GWL_USERDATA)
    if instance_id:
        instance = ctypes.cast(instance_id, ctypes.py_object).value
        return instance.wnd_proc(hwnd, msg, wparam, lparam)
    else:
        return DefWindowProc(hwnd, msg, wparam, lparam)
