# Log Analyser

A simple and minimalistic log analyser written in Python.

Originally made for Linux, but in theory, it should also work on Windows since the GUI uses PyQt5 and everything else is built into Python.

## Features

- Analyses `.log` and `.txt` files.
- Works with any supported text log file containing `ERROR`, `WARNING`, or `INFO` entries.
- Simple and minimalistic graphical interface.

## Installation

### Precompiled version

Download the executable for Linux from the [Releases](../../releases) page and run it.

### Running from source

1. Install Python 3.
2. Install PyQt5:

```bash
python -m pip install PyQt5
```

3. Run the application:

```bash
python main.py
```

On Linux, you may need to use `python3` instead of `python`.

## Limitations

The code is pretty bad, and performance was not a priority when making this project.

**Do not use it for large log files.** Files containing more than a few thousand lines may cause the application to freeze or crash.

Use it for small log files if you want to avoid potential problems.

## Compatibility

- **Linux:** Primary target platform.
- **Windows:** Should theoretically work, but has not necessarily been tested.

## Final note

This is a small project made for simplicity, not a production-ready log analysis tool. Use it at your own risk.
