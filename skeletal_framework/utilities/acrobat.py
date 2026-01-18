import ctypes
from collections.abc import Callable
from ctypes import wintypes
from typing import Any, TYPE_CHECKING

import psutil
import pyvda
from pyvda.utils import Managers
from pyvda.com_defns import IApplicationView

import win32con

from skeletal_framework.win32_bindings.monitor_info import GetMonitorInfo, MonitorFromPoint


IN  = 1
OPUT = 2
USER32 = ctypes.WinDLL('User32', use_last_error = True)


def main():
    process = AppProcess.get_process_by_name(name = 'Acrobat.exe')
    if process is not None:
        process.switch_to_this_window()

        monitor = GetMonitorInfo(
            hMonitor = MonitorFromPoint(
                x = 0, y = 0
            )
        )

        width, height = 1040, monitor.height - 40
        process.set_window_pos(
            hwnd_insert_after = 0,
            x = (monitor.width - width) // 2,
            y = (monitor.height - height) // 2,
            width = width, height = height,
            flags = win32con.SWP_NOZORDER
        )


class AppProcess(psutil.Process, pyvda.AppView):
    _Managers = Managers()

    @property
    def caption(self):
        text_len = self._get_window_text_length(self.hwnd) + 1
        text_buffer = ctypes.create_unicode_buffer(text_len)

        self._get_window_text(self.hwnd, text_buffer, text_len)
        return text_buffer.value

    def __init__(self, view: IApplicationView):
        pyvda.AppView.__init__(self, view = view)

        _, pid = self._get_pid()
        psutil.Process.__init__(self, pid = pid)

    def _get_pid(self) -> tuple[int, int]:
        pid = wintypes.DWORD()
        tid = self._get_window_thread_process_id(self.hwnd, ctypes.byref(pid))
        if tid == 0:
            raise ctypes.WinError(ctypes.get_last_error())
        return tid, pid.value

    def switch_to_this_window(self):
        self._switch_to_this_window(hwnd = self.hwnd, fUnknown = True)

    def set_window_pos(self, hwnd_insert_after: int, x: int, y: int, width: int, height: int, flags: int) -> bool:
        return self._set_window_pos(
            hWnd = self.hwnd,
            hWndInsertAfter = hwnd_insert_after,
            X = x, Y = y, cx = width, cy = height,
            uFlags = flags)

    def get_window_rect(self) -> tuple[int, int, int, int]:
        rect = wintypes.RECT()
        self._get_window_rect(self.hwnd, ctypes.byref(rect))

        return rect.left, rect.top, rect.right, rect.bottom

    @classmethod
    def get_processes(cls) -> list[AppProcess]:
        view_array = cls._Managers.view_collection.GetViewsByZOrder()  # type: ignore
        return [AppProcess(view = v) for v in view_array.iter(IApplicationView) if bool(v.GetShowInSwitchers())]

    @classmethod
    def get_processes_by_name(cls, name: str) -> list[AppProcess]:
        processes = []
        for process in cls.get_processes():
            if process.name() == name:
                processes.append(process)
        return processes

    @classmethod
    def get_process_by_name(cls, name: str) -> AppProcess | None:
        for process in cls.get_processes():
            if process.name() == name:
                return process
        return None

    @classmethod
    def get_process_by_caption(cls, caption: str, **kwargs: Any) -> AppProcess | None:
        def matches_criteria(process: AppProcess, attrib: str, value: object) -> bool:
            """Checks if a process attribute/method matches a value."""
            if hasattr(process, attrib):
                attr_value = getattr(process, attrib)
                if isinstance(attr_value, Callable):
                    return attr_value() == value
                else:
                    return attr_value == value
            return False

        for process in cls.get_processes():
            if caption in process.caption:
                if not kwargs or all(
                        matches_criteria(
                            process = process,
                            attrib = attrib,
                            value = value
                        ) for attrib, value in kwargs.items()
                ):
                    # Found a match
                    return process

        return None

    if TYPE_CHECKING:
        @staticmethod
        def _get_window_thread_process_id(hWnd: int, lpdwProcessId: Any) -> int: ...
        @staticmethod
        def _get_window_text(hWnd: int, lpString: ctypes.Array, nMaxCount: int) -> bool: ...
        @staticmethod
        def _get_window_text_length(hWnd: int) -> int: ...
        @staticmethod
        def _switch_to_this_window(hwnd: int, fUnknown: bool) -> None: ...
        @staticmethod
        def _set_window_pos(hWnd: int, hWndInsertAfter: int, X: int, Y: int, cx: int, cy: int, uFlags: int) -> bool: ...
        @staticmethod
        def _get_window_rect(hWnd: int, lpRect: wintypes.RECT) -> bool: ...

    else:
        _get_window_text = ctypes.WINFUNCTYPE(
            wintypes.BOOL,
            wintypes.HWND,
            wintypes.LPWSTR,
            wintypes.INT
        )(
            ('GetWindowTextW', USER32),
            (
                (IN, "hWnd"),
                (IN, "lpString"),
                (IN, "nMaxCount"),
            )
        )

        _get_window_text_length = ctypes.WINFUNCTYPE(
            wintypes.INT,
            wintypes.HWND
        )(
            ('GetWindowTextLengthW', USER32),
            (
                (IN, "hWnd"),
            )
        )

        _get_window_thread_process_id = ctypes.WINFUNCTYPE(
            wintypes.DWORD,
            wintypes.HWND,
            wintypes.LPDWORD
        )(
            ('GetWindowThreadProcessId', USER32),
            (
                (IN, "hWnd"),
                (IN, "lpdwProcessId"),
            )
        )

        _switch_to_this_window = ctypes.WINFUNCTYPE(
            None,
            wintypes.HWND,
            wintypes.BOOL
        )(
            ('SwitchToThisWindow', USER32),
            (
                (IN, "hwnd"),
                (IN, "fUnknown"),
            )
        )

        _set_window_pos = ctypes.WINFUNCTYPE(
            wintypes.BOOL,
            wintypes.HWND,
            wintypes.HWND,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            wintypes.UINT
        )(
            ('SetWindowPos', USER32),
            (
                (IN, "hWnd"),
                (IN, "hWndInsertAfter"),
                (IN, "X"),
                (IN, "Y"),
                (IN, "cx"),
                (IN, "cy"),
                (IN, "uFlags"),
            )
        )

        _get_window_rect = ctypes.WINFUNCTYPE(
            wintypes.BOOL,
            wintypes.HWND,
            wintypes.LPRECT
        )(
            ('GetWindowRect', USER32),
            (
                (IN, "hWnd"),
                (IN, "lpRect"),
            )
        )


if __name__ == '__main__':
    main()
