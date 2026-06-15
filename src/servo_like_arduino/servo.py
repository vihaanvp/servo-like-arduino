import servo_like_arduino.board as board_module
from .utils import delay


class Servo:
    def __init__(self):
        self._servo = None
        self.pin = None
        self.current_angle = None

    def attach(self, pin):
        board = board_module.Board.get_active_board()
        self.pin = pin
        self._servo = board._board.get_pin(f"d:{pin}:s")

    def detach(self):
        self._servo = None
        self.pin = None
        self.current_angle = None

    def _ensure_attached(self):
        if self._servo is None:
            raise RuntimeError("Servo not attached. Call attach(pin) first.")

    def _validate_and_clamp_angle(self, angle):
        try:
            angle = int(angle)
        except (TypeError, ValueError) as exc:
            raise ValueError("angle must be a number between 0 and 180") from exc
        return max(0, min(180, angle))

    def write(self, angle):
        self._ensure_attached()
        angle = self._validate_and_clamp_angle(angle)
        self._servo.write(angle)
        self.current_angle = angle

    def read(self):
        self._ensure_attached()
        if self.current_angle is None:
            raise RuntimeError("Servo angle is unknown. Call write() first.")
        return self.current_angle

    def move_smooth(self, target_angle, delay_ms=15):
        self._ensure_attached()
        target_angle = self._validate_and_clamp_angle(target_angle)

        if self.current_angle is None:
            self.write(target_angle)
            return

        if target_angle == self.current_angle:
            return

        step = 1 if target_angle > self.current_angle else -1
        for angle in range(self.current_angle + step, target_angle + step, step):
            self.write(angle)
            delay(delay_ms)

    def sweep(self, start=0, end=180, step=1, delay_ms=15):
        self._ensure_attached()
        if step <= 0:
            raise ValueError("step must be greater than 0")

        start = self._validate_and_clamp_angle(start)
        end = self._validate_and_clamp_angle(end)

        if start < end:
            angles = range(start, end + 1, step)
        else:
            angles = range(start, end - 1, -step)

        for angle in angles:
            self.write(angle)
            delay(delay_ms)