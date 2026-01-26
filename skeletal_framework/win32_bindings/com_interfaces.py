import ctypes
from ctypes import wintypes
from enum import IntFlag
from typing import TYPE_CHECKING

from comtypes import IUnknown, GUID, COMMETHOD, HRESULT

if TYPE_CHECKING:
    # --- Static Analysis & Type Stubs ---
    # These definitions exist solely to assist IDE autocomplete.
    # They are guarded by TYPE_CHECKING so they are never loaded at runtime.

    # Aliases for clarity in method signatures
    HWND = int
    BOOL = bool
    HICON = int
    HIMAGELIST = int
    RECT = ctypes.Structure

# Searched for CLSID_TaskbarList in "C:\Program Files (x86)\Windows Kits\10\Include\10.0.26100.0\um\shobjidl_core.h"
CLSID_TaskbarList = GUID("{56FDF344-FD6D-11D0-958A-006097C9A090}")


# https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nf-shobjidl_core-itaskbarlist3-setprogressstate
# Taskbar Progress Flags (TBPF)
# TBPF_NOPROGRESS (0x00000000)
# TBPF_INDETERMINATE (0x00000001)
# TBPF_NORMAL (0x00000002)
# TBPF_ERROR (0x00000004)
# TBPF_PAUSED (0x00000008)
class TaskbarState(IntFlag):
    NOPROGRESS     = 0x00
    INDETERMINATE  = 0x01  # Binary 00001
    NORMAL         = 0x02  # Binary 00010
    ERROR          = 0x04  # Binary 00100
    PAUSED         = 0x08  # Binary 01000


# https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nn-shobjidl_core-itaskbarlist
class ITaskbarList(IUnknown):
    # Searched for IID_ITaskbarList in "C:\Program Files (x86)\Windows Kits\10\Include\10.0.26100.0\um\shobjidl_core.h"
    _iid_ = GUID("{56FDF342-FD6D-11D0-958A-006097C9A090}")
    _methods_ = [
        # https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nf-shobjidl_core-itaskbarlist-hrinit
        # HRESULT HrInit();
        COMMETHOD([], HRESULT, "HrInit"),
        # https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nf-shobjidl_core-itaskbarlist-addtab
        # HRESULT AddTab(
        #   HWND hwnd
        # );
        COMMETHOD([], HRESULT, "AddTab", (['in'], wintypes.HWND, "hwnd")),
        # https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nf-shobjidl_core-itaskbarlist-deletetab
        # HRESULT DeleteTab(
        #   HWND hwnd
        # );
        COMMETHOD([], HRESULT, "DeleteTab", (['in'], wintypes.HWND, "hwnd")),
        # https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nf-shobjidl_core-itaskbarlist-activatetab
        # HRESULT ActivateTab(
        #   HWND hwnd
        # );
        COMMETHOD([], HRESULT, "ActivateTab", (['in'], wintypes.HWND, "hwnd")),
        # https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nf-shobjidl_core-itaskbarlist-setactivealt
        # HRESULT SetActiveAlt(
        #   HWND hwnd
        # );
        COMMETHOD([], HRESULT, "SetActiveAlt", (['in'], wintypes.HWND, "hwnd")),
    ]

    if TYPE_CHECKING:
        # --- Static Analysis & Type Stubs ---
        # These definitions exist solely to assist IDE autocomplete.
        # They are guarded by TYPE_CHECKING so they are never loaded at runtime.

        def HrInit(self) -> int:
            """
            Initializes the taskbar list object.
            This method must be called before any other methods are called.
            """
            ...

        def AddTab(self, hwnd: HWND) -> int:
            """
            Adds an item to the taskbar.
            :param hwnd: A handle to the window to be added to the taskbar.
            """
            ...

        def DeleteTab(self, hwnd: HWND) -> int:
            """
            Deletes an item from the taskbar.
            :param hwnd: A handle to the window to be deleted from the taskbar.
            """
            ...

        def ActivateTab(self, hwnd: HWND) -> int:
            """
            Activates an item on the taskbar. The window is not actually activated;
            the window's item on the taskbar is merely displayed as active.
            :param hwnd: A handle to the window to be displayed as active.
            """
            ...

        def SetActiveAlt(self, hwnd: HWND) -> int:
            """
            Marks the specified tab as the active tab.
            :param hwnd: A handle to the window to be marked as active.
            """
            ...


# https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nn-shobjidl_core-itaskbarlist2
class ITaskbarList2(ITaskbarList):
    # Searched for IID_ITaskbarList2 in "C:\Program Files (x86)\Windows Kits\10\Include\10.0.26100.0\um\shobjidl_core.h"
    _iid_ = GUID("{602D4995-B13A-429B-A66E-1935E44F4317}")
    _methods_ = [
        # https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nf-shobjidl_core-itaskbarlist2-markfullscreenwindow
        # HRESULT MarkFullscreenWindow(
        #   [in] HWND hwnd,
        #   [in] BOOL fFullscreen
        # );
        COMMETHOD(
            [], HRESULT, "MarkFullscreenWindow",
            (['in'], wintypes.HWND, "hwnd"),
            (['in'], wintypes.BOOL, "fFullscreen")
        ),
    ]

    if TYPE_CHECKING:
        # --- Static Analysis & Type Stubs ---
        # These definitions exist solely to assist IDE autocomplete.
        # They are guarded by TYPE_CHECKING so they are never loaded at runtime.

        def MarkFullscreenWindow(self, hwnd: HWND, fFullscreen: BOOL) -> int:
            """
            Marks a window as full-screen.
            :param hwnd: The handle of the window to be marked.
            :param fFullscreen: A Boolean value that marks the window as full-screen (True) or not (False).
            """
            ...


# https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nn-shobjidl_core-itaskbarlist3
class ITaskbarList3(ITaskbarList2):
    # Searched for IID_ITaskbarList3 in "C:\Program Files (x86)\Windows Kits\10\Include\10.0.26100.0\um\shobjidl_core.h"
    _iid_ = GUID("{EA1AFB91-9E28-4B86-90E9-9E9F8A5EEFAF}")
    _methods_ = [
        # https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nf-shobjidl_core-itaskbarlist3-setprogressvalue
        # HRESULT SetProgressValue(
        #   [in] HWND      hwnd,
        #   [in] ULONGLONG ullCompleted,
        #   [in] ULONGLONG ullTotal
        # );
        COMMETHOD(
            [], HRESULT, "SetProgressValue",
            (['in'], wintypes.HWND, "hwnd"),
            (['in'], ctypes.c_ulonglong, "ullCompleted"),
            (['in'], ctypes.c_ulonglong, "ullTotal")
        ),
        # https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nf-shobjidl_core-itaskbarlist3-setprogressstate
        # HRESULT SetProgressState(
        #   [in] HWND    hwnd,
        #   [in] TBPFLAG tbpFlags
        # );
        COMMETHOD(
            [], HRESULT, "SetProgressState",
            (['in'], wintypes.HWND, "hwnd"),
            (['in'], ctypes.c_int, "tbpFlags")
        ),
        # There are many more methods in List3, but we only need these two for now.
        # Since comtypes builds the VTable sequentially, as long as we only use
        # the methods we define, we don't strictly need to define the rest
        # (unlike ctypes where padding matters).
    ]

    if TYPE_CHECKING:
        # --- Static Analysis & Type Stubs ---
        # These definitions exist solely to assist IDE autocomplete.
        # They are guarded by TYPE_CHECKING so they are never loaded at runtime.

        def SetProgressValue(self, hwnd: HWND, ullCompleted: int, ullTotal: int) -> int:
            """
            Sets the progress bar value.
            :param hwnd: The handle of the window.
            :param ullCompleted: The completed progress (numerator).
            :param ullTotal: The total progress (denominator).
            """
            ...

        def SetProgressState(self, hwnd: HWND, tbpFlags: int) -> int:
            """
            Sets the progress bar state (Normal, Error, Paused, etc.).
            """
            ...


# --- PURELY FOR TESTING THE COM INTERFACE ---
if __name__ == '__main__':
    # !!! IMPORTANT ! READ THIS ! IMPORTANT !!!
    """
    For the PyCharm console output to work with this the run configuration
    needs to be change to emulate the terminal in the output console.

    From the "Run" widget drop down box . . .
    Choose "Current File" to select the current file (this file).
    Choose: Edit Configuration
    
    The "Run/Debug Configuration" dialog box will open . . .
    In the bottom left corner of the dialog click: Edit configuration templates...

    The "Run/Debug Configuration Templates" dialog box will open . . .
    
    Choose Python from the list on the left.
    In the upper right part of the dialog click: Modify Options
    In the context menu choose: Emulate terminal in output console.
    Click "Apply"
    Click "Close" to close the dialog.
    
    In the "Run/Debug Configuration" dialog click "Cancel"
    
    From the "Run" widget click the green play button . . .
    """

    # --- IMPORTS ---
    import sys
    import time
    from psutil import Process, NoSuchProcess
    from pyvda import get_apps_by_z_order

    from comtypes.client import CreateObject

    # --- WINDOWS API BINDINGS ---
    user32 = ctypes.WinDLL('user32', use_last_error = True)
    kernel32 = ctypes.WinDLL('kernel32', use_last_error = True)

    GetWindowTextW = user32.GetWindowTextW
    GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, wintypes.INT]
    GetWindowTextW.restype = wintypes.BOOL

    GetWindowTextLengthW = user32.GetWindowTextLengthW
    GetWindowTextLengthW.argtypes = [wintypes.HWND]
    GetWindowTextLengthW.restype = wintypes.INT

    GetWindowThreadProcessId = user32.GetWindowThreadProcessId
    GetWindowThreadProcessId.argtypes = [wintypes.HWND, wintypes.LPDWORD]
    GetWindowThreadProcessId.restype = wintypes.DWORD

    GetConsoleWindow = kernel32.GetConsoleWindow
    GetConsoleWindow.restype = wintypes.HWND
    GetConsoleWindow.argtypes = []

    # --- THE TASKBAR CLASS IMPLEMENTING THE COM INTERFACE ---
    class TaskbarProgress:
        """
        A wrapper class that simplifies the ITaskbarList3 COM interface.

        It automatically locates the parent terminal window (PyCharm, Windows Terminal,
        or CMD) to ensure the progress bar attaches to the correct window handle (HWND).

        COM Interface Mapping:
        ----------------------
        This class wraps the following ITaskbarList3 primitives:

        * `__init__` -> `CoCreateInstance(CLSID_TaskbarList)` & `HrInit()`
            Initializes the COM object and the taskbar interface.

        * `set_progress_state` -> `SetProgressState(hwnd, flags)`
            Controls the state (Normal, Paused, Error, Indeterminate).

        * `set_progress_value` -> `SetProgressValue(hwnd, current, total)`
            Updates the actual progress bar position.
        """

        def __init__(self, hwnd: int):
            self.hwnd = hwnd

            self._taskbar = CreateObject(CLSID_TaskbarList, interface = ITaskbarList3)
            self._taskbar.HrInit()

        def __enter__(self) -> TaskbarProgress:
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            try:
                self.set_progress_state(TaskbarState.NOPROGRESS)
            except Exception:
                pass

        def set_progress_state(self, flags: int):
            if flags & (TaskbarState.PAUSED | TaskbarState.ERROR):
                self.set_progress_value(progress = 100)

            self._taskbar.SetProgressState(self.hwnd, flags)

        def set_progress_value(self, progress: int):
            self._taskbar.SetProgressValue(self.hwnd, progress, 100)

        @property
        def window_text(self) -> str:
            text_len = GetWindowTextLengthW(self.hwnd) + 1
            text_buffer = ctypes.create_unicode_buffer(text_len)

            GetWindowTextW(self.hwnd, text_buffer, text_len)
            return text_buffer.value

        @classmethod
        def attach_to_console_process(cls) -> TaskbarProgress:
            """
            Factory Method:
            Locates the parent console process (handling PyCharm/Terminal wrappers)
            and returns a fully initialized Taskbar instance attached to it.
            """
            console_hwnd = GetConsoleWindow()
            if not console_hwnd:
                raise RuntimeError("Could not get console window handle.")

            console_pid = cls.get_window_thread_process_id(console_hwnd)

            target_hwnd = console_hwnd
            try:
                console_process = Process(pid = console_pid)
                parent_hwnd = cls.get_parent_terminal(child = console_process)

                if parent_hwnd:
                    target_hwnd = parent_hwnd
                else:
                    print("[!] Parent terminal not found. Defaulting to raw console window.")

            except NoSuchProcess:
                print("[!] Console process not found. Defaulting to raw console window.")

            # 3. Return the new class instance
            return cls(hwnd = target_hwnd)

        @classmethod
        def get_parent_terminal(cls, child: Process) -> int | None:
            pid: int | None = None
            for parent in child.parents():
                if parent.name() in ['pycharm64.exe', 'WindowsTerminal.exe']:
                    pid = parent.pid
                    break

            if pid:
                for app in get_apps_by_z_order(current_desktop = False):
                    try:
                        process_pid = cls.get_window_thread_process_id(app.hwnd)
                        if process_pid == pid:
                            return app.hwnd
                    except NoSuchProcess:
                        continue
            return None

        @staticmethod
        def get_window_thread_process_id(hwnd: int) -> int:
            pid = wintypes.DWORD()
            GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            return pid.value

    # --- MAIN BOOTSTRAP ---
    try:
        with TaskbarProgress.attach_to_console_process() as taskbar_progress:
            print(f"Attached to window: {taskbar_progress.window_text!r} (HWND: {taskbar_progress.hwnd})")

            # Normal Green Progress
            print("State: Normal")
            taskbar_progress.set_progress_state(TaskbarState.NORMAL)
            for i in range(101):
                taskbar_progress.set_progress_value(progress = i)
                sys.stdout.write(f"Progress: {i}%  \r")
                sys.stdout.flush()
                time.sleep(0.1)

            # Paused or Warning (Yellow)
            print("\nState: Paused or Warning (Yellow)")
            taskbar_progress.set_progress_state(TaskbarState.PAUSED)
            time.sleep(2)

            # Error (Red)
            print("State: Error (Red)")
            taskbar_progress.set_progress_state(TaskbarState.ERROR)
            time.sleep(2)

            # Indeterminate (Marquee)
            print("State: Indeterminate")
            taskbar_progress.set_progress_state(TaskbarState.INDETERMINATE)
            time.sleep(3)

    except OSError as e:
        print(f"\nCOM Error: {e}")
