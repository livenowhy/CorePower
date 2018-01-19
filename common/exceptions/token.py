#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/19
"""

from rest_framework.exceptions import APIException


class APITokenNotExistException(APIException):
    status_code = 2101
    default_detail = "token 不存在"


class APITokenErrorException(APIException):
    status_code = 2102
    default_detail = "token 不存在或者已经过期"