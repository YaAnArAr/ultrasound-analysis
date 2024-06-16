from dataclasses import dataclass

import numpy as np

from ..processing import Cloud


@dataclass
class CloudFeature:
    cloud: Cloud
    excentricity: float
    square: float


@dataclass
class ImageFeature:
    mean_square: float
    number_of_clouds: int


def extract_cloud_features(cloud: Cloud) -> CloudFeature:
    """
    Extracts features from one cloud
    :param cloud: cloud whose features will be extracted
    :returns: features
    """
    (x1, x2), (y1, y2) = cloud.bounding_box
    size = x2 - x1, y2 - y1
    excentricity = size[0] / size[1]

    return CloudFeature(
        cloud=cloud,
        excentricity=excentricity,
        square=cloud.square
    )


def extract_image_features(clouds: list[Cloud]) -> ImageFeature:
    """
    Extracts feature from image clouds
    :param clouds: image clouds
    :returns: image features
    """
    features = list(map(extract_cloud_features, clouds))
    return ImageFeature(
        mean_square=np.mean([c.square for c in features]),
        number_of_clouds=len(clouds)
    )
