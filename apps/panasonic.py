import requests

from config import PANASONIC


class Panasonic(object):
    url = ''
    base_params = {}
    headers = {
        'Host': 'app.psmartcloud.com',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Origin': 'https://app.psmartcloud.com',
        'xtoken': 'SSID={}'.format(PANASONIC['SSID']),
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        # 'Referer': '',  # no need
        # 'Content-Length': '468',  # no need
        'Connection': 'keep-alive',
    }
    cookies = {
        'acw_tc': PANASONIC['ACW_TC'],
    }

    def _control(self, action_params):
        params = {**self.base_params, **action_params}
        data = {
            "id": 1,
            "usrId": PANASONIC['USER_ID'],
            "deviceId": PANASONIC['DEVICE_ID'],
            "token": PANASONIC['TOKEN'],
            "params": params,
        }
        response = requests.post(self.url, headers=self.headers, cookies=self.cookies, json=data, verify=False)
        print(response.json())

    def control(self, action=''):
        pass


class BathHeater(Panasonic):
    url = 'https://app.psmartcloud.com/App/ADevSetStatusInfoFV54BA1C'
    base_params = {
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

    def control(self, action='关闭灯'):
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
        dic = {
            "runningMode": running_mode,
            "lightSet": light_set,
        }
        self._control(dic)


class AirCondition(Panasonic):
    url = 'https://app.psmartcloud.com/App/ACDevSetStatusInfoAW'
    params = {
        'runMode': 3,
        'forceRunning': 0,
        'runStatus': 1,
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


if __name__ == '__main__':
    device = BathHeater()
    # device.control('打开灯')
    device.control('关闭灯')
