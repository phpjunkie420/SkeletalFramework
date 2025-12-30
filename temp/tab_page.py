import ctypes
import inspect
from abc import ABC, abstractmethod
from ctypes import wintypes
from typing import Optional, cast

import commctrl
import win32con

from core.core_context import CoreContext
from ui.controls.button import Button
from ui.controls.checkbox import *
from ui.controls.control import DrawItemEvent, DrawListViewItemEvent, DrawPaintEvent
from ui.controls.listview_icon_items import DesktopIconItem
from ui.controls.groupbox import GroupBox
from ui.controls.listview import *
from ui.dispatcher import dispatcher
from win32 import *

__all__ = ['TabPage', 'DesktopSettings', 'DriveSettings']

int_constants = {
    key: value for key, value in inspect.getmembers(commctrl)
    if isinstance(value, int) and (key.startswith('LVN_') or key.startswith('NM_'))
}

commctrl_constants = {}
for key, value in int_constants.items():
    if value not in commctrl_constants:
        commctrl_constants[value] = []
    commctrl_constants[value].append(key)

commctrl_constants = {key: ', '.join(value) for key, value in commctrl_constants.items()}


class TabPage(ABC):
    _class_registered = False
    _class_name = "TabPageClass"

    @property
    def context(self):
        return self._context

    @property
    def hwnd(self):
        return self._hwnd

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def desktop_listview(self):
        return self._desktop_listview

    @desktop_listview.setter
    def desktop_listview(self, value):
        self._desktop_listview = value

    @property
    def drive_listview(self):
        return self._drive_listview

    @drive_listview.setter
    def drive_listview(self, value):
        self._drive_listview = value

    def __init__(self, x: int, y: int, width: int, height: int):
        self._context = CoreContext()

        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._desktop_listview: Optional[ListView] = None
        self._drive_listview: Optional[ListView] = None

        if not self._class_registered:
            self._register_window_class(
                h_instance = self._context.h_instance
            )

        # Create the window for this tab page
        self._hwnd = CreateWindowEx(
            dwExStyle = 0,
            lpClassName = self._class_name, lpWindowName = "",
            dwStyle = win32con.WS_CHILD | win32con.WS_VISIBLE | win32con.WS_CLIPCHILDREN,
            x = x, y = y, nWidth = width, nHeight = height,
            hWndParent = self._context.main_window,
            hMenu = None,
            hInstance = self._context.h_instance,
            lpParam = id(self)  # Pass the "self" reference for dispatcher
        )

        self._create_controls()

    @abstractmethod
    def _create_controls(self): ...

    @abstractmethod
    def wnd_proc(self, hwnd, msg, wparam, lparam): ...

    @classmethod
    def _register_window_class(cls, h_instance):
        RegisterClassEx(
            ctypes.byref(
                WNDCLASSEX(
                    style = win32con.CS_HREDRAW | win32con.CS_VREDRAW,
                    lpfnWndProc = dispatcher,  # Dispatcher function
                    hInstance = h_instance,
                    hCursor = LoadCursor(0, win32con.IDC_ARROW),
                    hbrBackground = GetSysColorBrush(win32con.COLOR_BTNFACE),
                    lpszClassName = cls._class_name
                )
            )
        )

        cls._class_registered = True

    def destroy(self):
        pass


class DesktopSettings(TabPage):
    def __init__(self, x, y, width, height):
        self.choose_icon_button: Optional[Button] = None
        self.restore_default_button: Optional[Button] = None

        super(DesktopSettings, self).__init__(
            x, y, width, height
        )

    def _update_button_states(self):
        """Enables or disables the action buttons based on ListView selection."""
        selected_item = bool(self.desktop_listview and self.desktop_listview.selected_item)

        if self.choose_icon_button and self.choose_icon_button.hwnd:
            self.choose_icon_button.is_enabled = selected_item

        if self.restore_default_button and self.restore_default_button.hwnd:
            item = cast(DesktopIconItem, self.desktop_listview.selected_item)
            self.restore_default_button.is_enabled = (
                    selected_item and not item.defaulted
            )

    def _create_controls(self):
        group_box = GroupBox(
            parent_hwnd = self.hwnd,
            x = 10,
            y = 20,
            width = self.width - 20,
            height = 50,
            title = 'Desktop Icons',
            title_padding = 30,
            corner_radius = 5,
            font_name = 'Microsoft Sans Serif',
            font_size = 10
        )
        self.context.controls[group_box.hwnd] = group_box

        ShowComputerIcon()
        ShowUserFolderIcon()
        ShowNetworkIcon()
        ShowRecycleBinIcon()

        rect = wintypes.RECT()
        GetClientRect(self.hwnd, ctypes.byref(rect))

        width = rect.right - rect.left - 20
        height = rect.bottom - rect.top - 130

        self.desktop_listview = DesktopListView(
            parent_hwnd = self._hwnd,
            ctrl_id = 100,
            x = 10, y = 80,
            width = width, height = height
        )

        ThemeChangesDesktopIcons()
        ThemeChangesMousePointers()

        self.choose_icon_button = Button(
            parent_hwnd = self._hwnd,
            ctrl_id = 200,
            text = 'Choose Icon ...',
            font_name = 'Microsoft Sans Serif',
            font_size = 9,
            x = 10, y = 415, width = width // 2 - 2, height = 23,
            enabled = False
        )

        self.restore_default_button = Button(
            parent_hwnd = self._hwnd,
            ctrl_id = 201,
            text = 'Restore Default',
            font_name = 'Microsoft Sans Serif',
            font_size = 9,
            x = width // 2 + 12, y = 415, width = width // 2 - 2, height = 23,
            enabled = False
        )

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_NCCREATE:
            cs = ctypes.cast(lparam, ctypes.POINTER(CREATESTRUCT)).contents
            instance = ctypes.cast(cs.lpCreateParams, ctypes.py_object).value
            if isinstance(instance, TabPage):
                self._context.set(
                    key = 'desktop_settings',
                    value = hwnd
                )

        elif msg == win32con.WM_DRAWITEM:
            dis: DRAWITEMSTRUCT = ctypes.cast(lparam, ctypes.POINTER(DRAWITEMSTRUCT)).contents
            if dis.CtlType == win32con.ODT_BUTTON and dis.CtlID in self._context.controls:
                ctrl = self._context.controls[dis.CtlID]
                ctrl.draw_control(
                    DrawItemEvent(
                        hdc = dis.hDC,
                        rect = dis.rcItem,
                        state = dis.itemState
                    )
                )
                return True

        elif msg == win32con.WM_PAINT:
            if hwnd in self._context.controls:
                ctrl = self._context.controls[hwnd]
                ctrl.draw_control(
                    DrawPaintEvent(
                        hwnd = hwnd
                    )
                )
                return 0

        elif msg == win32con.WM_NOTIFY:
            nmhdr = ctypes.cast(lparam, ctypes.POINTER(NMHDR)).contents
            if nmhdr.idFrom in self._context.controls:
                ctrl = self._context.controls[nmhdr.idFrom]
                if nmhdr.hwndFrom == ctrl.hwnd:
                    cd: NMLVCUSTOMDRAW = ctypes.cast(lparam, ctypes.POINTER(NMLVCUSTOMDRAW)).contents
                    nmlv: NMLISTVIEW = ctypes.cast(lparam, ctypes.POINTER(NMLISTVIEW)).contents
                    nmcd = cd.nmcd

                    if nmhdr.code == commctrl.NM_CUSTOMDRAW:
                        return ctrl.draw_control(
                            DrawListViewItemEvent(
                                hdc = nmcd.hdc,
                                draw_stage = nmcd.dwDrawStage,
                                item_spec = nmcd.dwItemSpec,
                                item_state = nmcd.uItemState,
                                rect = nmcd.rc
                            )
                        )

                    elif nmhdr.code == commctrl.LVN_ITEMCHANGED:
                        is_selected = (nmlv.uNewState & commctrl.LVIS_SELECTED) != 0
                        was_selected = (nmlv.uOldState & commctrl.LVIS_SELECTED) != 0

                        if is_selected != was_selected:
                            if is_selected:
                                self.desktop_listview.selected_index = nmlv.iItem
                            else:
                                self.desktop_listview.selected_index = -1

                            self._update_button_states()
                        return 0

                    elif nmhdr.code == commctrl.NM_DBLCLK:
                        from ui.dialogs.select_icon_dialog import SelectIconDialog

                        index = self.desktop_listview.selected_index
                        item = self.desktop_listview.items[index]
                        dialog = SelectIconDialog(
                            parent_hwnd = self._hwnd,
                            selected_path = item.icon_location
                        )
                        if dialog == win32con.IDOK:
                            item.icon_location = dialog.result
                            self.desktop_listview.update_item_icon(index)

                        return 0

        elif msg == win32con.WM_COMMAND:
            ctrl_id = loword(wparam)
            # noinspection PyUnusedLocal
            notification_code = hiword(wparam)

            if ctrl_id in self._context.controls:
                ctrl = self._context.controls[ctrl_id]
                if isinstance(ctrl, Button):
                    if ctrl_id == 200:
                        from ui.dialogs.select_icon_dialog import SelectIconDialog
                        index = SendMessage(
                            self._hwnd,
                            commctrl.LVM_GETNEXTITEM,
                            -1,  # Start search from the beginning
                            commctrl.LVNI_SELECTED
                        )
                        item = self.desktop_listview.items[index]
                        dialog = SelectIconDialog(
                            parent_hwnd = self._hwnd,
                            selected_path = item.icon_location
                        )
                        if dialog == win32con.IDOK:
                            item.icon_location = dialog.result
                            self.desktop_listview.update_item_icon(index)
                    elif ctrl_id == 201:
                        pass

        elif msg == win32con.WM_DESTROY:
            PostQuitMessage(0)
            return 0

        return DefWindowProc(hwnd, msg, wparam, lparam)


class DriveSettings(TabPage):
    def __init__(self, x, y, width, height):
        super(DriveSettings, self).__init__(
            x, y, width, height
        )

    def _create_controls(self):
        rect = wintypes.RECT()
        GetClientRect(self._hwnd, ctypes.byref(rect))

        width = rect.right - rect.left - 20
        height = rect.bottom - rect.top - 43

        self._drive_listview = DriveListView(
            parent_hwnd = self._hwnd,
            ctrl_id = 101,
            x = 10,
            y = 10,
            width = width,
            height = height
        )

        Button(
            parent_hwnd = self._hwnd,
            ctrl_id = 202,
            text = 'Assign a New Icon',
            weight = win32con.FW_NORMAL,
            font_name = 'Microsoft Sans Serif',
            font_size = 9,
            x = 10, y = height + 15, width = width // 3 - 2, height = 23,
            corner_radius = 5
        )

        Button(
            parent_hwnd = self._hwnd,
            ctrl_id = 203,
            text = 'Change Selected Icon',
            weight = win32con.FW_NORMAL,
            font_name = 'Microsoft Sans Serif',
            font_size = 9,
            x = (width // 3) + 12, y = height + 15, width = width // 3 - 2, height = 23,
            corner_radius = 5
        )

        Button(
            parent_hwnd = self._hwnd,
            ctrl_id = 204,
            text = 'Remove Selected Icon',
            weight = win32con.FW_NORMAL,
            font_name = 'Microsoft Sans Serif',
            font_size = 9,
            x = (width // 3) * 2 + 14, y = height + 15, width = width // 3 - 2, height = 23,
            corner_radius = 5
        )

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_DRAWITEM:
            dis: DRAWITEMSTRUCT = ctypes.cast(lparam, ctypes.POINTER(DRAWITEMSTRUCT)).contents
            if dis.CtlType == win32con.ODT_BUTTON and dis.CtlID in self._context.controls:
                ctrl = self._context.controls[dis.CtlID]
                ctrl.draw_control(
                    DrawItemEvent(
                        hdc = dis.hDC,
                        rect = dis.rcItem,
                        state = dis.itemState
                    )
                )
                return True

        elif msg == win32con.WM_PAINT:
            if hwnd in self._context.controls:
                ctrl = self._context.controls[hwnd]
                ctrl.draw_control(
                    DrawPaintEvent(
                        hwnd = hwnd
                    )
                )
                return 0

        elif msg == win32con.WM_NOTIFY:
            nmhdr = ctypes.cast(lparam, ctypes.POINTER(NMHDR)).contents
            if nmhdr.idFrom in self._context.controls:
                ctrl = self._context.controls[nmhdr.idFrom]
                if nmhdr.hwndFrom == ctrl.hwnd:
                    cd: NMLVCUSTOMDRAW = ctypes.cast(lparam, ctypes.POINTER(NMLVCUSTOMDRAW)).contents
                    nmlv: NMLISTVIEW = ctypes.cast(lparam, ctypes.POINTER(NMLISTVIEW)).contents
                    nmcd = cd.nmcd

                    if nmhdr.code == commctrl.NM_CUSTOMDRAW:
                        return ctrl.draw_control(
                            DrawListViewItemEvent(
                                hdc = nmcd.hdc,
                                draw_stage = nmcd.dwDrawStage,
                                item_spec = nmcd.dwItemSpec,
                                item_state = nmcd.uItemState,
                                rect = nmcd.rc
                            )
                        )

                    elif nmhdr.code == commctrl.LVN_ITEMCHANGED:
                        is_selected = (nmlv.uNewState & commctrl.LVIS_SELECTED) != 0
                        was_selected = (nmlv.uOldState & commctrl.LVIS_SELECTED) != 0

                        if is_selected != was_selected:
                            if is_selected:
                                self.drive_listview.selected_index = nmlv.iItem
                            else:
                                self.drive_listview.selected_index = -1
                        return 0

                    elif nmhdr.code == commctrl.NM_DBLCLK:
                        from ui.dialogs.select_icon_dialog import SelectIconDialog

                        index = self.drive_listview.selected_index
                        item = self.drive_listview.items[index]
                        print(index)
                        # dialog = SelectIconDialog(
                        #     parent_hwnd = self._hwnd,
                        #     selected_path = item.icon_location
                        # )
                        # if dialog == win32con.IDOK:
                        #     item.icon_location = dialog.result
                        #     self.desktop_listview.update_item_icon(index)

                        return 0

        elif msg == win32con.WM_COMMAND:
            ctrl_id = loword(wparam)
            # noinspection PyUnusedLocal
            notification_code = hiword(wparam)

            if ctrl_id in self._context.controls:
                ctrl = self._context.controls[ctrl_id]

        elif msg == win32con.WM_DESTROY:
            PostQuitMessage(0)
            return 0

        return DefWindowProc(hwnd, msg, wparam, lparam)
