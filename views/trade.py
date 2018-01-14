#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/10
"""


from flask import Blueprint
from flask import request, jsonify
from flask_restful import Api, Resource

from views.api.v1.tradelog import AliTradeLogView, WxTradeLogView


trade = Blueprint('trade', __name__, url_prefix='/trade')

class Test(Resource):
    def get(self):
        data = "测试接口"
        return {"data": data}

api = Api()

api.add_resource(Test, '/test')
api.add_resource(AliTradeLogView, '/alitradelog')
api.add_resource(WxTradeLogView, '/wxtradelog')

api.init_app(trade)