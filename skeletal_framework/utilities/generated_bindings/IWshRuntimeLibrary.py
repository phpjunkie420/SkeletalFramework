from enum import IntFlag

import comtypes.gen._F935DC20_1CF0_11D0_ADB9_00C04FD58A0B_0_1_0 as __wrapper_module__
from comtypes.gen._F935DC20_1CF0_11D0_ADB9_00C04FD58A0B_0_1_0 import (
    IDrive, Volume, UnknownType, IWshShortcut, ForReading,
    SystemFolder, WshURLShortcut, Folder, GUID, IWshShell3, Directory,
    IWshShell_Class, BSTR, VARIANT, IWshNetwork, TextCompare,
    Compressed, WshMinimizedFocus, IWshCollection, _check_version,
    IWshEnvironment, ForWriting, Hidden, IWshShortcut_Class, ReadOnly,
    File, FileSystemObject, Alias, WshFinished, IWshURLShortcut_Class,
    IFileSystem, Normal, IUnknown, RamDisk, TemporaryFolder,
    IWshEnvironment_Class, IFolder, WshMinimizedNoFocus, IWshNetwork2,
    BinaryCompare, IWshShell2, StdOut, TristateFalse,
    IWshCollection_Class, WshShell, HRESULT, IFile, IWshExec, Remote,
    WshCollection, WshHide, VARIANT_BOOL, Folders, IDispatch,
    WshEnvironment, IFileCollection, ForAppending, WshNetwork,
    DatabaseCompare, TextStream, IFolderCollection, Files,
    IWshNetwork_Class, WshMaximizedFocus, WshNormalFocus, Drive,
    Fixed, WshRunning, WshFailed, TristateUseDefault, IFileSystem3,
    CoClass, TristateTrue, Library, Drives, System, WindowsFolder,
    dispid, _lcid, IDriveCollection, WshExec, StdErr, Removable,
    CDRom, TristateMixed, StdIn, typelib_path, WshNormalNoFocus,
    COMMETHOD, Archive, IWshURLShortcut, IWshShell, ITextStream,
    WshShortcut
)


class __MIDL___MIDL_itf_iwshom_0000_0000_0003(IntFlag):
    WindowsFolder = 0
    SystemFolder = 1
    TemporaryFolder = 2


class IOMode(IntFlag):
    ForReading = 1
    ForWriting = 2
    ForAppending = 8


class Tristate(IntFlag):
    TristateTrue = -1
    TristateFalse = 0
    TristateUseDefault = -2
    TristateMixed = -2


class __MIDL___MIDL_itf_iwshom_0000_0000_0004(IntFlag):
    StdIn = 0
    StdOut = 1
    StdErr = 2


class __MIDL___MIDL_itf_iwshom_0000_0000_0001(IntFlag):
    Normal = 0
    ReadOnly = 1
    Hidden = 2
    System = 4
    Volume = 8
    Directory = 16
    Archive = 32
    Alias = 1024
    Compressed = 2048


class CompareMethod(IntFlag):
    BinaryCompare = 0
    TextCompare = 1
    DatabaseCompare = 2


class __MIDL___MIDL_itf_iwshom_0000_0000_0002(IntFlag):
    UnknownType = 0
    Removable = 1
    Fixed = 2
    Remote = 3
    CDRom = 4
    RamDisk = 5


class __MIDL___MIDL_itf_iwshom_0001_0037_0001(IntFlag):
    WshRunning = 0
    WshFinished = 1
    WshFailed = 2


class __MIDL___MIDL_itf_iwshom_0001_0016_0001(IntFlag):
    WshHide = 0
    WshNormalFocus = 1
    WshMinimizedFocus = 2
    WshMaximizedFocus = 3
    WshNormalNoFocus = 4
    WshMinimizedNoFocus = 6


SpecialFolderConst = __MIDL___MIDL_itf_iwshom_0000_0000_0003
StandardStreamTypes = __MIDL___MIDL_itf_iwshom_0000_0000_0004
FileAttribute = __MIDL___MIDL_itf_iwshom_0000_0000_0001
DriveTypeConst = __MIDL___MIDL_itf_iwshom_0000_0000_0002
WshExecStatus = __MIDL___MIDL_itf_iwshom_0001_0037_0001
WshWindowStyle = __MIDL___MIDL_itf_iwshom_0001_0016_0001


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

