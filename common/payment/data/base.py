#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 18/1/14 下午5:03
"""

class PaymentData(object):
    def fetch(self, pay_type):
        method = getattr(self, pay_type, None)
        return method()