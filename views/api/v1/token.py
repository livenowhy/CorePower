#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/23
"""

import json
from flask import request, jsonify
from flask_restful import Resource

from manage.token.token import UserToken
from manage.users.users import User

from common.core.response import BasicResponse

import common.exceptions.user as usererror
import common.exceptions.token as token_error

from common.core.logger import logging as log

class TokenView(Resource):
    def post(self):
        """
        用户登录获取token

        /phoenix/v1/token/token
        http://localhost:8000/api/v1/token/token
        {
            "username": "username",
            "password": "password"
        }
        """

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

        username = parameters.get('username', None)
        password = parameters.get('password', None)
        log.info('TokenViewTokenViewTokenViewTokenView')
        if username is None:
            raise usererror.APIUserNameNoneException
        token = User.sign_in(username, password)
        data = token.read()
        return BasicResponse(data=data)

    def delete(self):
        """
        退出登录
        http://localhost:8000/phoenix/v1/token/token
        """
        logout_all = request.args.get('logout_all', True)
        if isinstance(logout_all, (str, unicode)) and 'false' == str(logout_all).lower():
            logout_all = False
        else:
            logout_all = True

        authorization = request.META.get('HTTP_AUTHORIZATION')
        token = authorization.split()[-1]
        UserToken.logout(token=token, logout_all=logout_all)
        return BasicResponse()

    def get(self):
        """
        测试验证token
        http://localhost:8000/newerp/users/token

        headers: ApiBearer token
        headers: ApiBearer 9f4d82831aef0fba581482ae84c1e9e62a75f221
        """
        authorization = request.META.get('HTTP_AUTHORIZATION')

        token = authorization.split()[-1]
        erp_token = UserToken.get(token)
        if erp_token.token_usable:
            return BasicResponse()
        else:
            raise token_error.APITokenErrorException
