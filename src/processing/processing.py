"""
This module contains classes and functions for frame processing
"""

from enum import Enum
from dataclasses import dataclass, field
from operator import itemgetter
from queue import Queue

import numpy as np

from numpy.typing import NDArray

from ..videotools import to_float_image

Pixel = tuple[int, int]

SENSIVITY = 5


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
        Note: if axis is not None, returned pixel is minimal by specified axis, 
        but it is not minimal in total
        :returns: minimal pixel, if axis is specified, minimal pixel for x or y is returned
        """
        if axis is None:
            return min(self.points)
        assert 0 <= axis <= 1
        return min(self.points, key=itemgetter(axis))

    @property
    def square(self) -> int:
        """
        Returns square of the cloud
        """
        return len(self.points)

    @property
    def bounding_box(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        Returns bounding box of the cloud in format:
        ((x_lower, x_upper), (y_lower, y_upper))
        """
        x_min = min(self.points, key=itemgetter(0))[0]
        x_max = max(self.points, key=itemgetter(0))[0]
        y_min = min(self.points, key=itemgetter(1))[1]
        y_max = max(self.points, key=itemgetter(1))[1]
        return (x_min, x_max), (y_min, y_max)


def get_frame_colors(frame: NDArray, sensivity: float | int = SENSIVITY) -> NDArray:
    """
    Returns HxW matrix containing color of each pixel, color 
    is determined by PixelColor enum
    :param frame: HxWx3 RGB image - a frame
    :param sensivity: maximal difference between values when 
    pixel is considered grayscale
    :returns: HxW array containing pixel colors
    """
    if isinstance(sensivity, int):
        sensivity /= 256
    assert len(frame.shape) == 3 and frame.shape[-1] == 3, 'frame should be a 3 channel image'
    frame = to_float_image(frame)
    medians = np.median(frame, axis=-1)
    result = np.zeros((frame.shape[:2]), dtype=np.uint8)
    result += (PixelColor.RED.value * ((frame[:, :, 0] - medians) > sensivity)).astype('uint8')
    result += (PixelColor.BLUE.value * ((frame[:, :, -1] - medians) > sensivity)).astype('uint8')
    return result


def get_color(frame: NDArray, color: PixelColor) -> NDArray:
    """
    Returns HxW matrix containing pixels with specific color, color
    is determined by PixelColor enum
    :param frame: HxW matrix containing color of each pixel
    :param color: color that detecting specific group of clouds
    :returns: HxW array containing pixels with color (gray-scaled image)
    """
    gray_scaled_frame = frame == color.value
    gray_scaled_frame = gray_scaled_frame.astype('int')
    return gray_scaled_frame


def get_clouds(frame: NDArray, color: PixelColor) -> list[Cloud]:
    """
    Returns list of point clouds of the frame
    :param frame: HxW image - a frame
    :param color: pixel's color for processing
    :returns: list of Cloud objects, where each one represents a cloud of specific color
    """
    gray_scaled_image = np.pad(get_color(frame, color), 1, constant_values=0)
    modified_image = np.pad(np.zeros(shape=frame.shape), 1, constant_values=0)
    dx = np.array([-1, -1, -1, 0, 0, 1, 1, 1])
    dy = np.array([-1, 1, 0, -1, 1, -1, 0, 1])
    counter = 1
    clouds = []
    for i in range(1, frame.shape[0] + 1):
        for j in range(1, frame.shape[1] + 1):
            if gray_scaled_image[i][j] == 1 and modified_image[i][j] == 0:
                queue = Queue()
                cloud = Cloud(color=color, points=set())
                queue.put(Pixel((i, j)))
                modified_image[i][j] = counter
                cloud.points.add(Pixel((i - 1, j - 1)))
                while not queue.empty():
                    x, y = queue.get()
                    for k in range(0, 8):
                        nx = x + dx[k]
                        ny = y + dy[k]
                        if gray_scaled_image[nx][ny] == 1 and modified_image[nx][ny] == 0:
                            queue.put(Pixel((nx, ny)))
                            modified_image[nx][ny] = counter
                            cloud.points.add(Pixel((nx - 1, ny - 1)))
                clouds.append(cloud)
                counter += 1
    return clouds
