#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 18/1/14 下午4:59
"""

from common.payment.data.refund import RefundData
from manage.trade.log import AliTradeLog, WxTradeLog


class TransactionRefundData(RefundData):
    def __init__(self, trade_no, refund_amount):
        self.trade_no = trade_no
        self.refund_amount = refund_amount

    def wx(self):
        data = dict()
        transaction = WxTradeLog.transaction(self.trade_no)
        if transaction is None:
            raise Exception('找不到订单的微信交易记录')
        data.update(appid=transaction.appid, out_trade_no=transaction.out_trade_no,
                    total_fee=transaction.total_fee, refund_fee=self.refund_amount.cent)
        return data

    def ali(self):
        data = dict()
        transaction = AliTradeLog.transaction(self.trade_no)
        if transaction is None:
            raise Exception('找不到订单的支付宝支付记录')

        data.update(trade_no=transaction.trade_no, amout=self.refund_amount.__str__(), desc='alipay refund')
        return data
