# Raylib Python Examples

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue)](http://mypy-lang.org/)

A collection of practical examples demonstrating audio, graphics, and game development with **Raylib** and **pyray** in Python, with **PyGLM** for vector/matrix math in advanced rendering examples.

## Features

- 📦 **Multiple example categories**: Audio, textures, input, and more
- 🎯 **Modern Python**: Type hints, dataclasses, and Python 3.14 best practices
- 🧮 **GLM math support**: Uses **PyGLM** for vector/matrix math in advanced shader examples
- ✅ **Validated code**: All examples pass `mypy` type checking and `black` formatting
- 🔧 **Easy setup**: Single venv and pip install

## Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (usually included with Python)
- PyGLM (installed via `requirements.txt`)

### Installation

```bash
# Clone the repository
git clone https://github.com/PurpBatBoi/raylib-python-examples.git
cd raylib-python-examples

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running Examples

After activation, run any example:

```bash
python main.py
python AUDIO/audio_module_playing.py
python AUDIO/audio_sound_positioning.py
```

Browse the repository structure to explore all available examples by category.


### Code Quality Checks

Install dev dependencies and run validation:

```bash
pip install -r requirements-dev.txt

# Format code
python -m black AUDIO/audio_module_playing.py

# Type check
python -m mypy AUDIO/audio_module_playing.py

# Check all files
python -m mypy $(find . -name "*.py" -not -path "./.venv/*")
python -m black --check $(find . -name "*.py" -not -path "./.venv/*")
```

### Style Guide

This project follows a comprehensive style guide. See [STYLE_GUIDE.md](STYLE_GUIDE.md) for detailed conventions including:
- pyray API usage
- Type hint requirements
- Python 3.14 best practices
- Code formatting and validation rules

## Contributing

Contributions are welcome! Please ensure all code:
1. Follows the style guide in [STYLE_GUIDE.md](STYLE_GUIDE.md)
2. Passes `mypy` type checking
3. Is formatted with `black`
4. Includes appropriate docstrings
5. Uses pyray APIs for primary examples

## Resources

- [Raylib Documentation](https://github.com/raysan5/raylib/wiki)
- [pyray GitHub](https://github.com/electronstudio/raylib-python-cffi)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Type Hints (PEP 484)](https://www.python.org/dev/peps/pep-0484/)

## License

This project is licensed under the zlib License. See [LICENSE](LICENSE).

These examples are Python ports of the original raylib C examples.
Original raylib examples and assets remain credited to their respective authors.

AI use disclosure: AI agents were used as an implementation, refactoring aid and experimentation purposes.
