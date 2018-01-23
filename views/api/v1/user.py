#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/17
"""

from flask import request, jsonify
from flask_restful import Resource

from manage.users.users import User


class UserView(Resource):
    def get(self):

        print 'ss'

    def post(self):
        user_name = 's'
        password = '333'
        email = '22'
        User.user_create(user_name, password, email)
        return {'data': 'is ok'}