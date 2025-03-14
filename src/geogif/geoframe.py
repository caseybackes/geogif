"""GeoFrame - A single frame in a GeoGIF."""
from dataclasses import dataclass
from typing import Tuple, Union

import numpy as np
from PIL import Image


@dataclass
class GeoFrame:
    """GeoFrame - A single frame in a GeoGIF."""

    __slots__ = [
        "image",
        "geotransform",
        "crs_wkt",
    ]  # Note: changed crs to crs_wkt to match field
    image: Union[Image.Image, np.ndarray]
    geotransform: Tuple[float, float, float, float, float, float]
    crs_wkt: str  # Store as WKT string for consistency
