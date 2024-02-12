from log import log, log_init, log_debug
        
log_init()


from uart import init_uart
from camera_qr import camera_open, scan_and_save
from mqtt import cmds, current_cmd as cmd 


from scanning_stage import ScanningStage
from command import Command
from state import State

from device import get_currentCell, set_currentCell, reset_currentCell, device_next_cell, device_grab_obj, device_home, device_reset


from order import parse_order, order, list_to_string, is_orderEmpty, is_collectedEmpty, get_WarehouseSize, is_inOrder

from camera_qr import scan_and_save

state = State.init
scanningStage = ScanningStage.move


scan_list = None
grab_list = None
    
def reset_lists():
    scan_list = None
    grab_list = None
    


state_handlers = [
        {"state": State.init,           "func": initializing_handler},
        {"state": State.wait,           "func": waiting_handler},
        {"state": State.new_order,      "func": setting_order_handler},
        {"state": State.start,          "func": starting_handler},
        {"state": State.scan,           "func": scanning_handler},
        {"state": State.finish,         "func": finish_handler},
        {"state": State.pause,          "func": pause_handler},
        {"state": State.change_order,   "func": ch_order_handler},
        {"state": State.break_order,    "func": break_handler}
]



def initializing_handler():
    log_debug("Initializing handler")
    global camera
    global state
    init_uart()
    device_home()
    log("Прогреваем камеру, это займёт некоторое время!")
    camera_open()
    log("Камера готова к работе!")
    log("\nОжидание команд пользователя..")
    state = State.wait


def waiting_handler():
    log_debug("Waiting handler")
    global state
    
    if cmd:
        if cmd == Command.order_ch: 
            log("Ожидаем новый заказ")
            state = State.new_order
        elif cmd == Command.launch:
            state = State.start
        else:
            log("В данный момент невозможно выполнить эту команду")
    reset_cmd()

    
def setting_order_handler():
    log_debug("Setting order handler")
    global state
    parse_order()
    log(f"Заказ пользователя: {list_to_string(order)}")
    
    if cmd:
        if cmd == Command.order_save:
            log("Пользователь подтвердил заказ!")
            state = State.wait
        else:
            log("В данный момент невозможно выполнить эту команду")
    reset_cmd()
        

def starting_handler():
    log_debug("Starting handler")
    global state
    if (not is_orderEmpty()):
        if (not is_collectedEmpty()):
            log("Заказ успешно собран!")
            state = State.finish
        else:
            log("Заказ пуст! Пожалуйста, задайте новый заказ!")
            state = State.wait
    else:
        log("Начинаем сборку заказа!")
        state = State.scan



def reset_scanningStage():
    global current_cell
    global scanningStage
    reset_lists()
    reset_current_cell()
    scanningStage = ScanningStage.move



def scanning_handler():
    global state
    global scanningStage
    log_debug("Scanning handler")
    
    if cmd:
        if cmd == Command.pause:
            if scanningStage == ScanningStage.grab:
                scanningStage = scanningStage.scan
            log("Пользователь поставил сборку заказа на паузу")
            state = State.pause
            return
        elif cmd == Command.order_break:
            log("Пользователь отменил заказ!")
            state = State.break_order
            return
        else:
            log("В данный момент невозможно выполнить эту команду")
    reset_cmd()
    
    if scanningStage == ScanningStage.move:
        if (current_cell == get_WarehouseSize()):
            log("Мы проверили весь склад в поисках ваших товаров. Есть не найденные или измененные позиции. Продолжим поиск с самого начала!")
            reset_current_cell()
        log_debug('Переходим к следующей ячейке склада')
        device_next_cell()
        log_debug(f'Текущая ячейка - #{get_currentCell()}')
        scanningStage = ScanningStage.scan
    
    elif scanningStage == ScanningStage.scan:
        log_debug('Фотографируем и сканируем QR code груза')
        
        photo_name = f'WarehouseItem.png'    
        
        if (not scan_list)
            data = scan_and_save(photo_name)
            if (not data):
                log_debug('Не получилось считать QR код. Повторяем ещё раз!')
            else:
                log_debug("QR код был успешно считан")
                scan_list = data
                log(f"Груз успешно распознан! Это - '{data}'")
                if (is_inOrder(data)):
                    log(f"Пользователь заказал товар '{data}'! Забираем в зону выдачи!")
                    grab_list = data
                else:
                    log(f"'Товар {data}' не находится в заказе!")
        
        if (scan_list):
            scan_list = None
            if (grab_list):
                scanningStage = ScanningStage.grab
            else:
                scanningStage = ScanningStage.move
        
    elif scanningStage == scanningStage.grab:
        if (grab_list):
            device_grab_obj()
            log(f"Товар '{grab_list}' отгружен в зону выдачи!")
            item_from_order_to_collected(grab_list)
            grab_list = None
        
        log_debug(f"В зоне выдачи: {orderlist_to_string(order)}")
        log_debug(f"Товары в сборке: {orderlist_to_string(collected)}")
        
        if (is_orderEmpty()):
            state = State.finish
        
        scanningStage = ScanningStage.move
        
    
        
def reset_scanning_data():
    reset_scanningStage()
    parse_order_lists()
    reset_collected_order()


def end_scanning():
    if (not is_collectedEmpty()):
        log(f"Собран заказ: {orderlist_to_string(collected)}")
    if (not is_orderEmpty()):
        log(f"Отмененные позиции: {orderlist_to_string(order)}")
    
    reset_scanning_data()
    device_home()
    device_reset()

    
def finish_handler():
    log_debug("Finish handler")
    global state
    log("\nЗаказ успешно собран!")
    end_scanning()
    state = State.wait
    
    
def break_handler():
    log_debug("Break order handler")
    global state
    end_scanning()
    state = State.wait


def pause_handler():
    log_debug("Pause handler")
    global state
    
    if cmd:
        if cmd == Command.order_ch:
            log("Изменение заказа..")
            state = State.change_order
        elif cmd == Command.launch:
            state = State.start
            log("Продолжаем сборку заказа")
        elif cmd == Command.order_break:
            log("Пользователь отменил заказ!")
            state = Start.break_order
        else:
            log("В данный момент невозможно выполнить эту команду")
    reset_cmd()
    
    
def ch_order_handler():
    log_debug("Changing order handler")
    global state
    parse_order()
    parse_order()
    log(f"Заказ пользователя: {list_to_string(order)}")
    
    if cmd:
        if cmd == Command.order_save:
            log("Пользователь подтвердил заказ!")
            state = State.pause
        else:
            log("В данный момент невозможно выполнить эту команду")
    reset_cmd()
    
    

while True:
    for handler in state_handlers:
        if handler["state"] == state:
            handler["func"]()
            break
