import ctypes
from ctypes import wintypes
from typing import TYPE_CHECKING

import psutil
import pyvda
from pyvda.com_defns import IApplicationView
from pyvda.utils import Managers

IN = 1


def main():
    # 2. Check for the method using dir() (which sees inheritance)
    print(f"Does Progress have __rich_console__? {'__rich_console__' in dir(AppProcess)}")

    # 3. Find out WHO actually defined it
    # We iterate over the Method Resolution Order (MRO) to find the parent
    print("\n--- Who defined it for Progress? ---")


class AppProcess(psutil.Process, pyvda.AppView):
    _USER32 = ctypes.WinDLL('user32', use_last_error = True)
    _Managers = Managers()

    def __init__(self, view):
        pyvda.AppView.__init__(self, view = view)
        psutil.Process.__init__(self, pid = self._get_pid())

    def _get_pid(self) -> int:
        pid = wintypes.DWORD()
        tid = self._get_window_thread_process_id(self.hwnd, ctypes.byref(pid))
        if tid == 0:
            raise ctypes.WinError(ctypes.get_last_error())
        return pid.value

    @classmethod
    def get_processes(cls) -> list[AppProcess]:
        view_array = _Managers.view_collection.GetViewsByZOrder()  # type: ignore
        return [AppProcess(view = v) for v in view_array.iter(IApplicationView) if bool(v.GetShowInSwitchers())]

    if TYPE_CHECKING:
        @staticmethod
        def _get_window_thread_process_id(hWnd: int, lpdwProcessId: Any) -> int: ...
        @staticmethod
        def _get_window_text(hWnd: int, lpString: ctypes.Array, nMaxCount: int) -> bool: ...
        @staticmethod
        def _get_window_text_length(hWnd: int) -> int: ...

    else:
        _get_window_text = ctypes.WINFUNCTYPE(
            wintypes.BOOL,
            wintypes.HWND,
            wintypes.LPWSTR,
            wintypes.INT
        )(
            ('GetWindowTextW', _USER32),
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
            ('GetWindowTextLengthW', _USER32),
            (
                (IN, "hWnd"),
            )
        )

        _get_window_thread_process_id = ctypes.WINFUNCTYPE(
            wintypes.DWORD,
            wintypes.HWND,
            wintypes.LPDWORD
        )(
            ('GetWindowThreadProcessId', _USER32),
            (
                (IN, "hWnd"),
                (IN, "lpdwProcessId"),
            )
        )
