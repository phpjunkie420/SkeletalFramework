from skeletal_framework.utilities.terminal import Terminal


class Labels:
    name: str = '__class__.__name__'
    x: str = '_x'
    y: str = '_y'
    width: str = '_width'
    text: str = '_text'
    ctrl_id: str = '_ctrl_id'
    font_size: str = '_font_size'
    mro: str = 'type(self).__mro__'

    def __init__(self, obj_dict):
        self._terminal = Terminal()

        self._max_length = 0
        self._max_length = max(len(text) for text in self.__dict__.values())

        for key, raw_text in self.__dict__.items():
            styled_text = f"[bold sand]{raw_text}[/][red]:[/]"
            formatted_label = self._terminal.format(styled_text, width = self._max_length, justify = 'right')
            setattr(self, key, formatted_label)
