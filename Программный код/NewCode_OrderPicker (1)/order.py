from log import log

from mqtt import order_msg



warehouse = ["гайки",
             "винты",
             "шайбы",
             "шпильки",
             "подшипники",
             "линейные направляющие",
             "валы",
             "двигатели",
             "датчики"
]

order = []
collected = []



def parse_order_lists():
    global order
    global collected
    order = []
    collected = []
    


def list_to_string(items):
    msg = ', '.join(str(item) for item in items)
    return msg
    

def parse_order():
    global order_msg
    if order_msg != "":
        log(f"Получен новый заказ от пользователя: {order_msg}")
        parse_order_lists()
        user_order = list(set(order_msg.split(", ")))
        correct_fl = True
        for word in user_order:
            if word in collected:
                log(f"Груз '{word}' находится в зоне выдачи!")
            elif word in warehouse:
                order.append(word)
                DPRINT(f"Груз '{word}' добавлен в очередь выдачи!")
            else:
                log(f"Внимание! Позиция '{word}' отсутствует на складе!")
                correct_fl = False
        
        if (not correct_fl):
            log("Внимание! Некоторые позиции заказа были отменены")
        
        msg = 'Заказ пользователя: ' + orderlist_to_string(order)
        log(msg)
        order_msg = NO_ORDER_MSG
        
def is_inOrder(item):
    return item is in order
    
def is_collected(item):
    return item is in collected

def is_orderEmpty():
    return len(order) == 0

def is_collectedEmpty():
    return len(collected) == 0

def get_WarehouseSize():
    return len(warehouse)
    
def item_from_order_to_collected(item):
    index = order.index(item)
    collected.append(order.pop(index))