from abc import ABC, abstractmethod
from ctypes import wintypes
from dataclasses import dataclass, astuple
from functools import singledispatch, singledispatchmethod
from typing import Any, Optional, Protocol, runtime_checkable

__all__ = ['Control', 'DrawEvent', 'DrawCBItemEvent', 'DrawControlEvent', 'DrawItemEvent', 'DrawListViewItemEvent', 'DrawPaintEvent']


@runtime_checkable
class HasIsChecked(Protocol):
    @property
    def is_checked(self) -> bool: ...
    @is_checked.setter
    def is_checked(self, value: bool) -> None: ...


# --- Internal generic functions for dispatching ---
@singledispatch
def _get_active_state(ctrl: 'Control') -> bool:
    raise AttributeError(f"'{type(ctrl).__name__}' object has no recognized 'is_active' state.")


@_get_active_state.register(HasIsChecked)
def _(ctrl: HasIsChecked) -> bool:
    return ctrl.is_checked


@runtime_checkable
class HasIsEnabled(Protocol):
    @property
    def is_enabled(self) -> bool: ...
    @is_enabled.setter
    def is_enabled(self, value: bool) -> None: ...


@_get_active_state.register(HasIsEnabled)
def _(ctrl: HasIsEnabled) -> bool:
    return ctrl.is_enabled


@singledispatch
def _set_active_state(ctrl: 'Control', _value: bool):
    raise AttributeError(f"Cannot set 'is_active' on a '{type(ctrl).__name__}' object.")


@_set_active_state.register(HasIsChecked)
def _(ctrl: HasIsChecked, value: bool):
    ctrl.is_checked = value


@_set_active_state.register(HasIsEnabled)
def _(ctrl: HasIsEnabled, value: bool):
    ctrl.is_enabled = value


@dataclass
class DrawEvent:
    def astuple(self) -> tuple:
        """
        Returns the attributes of a dataclass-based event as a tuple.
        """
        # The astuple function is the idiomatic way to get values from a dataclass.
        return astuple(self)


@dataclass
class DrawItemEvent(DrawEvent):
    hdc: wintypes.HDC
    rect: wintypes.RECT
    state: int


@dataclass
class DrawControlEvent(DrawEvent):
    hdc: wintypes.HDC


@dataclass
class DrawPaintEvent(DrawEvent):
    hwnd: int


@dataclass
class DrawCBItemEvent(DrawEvent):
    hdc: wintypes.HDC
    rect: wintypes.RECT
    item_id: int
    state: int


@dataclass
class DrawListViewItemEvent(DrawEvent):
    hdc: wintypes.HDC
    draw_stage: int
    item_spec: int
    item_state: int
    rect: wintypes.RECT


class Control(ABC):
    def __new__(cls, *args, **kwargs):
        if cls is Control:
            raise TypeError("Control class may not be instantiated directly")
        return super().__new__(cls)

    @property
    @abstractmethod
    def hwnd(self) -> bool: ...

    @property
    def is_active(self) -> bool:
        """
        Gets a boolean indicating the primary state of the control.
        Delegates to a dispatched function based on the control's protocol.
        """
        return _get_active_state(self)

    @is_active.setter
    def is_active(self, value: bool):
        """
        Sets the primary state of the control.
        Delegates to a dispatched function based on the control's protocol.
        """
        _set_active_state(self, value)

    @singledispatchmethod
    def draw_control(self, event: DrawEvent):
        # You might want to raise an error here for unhandled event types
        raise NotImplementedError(
            f"This control has no handler registered for event type: {type(event).__name__}"
        )

    @draw_control.register(DrawControlEvent)
    def _handle_draw_control(self, event: DrawControlEvent):
        self.on_draw_control(event)

    @draw_control.register(DrawItemEvent)
    def _handle_draw_item(self, event: DrawItemEvent):
        self.on_draw_item(event)

    @draw_control.register(DrawPaintEvent)
    def _handle_paint_item(self, event: DrawPaintEvent):
        self.on_paint_item(event)

    @draw_control.register(DrawCBItemEvent)
    def _handle_combobox_item(self, event: DrawCBItemEvent):
        self.on_draw_combobox_item(event)

    @draw_control.register(DrawListViewItemEvent)
    def _handle_listview_item(self, event: DrawListViewItemEvent):
        return self.on_draw_listview_item(event)

    def on_draw_control(self, event: DrawControlEvent):
        """Override in a subclass to handle a DrawHeaderEvent."""
        pass

    def on_draw_item(self, event: DrawItemEvent):
        """Override in a subclass to handle a DrawItemEvent."""
        pass

    def on_paint_item(self, event: DrawPaintEvent):
        """Override in a subclass to handle a DrawPaintEvent."""
        pass

    def on_draw_combobox_item(self, event: DrawCBItemEvent):
        """Override in a subclass to handle a DrawComboBoxItemEvent."""
        pass

    def on_draw_listview_item(self, event: DrawListViewItemEvent):
        """Override in a subclass to handle a DrawComboBoxItemEvent."""
        pass
