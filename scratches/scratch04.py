from typing import Any

from rich.console import Console
from rich.progress import Progress
import inspect


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


# --- Test it on the rich.Progress object ---
console = Console()
progress = Progress()
inspect_magic_genealogy(progress)
