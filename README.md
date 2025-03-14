# GeoGIF

A specification for geospatially-referenced animated GIF images.

## What is it?

GeoGIF is an extension of the standard GIF format that embeds geospatial metadata within the file. This allows each frame of an animated GIF to maintain its own geographic reference information, similar to how GeoTIFF works for static images. With GeoGIF, animated visualizations can be properly positioned and scaled on maps in GIS applications.

## Installation

```bash
pip install geogif
```



## Usage
### Command Line Interface (CLI)
GeoGIF provides a simple command-line interface with two main commands: `create` and `info`.

#### Create a GeoGIF
Convert a series of GoeTIFF files inot an animated GeoGIF:
```bash
geogif create -o output.gif --fps 10 /path/to/image1.tiff /path/to/image2.tiff /path/to/image3.tiff
```

It is more common to use wildcards to include multiple GeoTIFFs
```bash
geogif create -o temperature_animation.gif --fps 8 /path/to/temperature_*.tiff
```
Options

- `-o, --output`: Specify the output filename (required)
- `--fps`: Frames per second (default: 10)
- `-v, --verbose`: Enable detailed logging


#### Viewing GeoGIF Information
Analyze a GeoGIF file to view its metadata:
```bash
geotif info temperature_animation.gif
```
This will display information about the file including:

- Number of frames
- Frame duration
- Total Duration `> coming soon`
- Spatial reference information for each frame
- Coordinate bounds

### Python API
GeoGIF can also be used a Python module in your own applications:

```python
from geogif import GeoGIF
import numpy as np
from osgeo import osr

# Method 1: Create a GeoGIF from scratch
geogif = GeoGIF()

# Add frames manually with numpy arrays
image_data = np.zeros((100, 100), dtype=np.uint8)
geotransform = (0, 1, 0, 0, 0, 1)  # GDAL-style geotransform
crs = 4326  # EPSG code for WGS 84
geogif.add_frame(image_data, geotransform, crs)

# Save with desired frames per second
geogif.save("output.gif", fps=5)

# Method 2: Create from existing GeoTIFF files
geotiff_files = [
    "frame1.tif",
    "frame2.tif",
    "frame3.tif"
]
GeoGIF.create_from_geotiffs(geotiff_files, "animation.gif", fps=10)

# Method 3: Load and examine an existing GeoGIF
loaded_geogif = GeoGIF.from_file("existing.gif")
print(f"Number of frames: {len(loaded_geogif)}")
print(f"Frame duration: {loaded_geogif.duration_ms} ms")

# Accessing individual frames
frame = loaded_geogif[0]  # Get first frame
print(f"Geotransform: {frame.geotransform}")
print(f"CRS: {frame.crs}")

# Combining GeoGIFs
geogif1 = GeoGIF.from_file("animation1.gif")
geogif2 = GeoGIF.from_file("animation2.gif")
combined_geogif = geogif1 + geogif2
combined_geogif.save("combined.gif", fps=8)

```




## Why GeoGIF?

GeoGIF solves a key challenge in geospatial visualization: the ability to share animated, georeferenced data in a widely-supported format. While GeoTIFF is the standard for static geospatial imagery, there hasn't been an equivalent for animations until now.

### Key Benefits:

- **Temporal Data Visualization**: Perfect for showing change over time (climate data, urban growth, seasonal variations)
- **Wide Compatibility**: Built on the ubiquitous GIF format
- **Lightweight**: More efficient than video formats for many geospatial visualizations
- **Self-contained**: Geographic metadata travels with the imagery
- **Frame-specific Georeferencing**: Each frame can have its own coordinate reference system and transformation

## How It Works

GeoGIF embeds geospatial metadata within the GIF's Application Extension blocks, allowing for:

- Coordinate Reference System (CRS) information
- Georeferencing transformation matrices
- Metadata about the source data

This ensures that GIS software can correctly position and scale each frame of the animation.

## Example Use Cases

- Animated weather radar or satellite imagery
- Urban growth and land use change visualizations
- Temporal analysis of environmental phenomena
- Seasonal vegetation changes
- Historical map animations
- Visualize satellite video in GIS viewer (Arc,QGIS)

## Getting Started

Check out our [documentation](docs/README.md) to learn how to create and work with GeoGIF files.

## References

1. [GIF Graphics Interchange Format, Version 89a](https://www.loc.gov/preservation/digital/formats/fdd/fdd000133.shtml)
2. [OGC GeoTIFF standard](https://docs.ogc.org/is/19-008r4/19-008r4.html)

## Contributing

Contributions are welcom to this experimental and entirely notional GeoGIF specification and implementation! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
