import ctypes
from ctypes import wintypes
from enum import IntFlag
from typing import TYPE_CHECKING

from comtypes import IUnknown, GUID, COMMETHOD, HRESULT

if TYPE_CHECKING:
    # These imports are only seen by the IDE, not at runtime

    # Simple aliases for clarity in the stubs
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

    # --- Static Analysis Stubs (What the IDE sees) ---
    # These are only seen by the IDE, not at runtime
    if TYPE_CHECKING:
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

    # --- Static Analysis Stubs (What the IDE sees) ---
    # These are only seen by the IDE, not at runtime
    if TYPE_CHECKING:
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

    # --- Static Analysis Stubs (What the IDE sees) ---
    # These are only seen by the IDE, not at runtime
    if TYPE_CHECKING:
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
