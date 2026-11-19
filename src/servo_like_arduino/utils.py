import time


def delay(ms):
    time.sleep(ms / 1000)


def millis():
    return int(time.time() * 1000)