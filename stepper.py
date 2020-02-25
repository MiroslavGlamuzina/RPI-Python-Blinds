import RPi.GPIO as GPIO
import time
import sys
from state_manager import *

#  SETUP PINS
GPIO.setmode(GPIO.BCM)
control_pins = [18, 23, 24, 17]
for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# CONSTANTS
DELAY = 0.00075
UP_SEQUENCE = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]
DOWN_SEQUENCE = [
    [1, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 1, 1],
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 0],
    [1, 1, 0, 0],
    [1, 0, 0, 0],
]


def move(sequence, delay, steps):
    for i in range(steps):
        sys.stdout.write("\r Steps: " + str(i) + "/" + str(steps))
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(control_pins[pin], sequence[halfstep][pin])
            time.sleep(delay)
    GPIO.cleanup()


if sys.argv[1] == 'down' or sys.argv[1] == '1':
    TYPE = DOWN_SEQUENCE
    STEPS = update('DOWN')[0]
elif sys.argv[1] == 'up' or sys.argv[1] == '0':
    TYPE = UP_SEQUENCE
    STEPS = update('UP')[0]
elif sys.argv[1] == 'set':
    tmp = update('SET', int(sys.argv[2]))
    STEPS = tmp[0]
    TYPE = UP_SEQUENCE if tmp[1] else DOWN_SEQUENCE
elif sys.argv[1] == 'open':
    tmp = update('SET', 50)
    STEPS = tmp[0]
    TYPE = UP_SEQUENCE if tmp[1] else DOWN_SEQUENCE
elif sys.argv[1] == 'close':
    tmp = update('SET', 0)
    STEPS = tmp[0]
    TYPE = UP_SEQUENCE if tmp[1] else DOWN_SEQUENCE
elif sys.argv[1] == 'calibrate' or sys.argv[1] == 'c':
    log("Calibrating...\r\nEnsure to kill when blinds are fully down (at 0)")
    TYPE = DOWN_SEQUENCE
    STEPS = 6000
    calibrate()
elif sys.argv[1] == 'help' or sys.argv[1] == 'h':
    log("usage: python stepper.py [1(down)|0(up)|calibrate/c|help/h]")
    exit()
else:
    log('TYPE was not defined')
    exit()

move(TYPE, DELAY, STEPS)

print('Done!')
