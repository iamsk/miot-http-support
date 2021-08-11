import requests
import json

from apps.config import PANASONIC

cookies = {
    'SSID': PANASONIC['SSID'],
    'acw_tc': PANASONIC['ACW_TC'],
}

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
    # 'Referer': '', # no need referer
    'Content-Length': '468',
    'Connection': 'keep-alive',
}

runningModes = {
    '打开灯': 1,
    '关闭灯': 0,
    '换气': 38,
    '取暖': 37,
    '凉干燥': 40,
    '热干燥': 42,
    '待机': 32,
}


def _control(light_set=255, running_mode=255, time_set=3):  # 默认15分钟
    data = {
        "id": 1,
        "usrId": PANASONIC['USER_ID'],
        "deviceId": PANASONIC['DEVICE_ID'],
        "params": {
            "runningMode": running_mode,
            "DIYnextwindDirectionSet": 255,
            "DIYnextwindKindSet": 255,
            "warmTempset": 255,
            "DIYnextWarmTempset": 255,
            "DIYnextStepNo": 2,
            "windDirectionSet": 255,
            "timeSet": time_set,
            "DIYnextRunningMode": 255,
            "windKindSet": 255,
            "lightSet": int(light_set),
            "DIYnextTimeSet": 255,
        },
        "token": PANASONIC['TOKEN'],
    }
    response = requests.post('https://app.psmartcloud.com/App/ADevSetStatusInfoFV54BA1C', headers=headers,
                             cookies=cookies,
                             data=json.dumps(data), verify=False)
    print(response.json())


def control(light_set='关闭灯', running_mode='待机'):
    _control(runningModes[light_set], runningModes[running_mode])


if __name__ == '__main__':
    # _control(0, 32)
    control('打开灯', '换气')
