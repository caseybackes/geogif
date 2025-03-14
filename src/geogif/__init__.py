"""GeoGIF - A format for geospatially referenced animated GIFs.

This package provides tools for creating and manipulating animated GIFs
that contain geospatial metadata for each frame, combining the temporal
capabilities of GIF with the georeferencing capabilities of GeoTIFF.
"""

from osgeo import gdal

from .core import GeoGIF

__version__ = "0.1.0"
gdal.UseExceptions()
