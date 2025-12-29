import ctypes

__all__ = [
    'adjust_color', 'adjust_rgb', 'create_unicode_buffer', 'get_rgb', 'hiword', 'loword',
    'MAKELONG', 'MAKEWPARAM',
]

MAX_BUFFER_SIZE = 1024


def adjust_color(color_ref, factor):
    r, g, b = get_rgb(color_ref)

    return (
        int(max(0, min(255, r * factor))),
        int(max(0, min(255, g * factor))),
        int(max(0, min(255, b * factor)))
    )


def adjust_rgb(r, g, b, factor):
    return (
        int(max(0, min(255, r * factor))),
        int(max(0, min(255, g * factor))),
        int(max(0, min(255, b * factor)))
    )


def create_unicode_buffer(init: int | str, size: int | None = None) -> ctypes.Array[ctypes.c_wchar]:
    buffer_size = min(init, MAX_BUFFER_SIZE)

    return ctypes.create_unicode_buffer(buffer_size, size)


def get_rgb(color_ref):
    return (color_ref & 0xff), ((color_ref >> 8) & 0xff), ((color_ref >> 16) & 0xff)


def hiword(value: int) -> int:
    """
    Extracts the high-order word from a given 32-bit value.
    Equivalent to the Windows API HIWORD macro.
    Reference: https://learn.microsoft.com/en-us/windows/win32/winmsg/hiword
    """
    return (value >> 16) & 0xFFFF


def loword(value: int) -> int:
    """
    Extracts the low-order word from a given 32-bit value.
    Equivalent to the Windows API LOWORD macro.
    Reference: https://learn.microsoft.com/en-us/windows/win32/winmsg/loword
    """
    return value & 0xFFFF


# noinspection PyPep8Naming
def MAKELONG(low: int, high: int) -> int:
    """
    Creates a 32-bit signed integer (LONG) from two 16-bit words.
    Equivalent to the Windows API MAKELONG macro.
    Reference: https://learn.microsoft.com/en-us/windows/win32/winmsg/makelong
    """
    return (high << 16) | (low & 0xFFFF)


# noinspection PyPep8Naming
def MAKEWPARAM(low: int, high: int) -> int:
    """
    Replicates the C MAKEWPARAM macro.
    Creates a 32-bit value by combining two 16-bit values.
    """
    return (high << 16) | low
