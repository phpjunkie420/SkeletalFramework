import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from terminal import Terminal


def get_text_color(bg_r: int, bg_g: int, bg_b: int) -> tuple[int, int, int]:
    """
    Determines whether black or white text will be more readable on a given
    background color by calculating perceived luminance.
    """
    luminance = (0.299 * bg_r + 0.587 * bg_g + 0.114 * bg_b)
    return (0, 0, 0) if luminance > 128 else (255, 255, 255)


def generate_color_swatch() -> None:
    """
    Generates a PNG image displaying all the colors defined in the Terminal class.
    """
    terminal = Terminal()
    colors = list(terminal.color_map.items())

    # --- Layout Configuration ---
    swatch_width = 250
    swatch_height = 50
    padding = 10
    num_columns = 5

    # --- Calculate Image Dimensions ---
    num_rows = math.ceil(len(colors) / num_columns)
    img_width = (swatch_width * num_columns) + (padding * (num_columns + 1))
    img_height = (swatch_height * num_rows) + (padding * (num_rows + 1))

    # --- Create Image and Drawing Context ---
    image = Image.new('RGB', (img_width, img_height), (20, 20, 20))
    draw = ImageDraw.Draw(image)

    # --- Load Font ---
    try:
        # Attempt to load a common, clear system font
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        # Fallback to the default font if Arial is not found
        print("Arial font not found, using default PIL font.")
        font = ImageFont.load_default()

    # --- Draw Each Color Swatch ---
    x, y = padding, padding
    for i, (name, rgb_string) in enumerate(colors):
        r, g, b = map(int, rgb_string.split(';'))

        # Draw the colored swatch rectangle
        draw.rectangle(
            [x, y, x + swatch_width, y + swatch_height],
            fill = (r, g, b)
        )

        # Determine the best text color for readability
        text_color = get_text_color(r, g, b)

        # Draw the color name on the swatch
        text = f"{name} ({r}, {g}, {b})"
        text_bbox = draw.textbbox((0, 0), text, font = font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        text_x = x + (swatch_width - text_width) / 2
        text_y = y + (swatch_height - text_height) / 2
        draw.text((text_x, text_y), text, font = font, fill = text_color)

        # Move to the next position
        if (i + 1) % num_columns == 0:
            x = padding
            y += swatch_height + padding
        else:
            x += swatch_width + padding

    # --- Save the Image ---
    output_path = Path(__file__).parent / "color_palette.png"
    image.save(output_path)
    terminal.print(f"\n[bold green]Color palette swatch saved to:[/] [cyan]{output_path}[/]")


if __name__ == "__main__":
    generate_color_swatch()
