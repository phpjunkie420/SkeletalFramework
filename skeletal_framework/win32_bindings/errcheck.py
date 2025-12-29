import ctypes


# noinspection PyUnusedLocal
def errcheck_bool(result, func, args):
    if not result:
        raise ctypes.WinError(ctypes.get_last_error())
    return result


# noinspection PyUnusedLocal
def errcheck_zero(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return result


# noinspection PyUnusedLocal
def errcheck_hresult(result, func, args):
    if result < 0:
        raise ctypes.WinError(result)
    return result


def call_with_last_error_check(func, *args):
    ctypes.set_last_error(0)
    result = func(*args)
    if result == 0:
        err = ctypes.get_last_error()
        if err != 0:
            raise ctypes.WinError(err)
    return result
