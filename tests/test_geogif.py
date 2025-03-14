"""Tests for the geogif module."""
import os
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from geogif.core import GeoGIF


def test_geogif_from_geotiffs() -> None:
    """Test creating a GeoGIF from GeoTIFF files."""
    # This test would need actual GeoTIFF files
    # For CI purposes, this test would be skipped if files don't exist

    # Get test GeoTIFF files
    geotiff_files = list(sorted(Path.cwd().glob("*.tiff")))
    # Skip if test files don't exist
    if not all(Path(f).exists() for f in geotiff_files):
        pytest.skip("Test GeoTIFF files not found")

    output_file = "test_output.gif"

    try:
        geogif = GeoGIF.create_from_geotiffs(geotiff_files, output_file, fps=5)
        assert len(geogif.frames) == len(geotiff_files)
        assert Path(output_file).exists()
    finally:
        # Clean up
        if os.path.exists(output_file):
            os.remove(output_file)


def test_manual_geogif_creation() -> None:
    """Test manual creation of a GeoGIF."""
    geogif = GeoGIF()

    # Create some sample frames with geospatial information
    for i in range(3):  # Just use 3 frames for testing
        # Create a simple gradient image
        width, height = 100, 100  # Smaller size for faster tests
        pixels = np.zeros((height, width), dtype=np.uint8)
        for y in range(height):
            for x in range(width):
                pixels[y, x] = (x + y + i * 10) % 256

        # Define a geotransform (x_origin, pixel_width, 0, y_origin, 0, pixel_height)
        # This example shifts the origin slightly with each frame
        geotransform = (100 + i, 1, 0, 200 - i, 0, -1)

        # Use WGS84 as the CRS
        crs = 4326  # EPSG code for WGS84

        # Add the frame
        geogif.add_frame(pixels, geotransform, crs)

    # Save the GeoGIF
    output_file = "test_manual.gif"
    try:
        geogif.save(output_file, fps=5)
        assert len(geogif.frames) == 3
        assert os.path.exists(output_file)

        # Verify the file is a valid GIF
        img = Image.open(output_file)
        assert img.format == "GIF"
    finally:
        # Clean up
        if os.path.exists(output_file):
            os.remove(output_file)


def test_add_frame_validation() -> None:
    """Test validation in add_frame method."""
    geogif = GeoGIF()

    # Valid frame (using numpy array)
    valid_array = np.zeros((10, 10), dtype=np.uint8)
    geogif.add_frame(valid_array, (0, 1, 0, 0, 0, 1), 4326)
    assert len(geogif.frames) == 1

    # Valid frame (using PIL Image)
    valid_image = Image.new("L", (10, 10))
    geogif.add_frame(valid_image, (0, 1, 0, 0, 0, 1), 4326)
    assert len(geogif.frames) == 2

    # Invalid frame (wrong type)
    with pytest.raises(TypeError):
        geogif.add_frame("not_an_image", (0, 1, 0, 0, 0, 1), 4326)
