# A stupid way to extend miot/xiaoai. 

### Demo for Panasonic Bath Bully `FV-RB20VL1`

<img src="./images/toplogy.jpg" width="640">

1. 逆向 `Panasonic Smart China`，获得控制浴霸的请求信息（HTTP 请求），详见 `apps/panasonic.py`；
<img src="./images/panasonic.jpeg" width="640">
2. 通过米家 APP 添加 `巴法`，以支持第三方设备，实现监听巴法云的 MQTT 消息，巴法云目前不支持浴霸，需要使用其他设备进行替代并映射，因灯与运行模式完全独立，建议实现两个设备，详见 `server.py`；
<img src="./images/light.jpg" width="640">
<img src="./images/running_mode.jpg" width="640">
3. 为了更好的体验，需要在小爱音箱 APP 中，创建训练，转换浴霸指令为巴法云支持的指令。
<img src="./images/command_transform.jpeg" width="640">

### Installation:

`virtualenv -p python3 venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

### Run server:

`python apps/server.py`
