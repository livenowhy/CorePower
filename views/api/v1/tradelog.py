#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/10
"""

from flask import request, jsonify
from flask_restful import Resource

from manage.trade.log import AliTradeLog


class AliTradeLogView(Resource):
    def get(self):
        """ http://192.168.207.129:8888/api/v1/trade/alitradelog """

        alitradelog = AliTradeLog.find(out_trade_no=1, trade_no=2)
        data = "测试接口"

        for alilog in alitradelog:
            print alilog.read()

        return {"data": data}

    def post(self):
        out_trade_no = '23'
        total_fee = 122
        trade_status = 1
        trade_no = 33
        payment_type = 'ss'
        notify_type = 's'
        AliTradeLog.create(out_trade_no, total_fee, trade_status, trade_no, payment_type, notify_type)
        return {'data': 'is ok'}



class WxTradeLogView(Resource):
    def get(self):
        data = "测试接口"
        return {"data": data}