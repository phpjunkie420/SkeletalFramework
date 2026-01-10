import re
import sys
from contextlib import contextmanager
from typing import Literal

__all__ = ['Terminal']


class Terminal:
    # region Color List
    _COLOR_LIST = [
        # Whites & Grays
        ('aliceblue', '240;248;255'), ('azure', '240;255;255'), ('black', '0;0;0'),
        ('darkgray', '169;169;169'), ('darkslategray', '47;79;79'), ('dimgray', '105;105;105'),
        ('gainsboro', '220;220;220'), ('ghostwhite', '248;248;255'), ('gray', '128;128;128'),
        ('honeydew', '240;255;240'), ('ivory', '255;255;240'), ('lavender', '230;230;250'),
        ('lightcyan', '224;255;255'), ('lightgray', '211;211;211'), ('lightslategray', '119;136;153'),
        ('mintcream', '245;255;250'), ('silver', '192;192;192'), ('slategray', '112;128;144'),
        ('snow', '255;250;250'), ('white', '255;255;255'), ('whitesmoke', '245;245;245'),

        # Reds & Pinks
        ('coral', '255;127;80'), ('crimson', '220;20;60'), ('darkred', '100;0;0'),
        ('darksalmon', '233;150;122'), ('deeppink', '255;20;147'), ('firebrick', '178;34;34'),
        ('hot_pink', '255;105;180'), ('indianred', '205;92;92'), ('lavenderblush', '255;240;245'),
        ('lightcoral', '240;128;128'), ('lightpink', '255;182;193'), ('maroon', '128;0;0'),
        ('mediumvioletred', '199;21;133'), ('mistyrose', '255;228;225'), ('orangered', '255;69;0'),
        ('palevioletred', '219;112;147'), ('pink', '255;192;203'), ('red', '255;0;0'),
        ('rosybrown', '188;143;143'), ('salmon', '250;128;114'), ('tomato', '255;99;71'),

        # Oranges & Browns
        ('amber', '255;191;0'), ('antiquewhite', '250;235;215'), ('bisque', '255;228;196'),
        ('blanchedalmond', '255;235;205'), ('brown', '205;133;19'), ('burlywood', '222;184;135'),
        ('chocolate', '210;105;30'), ('cornsilk', '255;248;220'), ('darkbrown', '101;67;33'), ('darkdarkbrown', '50;33;16'),
        ('darkgold', '184;134;11'), ('darkorange', '255;140;0'), ('floralwhite', '255;250;240'),
        ('gold', '255;215;0'), ('goldenrod', '218;165;32'), ('linen', '250;240;230'),
        ('moccasin', '255;228;181'), ('navajowhite', '255;222;173'), ('oldlace', '253;245;230'),
        ('orange', '255;165;0'), ('papayawhip', '255;239;213'), ('peachpuff', '255;218;185'),
        ('peru', '205;133;63'), ('saddlebrown', '139;69;19'), ('sand', '238;213;183'),
        ('sandybrown', '244;164;96'), ('seashell', '255;245;238'), ('sienna', '160;82;45'),
        ('tan', '198;173;143'), ('wheat', '245;222;179'),

        # Yellows & Greens
        ('chartreuse', '127;255;0'), ('darkgreen', '0;75;0'), ('darkkhaki', '189;183;107'),
        ('darkolivegreen', '85;107;47'), ('darkseagreen', '143;188;143'), ('forestgreen', '34;139;34'),
        ('green', '0;255;0'), ('greenyellow', '173;255;47'), ('khaki', '240;230;140'),
        ('lawngreen', '124;252;0'), ('lemonchiffon', '255;250;205'), ('lightgoldenrodyellow', '250;250;210'),
        ('lightgreen', '144;238;144'), ('lightyellow', '255;255;224'), ('lime', '50;205;50'),
        ('limegreen', '50;205;50'), ('mediumseagreen', '60;179;113'), ('mediumspringgreen', '0;250;154'),
        ('olive', '128;128;0'), ('olivedrab', '107;142;35'), ('palegoldenrod', '238;232;170'),
        ('palegreen', '152;251;152'), ('seagreen', '46;139;87'), ('springgreen', '0;255;127'),
        ('yellow', '255;255;0'), ('yellowgreen', '154;205;50'),

        # Cyans & Blues
        ('aqua', '0;255;255'), ('aquamarine', '127;255;212'), ('blue', '100;149;237'),
        ('cadetblue', '95;158;160'), ('cornflowerblue', '100;149;237'), ('cyan', '0;255;255'),
        ('darkblue', '0;0;139'), ('darkcyan', '0;139;139'), ('darkslateblue', '72;61;139'),
        ('darkturquoise', '0;206;209'), ('deepskyblue', '0;191;255'), ('dodgerblue', '30;144;255'),
        ('lightblue', '173;216;230'), ('lightseagreen', '32;178;170'), ('lightskyblue', '135;206;235'),
        ('lightsteelblue', '176;196;222'), ('mediumaquamarine', '102;205;170'), ('mediumblue', '0;0;205'),
        ('mediumslateblue', '123;104;238'), ('mediumturquoise', '72;209;204'), ('midnightblue', '25;25;112'),
        ('navy', '0;0;128'), ('paleturquoise', '175;238;238'), ('powderblue', '176;224;230'),
        ('royalblue', '65;105;225'), ('sky_blue', '135;206;235'), ('slate_blue', '106;90;205'),
        ('steelblue', '70;130;180'), ('teal', '32;178;170'), ('turquoise', '64;224;208'),

        # Purples & Magentas
        ('blueviolet', '138;43;226'), ('darkmagenta', '139;0;139'), ('darkorchid', '153;50;204'),
        ('darkviolet', '148;0;211'), ('fuchsia', '255;0;255'), ('indigo', '75;0;130'),
        ('magenta', '255;0;255'), ('mediumorchid', '186;85;211'), ('mediumpurple', '147;112;219'),
        ('orchid', '218;112;214'), ('plum', '221;160;221'), ('purple', '186;85;211'),
        ('thistle', '216;191;216'), ('violet', '238;130;238'),

        # Solarized Accent Colors (https://ethanschoonover.com/solarized/)
        ('solar_yellow', '181;137;0'),
        ('solar_orange', '203;75;22'),
        ('solar_red', '220;50;47'),
        ('solar_magenta', '211;54;130'),
        ('solar_violet', '108;113;196'),
        ('solar_blue', '38;139;210'),
        ('solar_cyan', '42;161;152'),
        ('solar_green', '133;153;0'),

        # Dracula Theme Colors (https://draculatheme.com/)
        ('dracula_background', '40;42;54'),
        ('dracula_foreground', '248;248;242'),
        ('dracula_comment', '98;114;164'),
        ('dracula_cyan', '139;233;253'),
        ('dracula_green', '80;250;123'),
        ('dracula_orange', '255;184;108'),
        ('dracula_pink', '255;121;198'),
        ('dracula_purple', '189;147;249'),
        ('dracula_red', '255;85;85'),
        ('dracula_yellow', '241;250;140'),

        # Nord Theme Colors (https://www.nordtheme.com/)
        ('nord_red', '191;97;106'),
        ('nord_orange', '208;135;112'),
        ('nord_yellow', '235;203;139'),
        ('nord_green', '163;190;140'),
        ('nord_purple', '180;142;173'),
        ('nord_frost_light', '143;188;187'),
        ('nord_frost_medium', '136;192;208'),
        ('nord_frost_dark', '129;161;193'),
        ('nord_frost_darkest', '94;129;172'),

        # progress / logging colors
        ('info', '255;255;0'),
        ('progress1', '255;100;0'), ('progress2', '224;131;0'), ('progress3', '193;162;0'),
        ('progress4', '162;193;0'), ('progress5', '131;224;0'), ('progress6', '100;255;0'),
    ]
    # endregion

    def __init__(self) -> None:
        self.color_map: dict[str, str] = dict(self._COLOR_LIST)

        # A map of attribute names to their ANSI code.
        self.attribute_map: dict[str, str] = {
            'bold': '1', 'italic': '3', 'underline': '4', 'strike': '9'
        }

        self._pattern = re.compile(r'\[([\w\s]+)](.*?)\[/]', re.IGNORECASE | re.DOTALL)

    def print(self, *objects: object, sep: str = ' ', end: str = '\n', flush: bool = False, width: int | None = None, justify: Literal['left', 'center', 'right'] | None = None) -> None:
        """
        Behaves like the built-in print function but applies custom formatting.
        """
        # Format the text using the dedicated format method
        formatted_text = self.format(*objects, sep = sep, width = width, justify = justify)
        # Write directly to the stdout stream for maximum control
        sys.stdout.write(formatted_text + end)
        if flush:
            sys.stdout.flush()

    def rewrite_line(self, *objects: object, sep: str = ' ', width: int | None = None, justify: Literal['left', 'center', 'right'] | None = None):
        """Moves the cursor to the start of the line, clears it, and prints new text."""
        text = self.format(*objects, sep = sep, width = width, justify = justify)
        sys.stdout.write(f'\x1b[1G\x1b[2K{text}')
        sys.stdout.flush()

    def _apply_styles(self, text: str) -> str:
        """Replaces style tags like [bold red]...[/] with ANSI codes."""

        def replacer(match: re.Match) -> str:
            style_keys = match.group(1).lower().split()
            content = match.group(2)

            ansi_parts = []
            color_part = None

            for key in style_keys:
                if key in self.attribute_map:
                    ansi_parts.append(self.attribute_map[key])
                elif key in self.color_map:
                    # We only allow one color per tag, the last one wins.
                    color_part = f'38;2;{self.color_map[key]}'

            if color_part:
                ansi_parts.append(color_part)

            if not ansi_parts:
                return content  # No valid styles found

            full_ansi_code = f"\x1b[{';'.join(ansi_parts)}m"
            return f"{full_ansi_code}{content}\x1b[0m"

        return self._pattern.sub(replacer, text)

    def format(self, *objects: object, sep: str = ' ', width: int | None = None, justify: Literal['left', 'center', 'right'] | None = None) -> str:
        """Applies color formatting and optional justification to one or more objects."""
        # Convert all objects to strings and join them with the separator.
        text = sep.join(map(str, objects))

        # Apply styles to the entire text block.
        styled_text = self._apply_styles(text)

        # If no justification is needed, we are done.
        if justify is None or width is None:
            return styled_text

        # If justifying, process the now-styled text line by line.
        processed_lines = []
        for line in styled_text.splitlines():
            visible_length = self.get_visible_length(line)
            padding = len(line) - visible_length
            width_with_padding = width + padding

            if justify == 'center':
                processed_lines.append(line.center(width_with_padding))
            elif justify == 'left':
                processed_lines.append(line.ljust(width_with_padding))
            elif justify == 'right':
                processed_lines.append(line.rjust(width_with_padding))
            else:
                processed_lines.append(line)

        return '\n'.join(processed_lines)

    @staticmethod
    def get_visible_length(s: str) -> int:
        # This regex removes ANSI escape codes to get the visible length
        ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
        return len(ansi_escape.sub('', s))

    @staticmethod
    def show_cursor():
        """Shows the cursor."""
        sys.stdout.write('\x1b[?25h')
        sys.stdout.flush()

    @staticmethod
    def hide_cursor():
        """Hides the cursor."""
        sys.stdout.write('\x1b[?25l')
        sys.stdout.flush()

    @staticmethod
    def move_cursor_to_position(row: int, col: int):
        """Moves the cursor to an absolute position (row, col)."""
        sys.stdout.write(f'\x1b[{row};{col}H')
        sys.stdout.flush()

    @staticmethod
    def move_cursor_up(rows: int = 1):
        """Moves the cursor up by the specified number of rows."""
        sys.stdout.write(f'\x1b[{rows}A')
        sys.stdout.flush()

    @staticmethod
    def move_cursor_down(rows: int = 1):
        """Moves the cursor down by the specified number of rows."""
        sys.stdout.write(f'\x1b[{rows}B')
        sys.stdout.flush()

    @staticmethod
    def move_cursor_forward(cols: int = 1):
        """Moves the cursor right by the specified number of columns."""
        sys.stdout.write(f'\x1b[{cols}C')
        sys.stdout.flush()

    @staticmethod
    def move_cursor_backward(cols: int = 1):
        """Moves the cursor left by the specified number of columns."""
        sys.stdout.write(f'\x1b[{cols}D')
        sys.stdout.flush()

    @staticmethod
    def move_to_column(col: int = 1):
        """Moves the cursor to the specified absolute column on the current line."""
        sys.stdout.write(f'\x1b[{col}G')
        sys.stdout.flush()

    @staticmethod
    def move_cursor_to_next_line(rows: int = 1):
        """Moves the cursor to the start of the next line."""
        sys.stdout.write(f'\x1b[{rows}E')
        sys.stdout.flush()

    @staticmethod
    def move_cursor_to_previous_line(rows: int = 1):
        """Moves the cursor to the start of the previous line."""
        sys.stdout.write(f'\x1b[{rows}F')
        sys.stdout.flush()

    @staticmethod
    def insert_lines(rows: int = 1):
        sys.stdout.write(f'\x1b[{rows}L')
        sys.stdout.flush()

    @staticmethod
    def delete_lines(rows: int = 1):
        sys.stdout.write(f'\x1b[{rows}M')
        sys.stdout.flush()

    @staticmethod
    def clear_current_line():
        """Clears the current line in the console."""
        sys.stdout.write('\x1b[G\x1b[2K')
        sys.stdout.flush()

    @staticmethod
    def clear_lines(lines: int = 1):
        """Clears the specified number of lines above the cursor."""
        sys.stdout.write('\x1b[2K\x1b[G')
        sys.stdout.flush()

        for _ in range(lines):
            sys.stdout.write('\x1b[A\x1b[2K\x1b[G')
            sys.stdout.flush()

    @staticmethod
    def erase_down():
        sys.stdout.write('\x1b[J')
        sys.stdout.flush()

    @staticmethod
    def erase_up():
        sys.stdout.write('\x1b[1J')
        sys.stdout.flush()

    @staticmethod
    def clear_all():
        sys.stdout.write(f'\x1b[2J')
        sys.stdout.write(f'\x1b[H')
        sys.stdout.write(f'\x1b[3J')

        sys.stdout.flush()

    @staticmethod
    def save_cursor_position():
        sys.stdout.write('\x1b7')
        sys.stdout.flush()

    @staticmethod
    def restore_cursor_position():
        sys.stdout.write('\x1b8\x1b[J')

    @staticmethod
    @contextmanager
    def alt_screen():
        """A context manager to enter and exit the alternate screen buffer."""
        try:
            # Enter alternate screen and hide cursor
            sys.stdout.write('\x1b[?1049h\x1b[?25l')
            sys.stdout.flush()
            yield
        finally:
            # Exit alternate screen and show cursor
            sys.stdout.write('\x1b[?1049l\x1b[?25h')
            sys.stdout.flush()


if __name__ == '__main__':
    from time import sleep
    import math

    terminal = Terminal()
    terminal.hide_cursor()
    terminal.clear_all()

    terminal.print("[strike amber]Starting animation in 1 seconds...[/]", width = 70, justify = 'center')
    sleep(1)

    # Use the context manager to handle screen switching and cleanup
    # with terminal.alt_screen():
    rng = 6
    length = 100

    ceil = math.ceil(length / rng) * rng
    terminal.clear_all()

    style = 'underline'
    for i in range(ceil):
        # Example of a moving animation
        # terminal.move_cursor_to_position(i % rng + 1, 1)
        if (i % rng) == 0:
            terminal.print(terminal.get_cursor_position())
        style = ('strike' if style == 'underline' else 'underline') if i % rng == 0 else style
        terminal.print(f'[bold red]{i % rng + 1:02}[/] [{style} progress{i % rng + 1}]This line also', 'gets included with that line.[/]', width = 70, justify = 'center')
        sleep(0.1)

    sleep(1)  # Hold the final frame
    terminal.move_cursor_to_previous_line(ceil)
    terminal.erase_down()
    # terminal.clear_all()
    # sleep(1)

    # style = 'strike'
    # terminal.move_cursor_to_position(0, 0)
    # for i in range(ceil):
    #     # Example of a moving animation
    #     terminal.move_cursor_to_position(i % rng + 1, 1)
    #
    #     style = ('strike' if style == 'underline' else 'underline') if i % rng == 0 else style
    #     terminal.print(f'[bold red]{i % rng + 1:02}[/] [{style} progress{i % rng + 1}]And some other kind', 'of crazy silly text.[/]', width = 70, justify = 'center')
    #     sleep(0.1)
    #
    # sleep(1)
    # terminal.clear_all()
    # sleep(1)
    #
    # for i in range(10):
    #     terminal.rewrite_line(f'[amber]Line {i + 1}[/]', width = 70, justify = 'center')
    #     sleep(0.5)
    #
    # sleep(1)
    # terminal.rewrite_line()
    #
    # # After the 'with' block, the original screen is restored automatically.
    # terminal.print("[bold red]Animation complete...[/]", width = 70, justify = 'center')
    # terminal.print()
    terminal.show_cursor()
