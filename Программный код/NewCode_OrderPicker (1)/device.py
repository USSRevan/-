from uart import uart_print_answer_wait as uart_print


warehouse_size = 9

warehouse_cell_offset = 0
warehouse_cell_shift = 950

warehouse_grab_offset = 700

grab_linear_front_pos = 150

grab_capture_opened_pos = 130
grab_capture_closed_pos = 0



current_cell = 0

def get_currentCell():
    return current_cell
    
def set_currentCell(cell_num):
    global current_cell
    current_cell = cell_num

def reset_currentCell():
    set_currentCell(0)




def device_pause(time_sec=1):
    uart_print(f'G4 S{time_sec}')


def device_move_z(z):
    uart_print(f'G1 Z{z}')


def device_moveRelative_z(z):
    pos = convert_cell_to_pos(current_cell)
    device_move_z(pos + z)
    

def device_home_z():
    uart_print('G28 Z')
    

def device_move_y(y):
    uart_print(f'G1 Y{y}')
    
def device_home_y():
    uart_print('G28 Y')
    


def device_gripper_front():
    device_move_y(grab_linear_front_pos)
    
    
def device_gripper_back():
    device_home_y()


def device_gripper_open():
    uart_print(f'G1 U{grab_capture_opened_pos}')
    device_pause(1)
    

def device_gripper_close():
    uart_print(f'G1 U{grab_capture_closed_pos}')
    device_pause(1)





def device_reset():
    uart_print('G69')
    

def device_home():
    global current_cell
    log("Возврат домой")
    device_gripper_open()
    device_home_y()
    device_home_z()
    current_cell = 0
    


def convert_cell_to_pos(num):
    pos = 0
    if num == 0:
        pos = 0
    elif num >= 1:
        pos = (warehouse_cell_offset +
            (num - 1) * warehouse_cell_shift)
    return pos


def device_current_cell():
    pos = convert_cell_to_pos(current_cell)
    device_move_z(pos)


def device_next_cell():
    global current_cell
    log("Сканируем следующую ячейку склада")
    current_cell += 1
    device_current_cell()


def device_pull_object():
    device_move_y(0)

def device_release_object():
    device_gripper_open()

    
def device_grab_obj():
    device_moveRelative_z(warehouse_grab_offset)
    device_gripper_open()
    device_pause(0.6)
    device_gripper_front()
    device_pause(0.6)
    device_gripper_close()
    device_pause(0.6)
    device_pull_object()
    device_pause(0.6)
    device_home_z()
    device_release_object()
    device_pause(0.6)
