import pyvda
import pyvda.utils
import pyvda.com_defns
import psutil
import win32con

from skeletal_framework.win32_bindings.user32 import (
    GetWindowText,
    SetWindowPos,
    GetWindowThreadProcessId as GetPID,
    SwitchToThisWindow
)
from skeletal_framework.win32_bindings.monitor_info import GetMonitorInfo, MonitorFromPoint

MANAGERS = pyvda.utils.Managers()


class AppProcess(pyvda.AppView, psutil.Process):
    def __init__(self, view):
        pyvda.AppView.__init__(self, view = view)
        psutil.Process.__init__(self, pid = GetPID(hWnd = self.hwnd)[1])

    @property
    def caption(self) -> str:
        return GetWindowText(hWnd = self.hwnd)

    @classmethod
    def get_apps(cls) -> list[AppProcess]:
        views_arr = MANAGERS.view_collection.GetViewsByZOrder()

        result = []
        for view in views_arr.iter(pyvda.com_defns.IApplicationView):
            if view.GetShowInSwitchers():
                result.append(cls(view = view))

        return result


if __name__ == '__main__':
    for process in AppProcess.get_apps():
        if process.name() == 'Acrobat.exe':
            width, height = 1320, 1580

            monitor = GetMonitorInfo(
                hMonitor = MonitorFromPoint(
                    x = 0, y = 0
                )
            )

            SwitchToThisWindow(hwnd = process.hwnd, alt_tab = True)
            SetWindowPos(
                hWnd = process.hwnd,
                hWndInsertAfter = win32con.HWND_TOP,
                X = (monitor.width - width) // 2, Y = 10,
                cx = width, cy = height,
                uFlags = win32con.SWP_SHOWWINDOW
            )
            break
