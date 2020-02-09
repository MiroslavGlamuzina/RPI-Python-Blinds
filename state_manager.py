from datetime import datetime

MAX_UP = 6000
MIN_DOWN = 0
STEPS = 3000

def calibrate():
    file = open('/home/pi/RPI-Python-Blinds/state.txt', 'r+')
    file.seek(0)
    file.truncate()

    file.write("0")
    file.close()


def get_state(file):
    cur = file.readline()
    cur = int(0 if cur == '' else cur)

    #  Clean the file - TODO Check that cur is set properly .
    file.seek(0)
    file.truncate()

    return cur


def get_next_values(current_value, action):
    steps = STEPS
    if action == 'UP':
        next_value = int(current_value + STEPS)
        if next_value >= MAX_UP:
            next_value = MAX_UP
            steps = MAX_UP - current_value
    else:
        next_value = int(current_value - STEPS)
        if next_value <= MIN_DOWN:
            next_value = MIN_DOWN
            steps = current_value

    return [next_value, steps]


def update(action):
    file = open('/home/pi/RPI-Python-Blinds/state.txt', 'r+')
    cur = get_state(file)
    tmp = get_next_values(cur, action)
    next_value = tmp[0]
    next_steps = tmp[1]

    log(
        "Previous value: " + str(cur) + "\r\n" +
        "Value: " + str(next_value) + "\r\n" +
        "Steps: " + str(next_steps) + "\r\n"
    )

    file.write(str(next_value))
    file.close()
    return next_steps


def log(str_value):
    file = open('/home/pi/RPI-Python-Blinds/log.txt', 'a+')
    file.write(str(datetime.now()) + "\r\n" + str_value + "\r\n\r\n")
    print(str(datetime.now()) + "\r\n" + str_value + "\r\n\r\n")
    file.close()