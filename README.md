# Abstract Ctypes Interface

This project provides an abstract base class `AbstractDialogWindow` for creating Windows dialogs using `ctypes` and `user32.dll` calls directly.

## Usage

To create a window, inherit from `AbstractDialogWindow` and implement the required abstract methods.

### Class Name

You must define a `_class_name` for your window class. This string is used to register the window class with the OS.

```python
class MyDialog(AbstractDialogWindow):
    _class_name = 'MyUniqueDialogClass'
```

### Window Procedure (`wnd_proc`)

You must implement the `wnd_proc` method to handle window messages. It is crucial to handle `WM_DESTROY` to properly close the application loop.

Additionally, you should handle `WM_CREATE` to initialize the window geometry and create controls.

```python
    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_CREATE:
            self.invalidate_geometry()
            self.create_controls()
            return 0

        elif msg == win32con.WM_DESTROY:
            self.destroy()
            PostQuitMessage(0)
            return 0
        
        # ... handle other messages ...

        return DefWindowProc(hwnd, msg, wparam, lparam)
```

### Geometry and Sizing (`invalidate_geometry`)

The `invalidate_geometry` method is used to adjust the window size and position to ensure the client area matches the desired dimensions, accounting for window borders and decorations.

The `Client Rectangle` refers to the actual usable surface area inside the window borders and title bar. This is the canvas where your application draws its UI and places controls.

There is a 18x39 pixel offset between `GetWindowRect` and `GetClientRect`. This is due to a ~8px border shadowing around the window itself, and `GetWindowRect` will include this as part of the window.

If you create a window that is 400x160, the `GetClientRect` would be 382x121. So if you want to create a window that is 400x160 (client area), you'll have to set the width and the height in `CreateWindow` or `CreateWindowEx` to 418x199.

Calculations:
```
client_width = 400
client_height = 160

# Centering on monitor
(monitor_width - (client_width + 18)) // 2
(monitor_height - (client_height + 39)) // 2

# Window dimensions
client_width + 18, client_height + 39
```

The extra ~31px spacing from the top of the window is due to the size of the title bar. There isn't any shadowing around the top edge of the window itself.

```text
     ┌───────────────────────────────────────┐
     │               Title Bar               │ ← ~31 pixels tall
     ├───────────────────────────────────────┤   (GetWindowRect)
     │                                       │
     │                                       │
     │           Client  Rectangle           │
     │            (GetClientRect)            │
     │                                       │
~8px │                                       │ ~8px
   ← │                                       │ →
     └───────────────────────────────────────┘ 
    ↓ ~8px       border shadowing        ~8px ↓
                 (GetWindowRect)
```
