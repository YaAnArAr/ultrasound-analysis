"""
This module contains classes and functions for frame processing
"""

from enum import Enum
from dataclasses import dataclass, field
from operator import itemgetter

from numpy.typing import NDArray


Pixel = tuple[int, int]


class PixelColor(Enum):
    """
    Enum containing constants for pixel color 
    """
    GRAY: int = 0
    RED: int = 1
    BLUE: int = 2


@dataclass
class Cloud:
    """
    Class, representing cloud points of specific color
    """
    color: PixelColor
    points: set[Pixel] = field(default_factory=set)

    def min(self, axis: int | None = None) -> Pixel:
        """
        Returns minimal pixel, if axis is specified, minimal pixel for x or y is returned
        Note: if axis is not None, returned pixel is minimal by specified axis, but it is not minimal in total
        :returns: minimal pixel, if axis is specified, minimal pixel for x or y is returned
        """
        if axis is None:
            return min(self.points)
        
        assert 0 <= axis <= 1
        return min(self.points, key=itemgetter(axis)) 
        
    def square(self) -> int:
        """
        Returns square of the cloud
        """
        return len(self.points)


def get_frame_colors(frame: NDArray) -> NDArray:
    """
    Returns HxW matrix containing color of each pixel, color is determined by PixelColor enum
    :param frame: HxWx3 image - a frame
    :returns: HxW array containing pixel colors
    """
    assert len(frame.shape) == 3 and frame.shape[-1] == 3, 'frame should be a 3 channel image'
    raise NotImplementedError


def get_clouds(frame: NDArray) -> list[Cloud]:
    """
    Returns list of point clouds of the frame
    :param frame: HxWx3 image - a frame
    :returns: list of Cloud objects, where each one represents a cloud of specific color
    """
    assert len(frame.shape) == 3 and frame.shape[-1] == 3, 'frame should be a 3 channel image'
    raise NotImplementedError
