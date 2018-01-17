#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/17
"""

import hashlib


def md5_encrypt(encrypt_str):
    m = hashlib.md5()
    m.update(encrypt_str)
    return m.hexdigest()
