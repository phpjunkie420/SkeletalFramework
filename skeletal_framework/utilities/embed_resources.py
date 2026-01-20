import base64
import textwrap
from pathlib import Path

FILE_TEMPLATE = """
import base64
import io

from PIL import Image

{var_name} = Image.open(
    fp = io.BytesIO(
        initial_bytes = base64.decodebytes(
            {byte_string}
        )
    )
)

__all__ = ['{var_name}']
"""


def encode_image(image: str, var_name: str, filename: str):
    with open(image, "rb") as file:
        binary_image = file.read()

    encoded_image = base64.encodebytes(binary_image)
    splitlines = [f"b'{line.decode('ascii')}'" for line in encoded_image.splitlines()]

    indent = ' ' * 13
    length = len(splitlines) - 1

    for index, line in enumerate(splitlines):
        if index == 0:
            splitlines[index] = f'({line}'

        elif index == length:
            splitlines[index] = f'{indent}{line})'

        else:
            splitlines[index] = f'{indent}{line}'

    clean_template = textwrap.dedent(FILE_TEMPLATE).lstrip()
    final_source_code = clean_template.format(
        var_name = var_name,
        byte_string = '\n'.join(splitlines)
    )

    with open(filename.lower(), "w") as file:
        file.write(final_source_code)


if __name__ == '__main__':
    filename = Path(__file__).parent.parent / 'resources' / 'exception_face.py'

    encode_image(
        image = r'C:\Users\*********\Python\SkeletalFramework\images\exception_face.png',
        var_name = 'EXCEPTION_FACE',
        filename = str(filename)
    )
