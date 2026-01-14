import ctypes
from typing import TYPE_CHECKING
from comtypes import GUID, COMMETHOD, DISPMETHOD, HRESULT, dispid, POINTER
from comtypes.automation import IDispatch, BSTR

if TYPE_CHECKING:
    # Type aliases for clarity
    WindowStyle = int

# GUID for the "WScript.Shell" Object
CLSID_WScriptShell = GUID("{72C24DD5-D70A-438B-8A42-98424B88AFB8}")


class IWshShortcut(IDispatch):
    """
    Interface for the Shortcut object returned by CreateShortcut.
    UUID: {F935DC23-1CF0-11D0-ADB9-00C04FD58A0B}
    """
    _iid_ = GUID("{F935DC23-1CF0-11D0-ADB9-00C04FD58A0B}")
    _idlflags_ = ['dual', 'oleautomation']
    _methods_ = [
        COMMETHOD([dispid(0), 'propget'], HRESULT, 'FullName', (['out', 'retval'], POINTER(BSTR), 'out_FullName')),

        COMMETHOD([dispid(1000), 'propget'], HRESULT, 'Arguments', (['out', 'retval'], POINTER(BSTR), 'out_Arguments')),
        COMMETHOD([dispid(1000), 'propput'], HRESULT, 'Arguments', (['in'], BSTR, 'out_Arguments')),

        COMMETHOD([dispid(1001), 'propget'], HRESULT, 'Description', (['out', 'retval'], POINTER(BSTR), 'out_Description')),
        COMMETHOD([dispid(1001), 'propput'], HRESULT, 'Description', (['in'], BSTR, 'out_Description')),

        COMMETHOD([dispid(1002), 'propget'], HRESULT, 'Hotkey', (['out', 'retval'], POINTER(BSTR), 'out_HotKey')),
        COMMETHOD([dispid(1002), 'propput'], HRESULT, 'Hotkey', (['in'], BSTR, 'out_HotKey')),

        COMMETHOD([dispid(1003), 'propget'], HRESULT, 'IconLocation', (['out', 'retval'], POINTER(BSTR), 'out_IconPath')),
        COMMETHOD([dispid(1003), 'propput'], HRESULT, 'IconLocation', (['in'], BSTR, 'out_IconPath')),

        COMMETHOD([dispid(1004), 'propput'], HRESULT, 'RelativePath', (['in'], BSTR, 'rhs')),
        # Note: propget for RelativePath is often skipped or hidden in some versions, but the setter is distinct. We can skip defining the getter if unused.

        COMMETHOD([dispid(1005), 'propget'], HRESULT, 'TargetPath', (['out', 'retval'], POINTER(BSTR), 'out_Path')),
        COMMETHOD([dispid(1005), 'propput'], HRESULT, 'TargetPath', (['in'], BSTR, 'out_Path')),

        COMMETHOD([dispid(1006), 'propget'], HRESULT, 'WindowStyle', (['out', 'retval'], POINTER(ctypes.c_int), 'out_ShowCmd')),
        COMMETHOD([dispid(1006), 'propput'], HRESULT, 'WindowStyle', (['in'], ctypes.c_int, 'out_ShowCmd')),

        COMMETHOD([dispid(1007), 'propget'], HRESULT, 'WorkingDirectory', (['out', 'retval'], POINTER(BSTR), 'out_WorkingDirectory')),
        COMMETHOD([dispid(1007), 'propput'], HRESULT, 'WorkingDirectory', (['in'], BSTR, 'out_WorkingDirectory')),

        COMMETHOD([dispid(2000), 'hidden'], HRESULT, 'Load', (['in'], BSTR, 'PathLink')),
        COMMETHOD([dispid(2001)], HRESULT, 'Save'),
    ]

    # --- Type Hints for IDE ---
    if TYPE_CHECKING:
        Arguments: str
        Description: str
        Hotkey: str
        IconLocation: str
        TargetPath: str
        WindowStyle: int
        WorkingDirectory: str

        def Save(self): ...


# noinspection GrazieInspection,SpellCheckingInspection
class IWshShell3(IDispatch):
    """
    Interface for the main WScript.Shell object.
    UUID: {41904400-BE18-11D3-A28B-00104BD35090}
    """
    _iid_ = GUID("{41904400-BE18-11D3-A28B-00104BD35090}")
    _idlflags_ = ['dual', 'oleautomation']
    _disp_methods_ = [
        # CreateShortcut is Dispid 1002
        DISPMETHOD(
            [dispid(1002)], HRESULT, 'CreateShortcut',
            (['in'], BSTR, 'PathLink'),
            (['out', 'retval'], POINTER(POINTER(IWshShortcut)), 'out_Shortcut')
        ),
    ]

    if TYPE_CHECKING:
        def CreateShortcut(self, PathLink: str) -> IWshShortcut: ...
