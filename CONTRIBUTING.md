# Contributing to servo-like-arduino

> **Note:** This file has been modified using AI.

Thank you for contributing to **servo-like-arduino** — an Arduino-style servo control library for Python using PyFirmata2.

## Quick Links

- **PyPI:** `pip install servo-like-arduino`
- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions

---

## Ways to Contribute

### Bug Reports
- Search existing issues first
- Include: Python version, OS, Arduino board, servo model, PyFirmata2 version
- Minimal reproducible example
- Note: StandardFirmata servo support has limited precision (1° steps)

### Feature Requests
- Explain the use case
- Consider API consistency with `motor-like-arduino`, `ultrasonic-like-arduino`, `PyFirmata Simplifier`
- Keep it simple — this library focuses on *basic* servo control

### Pull Requests
**We welcome PRs for:**
- Bug fixes (especially angle validation, smooth movement edge cases)
- Additional movement patterns (e.g., eased motion, callback on complete)
- Support for continuous rotation servos
- Documentation improvements
- Type hints / stubs
- Tests in `tests/`

**Before submitting:**
1. Run examples: `python examples/servo_test.py`
2. Follow existing code style (PEP 8, type hints where practical)
3. Update `CHANGELOG.md` under `## Unreleased`
4. Keep changes focused — one logical change per PR

---

## Development Setup

```bash
git clone https://github.com/vihaanvp/servo-like-arduino.git
cd servo-like-arduino
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

**Requirements:**
- Python 3.8+
- Arduino running StandardFirmata (File → Examples → Firmata → StandardFirmata)
- `pyfirmata2`, `pyserial`

---

## Project Structure

```
servo-like-arduino/
├── src/servo_like_arduino/      # Package source
│   ├── __init__.py              # Public exports + __version__
│   ├── board.py                 # Board class (singleton pattern)
│   ├── servo.py                 # Servo class (attach, write, move_smooth, sweep)
│   └── utils.py                 # delay(), millis() — Arduino-like utilities
├── examples/                    # Runnable examples
│   ├── servo_test.py
│   ├── move_smooth.py
│   ├── endless_servo_sweep.py
│   └── endless_sweep.py
├── tests/                       # (Add tests here)
├── pyproject.toml               # Build config (setuptools)
├── requirements.txt
├── README.md
├── CLAUDE.md                    # AI assistant guidance
├── LICENSE
└── CONTRIBUTING.md              # This file
```

---

## Code Conventions

- **Servo angle:** 0–180 degrees. Clamped via `_validate_and_clamp_angle()` (casts to `int`, truncates, then `max(0, min(180, angle))`).
- **Pin notation:** PyFirmata2 servo format `d:<pin>:s` — uses Firmata's servo protocol.
- **State tracking:** `current_angle` tracks last written angle (no hardware read-back).
- **Error handling:** `RuntimeError` for state violations (not attached, read before write).
- **Smooth movement:** `move_smooth()` increments 1° at a time with `delay()` between steps.
- **Sweep:** `sweep(start, end, step, delay_ms)` — `step > 0` required, direction auto-detected.
- **Arduino-style imperative API:** `Board(port)` → `Servo()` → `servo.attach(pin)` → operations.

---

## Key Implementation Details

### Singleton Board Pattern
```python
# Module-level singleton in board.py
_active_board = None

class Board:
    def __init__(self, port):
        global _active_board
        self._board = Arduino(port)
        _active_board = self

    @classmethod
    def get_active_board(cls):
        return _active_board
```
- Only one `Board` can be active at a time
- `Servo` accesses board via `board_module.Board.get_active_board()`
- This differs from `motor-like-arduino` where motors are created via `board.attach_motor()`

### Angle Validation
```python
def _validate_and_clamp_angle(self, angle):
    angle = int(angle)  # truncates, doesn't round
    return max(0, min(180, angle))
```
- Accepts `int` or `float`, truncates to `int`
- Clamps to [0, 180] — no error on out-of-range, silently clamps

### Smooth Movement
```python
def move_smooth(self, target_angle, delay_ms=15):
    if self.current_angle is None:
        self.write(target_angle)
        return
    step = 1 if target_angle > self.current_angle else -1
    for angle in range(self.current_angle + step, target_angle + step, step):
        self.write(angle)
        delay(delay_ms)
```
- Uses `current_angle` to determine direction
- If no prior angle, jumps directly to target
- 1° steps with configurable delay

---

## Testing

Currently no automated test suite. **Manual testing checklist:**

- [ ] `python examples/servo_test.py` — basic write/read
- [ ] `python examples/move_smooth.py` — smooth movement
- [ ] `python examples/endless_servo_sweep.py` — continuous sweep
- [ ] Verify `write()` clamps 0–180 (test -10, 200, 90.7)
- [ ] Verify `read()` raises before first `write()`
- [ ] Verify `detach()` releases pin
- [ ] Test with standard hobby servos (SG90, MG996R) and continuous rotation

**To add tests:** Create `tests/` with `pytest`. Test against a mock PyFirmata2 board or real hardware.

---

## Release Process

Maintainer only:
```bash
# Update version in src/servo_like_arduino/__init__.py
# Update CHANGELOG.md
git tag vX.Y.Z
git push origin vX.Y.Z
python -m build
python -m twine upload dist/*
```

---

## Related Projects

| Project | Purpose |
|---------|---------|
| [motor-like-arduino](https://github.com/vihaanvp/motor-like-arduino) | DC motor control |
| [ultrasonic-like-arduino](https://github.com/vihaanvp/ultrasonic-like-arduino) | HC-SR04 ultrasonic sensor |
| [PyFirmata Simplifier](https://github.com/vihaanvp/pyfirmata-simplifier) | Unified motor + servo in one package |

When adding features, consider API consistency across these libraries.

---

## License

By contributing, you agree your contributions are licensed under the MIT License (see [LICENSE](LICENSE)).