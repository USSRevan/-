import enum

class State(enum.Enum):
    init = 0
    wait = 1
    new_order = 2
    start = 3
    scan = 4
    finish = 5
    pause = 6
    change_order = 7
    break_order = 8
