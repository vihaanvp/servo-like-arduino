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

    def write(self, angle):
        if self._servo is None:
            raise RuntimeError(
                "Servo not attached. Call attach(pin) first."
            )

        angle = max(0, min(180, int(angle)))

        self._servo.write(angle)
        self.current_angle = angle
    def read(self):
        if self.current_angle is None:
            raise RuntimeError(
                "Servo angle is unknown. Call write() first."
            )

        return self.current_angle

    def move_smooth(self, target_angle, delay_ms=15):
        if self._servo is None:
            raise RuntimeError(
                "Servo not attached. Call attach(pin) first."
            )

        target_angle = max(0, min(180, int(target_angle)))

        if self.current_angle is None:
            self.write(target_angle)
            return

        step = 1 if target_angle > self.current_angle else -1

        for angle in range(
            self.current_angle,
            target_angle + step,
            step
        ):
            self._servo.write(angle)
            self.current_angle = angle
            delay(delay_ms)

    def sweep(
        self,
        start=0,
        end=180,
        step=1,
        delay_ms=15
    ):
        if self._servo is None:
            raise RuntimeError(
                "Servo not attached. Call attach(pin) first."
            )

        if step <= 0:
            raise ValueError(
                "step must be greater than 0"
            )

        if start < end:
            for angle in range(start, end + 1, step):
                self.write(angle)
                delay(delay_ms)
        else:
            for angle in range(start, end - 1, -step):
                self.write(angle)
                delay(delay_ms)