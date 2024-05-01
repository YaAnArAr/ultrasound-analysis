"""
This module contains classes and functions for video operations
"""

from pathlib import Path

import cv2

from numpy.typing import NDArray


CROP_OFFSET = ((150, 100), (20, 20))


def crop_frame(frame: NDArray, crop_offset: tuple[tuple[int, int]] = CROP_OFFSET) -> NDArray:
    """
    Crop frame
    :param frame: frame that need to crop
    :param crop_offset: cropping offset in the following format:
    :returns: cropped frame
    """
    x_offset, y_offset = crop_offset
    x_first_offset, x_second_offset = x_offset
    y_first_offset, y_second_offset = y_offset
    x, y = frame.shape[0], frame.shape[1]
    cropped_frame = frame[x_first_offset:x - x_second_offset, 
                          y_first_offset:y - y_second_offset]
    return cropped_frame


def read_video(path: Path | str) -> NDArray:
    """
    Read the video frame-by-frame
    :param path: path to the video
    :returns: generator, yielding RGB cropped video frames
    """
    cap = cv2.VideoCapture(path)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            yield crop_frame(frame).astype('uint8')
