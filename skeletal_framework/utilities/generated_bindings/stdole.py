from enum import IntFlag

import comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0 as __wrapper_module__
from comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0 import (
    VgaColor, StdPicture, FONTSTRIKETHROUGH, GUID, IFont,
    OLE_YSIZE_PIXELS, DISPPROPERTY, IPictureDisp, BSTR,
    IFontEventsDisp, FONTUNDERSCORE, OLE_YSIZE_CONTAINER,
    OLE_YSIZE_HIMETRIC, FONTITALIC, OLE_XSIZE_PIXELS,
    OLE_XPOS_CONTAINER, Checked, OLE_COLOR, FONTNAME, _check_version,
    StdFont, OLE_XSIZE_CONTAINER, IUnknown, OLE_ENABLEDEFAULTBOOL,
    OLE_XSIZE_HIMETRIC, EXCEPINFO, OLE_YPOS_CONTAINER,
    OLE_YPOS_HIMETRIC, Color, IFontDisp, HRESULT, Monochrome, Gray,
    Picture, FontEvents, VARIANT_BOOL, IDispatch, OLE_OPTEXCLUSIVE,
    OLE_CANCELBOOL, IEnumVARIANT, Default, CoClass, OLE_YPOS_PIXELS,
    FONTSIZE, Library, dispid, _lcid, Font, OLE_XPOS_HIMETRIC,
    DISPPARAMS, OLE_XPOS_PIXELS, FONTBOLD, IPicture, OLE_HANDLE,
    typelib_path, Unchecked, COMMETHOD, DISPMETHOD
)


class LoadPictureConstants(IntFlag):
    Default = 0
    Monochrome = 1
    VgaColor = 2
    Color = 4


class OLE_TRISTATE(IntFlag):
    Unchecked = 0
    Checked = 1
    Gray = 2


__all__ = [
    'Monochrome', 'VgaColor', 'Gray', 'Picture', 'StdPicture',
    'FONTSTRIKETHROUGH', 'FontEvents', 'IFont', 'OLE_YSIZE_PIXELS',
    'OLE_TRISTATE', 'OLE_OPTEXCLUSIVE', 'OLE_CANCELBOOL',
    'IPictureDisp', 'Default', 'IFontEventsDisp', 'FONTUNDERSCORE',
    'OLE_YSIZE_CONTAINER', 'OLE_YSIZE_HIMETRIC', 'OLE_YPOS_PIXELS',
    'FONTSIZE', 'LoadPictureConstants', 'FONTITALIC',
    'OLE_XSIZE_PIXELS', 'Library', 'Font', 'OLE_XPOS_HIMETRIC',
    'OLE_XPOS_CONTAINER', 'Checked', 'OLE_COLOR', 'FONTNAME',
    'StdFont', 'OLE_XPOS_PIXELS', 'FONTBOLD', 'OLE_XSIZE_CONTAINER',
    'IPicture', 'OLE_HANDLE', 'typelib_path', 'OLE_ENABLEDEFAULTBOOL',
    'OLE_XSIZE_HIMETRIC', 'Unchecked', 'OLE_YPOS_CONTAINER',
    'OLE_YPOS_HIMETRIC', 'Color', 'IFontDisp'
]

