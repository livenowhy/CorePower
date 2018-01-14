#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/11
"""
from common.constants.base import ConstantBase


class PayType(ConstantBase):
    CASH_ON_DELIVERY = 3
    WX = 28
    ALI = 30
    EBANK = 32

    @classmethod
    def dict(cls):
        return {
            cls.CASH_ON_DELIVERY: u"货到付款",
            cls.WX: u"微信支付",
            cls.ALI: u"支付宝支付",
            cls.EBANK: u"一网通支付",
        }

    @classmethod
    def online_type(cls):
        return {
            cls.WX: "wx",
            cls.ALI: "ali",
            cls.EBANK: "ebank",
        }


class OnlinePayment(ConstantBase):
    WX = "wx"
    ALI = "ali"
    EBANK = "ebank"
    JOINPAY = "joinpay"
    CASH_OFFLINE = "cashoffline"

    BIG_PAY = 'bigpay'   # 哔咯支付
    WX_SHOP = 'wxshop'   # 微信小店收款

    @classmethod
    def cashier_type(cls, payment):
        """ 线下收银台,收款方式 """
        return payment == 'cashoffline' or payment == 'joinpay' or payment == 'bigpay' or payment == 'wxshop'

    @classmethod
    def get_payment_info(cls, payment):
        payment_info = {
            cls.WX: {
                "pay_id": 28,
                "pay_name": "微信支付"
            },
            cls.ALI: {
                "pay_id": 30,
                "pay_name": "支付宝支付"
            },
            cls.EBANK: {
                "pay_id": 32,
                "pay_name": "一网通支付"
            },
            cls.JOINPAY: {
                "pay_id": 34,
                "pay_name": "汇聚支付"
            },
            cls.CASH_OFFLINE: {
                "pay_id": 5,
                "pay_name": "线下现金支付"
            },
            cls.BIG_PAY: {
                "pay_id": 6,
                "pay_name": "哔咯支付"
            },
            cls.WX_SHOP: {
                "pay_id": 7,
                "pay_name": "微信小店收款"
            },
        }
        return payment_info.get(payment)

class TradeStatus(ConstantBase):
    PENDING_PAY = 0
    PAID = 1

    @classmethod
    def dict(cls):
        return {
            cls.PENDING_PAY: u"待支付",
            cls.PAID: u"已支付",
        }

class TradeType(ConstantBase):
    ORDER = 1
    UPASS = 2
    USERVICE = 3
    HILIFE = 4
    HILIFE_THREE_SERVICE = 5
    HALLOWMAS = 6
    AGENTPAY = 7
    OTO_SERVICE = 8

    @classmethod
    def dict(cls):
        return {
            cls.ORDER: u"订单",
            cls.UPASS: u"upass",
            cls.USERVICE: u"upass服务",
            cls.HILIFE: u"hi百货线下订单",
            cls.HILIFE_THREE_SERVICE: u"hi百货线下店中店服务订单",
            cls.HALLOWMAS: u"万圣节诊疗卡",
            cls.AGENTPAY: u"亲友代付",
            cls.OTO_SERVICE: u"oto订单",
        }