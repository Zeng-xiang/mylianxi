import random
import requests
from tantan import config
from common import  keys
from django.core.cache import cache
def send_vcode(size=4):
    start = 10 ** (size-1)
    end = 10 ** size - 1
    return str(random.randint(start,end))


def send_sms(phone):
    vcode = send_vcode()
    print(vcode)
    params = config.YZX_PARMS.copy()
    params['mobile'] = phone
    cache.set(keys.VCODE_KEYS % phone,vcode,timeout=1800)
    params['param'] = vcode

    resp = requests.post(config.YZX_URL,json=params)

    if resp.status_code == 200:
        #表示访问服务器没有问题
        result = resp.json()
        if result['code'] == '000000':
            return True,'ok'
        else:
            return False,result['msg']
    else:
        return False,'访问短信服务器有误'