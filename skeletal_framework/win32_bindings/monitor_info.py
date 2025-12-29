"""
Windows Monitor Information Interface Module

This module provides a Python interface to Windows API functions for retrieving monitor information.
It wraps the Windows API functions MonitorFromPoint and GetMonitorInfo, providing easy access to
monitor properties such as position, dimensions, and work area.
"""
import collections.abc
import ctypes
from abc import ABC, abstractmethod
from ctypes import wintypes
from collections.abc import Callable
from typing import (Any, Dict, Generic, Iterator, Literal, Mapping, Optional, Sequence, SupportsIndex, Tuple, TypeVar, Union, overload)

__all__ = ['GetMonitorInfo', 'MonitorFromPoint', 'EnumDisplayMonitors', 'MonitorInfo']

IN = 1
OUT = 2

MONITOR_DEFAULTTONULL = 0x00000000
MONITOR_DEFAULTTOPRIMARY = 0x00000001
MONITOR_DEFAULTTONEAREST = 0x00000002
MONITOR_ANONYMOUS = 0x00000004
MONITOR_DEFAULT = MONITOR_DEFAULTTONULL | MONITOR_DEFAULTTOPRIMARY
CCHDEVICENAME = 32

T = TypeVar('T')
K = TypeVar('K', bound = Union[str, int])
V = TypeVar('V')


class RectangleSequence(collections.abc.Sequence[int], ABC):
    """
    Base class for rectangle-like sequence objects.

    Provides common functionality for both Workspace and other rectangle-based
    sequence types, implementing the Sequence protocol with proper slicing
    support, equality testing, and pattern matching.
    """

    @property
    @abstractmethod
    def left(self) -> int:
        """X-coordinate of the left edge"""
        pass

    @property
    @abstractmethod
    def top(self) -> int:
        """Y-coordinate of the top edge"""
        pass

    @property
    @abstractmethod
    def right(self) -> int:
        """X-coordinate of the right edge"""
        pass

    @property
    @abstractmethod
    def bottom(self) -> int:
        """Y-coordinate of the bottom edge"""
        pass

    @property
    def width(self) -> int:
        """Width of the rectangle in pixels"""
        return self.right - self.left

    @property
    def height(self) -> int:
        """Height of the rectangle in pixels"""
        return self.bottom - self.top

    @property
    def _data(self) -> Tuple[int, int, int, int]:
        """Internal tuple representation of the rectangle coordinates"""
        return self.left, self.top, self.right, self.bottom

    def __iter__(self) -> Iterator[int]:
        """Returns iterator over rectangle coordinates (left, top, right, bottom)"""
        return iter(self._data)

    def __len__(self) -> int:
        """Returns number of coordinates (always 4 for a rectangle)"""
        return 4

    @overload
    def __getitem__(self, index: SupportsIndex) -> int:
        ...

    @overload
    def __getitem__(self, index: slice) -> 'RectangleSequence':
        ...

    def __getitem__(self, index: Union[SupportsIndex, slice]) -> Union[int, 'RectangleSequence']:
        """
        Get item or slice from the sequence.

        When a slice is used (e.g., x[:2]), this returns a new RectangleSequence
        instead of a plain sequence, keeping the type consistent for comparisons.

        Args:
            index: Integer index or slice

        Returns:
            Either a single coordinate value or a new RectangleSequence

        Raises:
            IndexError: If index is out of range
        """
        if isinstance(index, slice):
            # For a slice, create a SlicedRectangle with the sliced values
            return SlicedRectangle(self._data[index])
        else:
            # For single item access, return the raw item
            return self._data[index]

    def __eq__(self, other: Any) -> bool:
        """
        Compare rectangle coordinates with another object.

        Args:
            other: Another object to compare with

        Returns:
            True if the coordinates match, False otherwise
        """
        if isinstance(other, RectangleSequence):
            return self._data == other._data
        elif isinstance(other, collections.abc.Sequence):
            return self._data == tuple(other)
        return NotImplemented

    def __match_args__(self) -> tuple:
        """Support for pattern matching with match/case"""
        return self._data

    def __str__(self) -> str:
        """String representation of rectangle coordinates"""
        return str(self._data)

    def as_dict(self) -> Dict[str, int]:
        """
        Return the rectangle coordinates as a dictionary.

        Returns:
            Dict with keys 'left', 'top', 'right', 'bottom'
        """
        return {
            'left'  : self.left,
            'top'   : self.top,
            'right' : self.right,
            'bottom': self.bottom
        }

    @property
    def center(self) -> Tuple[int, int]:
        """
        Calculate the center point of the rectangle.

        Returns:
            (x, y) coordinates of the center
        """
        return (
            self.left + (self.width // 2),
            self.top + (self.height // 2)
        )


class SlicedRectangle(RectangleSequence):
    """
    A rectangle created from a slice of another rectangle.

    This allows for creating new RectangleSequence objects from slices
    while maintaining the same interface for consistency.
    """

    def __init__(self, data: Sequence[int]):
        """
        Initialize with coordinate data.

        Args:
            data: Sequence of coordinate values (may be incomplete if sliced)
        """
        # Pad with zeros to ensure we have 4 values
        self._rect_data = tuple(list(data) + [0] * (4 - len(data)))[:4]

    @property
    def left(self) -> int:
        return self._rect_data[0]

    @property
    def top(self) -> int:
        return self._rect_data[1]

    @property
    def right(self) -> int:
        return self._rect_data[2]

    @property
    def bottom(self) -> int:
        return self._rect_data[3]

    def __repr__(self) -> str:
        return f"SlicedRectangle(left={self.left}, top={self.top}, right={self.right}, bottom={self.bottom})"


class Workspace(RectangleSequence):
    """
    Represents a monitor's workspace area (visible area excluding taskbar and other UI elements).

    Implements the Sequence protocol to allow tuple-like operations. The sequence contains
    four elements representing the workspace coordinates: (left, top, right, bottom).
    Windows RECT structure defines the rectangular area with coordinates relative to the screen origin.

    Attributes:
        _workspace (wintypes.RECT): Windows RECT structure containing workspace coordinates
            - left: x-coordinate of upper-left corner
            - top: y-coordinate of upper-left corner
            - right: x-coordinate of lower-right corner
            - bottom: y-coordinate of the lower right corner

    Properties:
        left (int): Left coordinate (x-coordinate of the upper-left corner)
        top (int): Top coordinate (y-coordinate of the upper-left corner)
        right (int): Right coordinate (x-coordinate of the lower-right corner)
        bottom (int): Bottom coordinate (y-coordinate of the lower-right corner)
        width (int): Width of workspace (right - left)
        height (int): Height of workspace (bottom - top)
    """

    def __init__(self, workspace: wintypes.RECT):
        """
        Initialize with a Windows RECT structure.

        Args:
            workspace: Windows RECT structure defining the workspace area
        """
        self._workspace = workspace

    @property
    def left(self) -> int:
        """X-coordinate of the workspace's left edge"""
        return self._workspace.left

    @property
    def top(self) -> int:
        """Y-coordinate of the workspace's top edge"""
        return self._workspace.top

    @property
    def right(self) -> int:
        """X-coordinate of the workspace's right edge"""
        return self._workspace.right

    @property
    def bottom(self) -> int:
        """Y-coordinate of the workspace's bottom edge"""
        return self._workspace.bottom

    def __repr__(self) -> str:
        """Returns detailed string representation of workspace coordinates"""
        return f"Workspace(left={self.left}, top={self.top}, right={self.right}, bottom={self.bottom})"

    def contains_point(self, x: int, y: int) -> bool:
        """
        Check if the workspace contains a specific point.

        Args:
            x: X-coordinate to check
            y: Y-coordinate to check

        Returns:
            True if the point is within the workspace boundaries
        """
        return (
                self.left <= x < self.right and
                self.top <= y < self.bottom
        )

    def intersects(self, other: RectangleSequence) -> bool:
        """
        Check if this workspace intersects with another rectangle.

        Args:
            other: Another rectangle to check intersection with

        Returns:
            True if the rectangles intersect
        """
        return not (
                self.right <= other.left or
                self.left >= other.right or
                self.bottom <= other.top or
                self.top >= other.bottom
        )


class PropertyAccessMixin(Mapping[K, V], Generic[K, V]):
    """
    Mixin class providing dictionary-like property access.

    Implements the Mapping protocol for read-only dictionary-like access to
    properties with proper typing support.
    """

    def __init__(self):
        self._property_cache: Dict[K, V] = {}

    @abstractmethod
    def _get_property(self, key: K) -> V:
        """
        Abstract method to be implemented by subclasses.

        Args:
            key: Property key

        Returns:
            Property value

        Raises:
            KeyError: If property doesn't exist
        """
        pass

    def __getitem__(self, key: K) -> V:
        """Dictionary-style access to properties"""
        if key not in self._property_cache:
            self._property_cache[key] = self._get_property(key)
        return self._property_cache[key]

    def __iter__(self) -> Iterator[K]:
        """Iterate over property keys"""
        # Subclasses should implement this
        raise NotImplementedError

    def __len__(self) -> int:
        """Number of properties"""
        # Subclasses should implement this
        raise NotImplementedError


class MonitorMeta(type(ctypes.Structure), type(PropertyAccessMixin)):
    pass


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-monitorinfo
# typedef struct MONITORINFO {
#   DWORD cbSize;
#   RECT  rcMonitor;
#   RECT  rcWork;
#   DWORD dwFlags;
# } MONITORINFO, *LPMONITORINFO;
class MonitorInfo(ctypes.Structure, PropertyAccessMixin[Union[str, int], Any], metaclass = MonitorMeta):
    """
    Windows monitor information structure wrapper.

    Wraps the Windows MONITORINFO structure and provides Pythonic access to monitor properties.
    Includes both the complete monitor area and the work area (excluding taskbar).

    Properties:
        Monitor (Tuple[int, int, int, int]): Monitor coordinates (left, top, right, bottom)
        Workspace (Workspace): Work area coordinates as a Workspace object
        Flags (int): Monitor flags from Windows API
        Device (str): Display device name
        left (int): Left coordinate of monitor's screen area
        top (int): Top coordinate of monitor's screen area
        right (int): Right coordinate of monitor's screen area
        bottom (int): Bottom coordinate of monitor's screen area
        width (int): Monitor width in pixels
        height (int): Monitor height in pixels
    """
    _fields_ = [
        ('cbSize', wintypes.DWORD),
        ('rcMonitor', wintypes.RECT),
        ('rcWork', wintypes.RECT),
        ('dwFlags', wintypes.DWORD),
        ('szDevice', wintypes.CHAR * CCHDEVICENAME),
    ]

    # Define valid property names for better type hinting
    _STR_PROPERTIES = Literal[
        'Monitor', 'Work', 'Workspace', 'Flags', 'Device',
        'left', 'top', 'right', 'bottom', 'width', 'height',
        'isPrimary', 'isAnonymous', 'center'
    ]

    def __init__(self, *args, **kwargs) -> None:
        """Initialize monitor structure and set required size field"""
        ctypes.Structure.__init__(self, *args, **kwargs)
        PropertyAccessMixin.__init__(self)
        self.cbSize = ctypes.sizeof(self)
        self._monitor_tuple = None
        self._workspace_obj = None
        self._monitor_rect = None
        self._string_properties = {
            'Monitor', 'Work', 'Workspace', 'Flags', 'Device',
            'left', 'top', 'right', 'bottom', 'width', 'height',
            'isPrimary', 'isAnonymous', 'center'
        }

    @property
    def Monitor(self) -> Tuple[int, int, int, int]:
        """Monitor's complete screen area coordinates"""
        if self._monitor_tuple is None:
            self._monitor_tuple = (
                self.rcMonitor.left,
                self.rcMonitor.top,
                self.rcMonitor.right,
                self.rcMonitor.bottom
            )

        return self._monitor_tuple

    @property
    def MonitorRect(self) -> RectangleSequence:
        """Monitor's complete screen area as a RectangleSequence"""
        if self._monitor_rect is None:
            # Create a SlicedRectangle from the monitor coordinates
            self._monitor_rect = SlicedRectangle(self.Monitor)
        return self._monitor_rect

    @property
    def Workspace(self) -> Workspace:
        """Usable work area excluding taskbar and other UI elements"""
        if self._workspace_obj is None:
            self._workspace_obj = Workspace(self.rcWork)
        return self._workspace_obj

    @property
    def Flags(self) -> int:
        """Monitor configuration flags from Windows API"""
        return self.dwFlags

    @property
    def Device(self) -> str:
        r"""Display device name (e.g. r'\\.\DISPLAY1')"""
        return self.szDevice.decode('utf-8')

    @property
    def left(self) -> int:
        """Left edge x-coordinate"""
        return self.rcMonitor.left

    @property
    def top(self) -> int:
        """Top edge y-coordinate"""
        return self.rcMonitor.top

    @property
    def right(self) -> int:
        """Right edge x-coordinate"""
        return self.rcMonitor.right

    @property
    def bottom(self) -> int:
        """Bottom edge y-coordinate"""
        return self.rcMonitor.bottom

    @property
    def width(self) -> int:
        """Monitor width in pixels"""
        return self.rcMonitor.right - self.rcMonitor.left

    @property
    def height(self) -> int:
        """Monitor height in pixels"""
        return self.rcMonitor.bottom - self.rcMonitor.top

    @property
    def isPrimary(self) -> bool:
        """Whether this is the primary monitor"""
        return self.dwFlags > 0

    @property
    def isAnonymous(self) -> bool:
        """Whether this monitor has no EDID data"""
        return bool(self.dwFlags & MONITOR_ANONYMOUS)

    @property
    def center(self) -> Tuple[int, int]:
        """Center coordinates of the monitor"""
        return (
            self.left + (self.width // 2),
            self.top + (self.height // 2)
        )

    def _get_property(self, key: Union[str, int]) -> Any:
        """
        Internal method to get a property value by key.

        Handles both string keys and integer indices.

        Args:
            key: Either a string property name or an integer index

        Returns:
            Property value

        Raises:
            KeyError: If string property doesn't exist
            IndexError: If integer index is out of range
            TypeError: If key is not a string or integer
        """
        if isinstance(key, str):
            # String key lookup
            if key == 'Monitor':
                return self.Monitor
            elif key == 'Work':
                return (self.rcWork.left, self.rcWork.top,
                        self.rcWork.right, self.rcWork.bottom)
            elif key == 'Workspace':
                return self.Workspace
            elif key == 'Flags':
                return self.Flags
            elif key == 'Device':
                return self.Device
            elif key == 'left':
                return self.left
            elif key == 'top':
                return self.top
            elif key == 'right':
                return self.right
            elif key == 'bottom':
                return self.bottom
            elif key == 'width':
                return self.width
            elif key == 'height':
                return self.height
            elif key == 'isPrimary':
                return self.isPrimary
            elif key == 'isAnonymous':
                return self.isAnonymous
            elif key == 'center':
                return self.center
            else:
                raise KeyError(f"Unknown property: {key}")
        elif isinstance(key, int):
            # Integer index lookup (for monitor coordinates)
            try:
                return self.Monitor[key]
            except IndexError:
                raise IndexError("Monitor index out of range")
        else:
            raise TypeError(f"Key must be a string or integer, not {type(key).__name__}")

    @overload
    def __getitem__(self, key: _STR_PROPERTIES) -> Any:
        ...

    @overload
    def __getitem__(self, key: int) -> int:
        ...

    @overload
    def __getitem__(self, key: slice) -> RectangleSequence:
        ...

    def __getitem__(self, key: Union[str, int, slice]) -> Any:
        """
        Access monitor properties using either string keys, numeric indices, or slices.

        Examples:
            monitor['Monitor']   # Returns full monitor coordinates
            monitor['Device']    # Returns display device name
            monitor[0]           # Returns left coordinate
            monitor[1:3]         # Returns (top, right) coordinates as a RectangleSequence

        Args:
            key: String property name, integer index, or slice

        Returns:
            The requested property value or coordinate(s)
        """
        if isinstance(key, slice):
            # Handle slices by delegating to the MonitorRect object
            return self.MonitorRect[key]
        else:
            # Use the PropertyAccessMixin implementation for strings and integers
            return PropertyAccessMixin.__getitem__(self, key)

    def __setitem__(self, key: Union[str, int], value: Any) -> None:
        """Prevent modification of monitor properties"""
        raise NotImplementedError("Monitor properties are read-only")

    def __iter__(self) -> Iterator[str]:
        """Iterate over property names"""
        return iter(self._string_properties)

    def __len__(self) -> int:
        """Number of accessible properties"""
        return len(self._string_properties)

    def as_dict(self) -> Dict[str, Any]:
        """
        Return all monitor properties as a dictionary.

        Returns:
            Dictionary of all monitor properties
        """
        return {
            'Monitor'    : self.Monitor,
            'Work'       : self['Work'],
            'Workspace'  : self.Workspace,
            'Flags'      : self.Flags,
            'Device'     : self.Device,
            'left'       : self.left,
            'top'        : self.top,
            'right'      : self.right,
            'bottom'     : self.bottom,
            'width'      : self.width,
            'height'     : self.height,
            'isPrimary'  : self.isPrimary,
            'isAnonymous': self.isAnonymous,
            'center'     : self.center
        }

    def contains_point(self, x: int, y: int) -> bool:
        """
        Check if a point is contained within this monitor.

        Args:
            x: X-coordinate to check
            y: Y-coordinate to check

        Returns:
            True if the point is within this monitor's area
        """
        return (
                self.left <= x < self.right and
                self.top <= y < self.bottom
        )

    def __str__(self) -> str:
        """Human-readable representation showing all properties"""
        return (f"{{'Monitor': {self.Monitor}, 'Work': {self['Work']}, "
                f"'Flags': {self.Flags}, 'Device': '{self.Device}'}}")

    def __eq__(self, other: Any) -> bool:
        """Compare monitor coordinates with another object"""
        if isinstance(other, MonitorInfo):
            return self.Monitor == other.Monitor
        elif isinstance(other, collections.abc.Sequence):
            return self.Monitor == other
        return NotImplemented

    def __repr__(self) -> str:
        """Detailed string representation"""
        return (f"Monitor(left={self.left}, top={self.top}, right={self.right}, bottom={self.bottom}, "
                f"device='{self.Device}', flags={self.Flags})")

    def __match_args__(self) -> tuple:
        """Support for pattern matching with match/case"""
        return self.Monitor


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-monitorfrompoint
# HMONITOR MonitorFromPoint(
#   [in] POINT pt,
#   [in] DWORD dwFlags
# );
_MonitorFromPoint = ctypes.WINFUNCTYPE(
    wintypes.HMONITOR,
    wintypes.POINT,
    wintypes.DWORD,
)(
    ('MonitorFromPoint', ctypes.windll.user32),
    (
        (IN, 'pt'),
        (IN, 'dwFlags', MONITOR_DEFAULTTONEAREST),
    )
)


class RECT(ctypes.Structure):
    _fields_ = [
        ('_left', wintypes.LONG),
        ('_top', wintypes.LONG),
        ('_right', wintypes.LONG),
        ('_bottom', wintypes.LONG),
    ]

    @property
    def left(self) -> int:
        return self._left

    @property
    def top(self) -> int:
        return self._top

    @property
    def right(self) -> int:
        return self._right

    @property
    def bottom(self) -> int:
        return self._bottom

    @property
    def width(self) -> int:
        return self.right - self.left

    @property
    def height(self) -> int:
        return self.bottom - self.top

    @property
    def center(self) -> Tuple[int, int]:
        return self.left + (self.width // 2), self.top + (self.height // 2)


# First, define the correct callback type
MonitorEnumProc = ctypes.WINFUNCTYPE(
    wintypes.BOOL,  # Return type should be BOOL
    wintypes.HMONITOR,  # First parameter is HMONITOR
    wintypes.HDC,  # Second parameter is HDC
    ctypes.POINTER(RECT),  # Third parameter is RECT*
    wintypes.LPARAM  # Fourth parameter is LPARAM
)

# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumdisplaymonitors
# BOOL EnumDisplayMonitors(
#   [in] HDC             hdc,
#   [in] LPCRECT         lprcClip,
#   [in] MONITORENUMPROC lpfnEnum,
#   [in] LPARAM          dwData
# );
# Correctly define the EnumDisplayMonitors function
_EnumDisplayMonitors = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HDC,
    wintypes.LPRECT,
    MonitorEnumProc,  # Use the correct callback type
    wintypes.LPARAM,
)(
    ('EnumDisplayMonitors', ctypes.windll.user32),
    (
        (IN, 'hDC'),
        (IN, 'lpRect'),
        (IN, 'lpfnEnum'),
        (IN, 'dwData'),
    )
)


def EnumDisplayMonitors(lpfnEnum: Callable, py_object: Optional[object] = None) -> bool:
    """
    Enumerates all display monitors and calls the specified callback function for each monitor.

    Similar to win32gui.EnumWindows, this function allows passing custom data to the callback
    function, which can be a list, dictionary, or another callback function.

    Args:
        lpfnEnum: Callback function to be called for each monitor.
                 The callback receives (hMonitor, hDC, rect, data) where:
                 - hMonitor: Handle to the monitor
                 - hDC: Device context handle
                 - rect: RECT structure with monitor coordinates
                 - data: User-provided data (dwData parameter)
        py_object: User-defined data to pass to the callback. Can be any Python object,
               including lists, dictionaries, or functions.

    Returns:
        bool: True if successful, False otherwise.
    """

    # Create a wrapper callback that unpacks the pointer for your real callback
    def callback_wrapper(hMonitor, hDC, lpRect, lParam):
        # Dereference the pointer to get the actual RECT structure
        rect = lpRect.contents

        # Handle the case where we're using the data parameter
        if py_object is not None:
            # Call the user's callback with the user data
            return lpfnEnum(hMonitor, hDC, rect, py_object)
        else:
            # Call without extra data
            return lpfnEnum(hMonitor, hDC, rect, lParam)

    # Create a properly typed callback function
    callback = MonitorEnumProc(callback_wrapper)

    return _EnumDisplayMonitors(
        hDC = None,  # hDC
        lpRect = None,  # lpRect
        lpfnEnum = callback,  # lpfnEnum
        dwData = 0
    )


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getmonitorinfoa
# BOOL GetMonitorInfoA(
#   [in]  HMONITOR      hMonitor,
#   [out] LPMONITORINFO lpmi
# );
_GetMonitorInfo = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HMONITOR,
    ctypes.POINTER(MonitorInfo)
)(
    ('GetMonitorInfoA', ctypes.windll.user32),
    (
        (IN, 'hMonitor'),
        (IN, 'lpmi'),
    )
)


def MonitorFromPoint(x: int, y: int) -> wintypes.HMONITOR:
    # """
    # Retrieves a handle to the monitor that contains the specified point.
    #
    # Args:
    #     x (int): The x-coordinate of the point
    #     y (int): The y-coordinate of the point
    #     flags (int, optional): Behavior flags if point is not on any monitor.
    #         Defaults to MONITOR_DEFAULTTONEAREST.
    #
    # Returns:
    #     wintypes.HMONITOR: Handle to the monitor containing the point
    # """
    # result = _MonitorFromPoint(wintypes.POINT(x, y), MONITOR_DEFAULTTONULL)
    # if result:
    #     return result
    # else:
    return _MonitorFromPoint(wintypes.POINT(x, y), MONITOR_DEFAULTTONEAREST)


def GetMonitorInfo(hMonitor: wintypes.HMONITOR) -> MonitorInfo:
    """
    Retrieves information about a monitor by its handle.

    Args:
        hMonitor (wintypes.HMONITOR): Handle to the monitor

    Returns:
        Monitor: Monitor information structure containing coordinates,
                work area, flags, and device name

    Raises:
        WindowsError: If the function fails
    """
    mi = MonitorInfo()
    result = _GetMonitorInfo(hMonitor, ctypes.byref(mi))
    if result:
        return mi
    else:
        raise ctypes.WinError()  # Raise an exception for failure


# Example usage:
if __name__ == '__main__':
    # Example 1: Using a list to collect monitors
    monitors = []

    def collect_monitors(hMonitor, _hDC, _rect, monitors_list):
        """
        Collects information about a monitor and adds it to the provided list.

        This function uses the given monitor handle to retrieve monitor information
        and appends it to the monitors list. It is designed to be used as a callback
        function for enumerating monitors.

        :param hMonitor: Handle to the monitor whose information is being collected.
        :param _hDC: Handle to the device context. Unused in the function.
        :param _rect: A tuple or structure representing the monitor's rectangle.
        :param monitors_list: List to which the monitor information will be appended.
        :return: Always returns True to continue enumeration.

        :rtype: bool
        """
        # Get monitor info and add to list
        monitor_info = GetMonitorInfo(hMonitor)
        monitors_list.append(monitor_info)
        return True  # Continue enumeration

    # Pass the list as py_object
    EnumDisplayMonitors(lpfnEnum = collect_monitors, py_object = monitors)
    # Now the 'monitors' list is filled with monitor information

    for monitor in monitors:
        print(f"Monitor: {monitor.Device}")
        print(f"  Left: {monitor.left}, Top: {monitor.top}, Right: {monitor.right}, Bottom: {monitor.bottom}")
        print(f"  Width: {monitor.width}, Height: {monitor.height}")
        print(f"  Is Primary: {monitor.isPrimary}")
        print(f"  Is Anonymous: {monitor.isAnonymous}")
        print(f"  Center: {monitor.center}")
        print()

    # Example 2: Using a dictionary for statistics
    monitor_stats = {'count': 0, 'total_width': 0, 'total_height': 0}

    def gather_stats(hMonitor, _hDC, _rect, stats):
        monitor_info = GetMonitorInfo(hMonitor)
        stats['count'] += 1
        stats['total_width'] += monitor_info.width
        stats['total_height'] += monitor_info.height
        return True

    # Pass the dictionary as py_object
    EnumDisplayMonitors(lpfnEnum = gather_stats, py_object = monitor_stats)
    for stat, value in monitor_stats.items():
        print(f"{stat}: {value}")

    print()

    # Example 3: Using a callback function
    def process_monitor(monitor_info):
        print(f"Monitor: {monitor_info.Device}")
        print(f"  Left: {monitor_info.left}, Top: {monitor_info.top}, Right: {monitor_info.right}, Bottom: {monitor_info.bottom}")
        print(f"  Width: {monitor_info.width}, Height: {monitor_info.height}")
        print(f"  Is Primary: {monitor_info.isPrimary}")
        print(f"  Is Anonymous: {monitor_info.isAnonymous}")
        print(f"  Center: {monitor_info.center}")
        print()
        return True

    def callback_with_processor(hMonitor, _hDC, _rect, processor):
        monitor_info = GetMonitorInfo(hMonitor)
        return processor(monitor_info)

    # Pass the processing function as py_object
    EnumDisplayMonitors(lpfnEnum = callback_with_processor, py_object = process_monitor)

    print()

    # Get monitor at coordinate (0,0)
    monitor = GetMonitorInfo(
        hMonitor = MonitorFromPoint(
            x = 0,
            y = 0
        )
    )

    # Basic property access
    print(f"Monitor dimensions: {monitor.width}x{monitor.height}")
    print(f"Device: {monitor.Device}")

    # Sequence access to monitor coordinates
    print(f"Monitor coordinates: {monitor.Monitor}")
    left, top, right, bottom = monitor.Monitor
    print(f"Unpacked coordinates: L={left}, T={top}, R={right}, B={bottom}")

    # Dictionary-style access
    print(f"Work area: {monitor['Work']}")
    print(f"Is primary monitor: {monitor['isPrimary']}")

    # Accessing workspace
    workspace = monitor.Workspace
    print(f"Workspace dimensions: {workspace.width}x{workspace.height}")

    # Slicing examples
    top_left = monitor[:2]  # Get just left and top coordinates
    print(f"Top-left corner: {top_left}")

    # Pattern matching example
    match monitor.Monitor[2:]:
        case (3840, 1600):
            print("This is the primary monitor at (3840, 1600)")
        case (x, _) if x > 0:
            print(f"This is a secondary monitor, {x}px from the left edge")
        case _:
            print("Other monitor configuration")

    # Test point containment
    test_x, test_y = 100, 100
    print(f"Point ({test_x}, {test_y}) is within monitor: {monitor.contains_point(test_x, test_y)}")

    # Advanced workspace usage
    center_x, center_y = workspace.center
    print(f"Workspace center: ({center_x}, {center_y})")

    # Converting to dictionary
    monitor_dict = monitor.as_dict()
    print(f"All monitor properties: {monitor_dict.keys()}")
