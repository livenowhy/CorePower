#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/23
"""

import datetime
from flask_restful import ResponseBase
from common.core.utils.utils import epoch


class BasicResponse(ResponseBase):
    def __init__(self, data=None, status=200, message='success'):
        res = {
            'status_code': status,
            'message': message,
            'time': epoch(datetime.datetime.now())
        }
        if data is not None:
            res['data'] = data
        super(BasicResponse, self).__init__(res, status=200)