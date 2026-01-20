import ctypes
from typing import Dict, List

import win32api
import win32con
import win32gui
from PIL import Image

from wikipedia.core import *
from wikipedia.ui.controls import *
from wikipedia.win32 import *


class WikipediaSearchDialog:
    """Example window that demonstrates the RoundedComboBox class usage."""

    def __init__(self):
        # Track comboboxes, buttons, and image panels
        self.comboboxes: Dict[int, ComboBox] = {}
        self.tracked_buttons: Dict[int, Button] = {}
        self.image_panels: List[ImagePanel] = []

        self._data = DataStore()

        wc = win32gui.WNDCLASS()
        wc.lpszClassName = "ExampleWindow"
        wc.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        wc.hbrBackground = win32con.COLOR_BTNFACE + 1
        wc.lpfnWndProc = self.wnd_proc
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)

        self.atom = win32gui.RegisterClass(wc)

        monitor = GetMonitorInfo(
            hMonitor = MonitorFromPoint(
                x = 0,
                y = 0
            )
        )

        # There is a 18x39 pixel offset between GetWindowRect and GetClientRect.
        # This is due to a ~8px border shadowing around the window itself, and
        # GetWindowRect will include this as part of the window. If you create a
        # window that 400x160 the GetClientRect would be 382x121, so if you want
        # to create a window that is 400x160, you'll have to set the width and
        # the height in CreateWindow or CreateWindowEx to 418x199.
        #
        # client_width = 400
        # client_height = 160
        #
        # (monitor_width - client_width + 18) // 2
        # (monitor_height - client_height + 39) // 2
        #
        # client_width + 18, client_height + 39
        #
        # The extra ~31px spacing from the top of the window is due to the size
        # of the title bar. There isn't any shadowing around the top edge of the
        # window itself.
        #   ┌───────────────────────────────────────┐
        #   │               Title Bar               │ ← ~31 pixels tall
        #   ├───────────────────────────────────────┤   (GetWindowRect)
        #   │                                       │
        #   │                                       │
        #   │            Client Rectangle           │
        #   │            (GetClientRect)            │
        #   │                                       │
        #   │                                       │
        #   │                                       │
        # ← └───────────────────────────────────────┘ →
        #  ↓ ~8px       border shadowing        ~8px ↓
        #               (GetWindowRect)

        self._width = 400
        self._height = 160

        # Create the window
        self.hwnd = win32gui.CreateWindowEx(
            win32con.WS_EX_TOPMOST,
            self.atom,
            "Wikipedia.com",
            win32con.WS_SYSMENU,
            (monitor.width - self._width) // 2, (monitor.height - self._height) // 2,
            self._width, self._height,
            0, 0,
            win32gui.GetModuleHandle(None),
            None
        )
        left, top, right, bottom = win32gui.GetClientRect(self.hwnd)
        width = right - left
        height = bottom - top

        width_adjustment = self._width - width
        height_adjustment = self._height - height

        if width_adjustment > 0 or height_adjustment > 0:
            left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
            current_width = right - left
            current_height = bottom - top

            width = current_width + width_adjustment
            height = current_height + height_adjustment
            win32gui.SetWindowPos(
                self.hwnd,
                0,  # hWndInsertAfter (not changing z-order)
                (monitor.width - width) // 2, (monitor.height - height) // 2,
                width, height,
                win32con.SWP_NOZORDER
            )

        self.group_box = GroupBox(
            hwnd = self.hwnd,
            x = 10,
            y = 65,
            width = 380,
            height = 45,
            title = 'Wikipedia.com',
            title_padding = 30,
            corner_radius = 5,
            font_name = 'Helvetica',
            font_size = 10
        )

        # region ImagePanels
        image = Image.open(r"C:\Users\phpjunkie\Python\Scrapper\wikipedia\images\Wikipedia.png")
        # noinspection PyUnresolvedReferences
        self.image1 = ImagePanel(
            parent_hwnd = self.hwnd,
            rect = (3, 3, 50, 50),
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        )
        self.image_panels.append(self.image1)

        image_path = r"C:\Users\phpjunkie\Python\Scrapper\wikipedia\images\Wikipedia-logo.png"
        self.image2 = ImagePanel(
            parent_hwnd = self.hwnd,
            rect = ((self._width - 150) // 2, 3, 150, 50),
            image = image_path
        )
        self.image_panels.append(self.image2)

        self.image3 = ImagePanel(
            parent_hwnd = self.hwnd,
            rect = (347, 3, 50, 50),
            image = image
        )
        self.image_panels.append(self.image3)
        # endregion

        self.combo = ComboBox(self.hwnd, 100, 20, 75, 333, 200, corner_radius = 5)
        self.comboboxes[100] = self.combo
        # Add some example items
        self.combo.add_items(self._data.shows)

        self.button1 = Button(self.hwnd, 200, "X", 357, 76, 22, 22, corner_radius = 5)
        self.tracked_buttons[200] = self.button1

        self.button2 = Button(self.hwnd, 201, "Continue Scraping", (self._width - 160) // 2, 129, 160, 22, corner_radius = 5)
        self.tracked_buttons[201] = self.button2

        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)
        win32gui.UpdateWindow(self.hwnd)

    def wnd_proc(self, hwnd, message, wparam, lparam):
        """Window procedure to handle window messages."""
        if message == win32con.WM_DESTROY:
            self.destroy()

            win32gui.PostQuitMessage(0)
            return 0
        elif lparam == win32con.WM_LBUTTONUP:
            print('WM_LBUTTONUP')

        elif message == win32con.WM_NOTIFY:
            print('gfhdhdgnd')
        elif message == win32con.WM_DRAWITEM:
            item_struct: DRAWITEMSTRUCT = ctypes.cast(lparam, ctypes.POINTER(DRAWITEMSTRUCT)).contents
            if item_struct.CtlType == CtlType.ODT_COMBOBOX and item_struct.CtlID in self.comboboxes and item_struct.itemID != -1:
                self.draw_combobox_item(
                    dc_handle = item_struct.hDC,
                    rect = (item_struct.rcItem.left, item_struct.rcItem.top, item_struct.rcItem.right, item_struct.rcItem.bottom),
                    item_id = item_struct.itemID,
                    draw_item = item_struct
                )
                return True

            elif item_struct.CtlType == CtlType.ODT_BUTTON and item_struct.CtlID in self.tracked_buttons:
                self.tracked_buttons[item_struct.CtlID].draw(
                    dc_handle = item_struct.hDC,
                    rect = (item_struct.rcItem.left, item_struct.rcItem.top, item_struct.rcItem.right, item_struct.rcItem.bottom),
                    state = item_struct.itemState
                )
                return True

        elif message == win32con.WM_PAINT:
            # Begin painting
            hdc, ps = win32gui.BeginPaint(hwnd)

            # Get client area dimensions
            rect = win32gui.GetClientRect(hwnd)
            client_width = rect[2]
            client_height = rect[3]  # noqa

            # Create sunken area (full width x 50 height)
            self._draw_sunken_area(hdc, 0, 0, client_width, 54)
            self.group_box.draw(hdc)
            self._draw_footer(hdc)

            # End painting
            win32gui.EndPaint(hwnd, ps)
            return 0

        elif message == win32con.WM_COMMAND:
            control_id = win32api.LOWORD(wparam)
            notification_code = win32api.HIWORD(wparam)

            if control_id in self.comboboxes:
                if notification_code == win32con.CBN_SELCHANGE:
                    combo = self.comboboxes[control_id]
                    selected_text = combo.get_selected_text()
                    combo.set_text(selected_text)  # Update edit text to match selection

                    return 0
            elif control_id in self.tracked_buttons:
                if notification_code == win32con.BN_CLICKED:
                    if control_id == 200:
                        text = self.combo.get_text()
                        self.combo.set_text(text = '')
                        self.combo.remove_item(text = text)
                        self._data.remove_show(
                            show = text
                        )

                        return 0
                    elif control_id == 201:
                        text = self.combo.get_text()

                        if text:
                            index = self.combo.find_string_exact(text = text)
                            if index == win32con.CB_ERR:
                                self.combo.add_item(text = text)

                        self._data.show = text

                        self.destroy()
                        win32gui.PostQuitMessage(0)

                        return 0

        return win32gui.DefWindowProc(hwnd, message, wparam, lparam)

    def draw_combobox_item(self, dc_handle, rect, item_id, draw_item):
        """Draw a combobox list item."""
        combo_id = draw_item.CtlID
        combo = self.comboboxes[combo_id]
        hwnd_combo = draw_item.hwndItem

        # Get the item text
        buffer_size = win32gui.SendMessage(hwnd_combo, win32con.CB_GETLBTEXTLEN, item_id, 0) + 1
        buffer = ctypes.create_unicode_buffer(buffer_size)
        win32gui.SendMessage(hwnd_combo, win32con.CB_GETLBTEXT, item_id, buffer)
        text = buffer.value

        # Check if the item is selected
        is_selected = (draw_item.itemState & win32con.ODS_SELECTED) != 0

        # Set the colors based on selection state
        if is_selected:
            bg_color = win32api.RGB(200, 200, 200)  # Light gray for selected item
        else:
            bg_color = win32api.RGB(225, 225, 225)  # White for normal items

        # Create and select the brush for the background
        brush = win32gui.CreateSolidBrush(bg_color)
        win32gui.FillRect(dc_handle, rect, brush)
        win32gui.DeleteObject(brush)

        # Set text properties
        win32gui.SetTextColor(dc_handle, win32api.RGB(0, 0, 0))
        win32gui.SetBkMode(dc_handle, win32con.TRANSPARENT)

        # Create and select font
        hf = win32gui.CreateFontIndirect(combo.font)
        old_font = win32gui.SelectObject(dc_handle, hf)

        # Draw the text with padding
        text_rect = (rect[0] + 5, rect[1], rect[2], rect[3])
        win32gui.DrawText(
            dc_handle,
            text,
            -1,
            text_rect,
            win32con.DT_VCENTER | win32con.DT_SINGLELINE
        )

        # Cleanup
        win32gui.SelectObject(dc_handle, old_font)
        win32gui.DeleteObject(hf)

    @staticmethod
    def _draw_sunken_area(hdc, x, y, width, height):
        """Draw a sunken area with white background and double-width border."""
        # Draw the white background of the sunken area
        white_brush = win32gui.CreateSolidBrush(win32api.RGB(255, 255, 255))
        win32gui.FillRect(hdc, (x, y, x + width, y + height), white_brush)
        win32gui.DeleteObject(white_brush)
        std_shadow_color = win32api.GetSysColor(win32con.COLOR_3DSHADOW)
        std_highlight_color = win32api.GetSysColor(win32con.COLOR_3DHIGHLIGHT)

        r = std_highlight_color & 0xFF
        g = (std_highlight_color >> 8) & 0xFF
        b = (std_highlight_color >> 16) & 0xFF

        r = max(0, int(r * 0.90))
        g = max(0, int(g * 0.90))
        b = max(0, int(b * 0.90))

        darker_highlight_color = win32api.RGB(r, g, b)

        # Create pens for drawing the edges
        dark_pen = win32gui.CreatePen(win32con.PS_SOLID, 2, std_shadow_color)
        light_pen = win32gui.CreatePen(win32con.PS_SOLID, 2, darker_highlight_color)
        light_pen2 = win32gui.CreatePen(win32con.PS_SOLID, 2, std_highlight_color)

        # Select dark pen for top and left edges
        old_pen = win32gui.SelectObject(hdc, dark_pen)

        # Draw top edge (double width)
        win32gui.MoveToEx(hdc, x, y)
        win32gui.LineTo(hdc, x + width - 1, y)

        # Draw second line for top edge
        win32gui.MoveToEx(hdc, x, y + 1)
        win32gui.LineTo(hdc, x + width - 1, y + 1)

        # Draw left edge (double width)
        win32gui.MoveToEx(hdc, x, y)
        win32gui.LineTo(hdc, x, y + height - 1)

        # Draw second line for left edge
        win32gui.MoveToEx(hdc, x + 1, y)
        win32gui.LineTo(hdc, x + 1, y + height - 1)

        # Switch to light pen for bottom and right edges
        win32gui.SelectObject(hdc, light_pen)
        win32gui.MoveToEx(hdc, x, y + height - 1)
        win32gui.LineTo(hdc, x + width, y + height - 1)

        win32gui.MoveToEx(hdc, x + width - 1, y)
        win32gui.LineTo(hdc, x + width - 1, y + height - 1)

        win32gui.SelectObject(hdc, light_pen2)
        win32gui.MoveToEx(hdc, x, y + height - 2)
        win32gui.LineTo(hdc, x + width, y + height - 2)

        win32gui.MoveToEx(hdc, x + width - 2, y)
        win32gui.LineTo(hdc, x + width - 2, y + height - 1)

        # Restore original pen
        win32gui.SelectObject(hdc, old_pen)

        # Cleanup
        win32gui.DeleteObject(dark_pen)
        win32gui.DeleteObject(light_pen)
        win32gui.DeleteObject(light_pen2)

    def _draw_footer(self, hdc):
        bg_color = win32api.GetSysColor(win32con.COLOR_BTNFACE)

        r = bg_color & 0xFF
        g = (bg_color >> 8) & 0xFF
        b = (bg_color >> 16) & 0xFF

        r = max(0, int(r * 0.90))
        g = max(0, int(g * 0.90))
        b = max(0, int(b * 0.90))

        bg_color = win32api.RGB(r, g, b)
        bg_brush = win32gui.CreateSolidBrush(bg_color)

        # Get client rectangle width from the window
        client_rect = win32gui.GetClientRect(self.hwnd)
        client_width = client_rect[2]

        # Fill rect expects (left, top, right, bottom) coordinates
        # Not (left, top, width, height)
        win32gui.FillRect(hdc, (0, 120, client_width, self._height), bg_brush)

        win32gui.DeleteObject(bg_brush)

    def destroy(self):
        """Destroy the dialog and clean up all resources."""
        if self.hwnd:
            # Cleanup comboboxes
            for combo in self.comboboxes.values():
                combo.destroy()

            # Cleanup buttons
            for button in self.tracked_buttons.values():
                button.destroy()

            # Cleanup image panels
            for panel in self.image_panels:
                panel.destroy()

            # Clean up group box (doesn't have a destroy method typically)
            # If the group box has any resources that need cleanup, handle them here

            # Destroy the window
            win32gui.DestroyWindow(self.hwnd)

            try:
                win32gui.UnregisterClass(self.atom, win32gui.GetModuleHandle(None))
            except:  # noqa
                pass

            # Clear the window handle
            self.hwnd = None

    @staticmethod
    def mainloop() -> None:
        """Run the window message loop."""
        while (msg := win32gui.GetMessage(None, 0, 0))[0] > 0:
            win32gui.TranslateMessage(msg[1])
            win32gui.DispatchMessage(msg[1])


# Example usage
if __name__ == "__main__":
    demo = WikipediaSearchDialog()
    demo.mainloop()
    print(DataStore().show)
