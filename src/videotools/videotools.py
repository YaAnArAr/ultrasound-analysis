from collections.abc import Generator
from pathlib import Path

from numpy.typing import NDArray


def read_video(path: Path | str) -> Generator[NDArray, None, None]:
    '''
    Read the video frame-by-frame
    :param path: path to the video
    :returns: generator, yielding RGB video frames
    '''
    pass
