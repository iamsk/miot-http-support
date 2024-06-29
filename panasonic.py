import os

import requests
from dotenv import load_dotenv

load_dotenv()


class Panasonic(object):
    deviceId = ''
    token = ''
    url = ''
    params = {}
    headers = {
        'Host': 'app.psmartcloud.com',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'en-US,en;q=0.9',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Origin': 'https://app.psmartcloud.com',
        'xtoken': f'SSID={os.getenv("BEMFA_CLIENT_ID", "")}',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        # 'Referer': '',  # no need
        # 'Content-Length': '468',  # no need
        'Connection': 'keep-alive',
    }
    cookies = {
        'acw_tc': os.getenv("PANASONIC_ACW_TC", ""),
    }

    def update_params(self, action):
        pass

    def trigger(self):
        data = {
            "id": 1,
            "usrId": os.getenv("PANASONIC_USER_ID", ""),
            "deviceId": self.deviceId,
            "token": self.token,
            "params": self.params,
        }
        import pdb;
        pdb.set_trace()
        response = requests.post(self.url, headers=self.headers, cookies=self.cookies, json=data, verify=False)
        print(response.json())

    def control(self, action=''):
        self.update_params(action)
        self.trigger()


class BathHeater(Panasonic):
    deviceId = os.getenv("PANASONIC_DEVICE_ID", "")
    token = os.getenv("PANASONIC_TOKEN", "")
    url = 'https://app.psmartcloud.com/App/ADevSetStatusInfoFV54BA1C'
    params = {
        "DIYnextwindDirectionSet": 255,
        "DIYnextwindKindSet": 255,
        "warmTempset": 255,
        "DIYnextWarmTempset": 255,
        "DIYnextStepNo": 2,
        "windDirectionSet": 255,
        "timeSet": 3,  # 默认15分钟
        "DIYnextRunningMode": 255,
        "windKindSet": 255,
        "DIYnextTimeSet": 255,
    }

    def update_params(self, action):
        running_modes = {
            '打开灯': 1,
            '关闭灯': 0,
            '换气': 38,
            '取暖': 37,
            '凉干燥': 40,
            '热干燥': 42,
            '待机': 32,
        }
        light_set = running_modes[action] if action in ['打开灯', '关闭灯'] else 255
        running_mode = running_modes[action] if action in ['换气', '取暖', '凉干燥', '热干燥', '待机'] else 255
        self.params['runningMode'] = running_mode
        self.params['lightSet'] = light_set


class AirCondition(Panasonic):
    deviceId = os.getenv("PANASONIC_AIR_CONDITION_DEVICE_ID", "")
    token = os.getenv("PANASONIC_AIR_CONDITION_TOKEN", "")
    url = 'https://app.psmartcloud.com/App/ACDevSetStatusInfoAW'
    params = {
        'runMode': 3,
        'forceRunning': 0,
        'remoteForbidMode': 0,
        'remoteMode': 0,
        'setTemperature': 54,
        'setHumidity': 128,
        'windSet': 3,
        'exchangeWindSet': 0,
        'portraitWindSet': 15,
        'orientationWindSet': 13,
        'nanoeG': 0,
        'nanoe': 0,
        'ecoMode': 0,
        'muteMode': 1,
        'filterReset': 0,
        'powerful': 0,
        'powerfulMode': 0,
        'thermoMode': 0,
        'buzzer': 1,
        'autoRunMode': 3,
        'unusualPresent': 0,
        'runForbidden': 0,
        'inhaleTemperature': 27,
        'outsideTemperature': 32,
        'insideHumidity': 255,
        'alarmCode': 'F093',
        'nanoeModule': 0,
        'TDWindModule': 0,
    }

    def update_params(self, action):
        running_modes = {
            'on': 1,
            'off': 0,
        }
        self.params['runStatus'] = running_modes[action]


if __name__ == '__main__':
    device = BathHeater()
    device.control('打开灯')
    # device.control('关闭灯')
    exit()
    device = AirCondition()
    device.control('on')
