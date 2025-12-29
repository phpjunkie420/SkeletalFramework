import ctypes


# noinspection PyUnusedLocal
def errcheck_bool(result, func, args):
    if not result:
        error_msg = f"API Call '{func.__name__}' failed with error code {ctypes.get_last_error()}"
        raise ctypes.WinError(ctypes.get_last_error(), error_msg)
    return result


# noinspection PyUnusedLocal
def errcheck_zero(result, func, args):
    if result == 0:
        error_msg = f"API Call '{func.__name__}' failed with error code {ctypes.get_last_error()}"
        raise ctypes.WinError(ctypes.get_last_error(), error_msg)
    return result


def call_with_last_error_check(func, *args):
    ctypes.set_last_error(0)
    result = func(*args)
    if result == 0:
        err = ctypes.get_last_error()
        if err != 0:
            error_msg = f"API Call '{func.__name__}' failed with error code {ctypes.get_last_error()}"
            raise ctypes.WinError(err, error_msg)
    return result
