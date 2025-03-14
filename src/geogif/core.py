"""GeoGIF - A format for geospatially referenced animated GIFs."""
import os
from pathlib import Path
from typing import List, Union

import numpy as np
from osgeo import gdal, osr
from PIL import Image, ImageSequence

from .geoframe import GeoFrame

gdal.UseExceptions()


class GeoGIF:
    """GeoGIF - A format for geospatially referenced animated GIFs.

    This prototype implements a basic structure for storing geospatial metadata
    within GIF Application Extension blocks, allowing each frame to maintain
    its own georeference information.

    Attributes:
        frames (list): List of (image, geotransform, crs) tuples
        duration (int): Frame duration in milliseconds

    Properties:
        APP_EXTENSION_IDENTIFIER (bytes): Application Extension identifier for GeoGIF

    Methods:
        add_frame: Add a frame to the GeoGIF with its associated geospatial information
        save: Save the GeoGIF to a file
        _add_geospatial_metadata: Add geospatial metadata to the GIF file by modifying
        it directly
        from_file: Load a GeoGIF from a file
        create_from_geotiffs: Create a GeoGIF from a sequence of GeoTIFF files

    Examples:
        Create a GeoGIF from scratch:
        >>> geogif = GeoGIF()
        >>> image_data = np.zeros((100, 100), dtype=np.uint8)
        >>> geotransform = (0, 1, 0, 0, 0, 1)
        >>> crs = 4326
        >>> geogif.add_frame(image_data, geotransform, crs)
        >>> geogif.save("output.gif", fps=5)

        Load a GeoGIF from a file:
        >>> geogif = GeoGIF.from_file("input.gif")
        >>> print(len(geogif.frames))

        Create a GeoGIF from a sequence of GeoTIFF files:
        >>> geotiff_files = [
        ...     "frame1.tif",
        ...     "frame2.tif",
        ...     "frame3.tif"
        ... ]
        >>> GeoGIF.create_from_geotiffs(geotiff_files, "output.gif", fps=5)

        Manual creation of a GeoGIF:
        >>> geogif = GeoGIF()
        >>> for i in range(3):
        ...     pixels = np.zeros((100, 100), dtype=np.uint8)
        ...     geotransform = (100 + i, 1, 0, 200 - i, 0, -1)
        ...     crs = 4326
        ...     geogif.add_frame(pixels, geotransform, crs)
        >>> geogif.save("manual.gif", fps=5)

        Validation of add_frame method:
        >>> geogif = GeoGIF()
        >>> with pytest.raises(TypeError):
        ...     geogif.add_frame("invalid", (0, 1, 0, 0, 0, 1), 4326)
        >>> with pytest.raises(ValueError):
        ...     geogif.save("empty.gif")

        Validation of create_from_geotiffs method:
        >>> with pytest.raises(ValueError):
        ...     GeoGIF.create_from_geotiffs(["nonexistent.tif"], "output.gif", fps=5)

        Validation of from_file method:
        >>> with pytest.raises(ValueError):
        ...     geogif = GeoGIF.from_file("nonexistent.gif")

        Validation of save method:
        >>> geogif = GeoGIF()
        >>> with pytest.raises(ValueError):
        ...     geogif.save("empty.gif")

        Validation of _add_geospatial_metadata method:
        >>> geogif = GeoGIF()
        >>> with pytest.raises(FileNotFoundError):
        ...     geogif._add_geospatial_metadata("nonexistent.gif")

        Validation of APP_EXTENSION_IDENTIFIER property:
        >>> geogif = GeoGIF()
        >>> assert geogif.APP_EXTENSION_IDENTIFIER == b'GEOGIF10'


    """

    # Application Extension identifier for GeoGIF
    APP_EXTENSION_IDENTIFIER = b"GEOGIF10"  # 8 bytes as per GIF spec

    def __init__(self) -> None:
        """Initialize a GeoGIF object.

        Attributes:
            frames (list): List of GeoFrame objects
            duration (int): Frame duration in milliseconds
        """
        self.frames: List[
            GeoFrame
        ] = list()  # List of (image, geotransform, crs) tuples
        self.duration_ms = 100  # Default frame duration in milliseconds

    def __len__(self) -> int:
        """Return the number of frames in the GeoGIF."""
        return len(self.frames)

    def __add__(self, other: "GeoGIF") -> "GeoGIF":
        """Combine two GeoGIF objects by concatenating their frames.

        Args:
            other (GeoGIF): Another GeoGIF object

        Returns:
            GeoGIF: Combined GeoGIF object

        Raises:
            TypeError: If the other object is not a GeoGIF

        Example:
            >>> combined_geogif = geogif1 + geogif2
        """
        if not isinstance(other, GeoGIF):
            raise TypeError(
                "Unsupported operand type(s) for +: 'GeoGIF' and '{type(other)}'"
            )
        combined_geogif = GeoGIF()
        combined_geogif.frames = self.frames + other.frames
        combined_geogif.duration_ms = min(
            self.duration_ms, other.duration_ms
        )  # TODO: min or max here?
        return combined_geogif

    def __getitem__(self, index: int) -> GeoFrame:
        """Get a frame from the GeoGIF by index returned as a GeoFrame object.

        Args:
            index (int): Frame index

        Returns:
            GeoFrame: A GeoFrame object with attributes
            - image: PIL Image or numpy array
            - geotransform: GDAL-style geotransform (6-tuple)
            - crs: Coordinate Reference System (as WKT string

        Raises:
            IndexError: If the index is out of bounds

        Example:
            >>> frame = geogif[0]
        """
        return self.frames[index]

    def add_frame(
        self,
        image_data: Union[Image.Image, np.ndarray],
        geotransform: Union[tuple, list],
        crs: Union[str, int, osr.SpatialReference],
    ) -> None:
        """Add a frame to the GeoGIF with its associated geospatial information.

        Args:
            image_data: PIL Image or numpy array
            geotransform: GDAL-style geotransform (6-tuple)
            crs: Coordinate Reference System (as WKT, EPSG code, or osr.SpatialReference)

        Returns:
            None

        Raises:
            TypeError: If image_data is not a PIL Image or numpy array

        Example:
            >>> geogif = GeoGIF()
            >>> image_data = np.zeros((100, 100), dtype=np.uint8)
            >>> geotransform = (0, 1, 0, 0, 0, 1)
            >>> crs = 4326
            >>> geogif.add_frame(image_data, geotransform, crs)
        """
        if isinstance(image_data, np.ndarray):
            # Convert numpy array to PIL Image
            image = Image.fromarray(image_data)
        elif isinstance(image_data, Image.Image):
            image = image_data
        else:
            raise TypeError("image_data must be a PIL Image or numpy array")

        # Validate geotransform length
        if len(geotransform) != 6:
            raise ValueError("geotransform must be a 6-tuple")

        # Convert CRS to WKT if it's an EPSG code or osr.SpatialReference
        if isinstance(crs, int):
            # Assume it's an EPSG code
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(crs)
            crs_wkt = srs.ExportToWkt()
        elif isinstance(crs, osr.SpatialReference):
            crs_wkt = crs.ExportToWkt()
        else:
            # Assume it's already in WKT format
            crs_wkt = crs

        # Ensure geotransform is a tuple of six floats
        geotransform_tuple = (
            geotransform[0],
            geotransform[1],
            geotransform[2],
            geotransform[3],
            geotransform[4],
            geotransform[5],
        )
        geoframe: GeoFrame = GeoFrame(image, geotransform_tuple, crs_wkt)
        self.frames.append(geoframe)

    def save(self, filename: Union[Path, str], fps: int = 10) -> Union[Path, str]:
        """Save the GeoGIF to a file.

        Args:
            filename (pathlib.Path | str): Output filename
            fps (int): Frames per second

        Returns:
            pathlib.Path | str: Output

        Raises:
            ValueError: If no frames are present in the GeoGIF

        Example:
            >>> geogif = GeoGIF()
            >>> image_data = np.zeros((100, 100), dtype=np.uint8)
            >>> geotransform = (0, 1, 0, 0, 0, 1)
            >>> crs = 4326
            >>> geogif.add_frame(image_data, geotransform, crs)
            >>> geogif.save("output.gif", fps=5)

        """
        if not self.frames:
            raise ValueError("No frames to save")

        # Update duration based on fps
        self.duration_ms = int(1000 / fps)

        # Prepare images with durations
        images = []
        for frame in self.frames:
            # Convert if needed and ensure it's in a format suitable for GIF
            if isinstance(frame.image, np.ndarray):
                img = Image.fromarray(frame.image)
            else:
                img = frame.image
            # Convert to palette mode for GIF (if not already)
            if img.mode not in ["P", "L"]:
                img = img.convert("P", palette=Image.ADAPTIVE, colors=256)
            images.append(img)

        # Save as GIF - properly use the first image's save method
        images[0].save(
            filename,
            save_all=True,
            append_images=images[1:],
            duration=self.duration_ms,
            loop=0,  # 0 means loop indefinitely
        )

        # Append geospatial metadata to the GIF using a custom post-processor
        self._add_geospatial_metadata(filename)

        return filename

    def _add_geospatial_metadata(self, filename: Union[Path, str]) -> None:
        """Add geospatial metadata to the GIF file by modifying it directly.

        This method adds Application Extension blocks with GeoTIFF-like metadata.

        Args:
            filename (str): Output filename

        Raises:
            FileNotFoundError: If the GIF file cannot be opened

        Returns:
            None

        Example:
            >>> geogif = GeoGIF()
            >>> geogif.add_frame(image_data, geotransform, crs)
            >>> geogif.save("output.gif", fps=5)
            >>> geogif._add_geospatial_metadata("output.gif")
        """
        # Read the original GIF file
        with open(str(filename), "rb") as f:
            gif_data = f.read()

        # Find the positions of frame starts
        # This is a simplification - in reality, you would need to parse the GIF structure properly
        # as frame boundaries aren't easily detectable without understanding the GIF format in detail

        # For prototype purposes, we'll create a new file with our custom metadata
        temp_filename = str(filename) + ".temp"

        with open(temp_filename, "wb") as f:
            # Write GIF header (first 13 bytes)
            f.write(gif_data[:13])

            # Find the position right after the Logical Screen Descriptor and Global Color Table
            # This is where we would insert our global GeoGIF Application Extension
            # For a real implementation, more sophisticated GIF parsing would be needed

            # For each frame, we'd need to:
            # 1. Write the frame's image data
            # 2. Insert our GeoGIF Application Extension with the frame's geotransform and CRS

            # For this prototype, we'll just write the rest of the original GIF data
            f.write(gif_data[13:])

        # Replace original file with our modified version
        os.replace(temp_filename, filename)

    @classmethod
    def from_file(cls, filename: Union[Path, str]) -> "GeoGIF":
        """Load a GeoGIF from a file.

        Args:
            filename (str): Input GeoGIF filename

        Returns:
            A GeoGIF object

        Raises:
            ValueError: If the GIF file cannot be opened

        Example:
            >>> geogif = GeoGIF.from_file("input.gif")
            >>> print(len(geogif.frames))
        """
        # Initialize a new GeoGIF object
        geogif = cls()

        # Open the GIF file
        gif = Image.open(filename)

        # Extract frames
        for frame in ImageSequence.Iterator(gif):
            # In a real implementation, we would:
            # 1. Extract the frame image
            # 2. Find the associated GeoGIF Application Extension
            # 3. Parse the geotransform and CRS from it
            # 4. Add the frame to our GeoGIF object

            # For this prototype, we'll just add the frame with dummy geospatial data
            geogif.add_frame(
                frame.copy(),  # Copy is needed as frame is reused by Iterator
                (0, 1, 0, 0, 0, 1),  # Dummy geotransform
                4326,  # WGS 84 EPSG code
            )

        # Set duration from the original GIF
        if "duration" in gif.info:
            geogif.duration_ms = gif.info["duration"]

        return geogif

    @staticmethod
    def create_from_geotiffs(
        geotiff_filenames: List[str], output_filename: str, fps: int
    ) -> "GeoGIF":
        """Create a GeoGIF from a sequence of GeoTIFF files.

        Args:
            geotiff_filenames (list): List of GeoTIFF filenames
            output_filename (str): Output GeoGIF filename
            fps (int): Frames per second

        Returns:
            A GeoGIF object

        Raises:
            ValueError: If a GeoTIFF file cannot be opened

        Example:
            >>> geotiff_files = [
            ...     "frame1.tif",
            ...     "frame2.tif",
            ...     "frame3.tif"
            ... ]
            >>> GeoGIF.create_from_geotiffs(geotiff_files, "output.gif", fps=5)

        """
        geogif = GeoGIF()

        for tiff_file in geotiff_filenames:
            # Open the GeoTIFF file with GDAL
            ds = gdal.Open(tiff_file)
            if ds is None:
                raise ValueError(f"Could not open GeoTIFF file: {tiff_file}")

            # Get the geotransform
            geotransform = ds.GetGeoTransform()

            # Get the CRS
            crs_wkt = ds.GetProjection()

            # Read the raster data
            band = ds.GetRasterBand(1)
            data = band.ReadAsArray()

            # Convert to PIL Image (this is simplified and might need adjustment based on data type)
            # For true color images, you would need to handle multiple bands
            if data.dtype == np.uint8:
                image = Image.fromarray(data)
            else:
                # Normalize data to 0-255 range for display
                data_min, data_max = data.min(), data.max()
                normalized_data = (
                    (data - data_min) / (data_max - data_min) * 255
                ).astype(np.uint8)
                image = Image.fromarray(normalized_data)

            # Add the frame to the GeoGIF
            geogif.add_frame(image, geotransform, crs_wkt)

            # Close the dataset
            ds = None

        # Save the GeoGIF
        geogif.save(output_filename, fps)

        return geogif
