"""
This module contains classes and functions for video operations
"""

from pathlib import Path

import cv2

from numpy.typing import NDArray


def crop_frame(frame: NDArray) -> NDArray:
    """
    Crop frame
    :param frame: frame that need to crop
    :returns: cropped frame
    """
    x_first_offset = 150
    x_second_offset = 100
    y_offset = 20
    x, y = frame.shape[0], frame.shape[1]
    cropped_frame = frame[x_first_offset:x - x_second_offset, y_offset:y - y_offset]
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
