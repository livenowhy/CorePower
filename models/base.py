#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2017/12/28
"""


from . import db
from datetime import datetime


class BaseModel(object):
    """ 用户 """
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Boolean, default=True)