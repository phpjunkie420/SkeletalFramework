import ctypes
from ctypes import wintypes

from win32_bindings.errcheck import call_with_last_error_check

__all__ = [
    'GetModuleHandle'
]

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-getmodulehandlew
# HMODULE GetModuleHandleW(
#   [in, optional] LPCWSTR lpModuleName
# );
_GetModuleHandle = kernel32.GetModuleHandleW
_GetModuleHandle.argtypes = [wintypes.LPCWSTR]
_GetModuleHandle.restype = wintypes.HMODULE


def GetModuleHandle(lpModuleName: str | None) -> int:
    """
    Retrieves a module handle for the specified module. The module must have been loaded by the calling process.

    Args:
        lpModuleName (str | None): The name of the loaded module (either a .dll or .exe file).
                                   If this parameter is None, GetModuleHandle returns a handle to the file
                                   used to create the calling process (.exe file).

    Returns:
        int: If the function succeeds, the return value is a handle to the specified module.
             If the function fails, the return value is NULL.
    """
    return call_with_last_error_check(_GetModuleHandle, lpModuleName)
