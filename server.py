import os

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

from panasonic import AirCondition, BathHeater

load_dotenv()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for topic in os.getenv("BEMFA_TOPICS", "").split(","):
        client.subscribe(topic)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    if msg.topic == 'bathbully005':
        cmds = msg.payload.decode().split('#')
        running_mode = cmds[1] if len(cmds) > 1 else cmds[0]
        device = BathHeater()
        mappings = {
            'on': '打开灯',  # 打开空调 <-> 打开浴霸灯
            'off': '关闭灯',  # 关闭空调 <-> 关闭浴霸灯
            '3': '取暖',  # 空调打开辅热模式 <-> 取暖
            '4': '换气',  # 空调开启柔风模式 <-> 换气
            '5': '热干燥',  # 空调开启干燥模式 <-> 热干燥
            '6': '待机',  # 空调开启睡眠模式 <-> 浴霸待机
            '7': '凉干燥',  # 空调开启节能模式 <-> 凉干燥
        }
        device.control(action=mappings[running_mode])
    if msg.topic == 'aircondition005':
        action = msg.payload.decode()
        device = AirCondition()
        device.control(action)


client = mqtt.Client(client_id=os.getenv("BEMFA_CLIENT_ID", ""))
client.on_connect = on_connect
client.on_message = on_message
client.connect("bemfa.com", 9501, 60)
client.loop_forever()
