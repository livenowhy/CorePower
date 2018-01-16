#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/16
"""


class OutTradeNoUsedException(Exception):
    def __init__(self):
        super(OutTradeNoUsedException, self).__init__('商户订单号重复')


class OrderPaidException(Exception):
    def __init__(self):
        super(OrderPaidException, self).__init__('订单已支付')


class OrderClosedException(Exception):
    def __init__(self):
        super(OrderClosedException, self).__init__('订单已关闭')
