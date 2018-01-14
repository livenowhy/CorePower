#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/11
"""

import hashlib
import os
import pytz
import time
import random
import datetime

TIME_ZONE = 'Asia/Shanghai'

def md5_for_file(file, block_size=1024):
    md5 = hashlib.md5()
    while True:
        data = file.read(block_size)
        if not data:
            break
        md5.update(data)
    if hasattr(file, 'seek'):  # ??
        file.seek(0, os.SEEK_SET)
    else:
        print 'no seek attr'

    return md5.hexdigest()


def _append_tz(t):
    tz = pytz.timezone(TIME_ZONE)
    return tz.localize(t)


def epoch(t):
    """ Date/Time converted to seconds since epoch """
    if not hasattr(t, 'tzinfo'):
        return
    return int(time.mktime(_append_tz(t).timetuple()))


def now_compat():
    """ 兼容 """
    return datetime.datetime.now() - datetime.timedelta(hours=8)


def generate_verify_code(length):
    chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    x = [random.choice(chars) for i in range(0, length)]
    _verify_code = ''.join(x)
    return _verify_code