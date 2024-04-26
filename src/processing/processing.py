'''
This module contains classes and functions for frame processing
'''

from enum import Enum

from numpy.typing import NDArray


class PixelColor(Enum):
    '''
    Enum containing constants for pixel color 
    '''
    GRAY: int = 0
    RED: int = 1
    BLUE: int = 2


def get_frame_colors(frame: NDArray) -> NDArray:
    '''
    Returns HxW matrix containing color of each pixel, color is determined by PixelColor enum
    :param frame: HxWx3 image - a frame
    :returns: HxW array containing pixel colors
    '''
    
    assert len(frame.shape) == 3 and frame.shape[-1] == 3, 'frame should be a 3 channel image'
    raise NotImplementedError
