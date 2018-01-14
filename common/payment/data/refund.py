#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 18/1/14 下午5:04
"""


from .base import PaymentData

class RefundData(PaymentData):
    def wx(self, *args, **kwargs):
        """
        微信退款相关参数
        appid: Required. 微信支付应用ID
        out_trade_no: Required. 交易号
        total_fee: Required. 订单总金额（分）
        refund_fee: Required. 申请退款金额（分）
        """
        pass

    def ali(self, *args, **kwargs):
        """ 支付宝退款相关参数 """
        pass