# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**servo-like-arduino** is a Python package that provides Arduino-style servo control using PyFirmata2. The library wraps PyFirmata2 to offer a familiar Arduino API for controlling servos connected to Arduino boards via USB.

### Key Architecture

- **Board**: Global singleton that manages the connection to an Arduino board via PyFirmata2. Only one Board can be active at a time; it's stored in a module-level `_active_board` variable.
- **Servo**: Represents an individual servo attached to a specific pin. Must call `attach(pin)` before any operations. Tracks current angle internally (`current_angle`) to support smooth movements.
- **Utils**: Helper functions for timing (`delay`, `millis`) that provide Arduino-like interfaces using Python's `time` module.

### State Management

The library uses Arduino-style imperative patterns rather than context managers:
1. User creates a `Board` instance with a serial port
2. User creates one or more `Servo` instances
3. User calls `servo.attach(pin)` to bind to a hardware pin
4. Servo operations (write, move_smooth, sweep) communicate with the board

The `Board` validates it exists before servo operations and raises `RuntimeError` if the board is not initialized.

## Building and Publishing

```powershell
# Build the package
python -m build

# Publish to PyPI (requires credentials configured)
python -m twine upload dist/*
```

The package uses setuptools with configuration in `pyproject.toml`. Dependencies are listed there and in `requirements.txt`.

## Testing and Examples

Run examples directly with Python to verify servo behavior:

```powershell
# Examples are in ./examples/ directory
python examples\servo_test.py
python examples\move_smooth.py
python examples\endless_servo_sweep.py
```

For interactive testing:
```powershell
python -i -c "from servo_like_arduino import *; Board('/dev/ttyUSB0')"
# Then in the REPL:
# servo = Servo()
# servo.attach(9)
# servo.write(90)
```

## Dependencies

- **pyfirmata2**: Communicates with Arduino boards running StandardFirmata firmware
- **pyserial**: Serial communication (required by pyfirmata2)

To install dependencies:
```powershell
pip install -r requirements.txt
```

## Common Development Patterns

### Servo Angle Validation

Servo angles are clamped to [0, 180] range in all methods. This prevents invalid values from reaching the hardware:
- `write()` clamps via `max(0, min(180, angle))`
- `move_smooth()` and `sweep()` apply the same clamping
- `move_smooth()` calculates step direction based on current vs. target angle

### Error Handling

The library validates state transitions:
- Servo must be attached before write/read/move_smooth/sweep operations
- `read()` requires `write()` to have been called first (tracks `current_angle`)
- These raise `RuntimeError` with descriptive messages

### Smooth Movement Implementation

`move_smooth()` increments angle one degree at a time from current to target position, applying a delay between each step. If no current angle exists, it writes directly to the target angle. Step direction is determined dynamically (positive for increasing angles, negative for decreasing).

## Port Configuration

On different systems, the Arduino serial port appears as:
- **Linux**: `/dev/ttyUSB0`, `/dev/ttyACM0`
- **macOS**: `/dev/tty.usbserial-*`, `/dev/tty.usbmodem*`
- **Windows**: `COM3`, `COM4`, etc.

Identify the port with device manager or by checking which port appears when plugging in the Arduino.
