from pyfirmata2 import Arduino

_active_board = None


class Board:
    def __init__(self, port):
        global _active_board
        self._board = Arduino(port)
        _active_board = self

    @staticmethod
    def get_active_board():
        if _active_board is None:
            raise RuntimeError("No board initialized. Create a Board first.")
        return _active_board