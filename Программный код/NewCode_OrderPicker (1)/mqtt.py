from paho.mqtt import client as client


mqtt_ip     = 'mqtt.by'
port        = 1883
client_id   = f'FriendsOrderPicker-{random.randint(0,1000)}'
user        = 'u_66I8PA'
password    = 'XNPpIQJB'

order_topic = 'user/FriendsOrderPicker/order'
cmd_topic   = 'user/FriendsOrderPicker/current_cmd'
log_topic   = 'user/FriendsOrderPicker/log'


mqttClient = None


def add_msg_handler(topic, callback):
    mqttClient.subscribe(topic)
    mqttClient.message_callback_add(topic, callback)


def log_publish(msg):
    mqttClient.publish(log_topic, msg)


def launch_mqtt_loop():
    mqttClient.loop_start()

def stop_mqtt_loop():
    mqttClient.loop_stop()

    
    
def on_message(userdata, msg):
    pass
    print(f"Topic: '{msg.topic}')
    print(f"Message: '{str(msg.payload)}'")
    
   
def set_will():
    mqttClient.will_set(log_topic, "Offline..")


def subcribe():
    mqttClient.subscribe(order_topic)
    mqttClient.subscribe(cmd_topic)
    

def mqtt_on_connect(userdata, flags, rc):
    if (not rc):
        print(f"Подключено к MQTT серверу -- '{mqtt_ip}'")
        log_publish("Online")
        subcribe()
        mqttClient.on_message = on_message
        set_will()
    else:
        print(f'Failed to connect, return code {rc}')
        

def mqtt_connect():
    global mqttClient
    mqttClient = mqttClient.Client(client_id)
    mqttClient.username_pw_set(user, password)
    mqttClient.on_connect = mqtt_on_connect
    mqttClient.connect(mqtt_ip, port)
    return mqttClient
    
    
def get_mqtt():
    return mqttClient




client = ''




from command import Command



cmds = [
    {"cmd": Command.none,          "mqtt": "cmd_nothing"},
    {"cmd": Command.launch,        "mqtt": "cmd_launch"},
    {"cmd": Command.order_break,   "mqtt": "cmd_break"},
    {"cmd": Command.pause,         "mqtt": "cmd_pause"},
    {"cmd": Command.order_ch,      "mqtt": "cmd_order_change"},
    {"cmd": Command.order_save,    "mqtt": "cmd_order_confirm"}
]


current_cmd = None


def cmd_reset():
    global current_cmd
    current_cmd = None



order_msg = ""



def mqtt_on_cmd(userdata, msg):
    global current_cmd
    cmd_text = msg.payload.decode('utf-8')
    current_cmd = None
 
    for command in cmds:
        if cmd_text == command["mqtt"]:
            current_cmd = command["cmd"]
            break
    if current_cmd != None:
        print(f"Получена команда '{cmd_text}'")
     
     
def mqtt_on_order(userdata, msg):
    global order_msg
    order_msg = msg.payload.decode('utf-8')
    print(f"Получен заказ: '{order_msg}'")



def mqtt_init():   
    client = mqtt_connect()
    subscribe_and_handler(client, order_topic, mqtt_on_order)
    subscribe_and_handler(client, cmd_topic, mqtt_on_cmd)
    launch_mqtt_loop(client)
    return client
