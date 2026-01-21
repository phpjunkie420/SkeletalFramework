from abc import ABC, abstractmethod
from ctypes import wintypes
from dataclasses import dataclass, astuple
from functools import singledispatch, singledispatchmethod
from typing import Any, Optional, Protocol, runtime_checkable

__all__ = [
    'Control', 'DrawEvent', 'DrawCBItemEvent', 'DrawControlEvent',
    'DrawItemEvent', 'DrawListViewItemEvent', 'DrawPaintEvent'
]


# =============================================================================
# PROTOCOLS
# =============================================================================
@runtime_checkable
class HasIsChecked(Protocol):
    """
    Protocol for controls that maintain a binary toggle state (e.g., Checkbox, RadioButton).
    """

    @property
    def is_checked(self) -> bool: ...

    @is_checked.setter
    def is_checked(self, value: bool) -> None: ...


@runtime_checkable
class HasIsEnabled(Protocol):
    """
    Protocol for controls that maintain an enabled/disabled state (e.g., Button).
    """

    @property
    def is_enabled(self) -> bool: ...

    @is_enabled.setter
    def is_enabled(self, value: bool) -> None: ...


# =============================================================================
# DISPATCH FUNCTIONS (INTERNAL IMPLEMENTATION)
# =============================================================================
# CRITICAL WARNING:
# I have run into this problem during development, and a single Control class
# MUST NOT implement both `HasIsChecked` and `HasIsEnabled`.
#
# If a class satisfies both protocols (e.g., a Checkbox that is also Disable-able),
# `singledispatch` will encounter an ambiguity. It cannot determine whether
# `is_active` should return the checked state or the enabled state.
#
# Python's resolution order in these cases is implicit and fragile.
# If a control needs both properties, you must explicitly register that specific
# class with `_get_active_state` to define which property `is_active` maps to.
# =============================================================================
@singledispatch
def _get_active_state(ctrl: 'Control') -> bool:
    raise AttributeError(f"'{type(ctrl).__name__}' object does not have a recognized 'is_active' state.")


@singledispatch
def _set_active_state(ctrl: 'Control', _value: bool):
    raise AttributeError(f"Cannot set 'is_active' on a '{type(ctrl).__name__}' object.")


# --- PROTOCOL IMPLEMENTATIONS ---
@_get_active_state.register(HasIsChecked)
def _(ctrl: HasIsChecked) -> bool:
    """Strategy: Active state for toggleable controls maps to 'is_checked'."""
    return ctrl.is_checked


@_get_active_state.register(HasIsEnabled)
def _(ctrl: HasIsEnabled) -> bool:
    """Strategy: Active state for standard controls maps to 'is_enabled'."""
    return ctrl.is_enabled


@_set_active_state.register(HasIsChecked)
def _(ctrl: HasIsChecked, value: bool):
    ctrl.is_checked = value


@_set_active_state.register(HasIsEnabled)
def _(ctrl: HasIsEnabled, value: bool):
    ctrl.is_enabled = value


# =============================================================================
# EVENT DATA STRUCTURES
# =============================================================================
@dataclass
class DrawEvent:
    """Base container for all drawing-related metadata sent from WndProc."""

    def astuple(self) -> tuple:
        """Helper to unpack event data for legacy API calls."""
        return astuple(self)


@dataclass
class DrawItemEvent(DrawEvent):
    """Event data for Owner-Drawn controls (WM_DRAWITEM)."""
    hdc: wintypes.HDC
    rect: wintypes.RECT
    state: int


@dataclass
class DrawControlEvent(DrawEvent):
    """Event data for simple control painting."""
    hdc: wintypes.HDC


@dataclass
class DrawPaintEvent(DrawEvent):
    """Event data for the standard paint cycle (WM_PAINT)."""
    hwnd: int


@dataclass
class DrawCBItemEvent(DrawEvent):
    """Event data specifically for ComboBox items."""
    hdc: wintypes.HDC
    rect: wintypes.RECT
    item_id: int
    state: int


@dataclass
class DrawListViewItemEvent(DrawEvent):
    """Event data for ListView Custom Draw (NM_CUSTOMDRAW)."""
    hdc: wintypes.HDC
    draw_stage: int
    item_spec: int
    item_state: int
    rect: wintypes.RECT


# =============================================================================
# BASE CONTROL CLASS
# =============================================================================
class Control(ABC):
    """
    Abstract base class for all UI elements.

    Implements the 'Message Cracker' pattern to route raw Windows messages
    into typed 'DrawEvent' objects for handling by subclasses.
    """

    def __new__(cls, *args, **kwargs):
        if cls is Control:
            raise TypeError("Control class may not be instantiated directly")
        return super().__new__(cls)

    @property
    @abstractmethod
    def hwnd(self) -> bool:
        """The native Window Handle for this control."""
        ...

    # --- UNIFIED API STATE ---
    @property
    def is_active(self) -> bool:
        """
        Polymorphic property that represents the control's 'primary' state.

        * For Checkboxes: Returns `is_checked`.
        * For Buttons: Returns `is_enabled`.
        * For others: Uses the registered protocol handler.
        """
        return _get_active_state(self)

    @is_active.setter
    def is_active(self, value: bool):
        _set_active_state(self, value)

    # --- EVENT DISPATCHER ---
    @singledispatchmethod
    def draw_control(self, event: DrawEvent):
        """
        Routes an incoming DrawEvent to the specific handler for its type.

        This eliminates the need for large if/else blocks checking event types.
        """
        # Fallback for unregistered event types
        raise NotImplementedError(
            f"This control has no handler registered for event type: {type(event).__name__}"
        )

    # --- INTERNAL HANDLERS (ROUTER IMPLENTATION) ---
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

    # --- PUBLIC HOOKS (SUBCLASS OVERRIDES) ---
    def on_draw_control(self, event: DrawControlEvent):
        """Hook: Handle basic control drawing."""
        pass

    def on_draw_item(self, event: DrawItemEvent):
        """Hook: Handle WM_DRAWITEM (Owner Draw)."""
        pass

    def on_paint_item(self, event: DrawPaintEvent):
        """Hook: Handle WM_PAINT."""
        pass

    def on_draw_combobox_item(self, event: DrawCBItemEvent):
        """Hook: Handle specific ComboBox item painting."""
        pass

    def on_draw_listview_item(self, event: DrawListViewItemEvent):
        """
        Hook: Handle ListView Custom Draw (NM_CUSTOMDRAW).

        Must return the appropriate LRESULT flag (e.g., CDRF_NOTIFYITEMDRAW).
        """
        pass
