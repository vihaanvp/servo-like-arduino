# servo-like-arduino

Arduino-style servo control for Python using PyFirmata2.

> ⚠️ NOTE: This project has been made completely using AI (ChatGPT). If any issues or security vunerabilities are found, please report in issues tab

## Installation

```bash
pip install pyfirmata2 pyserial
pip install servo-like-arduino
```

## Arduino Setup

Upload StandardFirmata to your Arduino:

File → Examples → Firmata → StandardFirmata

## Quick Start

```python
from servo_like_arduino import *

Board('/dev/ttyUSB0')

servo = Servo()
servo.attach(9)

servo.write(90)
```

## Smooth Movement

```python
servo.move_smooth(180)
```

## Sweep

```python
servo.sweep(
    start=0,
    end=180,
    step=1,
    delay_ms=15
)
```

## Features

- Arduino-style syntax
- Servo control
- Smooth movement
- Sweep functionality
- delay()
- millis()
- Built on PyFirmata2
