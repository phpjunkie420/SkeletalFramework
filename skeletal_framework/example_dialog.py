import ctypes
from ctypes import wintypes

import win32con

from abstract_window import AbstractDialogWindow
from win32_bindings.gdi32 import CreateSolidBrush, DeleteObject, SetBkColor, SetTextColor
from win32_bindings.user32 import CreateWindowEx, DefWindowProc, PostQuitMessage
from win32_bindings.uxtheme import SetWindowTheme


class ExampleDialog(AbstractDialogWindow):
    def __init__(self):
        super(ExampleDialog, self).__init__(
            window_name = 'Example Dialog',
            width = 800, height = 600,
            # dark_mode = True
        )
        self._hbr_edit_background = CreateSolidBrush(wintypes.RGB(255, 255, 255))

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_NCCREATE:
            self._hwnd = hwnd

        elif msg == win32con.WM_CREATE:
            self.invalidate_geometry()
            self.create_controls()
            return 0

        elif msg == win32con.WM_CTLCOLORSTATIC:
            hdc = wparam
            # Set text color to white
            SetTextColor(hdc, wintypes.RGB(200, 0, 0))
            # Set background color of the text to dark gray
            SetBkColor(hdc, wintypes.RGB(255, 255, 255))
            # Return the brush handle for the control background
            return self._hbr_edit_background

        elif msg == win32con.WM_CLOSE:
            pass

        elif msg == win32con.WM_DESTROY:
            self.destroy()
            PostQuitMessage(0)
            return 0

        return DefWindowProc(hwnd, msg, wparam, lparam)

    def create_controls(self):
        hwnd_edit = CreateWindowEx(
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

    def destroy(self):
        try:
            DeleteObject(self._hbr_edit_background)
        except OSError:
            pass

        super(ExampleDialog, self).destroy()


if __name__ == '__main__':
    dialog = ExampleDialog()
    dialog.show_window()
