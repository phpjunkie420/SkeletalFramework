import ctypes
from dataclasses import dataclass
from typing import Literal

from skeletal_framework.singleton_meta import SingletonMeta


@dataclass(frozen = True)
class CoreContext(metaclass = SingletonMeta):
    h_instance: int | None = None
    main_window: int | None = None

    def __post_init__(self):
        if hasattr(self, '_initialized'):
            return

        attrs = self.__dict__
        attrs['_initialized'] = True

        # noinspection PyUnresolvedReferences
        attrs['h_instance'] = ctypes.windll.kernel32.GetModuleHandleW(None)

    def setattr(self, key: Literal['main_window'], value):
        attrs = self.__dict__
        if key in attrs:
            attrs[key] = value
