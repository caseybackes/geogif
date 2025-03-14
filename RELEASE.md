# GeoGIF Release Guide

This document outlines the process for releasing new versions of the GeoGIF (pypi: `RealGeoGIF`) package. When a new release is created on GitHub, the package is automatically published to PyPI using GitHub Actions as a Trusted Publisher.

## Release Preparation

### 1. Update Version Number

Update the version in `pyproject.toml`:

```toml
[project]
name = "realgeogif"
version = "0.1.0"  # Update this for new releases
```

Follow [Semantic Versioning](https://semver.org/) guidelines:
- MAJOR version for incompatible API changes
- MINOR version for backwards-compatible functionality additions
- PATCH version for backwards-compatible bug fixes

### 2. Update Documentation

Ensure all documentation reflects the new version:
- Update README.md with new features
- Update code examples if API has changed
- Add new version to changelog

### 3. Pre-Release Testing

Perform these checks before creating a release:
- Run all tests: `pytest`
- Verify the package builds correctly: `python -m build`
- Test installation from a local build

## Creating a Release

### 1. Commit and Push Changes

```bash
git add .
git commit -m "Prepare release v0.1.1"
git push origin main
```

### 2. Create a GitHub Release

1. Go to the [Releases page](https://github.com/caseybackes/geogif/releases)
2. Click "Draft a new release"
3. Create a new tag (e.g., `v0.1.1`)
4. Write a title and description highlighting:
   - New features
   - Bug fixes
   - Breaking changes
   - Dependency updates
5. Click "Publish release"

### 3. Automatic Publishing

The GitHub Actions workflow will automatically:
- Build the package
- Publish to PyPI
- Tag the release in the repository

You can monitor the workflow progress in the "Actions" tab of your repository.

## Verifying the Release

### 1. Check PyPI

Verify the new version is available on PyPI:
- https://pypi.org/project/realgeogif/

### 2. Test Installation

```bash
# Create a fresh virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install the new version
pip install realgeogif

# Verify the correct version is installed
pip show realgeogif
```

### 3. Test Basic Functionality

Create a simple script to verify core functionality works as expected.

## Alternative: Manual Publishing

In case the automatic workflow fails, you can publish manually:

### 1. Generate API Token

Create a token at https://pypi.org/manage/account/#api-tokens

### 2. Build Package

```bash
rm -rf dist/
python -m build
```

### 3. Publish Manually

```bash
python -m twine upload dist/*
```

## GDAL Installation Notes

Since RealGeoGIF depends on GDAL, users may need to install it first:

- **Ubuntu/Debian**: `sudo apt-get install libgdal-dev`
- **macOS**: `brew install gdal`
- **Windows**: Using Conda: `conda install -c conda-forge gdal`

## Troubleshooting

### Build Errors

If you encounter build errors:
- Verify all dependencies are installed
- Check that GDAL is properly installed
- Make sure `pyproject.toml` is correctly formatted

### Publication Errors

If automatic publication fails:
- Check the GitHub Actions logs for details
- Verify that the Trusted Publisher configuration is correct
- Try manual publication as a fallback

## Version History

- 0.1.0: Initial release

## Links

- PyPI Package: https://pypi.org/project/realgeogif/
- GitHub Repository: https://github.com/caseybackes/geogif
- Documentation: [link to docs]
