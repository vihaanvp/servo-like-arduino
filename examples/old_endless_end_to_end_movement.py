from servo_like_arduino import *

Board('/dev/ttyUSB0')

servo = Servo()
servo.attach(6)

while True:
    servo.write(0)
    delay(1000)

    servo.write(180)
    delay(1000)