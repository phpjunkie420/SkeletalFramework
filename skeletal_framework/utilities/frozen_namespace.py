from dataclasses import FrozenInstanceError
from enum import auto, IntFlag, StrEnum
from pathlib import Path

__all__ = ['Host', 'Platform', 'Filter', 'OutputPath']


class FrozenNamespaceMeta(type):
    def __new__(mcs, name, bases, attrs):
        attrs['_is_frozen'] = True
        return super().__new__(mcs, name, bases, attrs)

    def __setattr__(cls, name, value):
        if getattr(cls, '_is_frozen', False):
            raise FrozenInstanceError(f"cannot assign to class attribute '{name}'")
        super().__setattr__(name, value)

    def __delattr__(cls, name):
        if getattr(cls, '_is_frozen', False):
            raise FrozenInstanceError(f"cannot delete class attribute '{name}'")
        super().__delattr__(name)

    def __iter__(cls):
        for name, value in cls.__dict__.items():
            if not name.startswith('_'):
                yield value


class FrozenNamespace(metaclass = FrozenNamespaceMeta): ...


class UserProfile(FrozenNamespace):
    Downloads = Path(r'C:\Users\phpjunkie\Media\Downloads\Sort')
    StreamFab = Path(r'C:\Users\phpjunkie\Media\StreamFab')


class LocalStorage(FrozenNamespace):
    Downloads = Path(r'D:\Media\Downloads\Sort')
    StreamFab = Path(r'D:\Media\StreamFab')


class RemoteStorage(FrozenNamespace):
    Downloads = Path(r'M:\Downloads\Sort')
    StreamFab = Path(r'M:\StreamFab')


# @formatter:off
class OutputPath(FrozenNamespace):
    UserProfile = Path(r'C:\Users\phpjunkie\Media')
    Storage     = Path(r'D:\Media')


class Host(FrozenNamespace):
    UserProfile     = UserProfile
    LocalStorage    = LocalStorage
    RemoteStorage   = RemoteStorage


# class Platform(FrozenNamespace):
#     Amazon        = Path('Amazon')
#     AppleTV       = Path('Apple TV')
#     DisneyPlus    = Path('Disney+')
#     Hulu          = Path('Hulu')
#     Netflix       = Path('Netflix')
#     ParamountPlus = Path('Paramount+')
#     DiscoveryPlus = Path('DiscoveryPlus')
#     HBOMax        = Path('HBO Max')


class Platform(StrEnum):
    Amazon        = 'Amazon'
    AppleTV       = 'Apple TV'
    DisneyPlus    = 'Disney+'
    Hulu          = 'Hulu'
    Netflix       = 'Netflix'
    ParamountPlus = 'Paramount+'
    DiscoveryPlus = 'DiscoveryPlus'
    HBOMax        = 'HBO Max'


class Filter(IntFlag):
    NoFilter    = auto()
    Directories = auto()
    Filenames   = auto()
    Both        = Directories | Filenames
# @formatter:on
