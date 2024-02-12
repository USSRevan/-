import serial

ser = ""

PORT = "COM21"
UART_SPEED = 115200


def init_uart():
    global ser
    ser = serial.Serial(PORT, UART_SPEED)
    return ser
    
def uart_print(msg):
    msg += '\n'
	ser.write(msg.encode('utf-8'))
    
    
def wait_for_answer():
    line = None 
    while (not line):
        line = ser.readline();


def uart_print_answer_wait(msg):
    uart_print(msg)
    wait_for_answer()