from typing import Any, ClassVar, TYPE_CHECKING


def inspect_magic_genealogy(obj: Any):
    if not isinstance(obj, type):
        obj = obj.__class__

    print(f"--- Magic Genealogy for: {obj.__name__} ---")

    # Track what we've seen so we know if a child overwrote a parent
    seen_methods = set()

    # Walk the MRO (Method Resolution Order)
    for cls in obj.__mro__:
        directory = dir(cls)
        # Get all magic methods defined *locally* in this class
        local_magic = {
            attr for attr in directory
            if attr.startswith("__") and attr.endswith("__")
        }

        if not local_magic:
            continue

        print(f"\n[Class: {cls.__name__}]")

        for name in local_magic:
            # Check if this is an override or the original
            status = "Overridden" if name in seen_methods else "Active"
            print(f"    {name:<25} ({status})")
            seen_methods.add(name)


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    @property
    def instances(cls) -> dict[type, Any]:
        return cls._instances


class Singleton(metaclass = SingletonMeta):
    # --- Static Analysis Stubs (What the IDE sees) ---
    # These are only seen by the IDE, not at runtime
    if TYPE_CHECKING:
        # ClassVar prevents it from becoming a dataclass field.
        instances: ClassVar[dict[type, Any]]


__all__ = ['Singleton']

inspect_magic_genealogy(Singleton)
