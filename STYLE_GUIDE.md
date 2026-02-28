# Raylib Python Examples Style Guide

## Scope

This guide applies to all example scripts in this repository.

## Required Rules

1. Use `pyray` APIs (`import pyray as pr`) for primary examples.
2. If a direct `raylib` variant is needed, add a separate sibling file with `_rl.py` suffix (for example, `audio_module_playing_rl.py`).
3. Add a version-check comment near the top of each file.
4. Validate types with `mypy`.
5. Format code with `black`.

## File Header Convention

Place a version-check line near imports:

```python
# Version checked: raylib 5.x/pyray API parity (reviewed YYYY-MM-DD).
```

Use a concrete review date.

## API Usage Convention

1. Prefer `pr.<function_or_type>` over raw `raylib` calls in primary files.
2. Keep constants explicit for key codes/flags when needed for compatibility.
3. Keep resource paths relative to `Path(__file__).resolve().parent`.

## Validation Commands

From repository root, prefer project venv:

```bash
.venv/bin/python -m mypy AUDIO/audio_module_playing.py AUDIO/audio_sound_positioning.py
.venv/bin/python -m black --check AUDIO/audio_module_playing.py AUDIO/audio_sound_positioning.py
```

For a broader run:

```bash
rg --files -g '*.py' | xargs .venv/bin/python -m mypy
rg --files -g '*.py' | xargs .venv/bin/python -m black --check
```

## Validation Reporting

When reviewing examples, report:

1. Files checked.
2. `mypy` result (pass/fail + errors).
3. `black --check` result (pass/fail + files needing reformat).
4. Any rule violations from this guide.

## Python 3.14 Coding Conventions

### Type Hints
- Use explicit type hints on all function parameters and return types (PEP 484).
- Prefer modern union syntax with `|` instead of `Union[]` (Python 3.10+).
- Use `Optional[T]` or `T | None` for nullable types.
- Annotate complex data with `TypedDict` or `dataclasses` for clarity.

Example:
```python
from typing import Optional

def process_audio(stream: bytearray | None, gain: float = 1.0) -> bool:
    """Process audio stream with optional gain adjustment."""
    pass
```

### Docstrings
- Follow PEP 257 conventions for all public modules, classes, and functions.
- Use triple-quoted strings even for single-line docstrings in public APIs.
- Include parameter and return type descriptions in the docstring body.

### String Formatting
- Use f-strings exclusively over `.format()` or `%` formatting.
- Example: `f"Loaded {sample_rate} Hz audio stream"` instead of `"Loaded {} Hz audio stream".format(sample_rate)`.

### Modern Control Flow
- Use `match`/`case` statements for complex conditionals (Python 3.10+).
- Use the walrus operator `:=` to simplify variable assignment in conditionals where appropriate.
- Prefer exception groups for handling multiple exceptions (Python 3.11+).

### Resource Management
- Use context managers (`with` statements) for all resource allocation (files, streams, etc.).
- Define custom context managers with `contextlib` or `__enter__`/`__exit__` methods when needed.

### Imports
- Organize imports into three groups: standard library, third-party, local (PEP 8).
- Use absolute imports; avoid wildcard imports.
- Import only what you need; use explicit names.

### Data Structures
- Prefer `dataclasses` (or `frozen_dataclass` for immutable data) over plain classes for simple data containers.
- Use `Enum` for fixed sets of named constants instead of module-level string/int constants.

### Code Style
- Follow PEP 8 conventions (enforced by `black`).
- Keep lines under 100 characters where reasonable.
- Use meaningful variable names; avoid single-letter names except in loop counters.
- Use constants in `UPPER_SNAKE_CASE` for module-level constant values.
