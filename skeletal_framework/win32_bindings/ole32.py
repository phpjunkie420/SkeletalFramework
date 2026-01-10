import ctypes

__all__ = [
    'CoGetApartmentType',
]

IN = 1

ole32 = ctypes.WinDLL('ole32', use_last_error = True)

# https://learn.microsoft.com/en-us/windows/win32/api/combaseapi/nf-combaseapi-cogetapartmenttype
# HRESULT CoGetApartmentType(
#   [out] APTTYPE          *pAptType,
#   [out] APTTYPEQUALIFIER *pAptQualifier
# );
_CoGetApartmentType = ctypes.WINFUNCTYPE(
    ctypes.HRESULT,
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int)
)(
    ('CoGetApartmentType', ole32),
    (
        (IN, 'pAptType'),
        (IN, 'pAptQualifier')
    )
)


def CoGetApartmentType() -> int:
    apt_type = ctypes.c_int()
    apt_qualifier = ctypes.c_int()

    return _CoGetApartmentType(ctypes.byref(apt_type), ctypes.byref(apt_qualifier))
