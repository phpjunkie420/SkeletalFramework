# -*- coding: mbcs -*-

from ctypes import *
import skeletal_framework.utilities.generated_bindings._00020430_0000_0000_C000_000000000046_0_2_0
from comtypes import (
    _check_version, BSTR, CoClass, COMMETHOD, dispid, GUID, IUnknown
)
from comtypes.automation import IDispatch, VARIANT
from ctypes import HRESULT
from ctypes.wintypes import VARIANT_BOOL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from comtypes import hints


_lcid = 0  # change this if required
typelib_path = 'C:\\Windows\\System32\\wshom.ocx'

# values for enumeration '__MIDL___MIDL_itf_iwshom_0000_0000_0003'
WindowsFolder = 0
SystemFolder = 1
TemporaryFolder = 2
__MIDL___MIDL_itf_iwshom_0000_0000_0003 = c_int  # enum

# values for enumeration 'IOMode'
ForReading = 1
ForWriting = 2
ForAppending = 8
IOMode = c_int  # enum

# values for enumeration 'Tristate'
TristateTrue = -1
TristateFalse = 0
TristateUseDefault = -2
TristateMixed = -2
Tristate = c_int  # enum

# values for enumeration '__MIDL___MIDL_itf_iwshom_0000_0000_0004'
StdIn = 0
StdOut = 1
StdErr = 2
__MIDL___MIDL_itf_iwshom_0000_0000_0004 = c_int  # enum

# values for enumeration '__MIDL___MIDL_itf_iwshom_0000_0000_0001'
Normal = 0
ReadOnly = 1
Hidden = 2
System = 4
Volume = 8
Directory = 16
Archive = 32
Alias = 1024
Compressed = 2048
__MIDL___MIDL_itf_iwshom_0000_0000_0001 = c_int  # enum

# values for enumeration 'CompareMethod'
BinaryCompare = 0
TextCompare = 1
DatabaseCompare = 2
CompareMethod = c_int  # enum

# values for enumeration '__MIDL___MIDL_itf_iwshom_0000_0000_0002'
UnknownType = 0
Removable = 1
Fixed = 2
Remote = 3
CDRom = 4
RamDisk = 5
__MIDL___MIDL_itf_iwshom_0000_0000_0002 = c_int  # enum

# values for enumeration '__MIDL___MIDL_itf_iwshom_0001_0037_0001'
WshRunning = 0
WshFinished = 1
WshFailed = 2
__MIDL___MIDL_itf_iwshom_0001_0037_0001 = c_int  # enum

# values for enumeration '__MIDL___MIDL_itf_iwshom_0001_0016_0001'
WshHide = 0
WshNormalFocus = 1
WshMinimizedFocus = 2
WshMaximizedFocus = 3
WshNormalNoFocus = 4
WshMinimizedNoFocus = 6
__MIDL___MIDL_itf_iwshom_0001_0016_0001 = c_int  # enum

# aliases for enums
SpecialFolderConst = __MIDL___MIDL_itf_iwshom_0000_0000_0003
StandardStreamTypes = __MIDL___MIDL_itf_iwshom_0000_0000_0004
FileAttribute = __MIDL___MIDL_itf_iwshom_0000_0000_0001
DriveTypeConst = __MIDL___MIDL_itf_iwshom_0000_0000_0002
WshExecStatus = __MIDL___MIDL_itf_iwshom_0001_0037_0001
WshWindowStyle = __MIDL___MIDL_itf_iwshom_0001_0016_0001


class IFileCollection(skeletal_framework.utilities.generated_bindings._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{C7C3F5A5-88A3-11D0-ABCB-00A0C90FFFC0}')
    _idlflags_ = ['hidden', 'dual', 'nonextensible', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def _get_Item(self, Key: hints.Incomplete) -> 'IFile': ...
        Item = hints.named_property('Item', _get_Item)
        __call__ = hints.to_dunder_call(Item)
        __getitem__ = hints.to_dunder_getitem(Item)
        __setitem__ = hints.to_dunder_setitem(Item)
        def _get__NewEnum(self) -> hints.Incomplete: ...
        _NewEnum = hints.normal_property(_get__NewEnum)
        __iter__ = hints.to_dunder_iter(_NewEnum)
        def _get_Count(self) -> hints.Incomplete: ...
        Count = hints.normal_property(_get_Count)
        __len__ = hints.to_dunder_len(Count)


class IFile(skeletal_framework.utilities.generated_bindings._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{C7C3F5A4-88A3-11D0-ABCB-00A0C90FFFC0}')
    _idlflags_ = ['hidden', 'dual', 'nonextensible', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def _get_Path(self) -> hints.Incomplete: ...
        Path = hints.normal_property(_get_Path)
        def _get_Name(self) -> hints.Incomplete: ...
        def _set_Name(self, pbstrName: hints.Incomplete) -> hints.Hresult: ...
        Name = hints.normal_property(_get_Name, _set_Name)
        def _get_ShortPath(self) -> hints.Incomplete: ...
        ShortPath = hints.normal_property(_get_ShortPath)
        def _get_ShortName(self) -> hints.Incomplete: ...
        ShortName = hints.normal_property(_get_ShortName)
        def _get_Drive(self) -> 'IDrive': ...
        Drive = hints.normal_property(_get_Drive)
        def _get_ParentFolder(self) -> 'IFolder': ...
        ParentFolder = hints.normal_property(_get_ParentFolder)
        def _get_Attributes(self) -> hints.Incomplete: ...
        def _set_Attributes(self, pfa: hints.Incomplete) -> hints.Hresult: ...
        Attributes = hints.normal_property(_get_Attributes, _set_Attributes)
        def _get_DateCreated(self) -> hints.Incomplete: ...
        DateCreated = hints.normal_property(_get_DateCreated)
        def _get_DateLastModified(self) -> hints.Incomplete: ...
        DateLastModified = hints.normal_property(_get_DateLastModified)
        def _get_DateLastAccessed(self) -> hints.Incomplete: ...
        DateLastAccessed = hints.normal_property(_get_DateLastAccessed)
        def _get_Size(self) -> hints.Incomplete: ...
        Size = hints.normal_property(_get_Size)
        def _get_Type(self) -> hints.Incomplete: ...
        Type = hints.normal_property(_get_Type)
        def Delete(self, Force: hints.Incomplete = ...) -> hints.Hresult: ...
        def Copy(self, Destination: hints.Incomplete, OverWriteFiles: hints.Incomplete = ...) -> hints.Hresult: ...
        def Move(self, Destination: hints.Incomplete) -> hints.Hresult: ...
        def OpenAsTextStream(self, IOMode: hints.Incomplete = ..., Format: hints.Incomplete = ...) -> 'ITextStream': ...


IFileCollection._methods_ = [
    COMMETHOD(
        [dispid(0), 'propget'],
        HRESULT,
        'Item',
        (['in'], VARIANT, 'Key'),
        (['out', 'retval'], POINTER(POINTER(IFile)), 'ppfile')
    ),
    COMMETHOD(
        [dispid(-4), 'restricted', 'hidden', 'propget'],
        HRESULT,
        '_NewEnum',
        (['out', 'retval'], POINTER(POINTER(IUnknown)), 'ppenum')
    ),
    COMMETHOD(
        [dispid(1), 'propget'],
        HRESULT,
        'Count',
        (['out', 'retval'], POINTER(c_int), 'plCount')
    ),
]

################################################################
# code template for IFileCollection implementation
# class IFileCollection_Impl(object):
#     @property
#     def Item(self, Key):
#         '-no docstring-'
#         #return ppfile
#
#     @property
#     def _NewEnum(self):
#         '-no docstring-'
#         #return ppenum
#
#     @property
#     def Count(self):
#         '-no docstring-'
#         #return plCount
#


class IFileSystem(skeletal_framework.utilities.generated_bindings._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{0AB5A3D0-E5B6-11D0-ABF5-00A0C90FFFC0}')
    _idlflags_ = ['hidden', 'dual', 'nonextensible', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def _get_Drives(self) -> 'IDriveCollection': ...
        Drives = hints.normal_property(_get_Drives)
        def BuildPath(self, Path: hints.Incomplete, Name: hints.Incomplete) -> hints.Incomplete: ...
        def GetDriveName(self, Path: hints.Incomplete) -> hints.Incomplete: ...
        def GetParentFolderName(self, Path: hints.Incomplete) -> hints.Incomplete: ...
        def GetFileName(self, Path: hints.Incomplete) -> hints.Incomplete: ...
        def GetBaseName(self, Path: hints.Incomplete) -> hints.Incomplete: ...
        def GetExtensionName(self, Path: hints.Incomplete) -> hints.Incomplete: ...
        def GetAbsolutePathName(self, Path: hints.Incomplete) -> hints.Incomplete: ...
        def GetTempName(self) -> hints.Incomplete: ...
        def DriveExists(self, DriveSpec: hints.Incomplete) -> hints.Incomplete: ...
        def FileExists(self, FileSpec: hints.Incomplete) -> hints.Incomplete: ...
        def FolderExists(self, FolderSpec: hints.Incomplete) -> hints.Incomplete: ...
        def GetDrive(self, DriveSpec: hints.Incomplete) -> 'IDrive': ...
        def GetFile(self, FilePath: hints.Incomplete) -> 'IFile': ...
        def GetFolder(self, FolderPath: hints.Incomplete) -> 'IFolder': ...
        def GetSpecialFolder(self, SpecialFolder: hints.Incomplete) -> 'IFolder': ...
        def DeleteFile(self, FileSpec: hints.Incomplete, Force: hints.Incomplete = ...) -> hints.Hresult: ...
        def DeleteFolder(self, FolderSpec: hints.Incomplete, Force: hints.Incomplete = ...) -> hints.Hresult: ...
        def MoveFile(self, Source: hints.Incomplete, Destination: hints.Incomplete) -> hints.Hresult: ...
        def MoveFolder(self, Source: hints.Incomplete, Destination: hints.Incomplete) -> hints.Hresult: ...
        def CopyFile(self, Source: hints.Incomplete, Destination: hints.Incomplete, OverWriteFiles: hints.Incomplete = ...) -> hints.Hresult: ...
        def CopyFolder(self, Source: hints.Incomplete, Destination: hints.Incomplete, OverWriteFiles: hints.Incomplete = ...) -> hints.Hresult: ...
        def CreateFolder(self, Path: hints.Incomplete) -> 'IFolder': ...
        def CreateTextFile(self, FileName: hints.Incomplete, Overwrite: hints.Incomplete = ..., Unicode: hints.Incomplete = ...) -> 'ITextStream': ...
        def OpenTextFile(self, FileName: hints.Incomplete, IOMode: hints.Incomplete = ..., Create: hints.Incomplete = ..., Format: hints.Incomplete = ...) -> 'ITextStream': ...


class IFileSystem3(IFileSystem):
    _case_insensitive_ = True
    _iid_ = GUID('{2A0B9D10-4B87-11D3-A97A-00104B365C9F}')
    _idlflags_ = ['dual', 'nonextensible', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def GetStandardStream(self, StandardStreamType: hints.Incomplete, Unicode: hints.Incomplete = ...) -> 'ITextStream': ...
        def GetFileVersion(self, FileName: hints.Incomplete) -> hints.Incomplete: ...


class IDriveCollection(skeletal_framework.utilities.generated_bindings._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{C7C3F5A1-88A3-11D0-ABCB-00A0C90FFFC0}')
    _idlflags_ = ['hidden', 'dual', 'nonextensible', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def _get_Item(self, Key: hints.Incomplete) -> 'IDrive': ...
        Item = hints.named_property('Item', _get_Item)
        __call__ = hints.to_dunder_call(Item)
        __getitem__ = hints.to_dunder_getitem(Item)
        __setitem__ = hints.to_dunder_setitem(Item)
        def _get__NewEnum(self) -> hints.Incomplete: ...
        _NewEnum = hints.normal_property(_get__NewEnum)
        __iter__ = hints.to_dunder_iter(_NewEnum)
        def _get_Count(self) -> hints.Incomplete: ...
        Count = hints.normal_property(_get_Count)
        __len__ = hints.to_dunder_len(Count)


class IDrive(skeletal_framework.utilities.generated_bindings._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{C7C3F5A0-88A3-11D0-ABCB-00A0C90FFFC0}')
    _idlflags_ = ['hidden', 'dual', 'nonextensible', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def _get_Path(self) -> hints.Incomplete: ...
        Path = hints.normal_property(_get_Path)
        def _get_DriveLetter(self) -> hints.Incomplete: ...
        DriveLetter = hints.normal_property(_get_DriveLetter)
        def _get_ShareName(self) -> hints.Incomplete: ...
        ShareName = hints.normal_property(_get_ShareName)
        def _get_DriveType(self) -> hints.Incomplete: ...
        DriveType = hints.normal_property(_get_DriveType)
        def _get_RootFolder(self) -> 'IFolder': ...
        RootFolder = hints.normal_property(_get_RootFolder)
        def _get_AvailableSpace(self) -> hints.Incomplete: ...
        AvailableSpace = hints.normal_property(_get_AvailableSpace)
        def _get_FreeSpace(self) -> hints.Incomplete: ...
        FreeSpace = hints.normal_property(_get_FreeSpace)
        def _get_TotalSize(self) -> hints.Incomplete: ...
        TotalSize = hints.normal_property(_get_TotalSize)
        def _get_VolumeName(self) -> hints.Incomplete: ...
        def _set_VolumeName(self, pbstrName: hints.Incomplete) -> hints.Hresult: ...
        VolumeName = hints.normal_property(_get_VolumeName, _set_VolumeName)
        def _get_FileSystem(self) -> hints.Incomplete: ...
        FileSystem = hints.normal_property(_get_FileSystem)
        def _get_SerialNumber(self) -> hints.Incomplete: ...
        SerialNumber = hints.normal_property(_get_SerialNumber)
        def _get_IsReady(self) -> hints.Incomplete: ...
        IsReady = hints.normal_property(_get_IsReady)


class IFolder(skeletal_framework.utilities.generated_bindings._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{C7C3F5A2-88A3-11D0-ABCB-00A0C90FFFC0}')
    _idlflags_ = ['hidden', 'dual', 'nonextensible', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def _get_Path(self) -> hints.Incomplete: ...
        Path = hints.normal_property(_get_Path)
        def _get_Name(self) -> hints.Incomplete: ...
        def _set_Name(self, pbstrName: hints.Incomplete) -> hints.Hresult: ...
        Name = hints.normal_property(_get_Name, _set_Name)
        def _get_ShortPath(self) -> hints.Incomplete: ...
        ShortPath = hints.normal_property(_get_ShortPath)
        def _get_ShortName(self) -> hints.Incomplete: ...
        ShortName = hints.normal_property(_get_ShortName)
        def _get_Drive(self) -> 'IDrive': ...
        Drive = hints.normal_property(_get_Drive)
        def _get_ParentFolder(self) -> 'IFolder': ...
        ParentFolder = hints.normal_property(_get_ParentFolder)
        def _get_Attributes(self) -> hints.Incomplete: ...
        def _set_Attributes(self, pfa: hints.Incomplete) -> hints.Hresult: ...
        Attributes = hints.normal_property(_get_Attributes, _set_Attributes)
        def _get_DateCreated(self) -> hints.Incomplete: ...
        DateCreated = hints.normal_property(_get_DateCreated)
        def _get_DateLastModified(self) -> hints.Incomplete: ...
        DateLastModified = hints.normal_property(_get_DateLastModified)
        def _get_DateLastAccessed(self) -> hints.Incomplete: ...
        DateLastAccessed = hints.normal_property(_get_DateLastAccessed)
        def _get_Type(self) -> hints.Incomplete: ...
        Type = hints.normal_property(_get_Type)
        def Delete(self, Force: hints.Incomplete = ...) -> hints.Hresult: ...
        def Copy(self, Destination: hints.Incomplete, OverWriteFiles: hints.Incomplete = ...) -> hints.Hresult: ...
        def Move(self, Destination: hints.Incomplete) -> hints.Hresult: ...
        def _get_IsRootFolder(self) -> hints.Incomplete: ...
        IsRootFolder = hints.normal_property(_get_IsRootFolder)
        def _get_Size(self) -> hints.Incomplete: ...
        Size = hints.normal_property(_get_Size)
        def _get_SubFolders(self) -> 'IFolderCollection': ...
        SubFolders = hints.normal_property(_get_SubFolders)
        def _get_Files(self) -> 'IFileCollection': ...
        Files = hints.normal_property(_get_Files)
        def CreateTextFile(self, FileName: hints.Incomplete, Overwrite: hints.Incomplete = ..., Unicode: hints.Incomplete = ...) -> 'ITextStream': ...


class ITextStream(skeletal_framework.utilities.generated_bindings._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{53BAD8C1-E718-11CF-893D-00A0C9054228}')
    _idlflags_ = ['hidden', 'dual', 'nonextensible', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def _get_Line(self) -> hints.Incomplete: ...
        Line = hints.normal_property(_get_Line)
        def _get_Column(self) -> hints.Incomplete: ...
        Column = hints.normal_property(_get_Column)
        def _get_AtEndOfStream(self) -> hints.Incomplete: ...
        AtEndOfStream = hints.normal_property(_get_AtEndOfStream)
        def _get_AtEndOfLine(self) -> hints.Incomplete: ...
        AtEndOfLine = hints.normal_property(_get_AtEndOfLine)
        def Read(self, Characters: hints.Incomplete) -> hints.Incomplete: ...
        def ReadLine(self) -> hints.Incomplete: ...
        def ReadAll(self) -> hints.Incomplete: ...
        def Write(self, Text: hints.Incomplete) -> hints.Hresult: ...
        def WriteLine(self, Text: hints.Incomplete = ...) -> hints.Hresult: ...
        def WriteBlankLines(self, Lines: hints.Incomplete) -> hints.Hresult: ...
        def Skip(self, Characters: hints.Incomplete) -> hints.Hresult: ...
        def SkipLine(self) -> hints.Hresult: ...
        def Close(self) -> hints.Hresult: ...


IFileSystem._methods_ = [
    COMMETHOD(
        [dispid(10010), 'propget'],
        HRESULT,
        'Drives',
        (['out', 'retval'], POINTER(POINTER(IDriveCollection)), 'ppdrives')
    ),
    COMMETHOD(
        [dispid(10000)],
        HRESULT,
        'BuildPath',
        (['in'], BSTR, 'Path'),
        (['in'], BSTR, 'Name'),
        (['out', 'retval'], POINTER(BSTR), 'pbstrResult')
    ),
    COMMETHOD(
        [dispid(10004)],
        HRESULT,
        'GetDriveName',
        (['in'], BSTR, 'Path'),
        (['out', 'retval'], POINTER(BSTR), 'pbstrResult')
    ),
    COMMETHOD(
        [dispid(10005)],
        HRESULT,
        'GetParentFolderName',
        (['in'], BSTR, 'Path'),
        (['out', 'retval'], POINTER(BSTR), 'pbstrResult')
    ),
    COMMETHOD(
        [dispid(10006)],
        HRESULT,
        'GetFileName',
        (['in'], BSTR, 'Path'),
        (['out', 'retval'], POINTER(BSTR), 'pbstrResult')
    ),
    COMMETHOD(
        [dispid(10007)],
        HRESULT,
        'GetBaseName',
        (['in'], BSTR, 'Path'),
        (['out', 'retval'], POINTER(BSTR), 'pbstrResult')
    ),
    COMMETHOD(
        [dispid(10008)],
        HRESULT,
        'GetExtensionName',
        (['in'], BSTR, 'Path'),
        (['out', 'retval'], POINTER(BSTR), 'pbstrResult')
    ),
    COMMETHOD(
        [dispid(10002)],
        HRESULT,
        'GetAbsolutePathName',
        (['in'], BSTR, 'Path'),
        (['out', 'retval'], POINTER(BSTR), 'pbstrResult')
    ),
    COMMETHOD(
        [dispid(10003)],
        HRESULT,
        'GetTempName',
        (['out', 'retval'], POINTER(BSTR), 'pbstrResult')
    ),
    COMMETHOD(
        [dispid(10015)],
        HRESULT,
        'DriveExists',
        (['in'], BSTR, 'DriveSpec'),
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pfExists')
    ),
    COMMETHOD(
        [dispid(10016)],
        HRESULT,
        'FileExists',
        (['in'], BSTR, 'FileSpec'),
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pfExists')
    ),
    COMMETHOD(
        [dispid(10017)],
        HRESULT,
        'FolderExists',
        (['in'], BSTR, 'FolderSpec'),
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pfExists')
    ),
    COMMETHOD(
        [dispid(10011)],
        HRESULT,
        'GetDrive',
        (['in'], BSTR, 'DriveSpec'),
        (['out', 'retval'], POINTER(POINTER(IDrive)), 'ppdrive')
    ),
    COMMETHOD(
        [dispid(10012)],
        HRESULT,
        'GetFile',
        (['in'], BSTR, 'FilePath'),
        (['out', 'retval'], POINTER(POINTER(IFile)), 'ppfile')
    ),
    COMMETHOD(
        [dispid(10013)],
        HRESULT,
        'GetFolder',
        (['in'], BSTR, 'FolderPath'),
        (['out', 'retval'], POINTER(POINTER(IFolder)), 'ppfolder')
    ),
    COMMETHOD(
        [dispid(10014)],
        HRESULT,
        'GetSpecialFolder',
        (['in'], SpecialFolderConst, 'SpecialFolder'),
        (['out', 'retval'], POINTER(POINTER(IFolder)), 'ppfolder')
    ),
    COMMETHOD(
        [dispid(1200)],
        HRESULT,
        'DeleteFile',
        (['in'], BSTR, 'FileSpec'),
        (['in', 'optional'], VARIANT_BOOL, 'Force', False)
    ),
    COMMETHOD(
        [dispid(1201)],
        HRESULT,
        'DeleteFolder',
        (['in'], BSTR, 'FolderSpec'),
        (['in', 'optional'], VARIANT_BOOL, 'Force', False)
    ),
    COMMETHOD(
        [dispid(1204)],
        HRESULT,
        'MoveFile',
        (['in'], BSTR, 'Source'),
        (['in'], BSTR, 'Destination')
    ),
    COMMETHOD(
        [dispid(1205)],
        HRESULT,
        'MoveFolder',
        (['in'], BSTR, 'Source'),
        (['in'], BSTR, 'Destination')
    ),
    COMMETHOD(
        [dispid(1202)],
        HRESULT,
        'CopyFile',
        (['in'], BSTR, 'Source'),
        (['in'], BSTR, 'Destination'),
        (['in', 'optional'], VARIANT_BOOL, 'OverWriteFiles', True)
    ),
    COMMETHOD(
        [dispid(1203)],
        HRESULT,
        'CopyFolder',
        (['in'], BSTR, 'Source'),
        (['in'], BSTR, 'Destination'),
        (['in', 'optional'], VARIANT_BOOL, 'OverWriteFiles', True)
    ),
    COMMETHOD(
        [dispid(1120)],
        HRESULT,
        'CreateFolder',
        (['in'], BSTR, 'Path'),
        (['out', 'retval'], POINTER(POINTER(IFolder)), 'ppfolder')
    ),
    COMMETHOD(
        [dispid(1101)],
        HRESULT,
        'CreateTextFile',
        (['in'], BSTR, 'FileName'),
        (['in', 'optional'], VARIANT_BOOL, 'Overwrite', True),
        (['in', 'optional'], VARIANT_BOOL, 'Unicode', False),
        (['out', 'retval'], POINTER(POINTER(ITextStream)), 'ppts')
    ),
    COMMETHOD(
        [dispid(1100)],
        HRESULT,
        'OpenTextFile',
        (['in'], BSTR, 'FileName'),
        (['in', 'optional'], IOMode, 'IOMode', 1),
        (['in', 'optional'], VARIANT_BOOL, 'Create', False),
        (['in', 'optional'], Tristate, 'Format', 0),
        (['out', 'retval'], POINTER(POINTER(ITextStream)), 'ppts')
    ),
]

################################################################
# code template for IFileSystem implementation
# class IFileSystem_Impl(object):
#     @property
#     def Drives(self):
#         '-no docstring-'
#         #return ppdrives
#
#     def BuildPath(self, Path, Name):
#         '-no docstring-'
#         #return pbstrResult
#
#     def GetDriveName(self, Path):
#         '-no docstring-'
#         #return pbstrResult
#
#     def GetParentFolderName(self, Path):
#         '-no docstring-'
#         #return pbstrResult
#
#     def GetFileName(self, Path):
#         '-no docstring-'
#         #return pbstrResult
#
#     def GetBaseName(self, Path):
#         '-no docstring-'
#         #return pbstrResult
#
#     def GetExtensionName(self, Path):
#         '-no docstring-'
#         #return pbstrResult
#
#     def GetAbsolutePathName(self, Path):
#         '-no docstring-'
#         #return pbstrResult
#
#     def GetTempName(self):
#         '-no docstring-'
#         #return pbstrResult
#
#     def DriveExists(self, DriveSpec):
#         '-no docstring-'
#         #return pfExists
#
#     def FileExists(self, FileSpec):
#         '-no docstring-'
#         #return pfExists
#
#     def FolderExists(self, FolderSpec):
#         '-no docstring-'
#         #return pfExists
#
#     def GetDrive(self, DriveSpec):
#         '-no docstring-'
#         #return ppdrive
#
#     def GetFile(self, FilePath):
#         '-no docstring-'
#         #return ppfile
#
#     def GetFolder(self, FolderPath):
#         '-no docstring-'
#         #return ppfolder
#
#     def GetSpecialFolder(self, SpecialFolder):
#         '-no docstring-'
#         #return ppfolder
#
#     def DeleteFile(self, FileSpec, Force):
#         '-no docstring-'
#         #return 
#
#     def DeleteFolder(self, FolderSpec, Force):
#         '-no docstring-'
#         #return 
#
#     def MoveFile(self, Source, Destination):
#         '-no docstring-'
#         #return 
#
#     def MoveFolder(self, Source, Destination):
#         '-no docstring-'
#         #return 
#
#     def CopyFile(self, Source, Destination, OverWriteFiles):
#         '-no docstring-'
#         #return 
#
#     def CopyFolder(self, Source, Destination, OverWriteFiles):
#         '-no docstring-'
#         #return 
#
#     def CreateFolder(self, Path):
#         '-no docstring-'
#         #return ppfolder
#
#     def CreateTextFile(self, FileName, Overwrite, Unicode):
#         '-no docstring-'
#         #return ppts
#
#     def OpenTextFile(self, FileName, IOMode, Create, Format):
#         '-no docstring-'
#         #return ppts
#

IFileSystem3._methods_ = [
    COMMETHOD(
        [dispid(20000)],
        HRESULT,
        'GetStandardStream',
        (['in'], StandardStreamTypes, 'StandardStreamType'),
        (['in', 'optional'], VARIANT_BOOL, 'Unicode', False),
        (['out', 'retval'], POINTER(POINTER(ITextStream)), 'ppts')
    ),
    COMMETHOD(
        [dispid(20010)],
        HRESULT,
        'GetFileVersion',
        (['in'], BSTR, 'FileName'),
        (['out', 'retval'], POINTER(BSTR), 'FileVersion')
    ),
]

################################################################
# code template for IFileSystem3 implementation
# class IFileSystem3_Impl(object):
#     def GetStandardStream(self, StandardStreamType, Unicode):
#         '-no docstring-'
#         #return ppts
#
#     def GetFileVersion(self, FileName):
#         '-no docstring-'
#         #return FileVersion
#

IDriveCollection._methods_ = [
    COMMETHOD(
        [dispid(0), 'propget'],
        HRESULT,
        'Item',
        (['in'], VARIANT, 'Key'),
        (['out', 'retval'], POINTER(POINTER(IDrive)), 'ppdrive')
    ),
    COMMETHOD(
        [dispid(-4), 'restricted', 'hidden', 'propget'],
        HRESULT,
        '_NewEnum',
        (['out', 'retval'], POINTER(POINTER(IUnknown)), 'ppenum')
    ),
    COMMETHOD(
        [dispid(1), 'propget'],
        HRESULT,
        'Count',
        (['out', 'retval'], POINTER(c_int), 'plCount')
    ),
]

################################################################
# code template for IDriveCollection implementation
# class IDriveCollection_Impl(object):
#     @property
#     def Item(self, Key):
#         '-no docstring-'
#         #return ppdrive
#
#     @property
#     def _NewEnum(self):
#         '-no docstring-'
#         #return ppenum
#
#     @property
#     def Count(self):
#         '-no docstring-'
#         #return plCount
#


class IWshShell_Class(CoClass):
    """Shell Object"""
    _reg_clsid_ = GUID('{F935DC22-1CF0-11D0-ADB9-00C04FD58A0B}')
    _idlflags_ = ['hidden']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


class IWshShell(skeletal_framework.utilities.generated_bindings._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    """Shell Object Interface"""
    _case_insensitive_ = True
    _iid_ = GUID('{F935DC21-1CF0-11D0-ADB9-00C04FD58A0B}')
    _idlflags_ = ['hidden', 'dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def _get_SpecialFolders(self) -> 'IWshCollection': ...
        SpecialFolders = hints.normal_property(_get_SpecialFolders)
        def _get_Environment(self, Type: hints.Incomplete = ...) -> 'IWshEnvironment': ...
        Environment = hints.named_property('Environment', _get_Environment)
        def Run(self, Command: hints.Incomplete, WindowStyle: hints.Incomplete = ..., WaitOnReturn: hints.Incomplete = ...) -> hints.Incomplete: ...
        def Popup(self, Text: hints.Incomplete, SecondsToWait: hints.Incomplete = ..., Title: hints.Incomplete = ..., Type: hints.Incomplete = ...) -> hints.Incomplete: ...
        def CreateShortcut(self, PathLink: hints.Incomplete) -> hints.Incomplete: ...
        def ExpandEnvironmentStrings(self, Src: hints.Incomplete) -> hints.Incomplete: ...
        def RegRead(self, Name: hints.Incomplete) -> hints.Incomplete: ...
        def RegWrite(self, Name: hints.Incomplete, Value: hints.Incomplete, Type: hints.Incomplete = ...) -> hints.Hresult: ...
        def RegDelete(self, Name: hints.Incomplete) -> hints.Hresult: ...


class IWshShell2(IWshShell):
    """Shell Object Interface"""
    _case_insensitive_ = True
    _iid_ = GUID('{24BE5A30-EDFE-11D2-B933-00104B365C9F}')
    _idlflags_ = ['hidden', 'dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def LogEvent(self, Type: hints.Incomplete, Message: hints.Incomplete, Target: hints.Incomplete = ...) -> hints.Incomplete: ...
        def AppActivate(self, App: hints.Incomplete, Wait: hints.Incomplete = ...) -> hints.Incomplete: ...
        def SendKeys(self, Keys: hints.Incomplete, Wait: hints.Incomplete = ...) -> hints.Hresult: ...


class IWshShell3(IWshShell2):
    """Shell Object Interface"""
    _case_insensitive_ = True
    _iid_ = GUID('{41904400-BE18-11D3-A28B-00104BD35090}')
    _idlflags_ = ['dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def Exec(self, Command: hints.Incomplete) -> 'IWshExec': ...
        def _get_CurrentDirectory(self) -> hints.Incomplete: ...
        def _set_CurrentDirectory(self, out_Directory: hints.Incomplete) -> hints.Hresult: ...
        CurrentDirectory = hints.normal_property(_get_CurrentDirectory, _set_CurrentDirectory)


IWshShell_Class._com_interfaces_ = [IWshShell3]


class IWshNetwork_Class(CoClass):
    """Network Object"""
    _reg_clsid_ = GUID('{F935DC26-1CF0-11D0-ADB9-00C04FD58A0B}')
    _idlflags_ = ['hidden']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


class IWshNetwork(skeletal_framework.utilities.generated_bindings._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    """Network Object"""
    _case_insensitive_ = True
    _iid_ = GUID('{F935DC25-1CF0-11D0-ADB9-00C04FD58A0B}')
    _idlflags_ = ['hidden', 'dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def _get_UserDomain(self) -> hints.Incomplete: ...
        UserDomain = hints.normal_property(_get_UserDomain)
        def _get_UserName(self) -> hints.Incomplete: ...
        UserName = hints.normal_property(_get_UserName)
        def _get_UserProfile(self) -> hints.Incomplete: ...
        UserProfile = hints.normal_property(_get_UserProfile)
        def _get_ComputerName(self) -> hints.Incomplete: ...
        ComputerName = hints.normal_property(_get_ComputerName)
        def _get_Organization(self) -> hints.Incomplete: ...
        Organization = hints.normal_property(_get_Organization)
        def _get_Site(self) -> hints.Incomplete: ...
        Site = hints.normal_property(_get_Site)
        def MapNetworkDrive(self, LocalName: hints.Incomplete, RemoteName: hints.Incomplete, UpdateProfile: hints.Incomplete = ..., UserName: hints.Incomplete = ..., Password: hints.Incomplete = ...) -> hints.Hresult: ...
        def RemoveNetworkDrive(self, Name: hints.Incomplete, Force: hints.Incomplete = ..., UpdateProfile: hints.Incomplete = ...) -> hints.Hresult: ...
        def EnumNetworkDrives(self) -> 'IWshCollection': ...
        def AddPrinterConnection(self, LocalName: hints.Incomplete, RemoteName: hints.Incomplete, UpdateProfile: hints.Incomplete = ..., UserName: hints.Incomplete = ..., Password: hints.Incomplete = ...) -> hints.Hresult: ...
        def RemovePrinterConnection(self, Name: hints.Incomplete, Force: hints.Incomplete = ..., UpdateProfile: hints.Incomplete = ...) -> hints.Hresult: ...
        def EnumPrinterConnections(self) -> 'IWshCollection': ...
        def SetDefaultPrinter(self, Name: hints.Incomplete) -> hints.Hresult: ...


class IWshNetwork2(IWshNetwork):
    """Network Object"""
    _case_insensitive_ = True
    _iid_ = GUID('{24BE5A31-EDFE-11D2-B933-00104B365C9F}')
    _idlflags_ = ['dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def AddWindowsPrinterConnection(self, PrinterName: hints.Incomplete, DriverName: hints.Incomplete = ..., Port: hints.Incomplete = ...) -> hints.Hresult: ...


IWshNetwork_Class._com_interfaces_ = [IWshNetwork2]


class IWshCollection(skeletal_framework.utilities.generated_bindings._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    """Generic Collection Object"""
    _case_insensitive_ = True
    _iid_ = GUID('{F935DC27-1CF0-11D0-ADB9-00C04FD58A0B}')
    _idlflags_ = ['dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def Item(self, Index: hints.Incomplete) -> hints.Incomplete: ...
        __call__ = hints.to_dunder_call(Item)
        __getitem__ = hints.to_dunder_getitem(Item)
        __setitem__ = hints.to_dunder_setitem(Item)
        def Count(self) -> hints.Incomplete: ...
        __len__ = hints.to_dunder_len(Count)
        def _get_length(self) -> hints.Incomplete: ...
        length = hints.normal_property(_get_length)
        def _NewEnum(self) -> hints.Incomplete: ...
        __iter__ = hints.to_dunder_iter(_NewEnum)


class IWshEnvironment(skeletal_framework.utilities.generated_bindings._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    """Environment Variables Collection Object"""
    _case_insensitive_ = True
    _iid_ = GUID('{F935DC29-1CF0-11D0-ADB9-00C04FD58A0B}')
    _idlflags_ = ['dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def _get_Item(self, Name: hints.Incomplete) -> hints.Incomplete: ...
        def _set_Item(self, Name: hints.Incomplete, out_Value: hints.Incomplete) -> hints.Hresult: ...
        Item = hints.named_property('Item', _get_Item, _set_Item)
        __call__ = hints.to_dunder_call(Item)
        __getitem__ = hints.to_dunder_getitem(Item)
        __setitem__ = hints.to_dunder_setitem(Item)
        def Count(self) -> hints.Incomplete: ...
        __len__ = hints.to_dunder_len(Count)
        def _get_length(self) -> hints.Incomplete: ...
        length = hints.normal_property(_get_length)
        def _NewEnum(self) -> hints.Incomplete: ...
        __iter__ = hints.to_dunder_iter(_NewEnum)
        def Remove(self, Name: hints.Incomplete) -> hints.Hresult: ...


IWshShell._methods_ = [
    COMMETHOD(
        [dispid(100), 'propget'],
        HRESULT,
        'SpecialFolders',
        (['out', 'retval'], POINTER(POINTER(IWshCollection)), 'out_Folders')
    ),
    COMMETHOD(
        [dispid(200), 'propget'],
        HRESULT,
        'Environment',
        (['in', 'optional'], POINTER(VARIANT), 'Type'),
        (['out', 'retval'], POINTER(POINTER(IWshEnvironment)), 'out_Env')
    ),
    COMMETHOD(
        [dispid(1000)],
        HRESULT,
        'Run',
        (['in'], BSTR, 'Command'),
        (['in', 'optional'], POINTER(VARIANT), 'WindowStyle'),
        (['in', 'optional'], POINTER(VARIANT), 'WaitOnReturn'),
        (['out', 'retval'], POINTER(c_int), 'out_ExitCode')
    ),
    COMMETHOD(
        [dispid(1001)],
        HRESULT,
        'Popup',
        (['in'], BSTR, 'Text'),
        (['in', 'optional'], POINTER(VARIANT), 'SecondsToWait'),
        (['in', 'optional'], POINTER(VARIANT), 'Title'),
        (['in', 'optional'], POINTER(VARIANT), 'Type'),
        (['out', 'retval'], POINTER(c_int), 'out_Button')
    ),
    COMMETHOD(
        [dispid(1002)],
        HRESULT,
        'CreateShortcut',
        (['in'], BSTR, 'PathLink'),
        (['out', 'retval'], POINTER(POINTER(IDispatch)), 'out_Shortcut')
    ),
    COMMETHOD(
        [dispid(1006)],
        HRESULT,
        'ExpandEnvironmentStrings',
        (['in'], BSTR, 'Src'),
        (['out', 'retval'], POINTER(BSTR), 'out_Dst')
    ),
    COMMETHOD(
        [dispid(2000)],
        HRESULT,
        'RegRead',
        (['in'], BSTR, 'Name'),
        (['out', 'retval'], POINTER(VARIANT), 'out_Value')
    ),
    COMMETHOD(
        [dispid(2001)],
        HRESULT,
        'RegWrite',
        (['in'], BSTR, 'Name'),
        (['in'], POINTER(VARIANT), 'Value'),
        (['in', 'optional'], POINTER(VARIANT), 'Type')
    ),
    COMMETHOD(
        [dispid(2002)],
        HRESULT,
        'RegDelete',
        (['in'], BSTR, 'Name')
    ),
]

################################################################
# code template for IWshShell implementation
# class IWshShell_Impl(object):
#     @property
#     def SpecialFolders(self):
#         '-no docstring-'
#         #return out_Folders
#
#     @property
#     def Environment(self, Type):
#         '-no docstring-'
#         #return out_Env
#
#     def Run(self, Command, WindowStyle, WaitOnReturn):
#         '-no docstring-'
#         #return out_ExitCode
#
#     def Popup(self, Text, SecondsToWait, Title, Type):
#         '-no docstring-'
#         #return out_Button
#
#     def CreateShortcut(self, PathLink):
#         '-no docstring-'
#         #return out_Shortcut
#
#     def ExpandEnvironmentStrings(self, Src):
#         '-no docstring-'
#         #return out_Dst
#
#     def RegRead(self, Name):
#         '-no docstring-'
#         #return out_Value
#
#     def RegWrite(self, Name, Value, Type):
#         '-no docstring-'
#         #return 
#
#     def RegDelete(self, Name):
#         '-no docstring-'
#         #return 
#


class WshCollection(CoClass):
    """Generic Collection Object"""
    _reg_clsid_ = GUID('{387DAFF4-DA03-44D2-B0D1-80C927C905AC}')
    _idlflags_ = ['noncreatable']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


WshCollection._com_interfaces_ = [IWshCollection]


class Library(object):
    """Windows Script Host Object Model"""
    name = 'IWshRuntimeLibrary'
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


class IWshURLShortcut(skeletal_framework.utilities.generated_bindings._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    """URLShortcut Object"""
    _case_insensitive_ = True
    _iid_ = GUID('{F935DC2B-1CF0-11D0-ADB9-00C04FD58A0B}')
    _idlflags_ = ['dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def _get_FullName(self) -> hints.Incomplete: ...
        FullName = hints.normal_property(_get_FullName)
        def _get_TargetPath(self) -> hints.Incomplete: ...
        def _set_TargetPath(self, out_Path: hints.Incomplete) -> hints.Hresult: ...
        TargetPath = hints.normal_property(_get_TargetPath, _set_TargetPath)
        def Load(self, PathLink: hints.Incomplete) -> hints.Hresult: ...
        def Save(self) -> hints.Hresult: ...


IWshURLShortcut._methods_ = [
    COMMETHOD(
        [dispid(0), 'propget'],
        HRESULT,
        'FullName',
        (['out', 'retval'], POINTER(BSTR), 'out_FullName')
    ),
    COMMETHOD(
        [dispid(1005), 'propget'],
        HRESULT,
        'TargetPath',
        (['out', 'retval'], POINTER(BSTR), 'out_Path')
    ),
    COMMETHOD(
        [dispid(1005), 'propput'],
        HRESULT,
        'TargetPath',
        (['in'], BSTR, 'out_Path')
    ),
    COMMETHOD(
        [dispid(2000), 'hidden'],
        HRESULT,
        'Load',
        (['in'], BSTR, 'PathLink')
    ),
    COMMETHOD([dispid(2001)], HRESULT, 'Save'),
]

################################################################
# code template for IWshURLShortcut implementation
# class IWshURLShortcut_Impl(object):
#     @property
#     def FullName(self):
#         '-no docstring-'
#         #return out_FullName
#
#     def _get(self):
#         '-no docstring-'
#         #return out_Path
#     def _set(self, out_Path):
#         '-no docstring-'
#     TargetPath = property(_get, _set, doc = _set.__doc__)
#
#     def Load(self, PathLink):
#         '-no docstring-'
#         #return 
#
#     def Save(self):
#         '-no docstring-'
#         #return 
#


class Folders(CoClass):
    _reg_clsid_ = GUID('{C7C3F5B4-88A3-11D0-ABCB-00A0C90FFFC0}')
    _idlflags_ = ['noncreatable']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


class IFolderCollection(skeletal_framework.utilities.generated_bindings._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{C7C3F5A3-88A3-11D0-ABCB-00A0C90FFFC0}')
    _idlflags_ = ['hidden', 'dual', 'nonextensible', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def Add(self, Name: hints.Incomplete) -> 'IFolder': ...
        def _get_Item(self, Key: hints.Incomplete) -> 'IFolder': ...
        Item = hints.named_property('Item', _get_Item)
        __call__ = hints.to_dunder_call(Item)
        __getitem__ = hints.to_dunder_getitem(Item)
        __setitem__ = hints.to_dunder_setitem(Item)
        def _get__NewEnum(self) -> hints.Incomplete: ...
        _NewEnum = hints.normal_property(_get__NewEnum)
        __iter__ = hints.to_dunder_iter(_NewEnum)
        def _get_Count(self) -> hints.Incomplete: ...
        Count = hints.normal_property(_get_Count)
        __len__ = hints.to_dunder_len(Count)


Folders._com_interfaces_ = [IFolderCollection]


class WshEnvironment(CoClass):
    """Environment Variables Collection Object"""
    _reg_clsid_ = GUID('{F48229AF-E28C-42B5-BB92-E114E62BDD54}')
    _idlflags_ = ['noncreatable']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


WshEnvironment._com_interfaces_ = [IWshEnvironment]

IWshEnvironment._methods_ = [
    COMMETHOD(
        [dispid(0), 'propget'],
        HRESULT,
        'Item',
        (['in'], BSTR, 'Name'),
        (['out', 'retval'], POINTER(BSTR), 'out_Value')
    ),
    COMMETHOD(
        [dispid(0), 'propput'],
        HRESULT,
        'Item',
        (['in'], BSTR, 'Name'),
        (['in'], BSTR, 'out_Value')
    ),
    COMMETHOD(
        [dispid(1)],
        HRESULT,
        'Count',
        (['out', 'retval'], POINTER(c_int), 'out_Count')
    ),
    COMMETHOD(
        [dispid(2), 'propget'],
        HRESULT,
        'length',
        (['out', 'retval'], POINTER(c_int), 'out_Count')
    ),
    COMMETHOD(
        [dispid(-4)],
        HRESULT,
        '_NewEnum',
        (['out', 'retval'], POINTER(POINTER(IUnknown)), 'out_Enum')
    ),
    COMMETHOD(
        [dispid(1001)],
        HRESULT,
        'Remove',
        (['in'], BSTR, 'Name')
    ),
]

################################################################
# code template for IWshEnvironment implementation
# class IWshEnvironment_Impl(object):
#     def _get(self, Name):
#         '-no docstring-'
#         #return out_Value
#     def _set(self, Name, out_Value):
#         '-no docstring-'
#     Item = property(_get, _set, doc = _set.__doc__)
#
#     def Count(self):
#         '-no docstring-'
#         #return out_Count
#
#     @property
#     def length(self):
#         '-no docstring-'
#         #return out_Count
#
#     def _NewEnum(self):
#         '-no docstring-'
#         #return out_Enum
#
#     def Remove(self, Name):
#         '-no docstring-'
#         #return 
#


class IWshExec(skeletal_framework.utilities.generated_bindings._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    """WSH Exec Object"""
    _case_insensitive_ = True
    _iid_ = GUID('{08FED190-BE19-11D3-A28B-00104BD35090}')
    _idlflags_ = ['dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def _get_Status(self) -> hints.Incomplete: ...
        Status = hints.normal_property(_get_Status)
        def _get_StdIn(self) -> 'ITextStream': ...
        StdIn = hints.normal_property(_get_StdIn)
        def _get_StdOut(self) -> 'ITextStream': ...
        StdOut = hints.normal_property(_get_StdOut)
        def _get_StdErr(self) -> 'ITextStream': ...
        StdErr = hints.normal_property(_get_StdErr)
        def _get_ProcessID(self) -> hints.Incomplete: ...
        ProcessID = hints.normal_property(_get_ProcessID)
        def _get_ExitCode(self) -> hints.Incomplete: ...
        ExitCode = hints.normal_property(_get_ExitCode)
        def Terminate(self) -> hints.Hresult: ...


IWshExec._methods_ = [
    COMMETHOD(
        [dispid(1), 'propget'],
        HRESULT,
        'Status',
        (['out', 'retval'], POINTER(WshExecStatus), 'Status')
    ),
    COMMETHOD(
        [dispid(3), 'propget'],
        HRESULT,
        'StdIn',
        (['out', 'retval'], POINTER(POINTER(ITextStream)), 'ppts')
    ),
    COMMETHOD(
        [dispid(4), 'propget'],
        HRESULT,
        'StdOut',
        (['out', 'retval'], POINTER(POINTER(ITextStream)), 'ppts')
    ),
    COMMETHOD(
        [dispid(5), 'propget'],
        HRESULT,
        'StdErr',
        (['out', 'retval'], POINTER(POINTER(ITextStream)), 'ppts')
    ),
    COMMETHOD(
        [dispid(6), 'propget'],
        HRESULT,
        'ProcessID',
        (['out', 'retval'], POINTER(c_int), 'PID')
    ),
    COMMETHOD(
        [dispid(7), 'propget'],
        HRESULT,
        'ExitCode',
        (['out', 'retval'], POINTER(c_int), 'ExitCode')
    ),
    COMMETHOD([dispid(8)], HRESULT, 'Terminate'),
]

################################################################
# code template for IWshExec implementation
# class IWshExec_Impl(object):
#     @property
#     def Status(self):
#         '-no docstring-'
#         #return Status
#
#     @property
#     def StdIn(self):
#         '-no docstring-'
#         #return ppts
#
#     @property
#     def StdOut(self):
#         '-no docstring-'
#         #return ppts
#
#     @property
#     def StdErr(self):
#         '-no docstring-'
#         #return ppts
#
#     @property
#     def ProcessID(self):
#         '-no docstring-'
#         #return PID
#
#     @property
#     def ExitCode(self):
#         '-no docstring-'
#         #return ExitCode
#
#     def Terminate(self):
#         '-no docstring-'
#         #return 
#

ITextStream._methods_ = [
    COMMETHOD(
        [dispid(10000), 'propget'],
        HRESULT,
        'Line',
        (['out', 'retval'], POINTER(c_int), 'Line')
    ),
    COMMETHOD(
        [dispid(-529), 'propget'],
        HRESULT,
        'Column',
        (['out', 'retval'], POINTER(c_int), 'Column')
    ),
    COMMETHOD(
        [dispid(10002), 'propget'],
        HRESULT,
        'AtEndOfStream',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'EOS')
    ),
    COMMETHOD(
        [dispid(10003), 'propget'],
        HRESULT,
        'AtEndOfLine',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'EOL')
    ),
    COMMETHOD(
        [dispid(10004)],
        HRESULT,
        'Read',
        (['in'], c_int, 'Characters'),
        (['out', 'retval'], POINTER(BSTR), 'Text')
    ),
    COMMETHOD(
        [dispid(10005)],
        HRESULT,
        'ReadLine',
        (['out', 'retval'], POINTER(BSTR), 'Text')
    ),
    COMMETHOD(
        [dispid(10006)],
        HRESULT,
        'ReadAll',
        (['out', 'retval'], POINTER(BSTR), 'Text')
    ),
    COMMETHOD(
        [dispid(10007)],
        HRESULT,
        'Write',
        (['in'], BSTR, 'Text')
    ),
    COMMETHOD(
        [dispid(10008)],
        HRESULT,
        'WriteLine',
        (['in', 'optional'], BSTR, 'Text', '')
    ),
    COMMETHOD(
        [dispid(10009)],
        HRESULT,
        'WriteBlankLines',
        (['in'], c_int, 'Lines')
    ),
    COMMETHOD(
        [dispid(10010)],
        HRESULT,
        'Skip',
        (['in'], c_int, 'Characters')
    ),
    COMMETHOD([dispid(10011)], HRESULT, 'SkipLine'),
    COMMETHOD([dispid(10012)], HRESULT, 'Close'),
]

################################################################
# code template for ITextStream implementation
# class ITextStream_Impl(object):
#     @property
#     def Line(self):
#         '-no docstring-'
#         #return Line
#
#     @property
#     def Column(self):
#         '-no docstring-'
#         #return Column
#
#     @property
#     def AtEndOfStream(self):
#         '-no docstring-'
#         #return EOS
#
#     @property
#     def AtEndOfLine(self):
#         '-no docstring-'
#         #return EOL
#
#     def Read(self, Characters):
#         '-no docstring-'
#         #return Text
#
#     def ReadLine(self):
#         '-no docstring-'
#         #return Text
#
#     def ReadAll(self):
#         '-no docstring-'
#         #return Text
#
#     def Write(self, Text):
#         '-no docstring-'
#         #return 
#
#     def WriteLine(self, Text):
#         '-no docstring-'
#         #return 
#
#     def WriteBlankLines(self, Lines):
#         '-no docstring-'
#         #return 
#
#     def Skip(self, Characters):
#         '-no docstring-'
#         #return 
#
#     def SkipLine(self):
#         '-no docstring-'
#         #return 
#
#     def Close(self):
#         '-no docstring-'
#         #return 
#


class Files(CoClass):
    _reg_clsid_ = GUID('{C7C3F5B6-88A3-11D0-ABCB-00A0C90FFFC0}')
    _idlflags_ = ['noncreatable']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


Files._com_interfaces_ = [IFileCollection]

IWshShell2._methods_ = [
    COMMETHOD(
        [dispid(3000)],
        HRESULT,
        'LogEvent',
        (['in'], POINTER(VARIANT), 'Type'),
        (['in'], BSTR, 'Message'),
        (['in', 'optional'], BSTR, 'Target', ''),
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'out_Success')
    ),
    COMMETHOD(
        [dispid(3010)],
        HRESULT,
        'AppActivate',
        (['in'], POINTER(VARIANT), 'App'),
        (['in', 'optional'], POINTER(VARIANT), 'Wait'),
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'out_Success')
    ),
    COMMETHOD(
        [dispid(3011)],
        HRESULT,
        'SendKeys',
        (['in'], BSTR, 'Keys'),
        (['in', 'optional'], POINTER(VARIANT), 'Wait')
    ),
]

################################################################
# code template for IWshShell2 implementation
# class IWshShell2_Impl(object):
#     def LogEvent(self, Type, Message, Target):
#         '-no docstring-'
#         #return out_Success
#
#     def AppActivate(self, App, Wait):
#         '-no docstring-'
#         #return out_Success
#
#     def SendKeys(self, Keys, Wait):
#         '-no docstring-'
#         #return 
#

IWshShell3._methods_ = [
    COMMETHOD(
        [dispid(3012)],
        HRESULT,
        'Exec',
        (['in'], BSTR, 'Command'),
        (['out', 'retval'], POINTER(POINTER(IWshExec)), 'ppExec')
    ),
    COMMETHOD(
        [dispid(3013), 'propget'],
        HRESULT,
        'CurrentDirectory',
        (['out', 'retval'], POINTER(BSTR), 'out_Directory')
    ),
    COMMETHOD(
        [dispid(3013), 'propput'],
        HRESULT,
        'CurrentDirectory',
        (['in'], BSTR, 'out_Directory')
    ),
]

################################################################
# code template for IWshShell3 implementation
# class IWshShell3_Impl(object):
#     def Exec(self, Command):
#         '-no docstring-'
#         #return ppExec
#
#     def _get(self):
#         '-no docstring-'
#         #return out_Directory
#     def _set(self, out_Directory):
#         '-no docstring-'
#     CurrentDirectory = property(_get, _set, doc = _set.__doc__)
#

IWshNetwork._methods_ = [
    COMMETHOD(
        [dispid(1610743808), 'propget'],
        HRESULT,
        'UserDomain',
        (['out', 'retval'], POINTER(BSTR), 'out_UserDomain')
    ),
    COMMETHOD(
        [dispid(1610743809), 'propget'],
        HRESULT,
        'UserName',
        (['out', 'retval'], POINTER(BSTR), 'out_UserName')
    ),
    COMMETHOD(
        [dispid(1610743810), 'hidden', 'propget'],
        HRESULT,
        'UserProfile',
        (['out', 'retval'], POINTER(BSTR), 'out_UserProfile')
    ),
    COMMETHOD(
        [dispid(1610743811), 'propget'],
        HRESULT,
        'ComputerName',
        (['out', 'retval'], POINTER(BSTR), 'out_ComputerName')
    ),
    COMMETHOD(
        [dispid(1610743812), 'hidden', 'propget'],
        HRESULT,
        'Organization',
        (['out', 'retval'], POINTER(BSTR), 'out_Organization')
    ),
    COMMETHOD(
        [dispid(1610743813), 'hidden', 'propget'],
        HRESULT,
        'Site',
        (['out', 'retval'], POINTER(BSTR), 'out_Site')
    ),
    COMMETHOD(
        [dispid(1000)],
        HRESULT,
        'MapNetworkDrive',
        (['in'], BSTR, 'LocalName'),
        (['in'], BSTR, 'RemoteName'),
        (['in', 'optional'], POINTER(VARIANT), 'UpdateProfile'),
        (['in', 'optional'], POINTER(VARIANT), 'UserName'),
        (['in', 'optional'], POINTER(VARIANT), 'Password')
    ),
    COMMETHOD(
        [dispid(1001)],
        HRESULT,
        'RemoveNetworkDrive',
        (['in'], BSTR, 'Name'),
        (['in', 'optional'], POINTER(VARIANT), 'Force'),
        (['in', 'optional'], POINTER(VARIANT), 'UpdateProfile')
    ),
    COMMETHOD(
        [dispid(1002)],
        HRESULT,
        'EnumNetworkDrives',
        (['out', 'retval'], POINTER(POINTER(IWshCollection)), 'out_Enum')
    ),
    COMMETHOD(
        [dispid(2000)],
        HRESULT,
        'AddPrinterConnection',
        (['in'], BSTR, 'LocalName'),
        (['in'], BSTR, 'RemoteName'),
        (['in', 'optional'], POINTER(VARIANT), 'UpdateProfile'),
        (['in', 'optional'], POINTER(VARIANT), 'UserName'),
        (['in', 'optional'], POINTER(VARIANT), 'Password')
    ),
    COMMETHOD(
        [dispid(2001)],
        HRESULT,
        'RemovePrinterConnection',
        (['in'], BSTR, 'Name'),
        (['in', 'optional'], POINTER(VARIANT), 'Force'),
        (['in', 'optional'], POINTER(VARIANT), 'UpdateProfile')
    ),
    COMMETHOD(
        [dispid(2002)],
        HRESULT,
        'EnumPrinterConnections',
        (['out', 'retval'], POINTER(POINTER(IWshCollection)), 'out_Enum')
    ),
    COMMETHOD(
        [dispid(2003)],
        HRESULT,
        'SetDefaultPrinter',
        (['in'], BSTR, 'Name')
    ),
]

################################################################
# code template for IWshNetwork implementation
# class IWshNetwork_Impl(object):
#     @property
#     def UserDomain(self):
#         '-no docstring-'
#         #return out_UserDomain
#
#     @property
#     def UserName(self):
#         '-no docstring-'
#         #return out_UserName
#
#     @property
#     def UserProfile(self):
#         '-no docstring-'
#         #return out_UserProfile
#
#     @property
#     def ComputerName(self):
#         '-no docstring-'
#         #return out_ComputerName
#
#     @property
#     def Organization(self):
#         '-no docstring-'
#         #return out_Organization
#
#     @property
#     def Site(self):
#         '-no docstring-'
#         #return out_Site
#
#     def MapNetworkDrive(self, LocalName, RemoteName, UpdateProfile, UserName, Password):
#         '-no docstring-'
#         #return 
#
#     def RemoveNetworkDrive(self, Name, Force, UpdateProfile):
#         '-no docstring-'
#         #return 
#
#     def EnumNetworkDrives(self):
#         '-no docstring-'
#         #return out_Enum
#
#     def AddPrinterConnection(self, LocalName, RemoteName, UpdateProfile, UserName, Password):
#         '-no docstring-'
#         #return 
#
#     def RemovePrinterConnection(self, Name, Force, UpdateProfile):
#         '-no docstring-'
#         #return 
#
#     def EnumPrinterConnections(self):
#         '-no docstring-'
#         #return out_Enum
#
#     def SetDefaultPrinter(self, Name):
#         '-no docstring-'
#         #return 
#

IWshNetwork2._methods_ = [
    COMMETHOD(
        [dispid(2004)],
        HRESULT,
        'AddWindowsPrinterConnection',
        (['in'], BSTR, 'PrinterName'),
        (['in', 'optional'], BSTR, 'DriverName', ''),
        (['in', 'optional'], BSTR, 'Port', 'LPT1')
    ),
]

################################################################
# code template for IWshNetwork2 implementation
# class IWshNetwork2_Impl(object):
#     def AddWindowsPrinterConnection(self, PrinterName, DriverName, Port):
#         '-no docstring-'
#         #return 
#


class TextStream(CoClass):
    _reg_clsid_ = GUID('{0BB02EC0-EF49-11CF-8940-00A0C9054228}')
    _idlflags_ = ['noncreatable']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


TextStream._com_interfaces_ = [ITextStream]


class IWshCollection_Class(CoClass):
    """Generic Collection Object"""
    _reg_clsid_ = GUID('{F935DC28-1CF0-11D0-ADB9-00C04FD58A0B}')
    _idlflags_ = ['hidden', 'noncreatable']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


IWshCollection_Class._com_interfaces_ = [IWshCollection]


class WshShortcut(CoClass):
    """Shortcut Object"""
    _reg_clsid_ = GUID('{A548B8E4-51D5-4661-8824-DAA1D893DFB2}')
    _idlflags_ = ['noncreatable']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


class IWshShortcut(skeletal_framework.utilities.generated_bindings._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    """Shortcut Object"""
    _case_insensitive_ = True
    _iid_ = GUID('{F935DC23-1CF0-11D0-ADB9-00C04FD58A0B}')
    _idlflags_ = ['dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def _get_FullName(self) -> hints.Incomplete: ...
        FullName = hints.normal_property(_get_FullName)
        def _get_Arguments(self) -> hints.Incomplete: ...
        def _set_Arguments(self, out_Arguments: hints.Incomplete) -> hints.Hresult: ...
        Arguments = hints.normal_property(_get_Arguments, _set_Arguments)
        def _get_Description(self) -> hints.Incomplete: ...
        def _set_Description(self, out_Description: hints.Incomplete) -> hints.Hresult: ...
        Description = hints.normal_property(_get_Description, _set_Description)
        def _get_Hotkey(self) -> hints.Incomplete: ...
        def _set_Hotkey(self, out_HotKey: hints.Incomplete) -> hints.Hresult: ...
        Hotkey = hints.normal_property(_get_Hotkey, _set_Hotkey)
        def _get_IconLocation(self) -> hints.Incomplete: ...
        def _set_IconLocation(self, out_IconPath: hints.Incomplete) -> hints.Hresult: ...
        IconLocation = hints.normal_property(_get_IconLocation, _set_IconLocation)
        def _set_RelativePath(self, rhs: hints.Incomplete) -> hints.Hresult: ...
        RelativePath = hints.normal_property(fset=_set_RelativePath)
        def _get_TargetPath(self) -> hints.Incomplete: ...
        def _set_TargetPath(self, out_Path: hints.Incomplete) -> hints.Hresult: ...
        TargetPath = hints.normal_property(_get_TargetPath, _set_TargetPath)
        def _get_WindowStyle(self) -> hints.Incomplete: ...
        def _set_WindowStyle(self, out_ShowCmd: hints.Incomplete) -> hints.Hresult: ...
        WindowStyle = hints.normal_property(_get_WindowStyle, _set_WindowStyle)
        def _get_WorkingDirectory(self) -> hints.Incomplete: ...
        def _set_WorkingDirectory(self, out_WorkingDirectory: hints.Incomplete) -> hints.Hresult: ...
        WorkingDirectory = hints.normal_property(_get_WorkingDirectory, _set_WorkingDirectory)
        def Load(self, PathLink: hints.Incomplete) -> hints.Hresult: ...
        def Save(self) -> hints.Hresult: ...


WshShortcut._com_interfaces_ = [IWshShortcut]

IFolder._methods_ = [
    COMMETHOD(
        [dispid(0), 'propget'],
        HRESULT,
        'Path',
        (['out', 'retval'], POINTER(BSTR), 'pbstrPath')
    ),
    COMMETHOD(
        [dispid(1000), 'propget'],
        HRESULT,
        'Name',
        (['out', 'retval'], POINTER(BSTR), 'pbstrName')
    ),
    COMMETHOD(
        [dispid(1000), 'propput'],
        HRESULT,
        'Name',
        (['in'], BSTR, 'pbstrName')
    ),
    COMMETHOD(
        [dispid(1002), 'propget'],
        HRESULT,
        'ShortPath',
        (['out', 'retval'], POINTER(BSTR), 'pbstrPath')
    ),
    COMMETHOD(
        [dispid(1001), 'propget'],
        HRESULT,
        'ShortName',
        (['out', 'retval'], POINTER(BSTR), 'pbstrName')
    ),
    COMMETHOD(
        [dispid(1004), 'propget'],
        HRESULT,
        'Drive',
        (['out', 'retval'], POINTER(POINTER(IDrive)), 'ppdrive')
    ),
    COMMETHOD(
        [dispid(1005), 'propget'],
        HRESULT,
        'ParentFolder',
        (['out', 'retval'], POINTER(POINTER(IFolder)), 'ppfolder')
    ),
    COMMETHOD(
        [dispid(1003), 'propget'],
        HRESULT,
        'Attributes',
        (['out', 'retval'], POINTER(FileAttribute), 'pfa')
    ),
    COMMETHOD(
        [dispid(1003), 'propput'],
        HRESULT,
        'Attributes',
        (['in'], FileAttribute, 'pfa')
    ),
    COMMETHOD(
        [dispid(1006), 'propget'],
        HRESULT,
        'DateCreated',
        (['out', 'retval'], POINTER(c_double), 'pdate')
    ),
    COMMETHOD(
        [dispid(1007), 'propget'],
        HRESULT,
        'DateLastModified',
        (['out', 'retval'], POINTER(c_double), 'pdate')
    ),
    COMMETHOD(
        [dispid(1008), 'propget'],
        HRESULT,
        'DateLastAccessed',
        (['out', 'retval'], POINTER(c_double), 'pdate')
    ),
    COMMETHOD(
        [dispid(1010), 'propget'],
        HRESULT,
        'Type',
        (['out', 'retval'], POINTER(BSTR), 'pbstrType')
    ),
    COMMETHOD(
        [dispid(1201)],
        HRESULT,
        'Delete',
        (['in', 'optional'], VARIANT_BOOL, 'Force', False)
    ),
    COMMETHOD(
        [dispid(1203)],
        HRESULT,
        'Copy',
        (['in'], BSTR, 'Destination'),
        (['in', 'optional'], VARIANT_BOOL, 'OverWriteFiles', True)
    ),
    COMMETHOD(
        [dispid(1205)],
        HRESULT,
        'Move',
        (['in'], BSTR, 'Destination')
    ),
    COMMETHOD(
        [dispid(10000), 'propget'],
        HRESULT,
        'IsRootFolder',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pfRootFolder')
    ),
    COMMETHOD(
        [dispid(1009), 'propget'],
        HRESULT,
        'Size',
        (['out', 'retval'], POINTER(VARIANT), 'pvarSize')
    ),
    COMMETHOD(
        [dispid(10001), 'propget'],
        HRESULT,
        'SubFolders',
        (['out', 'retval'], POINTER(POINTER(IFolderCollection)), 'ppfolders')
    ),
    COMMETHOD(
        [dispid(10002), 'propget'],
        HRESULT,
        'Files',
        (['out', 'retval'], POINTER(POINTER(IFileCollection)), 'ppfiles')
    ),
    COMMETHOD(
        [dispid(1101)],
        HRESULT,
        'CreateTextFile',
        (['in'], BSTR, 'FileName'),
        (['in', 'optional'], VARIANT_BOOL, 'Overwrite', True),
        (['in', 'optional'], VARIANT_BOOL, 'Unicode', False),
        (['out', 'retval'], POINTER(POINTER(ITextStream)), 'ppts')
    ),
]

################################################################
# code template for IFolder implementation
# class IFolder_Impl(object):
#     @property
#     def Path(self):
#         '-no docstring-'
#         #return pbstrPath
#
#     def _get(self):
#         '-no docstring-'
#         #return pbstrName
#     def _set(self, pbstrName):
#         '-no docstring-'
#     Name = property(_get, _set, doc = _set.__doc__)
#
#     @property
#     def ShortPath(self):
#         '-no docstring-'
#         #return pbstrPath
#
#     @property
#     def ShortName(self):
#         '-no docstring-'
#         #return pbstrName
#
#     @property
#     def Drive(self):
#         '-no docstring-'
#         #return ppdrive
#
#     @property
#     def ParentFolder(self):
#         '-no docstring-'
#         #return ppfolder
#
#     def _get(self):
#         '-no docstring-'
#         #return pfa
#     def _set(self, pfa):
#         '-no docstring-'
#     Attributes = property(_get, _set, doc = _set.__doc__)
#
#     @property
#     def DateCreated(self):
#         '-no docstring-'
#         #return pdate
#
#     @property
#     def DateLastModified(self):
#         '-no docstring-'
#         #return pdate
#
#     @property
#     def DateLastAccessed(self):
#         '-no docstring-'
#         #return pdate
#
#     @property
#     def Type(self):
#         '-no docstring-'
#         #return pbstrType
#
#     def Delete(self, Force):
#         '-no docstring-'
#         #return 
#
#     def Copy(self, Destination, OverWriteFiles):
#         '-no docstring-'
#         #return 
#
#     def Move(self, Destination):
#         '-no docstring-'
#         #return 
#
#     @property
#     def IsRootFolder(self):
#         '-no docstring-'
#         #return pfRootFolder
#
#     @property
#     def Size(self):
#         '-no docstring-'
#         #return pvarSize
#
#     @property
#     def SubFolders(self):
#         '-no docstring-'
#         #return ppfolders
#
#     @property
#     def Files(self):
#         '-no docstring-'
#         #return ppfiles
#
#     def CreateTextFile(self, FileName, Overwrite, Unicode):
#         '-no docstring-'
#         #return ppts
#


class FileSystemObject(CoClass):
    _reg_clsid_ = GUID('{0D43FE01-F093-11CF-8940-00A0C9054228}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


FileSystemObject._com_interfaces_ = [IFileSystem3]


class Folder(CoClass):
    _reg_clsid_ = GUID('{C7C3F5B3-88A3-11D0-ABCB-00A0C90FFFC0}')
    _idlflags_ = ['noncreatable']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


Folder._com_interfaces_ = [IFolder]


class Drives(CoClass):
    _reg_clsid_ = GUID('{C7C3F5B2-88A3-11D0-ABCB-00A0C90FFFC0}')
    _idlflags_ = ['noncreatable']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


Drives._com_interfaces_ = [IDriveCollection]


class IWshEnvironment_Class(CoClass):
    """Environment Variables Collection Object"""
    _reg_clsid_ = GUID('{F935DC2A-1CF0-11D0-ADB9-00C04FD58A0B}')
    _idlflags_ = ['hidden', 'noncreatable']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


IWshEnvironment_Class._com_interfaces_ = [IWshEnvironment]


class IWshShortcut_Class(CoClass):
    """Shortcut Object"""
    _reg_clsid_ = GUID('{F935DC24-1CF0-11D0-ADB9-00C04FD58A0B}')
    _idlflags_ = ['hidden', 'noncreatable']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


IWshShortcut_Class._com_interfaces_ = [IWshShortcut]

IWshCollection._methods_ = [
    COMMETHOD(
        [dispid(0)],
        HRESULT,
        'Item',
        (['in'], POINTER(VARIANT), 'Index'),
        (['out', 'retval'], POINTER(VARIANT), 'out_Value')
    ),
    COMMETHOD(
        [dispid(1)],
        HRESULT,
        'Count',
        (['out', 'retval'], POINTER(c_int), 'out_Count')
    ),
    COMMETHOD(
        [dispid(2), 'propget'],
        HRESULT,
        'length',
        (['out', 'retval'], POINTER(c_int), 'out_Count')
    ),
    COMMETHOD(
        [dispid(-4)],
        HRESULT,
        '_NewEnum',
        (['out', 'retval'], POINTER(POINTER(IUnknown)), 'out_Enum')
    ),
]

################################################################
# code template for IWshCollection implementation
# class IWshCollection_Impl(object):
#     def Item(self, Index):
#         '-no docstring-'
#         #return out_Value
#
#     def Count(self):
#         '-no docstring-'
#         #return out_Count
#
#     @property
#     def length(self):
#         '-no docstring-'
#         #return out_Count
#
#     def _NewEnum(self):
#         '-no docstring-'
#         #return out_Enum
#


class IWshURLShortcut_Class(CoClass):
    """URLShortcut Object"""
    _reg_clsid_ = GUID('{F935DC2C-1CF0-11D0-ADB9-00C04FD58A0B}')
    _idlflags_ = ['hidden', 'noncreatable']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


IWshURLShortcut_Class._com_interfaces_ = [IWshURLShortcut]

IFile._methods_ = [
    COMMETHOD(
        [dispid(0), 'propget'],
        HRESULT,
        'Path',
        (['out', 'retval'], POINTER(BSTR), 'pbstrPath')
    ),
    COMMETHOD(
        [dispid(1000), 'propget'],
        HRESULT,
        'Name',
        (['out', 'retval'], POINTER(BSTR), 'pbstrName')
    ),
    COMMETHOD(
        [dispid(1000), 'propput'],
        HRESULT,
        'Name',
        (['in'], BSTR, 'pbstrName')
    ),
    COMMETHOD(
        [dispid(1002), 'propget'],
        HRESULT,
        'ShortPath',
        (['out', 'retval'], POINTER(BSTR), 'pbstrPath')
    ),
    COMMETHOD(
        [dispid(1001), 'propget'],
        HRESULT,
        'ShortName',
        (['out', 'retval'], POINTER(BSTR), 'pbstrName')
    ),
    COMMETHOD(
        [dispid(1004), 'propget'],
        HRESULT,
        'Drive',
        (['out', 'retval'], POINTER(POINTER(IDrive)), 'ppdrive')
    ),
    COMMETHOD(
        [dispid(1005), 'propget'],
        HRESULT,
        'ParentFolder',
        (['out', 'retval'], POINTER(POINTER(IFolder)), 'ppfolder')
    ),
    COMMETHOD(
        [dispid(1003), 'propget'],
        HRESULT,
        'Attributes',
        (['out', 'retval'], POINTER(FileAttribute), 'pfa')
    ),
    COMMETHOD(
        [dispid(1003), 'propput'],
        HRESULT,
        'Attributes',
        (['in'], FileAttribute, 'pfa')
    ),
    COMMETHOD(
        [dispid(1006), 'propget'],
        HRESULT,
        'DateCreated',
        (['out', 'retval'], POINTER(c_double), 'pdate')
    ),
    COMMETHOD(
        [dispid(1007), 'propget'],
        HRESULT,
        'DateLastModified',
        (['out', 'retval'], POINTER(c_double), 'pdate')
    ),
    COMMETHOD(
        [dispid(1008), 'propget'],
        HRESULT,
        'DateLastAccessed',
        (['out', 'retval'], POINTER(c_double), 'pdate')
    ),
    COMMETHOD(
        [dispid(1009), 'propget'],
        HRESULT,
        'Size',
        (['out', 'retval'], POINTER(VARIANT), 'pvarSize')
    ),
    COMMETHOD(
        [dispid(1010), 'propget'],
        HRESULT,
        'Type',
        (['out', 'retval'], POINTER(BSTR), 'pbstrType')
    ),
    COMMETHOD(
        [dispid(1200)],
        HRESULT,
        'Delete',
        (['in', 'optional'], VARIANT_BOOL, 'Force', False)
    ),
    COMMETHOD(
        [dispid(1202)],
        HRESULT,
        'Copy',
        (['in'], BSTR, 'Destination'),
        (['in', 'optional'], VARIANT_BOOL, 'OverWriteFiles', True)
    ),
    COMMETHOD(
        [dispid(1204)],
        HRESULT,
        'Move',
        (['in'], BSTR, 'Destination')
    ),
    COMMETHOD(
        [dispid(1100)],
        HRESULT,
        'OpenAsTextStream',
        (['in', 'optional'], IOMode, 'IOMode', 1),
        (['in', 'optional'], Tristate, 'Format', 0),
        (['out', 'retval'], POINTER(POINTER(ITextStream)), 'ppts')
    ),
]

################################################################
# code template for IFile implementation
# class IFile_Impl(object):
#     @property
#     def Path(self):
#         '-no docstring-'
#         #return pbstrPath
#
#     def _get(self):
#         '-no docstring-'
#         #return pbstrName
#     def _set(self, pbstrName):
#         '-no docstring-'
#     Name = property(_get, _set, doc = _set.__doc__)
#
#     @property
#     def ShortPath(self):
#         '-no docstring-'
#         #return pbstrPath
#
#     @property
#     def ShortName(self):
#         '-no docstring-'
#         #return pbstrName
#
#     @property
#     def Drive(self):
#         '-no docstring-'
#         #return ppdrive
#
#     @property
#     def ParentFolder(self):
#         '-no docstring-'
#         #return ppfolder
#
#     def _get(self):
#         '-no docstring-'
#         #return pfa
#     def _set(self, pfa):
#         '-no docstring-'
#     Attributes = property(_get, _set, doc = _set.__doc__)
#
#     @property
#     def DateCreated(self):
#         '-no docstring-'
#         #return pdate
#
#     @property
#     def DateLastModified(self):
#         '-no docstring-'
#         #return pdate
#
#     @property
#     def DateLastAccessed(self):
#         '-no docstring-'
#         #return pdate
#
#     @property
#     def Size(self):
#         '-no docstring-'
#         #return pvarSize
#
#     @property
#     def Type(self):
#         '-no docstring-'
#         #return pbstrType
#
#     def Delete(self, Force):
#         '-no docstring-'
#         #return 
#
#     def Copy(self, Destination, OverWriteFiles):
#         '-no docstring-'
#         #return 
#
#     def Move(self, Destination):
#         '-no docstring-'
#         #return 
#
#     def OpenAsTextStream(self, IOMode, Format):
#         '-no docstring-'
#         #return ppts
#


class Drive(CoClass):
    _reg_clsid_ = GUID('{C7C3F5B1-88A3-11D0-ABCB-00A0C90FFFC0}')
    _idlflags_ = ['noncreatable']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


Drive._com_interfaces_ = [IDrive]


class WshURLShortcut(CoClass):
    """URLShortcut Object"""
    _reg_clsid_ = GUID('{50E13488-6F1E-4450-96B0-873755403955}')
    _idlflags_ = ['noncreatable']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


WshURLShortcut._com_interfaces_ = [IWshURLShortcut]

IWshShortcut._methods_ = [
    COMMETHOD(
        [dispid(0), 'propget'],
        HRESULT,
        'FullName',
        (['out', 'retval'], POINTER(BSTR), 'out_FullName')
    ),
    COMMETHOD(
        [dispid(1000), 'propget'],
        HRESULT,
        'Arguments',
        (['out', 'retval'], POINTER(BSTR), 'out_Arguments')
    ),
    COMMETHOD(
        [dispid(1000), 'propput'],
        HRESULT,
        'Arguments',
        (['in'], BSTR, 'out_Arguments')
    ),
    COMMETHOD(
        [dispid(1001), 'propget'],
        HRESULT,
        'Description',
        (['out', 'retval'], POINTER(BSTR), 'out_Description')
    ),
    COMMETHOD(
        [dispid(1001), 'propput'],
        HRESULT,
        'Description',
        (['in'], BSTR, 'out_Description')
    ),
    COMMETHOD(
        [dispid(1002), 'propget'],
        HRESULT,
        'Hotkey',
        (['out', 'retval'], POINTER(BSTR), 'out_HotKey')
    ),
    COMMETHOD(
        [dispid(1002), 'propput'],
        HRESULT,
        'Hotkey',
        (['in'], BSTR, 'out_HotKey')
    ),
    COMMETHOD(
        [dispid(1003), 'propget'],
        HRESULT,
        'IconLocation',
        (['out', 'retval'], POINTER(BSTR), 'out_IconPath')
    ),
    COMMETHOD(
        [dispid(1003), 'propput'],
        HRESULT,
        'IconLocation',
        (['in'], BSTR, 'out_IconPath')
    ),
    COMMETHOD(
        [dispid(1004), 'propput'],
        HRESULT,
        'RelativePath',
        (['in'], BSTR, 'rhs')
    ),
    COMMETHOD(
        [dispid(1005), 'propget'],
        HRESULT,
        'TargetPath',
        (['out', 'retval'], POINTER(BSTR), 'out_Path')
    ),
    COMMETHOD(
        [dispid(1005), 'propput'],
        HRESULT,
        'TargetPath',
        (['in'], BSTR, 'out_Path')
    ),
    COMMETHOD(
        [dispid(1006), 'propget'],
        HRESULT,
        'WindowStyle',
        (['out', 'retval'], POINTER(c_int), 'out_ShowCmd')
    ),
    COMMETHOD(
        [dispid(1006), 'propput'],
        HRESULT,
        'WindowStyle',
        (['in'], c_int, 'out_ShowCmd')
    ),
    COMMETHOD(
        [dispid(1007), 'propget'],
        HRESULT,
        'WorkingDirectory',
        (['out', 'retval'], POINTER(BSTR), 'out_WorkingDirectory')
    ),
    COMMETHOD(
        [dispid(1007), 'propput'],
        HRESULT,
        'WorkingDirectory',
        (['in'], BSTR, 'out_WorkingDirectory')
    ),
    COMMETHOD(
        [dispid(2000), 'hidden'],
        HRESULT,
        'Load',
        (['in'], BSTR, 'PathLink')
    ),
    COMMETHOD([dispid(2001)], HRESULT, 'Save'),
]

################################################################
# code template for IWshShortcut implementation
# class IWshShortcut_Impl(object):
#     @property
#     def FullName(self):
#         '-no docstring-'
#         #return out_FullName
#
#     def _get(self):
#         '-no docstring-'
#         #return out_Arguments
#     def _set(self, out_Arguments):
#         '-no docstring-'
#     Arguments = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         '-no docstring-'
#         #return out_Description
#     def _set(self, out_Description):
#         '-no docstring-'
#     Description = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         '-no docstring-'
#         #return out_HotKey
#     def _set(self, out_HotKey):
#         '-no docstring-'
#     Hotkey = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         '-no docstring-'
#         #return out_IconPath
#     def _set(self, out_IconPath):
#         '-no docstring-'
#     IconLocation = property(_get, _set, doc = _set.__doc__)
#
#     def _set(self, rhs):
#         '-no docstring-'
#     RelativePath = property(fset = _set, doc = _set.__doc__)
#
#     def _get(self):
#         '-no docstring-'
#         #return out_Path
#     def _set(self, out_Path):
#         '-no docstring-'
#     TargetPath = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         '-no docstring-'
#         #return out_ShowCmd
#     def _set(self, out_ShowCmd):
#         '-no docstring-'
#     WindowStyle = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         '-no docstring-'
#         #return out_WorkingDirectory
#     def _set(self, out_WorkingDirectory):
#         '-no docstring-'
#     WorkingDirectory = property(_get, _set, doc = _set.__doc__)
#
#     def Load(self, PathLink):
#         '-no docstring-'
#         #return 
#
#     def Save(self):
#         '-no docstring-'
#         #return 
#


class WshNetwork(CoClass):
    """Network Object"""
    _reg_clsid_ = GUID('{093FF999-1EA0-4079-9525-9614C3504B74}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


WshNetwork._com_interfaces_ = [IWshNetwork2]

IDrive._methods_ = [
    COMMETHOD(
        [dispid(0), 'propget'],
        HRESULT,
        'Path',
        (['out', 'retval'], POINTER(BSTR), 'pbstrPath')
    ),
    COMMETHOD(
        [dispid(10000), 'propget'],
        HRESULT,
        'DriveLetter',
        (['out', 'retval'], POINTER(BSTR), 'pbstrLetter')
    ),
    COMMETHOD(
        [dispid(10001), 'propget'],
        HRESULT,
        'ShareName',
        (['out', 'retval'], POINTER(BSTR), 'pbstrShareName')
    ),
    COMMETHOD(
        [dispid(10002), 'propget'],
        HRESULT,
        'DriveType',
        (['out', 'retval'], POINTER(DriveTypeConst), 'pdt')
    ),
    COMMETHOD(
        [dispid(10003), 'propget'],
        HRESULT,
        'RootFolder',
        (['out', 'retval'], POINTER(POINTER(IFolder)), 'ppfolder')
    ),
    COMMETHOD(
        [dispid(10005), 'propget'],
        HRESULT,
        'AvailableSpace',
        (['out', 'retval'], POINTER(VARIANT), 'pvarAvail')
    ),
    COMMETHOD(
        [dispid(10004), 'propget'],
        HRESULT,
        'FreeSpace',
        (['out', 'retval'], POINTER(VARIANT), 'pvarFree')
    ),
    COMMETHOD(
        [dispid(10006), 'propget'],
        HRESULT,
        'TotalSize',
        (['out', 'retval'], POINTER(VARIANT), 'pvarTotal')
    ),
    COMMETHOD(
        [dispid(10007), 'propget'],
        HRESULT,
        'VolumeName',
        (['out', 'retval'], POINTER(BSTR), 'pbstrName')
    ),
    COMMETHOD(
        [dispid(10007), 'propput'],
        HRESULT,
        'VolumeName',
        (['in'], BSTR, 'pbstrName')
    ),
    COMMETHOD(
        [dispid(10008), 'propget'],
        HRESULT,
        'FileSystem',
        (['out', 'retval'], POINTER(BSTR), 'pbstrFileSystem')
    ),
    COMMETHOD(
        [dispid(10009), 'propget'],
        HRESULT,
        'SerialNumber',
        (['out', 'retval'], POINTER(c_int), 'pulSerialNumber')
    ),
    COMMETHOD(
        [dispid(10010), 'propget'],
        HRESULT,
        'IsReady',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pfReady')
    ),
]

################################################################
# code template for IDrive implementation
# class IDrive_Impl(object):
#     @property
#     def Path(self):
#         '-no docstring-'
#         #return pbstrPath
#
#     @property
#     def DriveLetter(self):
#         '-no docstring-'
#         #return pbstrLetter
#
#     @property
#     def ShareName(self):
#         '-no docstring-'
#         #return pbstrShareName
#
#     @property
#     def DriveType(self):
#         '-no docstring-'
#         #return pdt
#
#     @property
#     def RootFolder(self):
#         '-no docstring-'
#         #return ppfolder
#
#     @property
#     def AvailableSpace(self):
#         '-no docstring-'
#         #return pvarAvail
#
#     @property
#     def FreeSpace(self):
#         '-no docstring-'
#         #return pvarFree
#
#     @property
#     def TotalSize(self):
#         '-no docstring-'
#         #return pvarTotal
#
#     def _get(self):
#         '-no docstring-'
#         #return pbstrName
#     def _set(self, pbstrName):
#         '-no docstring-'
#     VolumeName = property(_get, _set, doc = _set.__doc__)
#
#     @property
#     def FileSystem(self):
#         '-no docstring-'
#         #return pbstrFileSystem
#
#     @property
#     def SerialNumber(self):
#         '-no docstring-'
#         #return pulSerialNumber
#
#     @property
#     def IsReady(self):
#         '-no docstring-'
#         #return pfReady
#

IFolderCollection._methods_ = [
    COMMETHOD(
        [dispid(2)],
        HRESULT,
        'Add',
        (['in'], BSTR, 'Name'),
        (['out', 'retval'], POINTER(POINTER(IFolder)), 'ppfolder')
    ),
    COMMETHOD(
        [dispid(0), 'propget'],
        HRESULT,
        'Item',
        (['in'], VARIANT, 'Key'),
        (['out', 'retval'], POINTER(POINTER(IFolder)), 'ppfolder')
    ),
    COMMETHOD(
        [dispid(-4), 'restricted', 'hidden', 'propget'],
        HRESULT,
        '_NewEnum',
        (['out', 'retval'], POINTER(POINTER(IUnknown)), 'ppenum')
    ),
    COMMETHOD(
        [dispid(1), 'propget'],
        HRESULT,
        'Count',
        (['out', 'retval'], POINTER(c_int), 'plCount')
    ),
]

################################################################
# code template for IFolderCollection implementation
# class IFolderCollection_Impl(object):
#     def Add(self, Name):
#         '-no docstring-'
#         #return ppfolder
#
#     @property
#     def Item(self, Key):
#         '-no docstring-'
#         #return ppfolder
#
#     @property
#     def _NewEnum(self):
#         '-no docstring-'
#         #return ppenum
#
#     @property
#     def Count(self):
#         '-no docstring-'
#         #return plCount
#


class WshShell(CoClass):
    """Shell Object"""
    _reg_clsid_ = GUID('{72C24DD5-D70A-438B-8A42-98424B88AFB8}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


WshShell._com_interfaces_ = [IWshShell3]


class File(CoClass):
    _reg_clsid_ = GUID('{C7C3F5B5-88A3-11D0-ABCB-00A0C90FFFC0}')
    _idlflags_ = ['noncreatable']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


File._com_interfaces_ = [IFile]


class WshExec(CoClass):
    """WSHExec object"""
    _reg_clsid_ = GUID('{08FED191-BE19-11D3-A28B-00104BD35090}')
    _idlflags_ = ['noncreatable']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{F935DC20-1CF0-11D0-ADB9-00C04FD58A0B}', 1, 0)


WshExec._com_interfaces_ = [IWshExec]

__all__ = [
    'IDrive', 'ForReading', 'CompareMethod', 'SystemFolder',
    'WshURLShortcut', 'SpecialFolderConst',
    '__MIDL___MIDL_itf_iwshom_0000_0000_0003', 'IWshShell_Class',
    'FileAttribute', '__MIDL___MIDL_itf_iwshom_0001_0037_0001',
    'IWshNetwork', 'DriveTypeConst', 'WshMinimizedFocus',
    'IWshCollection', 'IWshEnvironment', 'ForWriting', 'Hidden',
    'Tristate', 'FileSystemObject', 'Alias', 'RamDisk',
    'IWshEnvironment_Class', 'IWshNetwork2', 'BinaryCompare',
    'StdOut', 'IWshCollection_Class', 'WshShell', 'IFile', 'IWshExec',
    'Remote', 'WshCollection', 'WshHide', 'Folders', 'ForAppending',
    'WshNetwork', 'TextStream', 'Files', 'Fixed', 'WshExecStatus',
    'WshRunning', 'WshFailed', 'TristateTrue', 'Library', 'Drives',
    '__MIDL___MIDL_itf_iwshom_0001_0016_0001', 'IDriveCollection',
    'WshExec', 'StdErr', '__MIDL___MIDL_itf_iwshom_0000_0000_0002',
    'Removable', 'CDRom', 'StdIn', 'IWshShell', 'ITextStream',
    'Volume', 'UnknownType', 'IWshShortcut', 'IOMode', 'Folder',
    'IWshShell3', 'Directory', 'WshWindowStyle', 'TextCompare',
    'Compressed', 'IWshShortcut_Class', 'ReadOnly', 'File',
    'WshFinished', 'IWshURLShortcut_Class', 'IFileSystem',
    '__MIDL___MIDL_itf_iwshom_0000_0000_0001', 'Normal',
    'TemporaryFolder', 'IFolder', 'WshMinimizedNoFocus', 'IWshShell2',
    'TristateFalse', 'StandardStreamTypes',
    '__MIDL___MIDL_itf_iwshom_0000_0000_0004', 'WshEnvironment',
    'IFileCollection', 'DatabaseCompare', 'IFolderCollection',
    'IWshNetwork_Class', 'WshMaximizedFocus', 'WshNormalFocus',
    'Drive', 'TristateUseDefault', 'IFileSystem3', 'System',
    'WindowsFolder', 'TristateMixed', 'typelib_path',
    'WshNormalNoFocus', 'Archive', 'IWshURLShortcut', 'WshShortcut'
]

_check_version('1.4.14', 1755024953.667633)
