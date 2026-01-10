import comtypes.client
import comtypes.gen
import os
from pathlib import Path

output_folder = Path(__file__).parent.absolute() / 'generated_bindings'
if not output_folder.exists():
    output_folder.mkdir(parents = True, exist_ok = True)

init_file = output_folder / "__init__.py"
if not init_file.exists():
    print(f"Creating missing __init__.py in {output_folder}")
    init_file.open(mode = 'w').close()

comtypes.gen.__path__ = [str(output_folder)]
comtypes.client.gen_dir = str(output_folder)

wsh_path = Path(os.environ["SystemRoot"]) / "System32" / "wshom.ocx"
print(f"Generating Python wrapper for: {wsh_path}")
print(f"Output directory set to: {comtypes.client.gen_dir}")

module = comtypes.client.GetModule(str(wsh_path))

print(f"\nSuccess! The wrapper file is located here:")
print(module.__file__)

print("\n--- INSTRUCTIONS ---")
print("Open that file in your editor.")
print("Search for 'IWshShortcut' to see the exact GUIDs, DISPIDs, and method signatures.")
