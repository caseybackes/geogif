# GeoGIF

A specification for geospatially-referenced animated GIF images.

## What is it?

GeoGIF is an extension of the standard GIF format that embeds geospatial metadata within the file. This allows each frame of an animated GIF to maintain its own geographic reference information, similar to how GeoTIFF works for static images. With GeoGIF, animated visualizations can be properly positioned and scaled on maps in GIS applications.

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

## Getting Started

Check out our [documentation](docs/README.md) to learn how to create and work with GeoGIF files.

## References

1. [GIF Graphics Interchange Format, Version 89a](https://www.loc.gov/preservation/digital/formats/fdd/fdd000133.shtml)
2. [OGC GeoTIFF standard](https://docs.ogc.org/is/19-008r4/19-008r4.html)

## Contributing

Contributions are welcom to this experimental and entirely notional GeoGIF specification and implementation! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
