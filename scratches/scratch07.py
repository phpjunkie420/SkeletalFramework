from base64 import encodebytes, decodebytes
from io import BytesIO

from PIL import Image

image_path = r'skull.png'

with open(image_path, "rb") as file:
    binary_image = file.read()

encoded_image = encodebytes(binary_image)  # encoded_image would be a byte string

splitlines = encoded_image.splitlines()
for index, line in enumerate(splitlines):
    if not index:
        print(f'({splitlines[index]}')
    elif index == len(splitlines) - 1:
        print(f'{splitlines[index]})')
    else:
        print(f'{splitlines[index]}')

image = Image.open(
    fp = BytesIO(
        initial_bytes = decodebytes(
            encoded_image
        )
    )
)
image.show()
