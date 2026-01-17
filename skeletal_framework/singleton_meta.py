from typing import Any, ClassVar, TYPE_CHECKING


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    @property
    def instances(cls) -> dict[type, Any]:
        return cls._instances

    if TYPE_CHECKING:
        instances: ClassVar[dict[type, Any]]
