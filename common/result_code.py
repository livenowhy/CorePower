#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/16
"""

status_code = {
    0: 'OK',
    101: 'Parameters error'
}


def request_result(code, ret={}):
    result = {
        'status': code,
        'msg': status_code[code],
        'result': ret
    }
    return result
