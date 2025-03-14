# Contributing to GeoGIF

Thank you for considering contributing to GeoGIF! This document outlines the process for contributing to the project and provides guidelines to help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Development Environment](#development-environment)
  - [Installing Dependencies](#installing-dependencies)
- [Development Workflow](#development-workflow)
  - [Branching Strategy](#branching-strategy)
  - [Coding Standards](#coding-standards)
  - [Pre-commit Hooks](#pre-commit-hooks)
  - [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)
- [Communication](#communication)

## Code of Conduct

We expect all contributors to adhere to a respectful and inclusive environment. Please be considerate of others and maintain a professional attitude in all communications.

## Getting Started

### Development Environment

GeoGIF requires:
- Python 3.8 or newer
- GDAL 3.0.0 or newer

### Installing Dependencies

1. Clone the repository:
   ```bash
   git clone https://github.com/caseybackes/geogif.git
   cd geogif
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package with development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

### Branching Strategy

We use a simplified Git Flow model:

- `main`: The primary branch containing production-ready code
- `develop`: Integration branch for ongoing development
- Feature branches: Branch from `develop` with the naming convention:
  - `feature/short-description` for new features
  - `bugfix/short-description` for bug fixes
  - `issue-123/short-description` for working on specifc open issues
  - `docs/short-description` for documentation changes

### Coding Standards

GeoGIF follows these coding standards:

- Code formatting with Black (line length of 88 characters)
- Import sorting with isort
- Python type hints (enforced by mypy)
- PEP 8 guidelines enforced by flake8 (with some exceptions in `.flake8`)

### Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality:

- black: Formats code
- isort: Sorts imports
- flake8: Lints code
- mypy: Checks type hints

To run the hooks manually (without committing):
```bash
pre-commit run --all-files
```

### Testing

Tests are written using pytest. Run tests with:

```bash
pytest
```

To run tests with coverage:

```bash
pytest --cov=geogif
```

## Pull Request Process

1. Create a new branch from `develop` following the branching strategy
2. Make your changes
3. Ensure all pre-commit hooks and tests pass
4. Update documentation if necessary
5. Submit a pull request to the `develop` branch
6. Include a clear description of the changes and their purpose
7. Address any feedback from code reviews

## Release Process

1. Ensure all desired changes are merged into `develop` and tested
2. Update version number in `pyproject.toml` following [Semantic Versioning](https://semver.org/)
3. Create a pull request from `develop` to `main`
4. Once merged, create a tag with the version number:
   ```bash
   git tag -a v0.1.0 -m "Version 0.1.0"
   git push origin v0.1.0
   ```
5. GitHub Actions will handle the release process

## Communication

- **Issues**: Report bugs, request features, or ask questions through [GitHub Issues](https://github.com/caseybackes/geogif/issues)
- **Email**: For sensitive or private communications, contact the maintainer at casey.backes@gmail.com
- **Discussions**: Broader discussions about the project should happen in GitHub Issues for visibility

## Notes on Dependencies

GDAL is a soft requirement as far as specific versions are concerned (3.0.0 minimum), but is necessary for the core functionality of GeoGIF. Be aware that:

- GDAL version compatibility can be affected by the version of NumPy used during compilation
- Older Python environments might use GDAL compiled against NumPy 1.x
- Newer environments might use GDAL compiled against NumPy 2.x

When contributing, please be mindful of these potential compatibility issues.
