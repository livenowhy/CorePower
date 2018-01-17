#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/17
"""


from flask import Blueprint
from flask import request, jsonify
from flask_restful import Api, Resource

from views.api.v1.authuser import AuthUserView


auth_user = Blueprint('authuser', __name__, url_prefix='/authuser')


class Test(Resource):
    def get(self):
        """ http://192.168.234.176:8888/api/v1/authuser/test """
        data = "测试接口"
        return {"data": data}


api = Api()

api.add_resource(Test, '/test')
api.add_resource(AuthUserView, '/users')


api.init_app(auth_user)