#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/8
"""

import datetime
import random


class CodeAlgorithm(object):
    pass


class TradeNoAlgorithm(CodeAlgorithm):
    def generate(self):
        prefix = datetime.datetime.now().strftime('%Y%m%d')
        random_no = str(random.randint(1000000000, 9999999999))
        return '%s%s' % (prefix, random_no)


class ShortCodeAlgorithm(CodeAlgorithm):
    def generate(self):
        short_no = str(random.randint(100000000, 999999999))
        return short_no