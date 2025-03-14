#!/usr/bin/env python3
"""Command-line interface for the GeoGIF library."""
import argparse
import glob
import logging
import os
import sys
from typing import List, Optional

from .core import GeoGIF

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def create_geogif(
    geotiff_files: List[str], output_file: str, fps: int = 10, verbose: bool = False
) -> None:
    """Create a GeoGIF from GeoTIFF files."""
    setup_logging(verbose)

    if not geotiff_files:
        logger.error("No GeoTIFF files provided")
        sys.exit(1)

    # Check if files exist
    missing_files = [f for f in geotiff_files if not os.path.exists(f)]
    if missing_files:
        logger.error(f"The following files do not exist: {', '.join(missing_files)}")
        sys.exit(1)

    logger.info(f"Creating GeoGIF from {len(geotiff_files)} GeoTIFF files")

    try:
        geogif = GeoGIF.create_from_geotiffs(geotiff_files, output_file, fps=fps)
        logger.info(f"GeoGIFcreated with {len(geogif.frames)} frames at {output_file}")
    except Exception as e:
        logger.error(f"Error creating GeoGIF: {e}")
        sys.exit(1)


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="GeoGIF - Create animated GIFs with geospatial metadata"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Create command
    create_parser = subparsers.add_parser(
        "create", help="Create a GeoGIF from GeoTIFF files"
    )
    create_parser.add_argument(
        "files", nargs="+", help="GeoTIFF files to include in the GeoGIF"
    )
    create_parser.add_argument(
        "-o", "--output", required=True, help="Output GeoGIF filename"
    )
    create_parser.add_argument(
        "--fps", type=int, default=10, help="Frames per second (default: 10)"
    )
    create_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )

    # Info command (could be expanded in the future)
    info_parser = subparsers.add_parser(
        "info", help="Display information about a GeoGIF file"
    )
    info_parser.add_argument("file", help="GeoGIF file to analyze")
    info_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )

    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        parser.print_help()
        sys.exit(0)

    return parsed_args


def display_info(file: str, verbose: bool = False) -> None:
    """Display information about a GeoGIF file."""
    setup_logging(verbose)

    if not os.path.exists(file):
        logger.error(f"File does not exist: {file}")
        sys.exit(1)

    logger.info(f"Analyzing GeoGIF file: {file}")

    try:
        geogif = GeoGIF.from_file(file)
        logger.info(f"GeoGIF file contains {len(geogif.frames)} frames")
        logger.info(f"Frame duration: {geogif.duration_ms} ms")

        if verbose:
            for i, geoframe_i in enumerate(geogif.frames):
                logger.debug(f"{geoframe_i.__class__} {i+1}:")
                logger.debug(f"  Geotransform: {geoframe_i.geotransform}")
                logger.debug(f"  CRS: {geoframe_i.crs_wkt}...")
    except Exception as e:
        logger.error(f"Error analyzing GeoGIF: {e}")
        sys.exit(1)


def main(args: Optional[List[str]] = None) -> None:
    """Grants main entry point for the CLI."""
    parsed_args = parse_args(args)

    if parsed_args.command == "create":
        # Handle file globs (if any)
        files = []
        for file_pattern in parsed_args.files:
            expanded = glob.glob(file_pattern)
            if expanded:
                files.extend(expanded)
            else:
                files.append(file_pattern)  # Keep as is, will be checked later

        create_geogif(files, parsed_args.output, parsed_args.fps, parsed_args.verbose)
    elif parsed_args.command == "info":
        display_info(parsed_args.file, parsed_args.verbose)


if __name__ == "__main__":
    main()
