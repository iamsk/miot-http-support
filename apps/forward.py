import paho.mqtt.client as mqtt

from apps.panasonic import control
from apps.config import BEMFA

mappings = {
    'on': '打开灯',  # 打开风暖 <-> 打开浴霸灯
    'off': '关闭灯',  # 关闭风暖 <-> 关闭浴霸灯
    '3': '取暖',  # 打开风暖辅热功能 <-> 取暖
    '4': '换气',  # 打开风暖柔风功能 <-> 换气
    '5': '热干燥',  # 打开风暖干燥功能 <-> 热干燥
    '6': '待机',  # 打开风暖睡眠模式 <-> 浴霸待机
    '7': '凉干燥',  # 打开风暖节能模式 <-> 凉干燥
}


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for topic in BEMFA['TOPICS']:
        client.subscribe(topic)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    if msg.topic == 'bathbully005':
        cmds = msg.payload.decode().split('#')
        if len(cmds) > 1:
            running_mode = cmds[1]
            control(running_mode=mappings[running_mode])
    if msg.topic == 'bathbully002':
        light_set = msg.payload.decode()
        control(light_set=mappings[light_set])


client = mqtt.Client(client_id=BEMFA['CLIENT_ID'])
client.on_connect = on_connect
client.on_message = on_message
client.connect("bemfa.com", 9501, 60)
client.loop_forever()
