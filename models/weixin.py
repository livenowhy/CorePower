#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/9
@func: 微信相关
"""

from . import db
from models.base import BaseModel


class WxAppMchModel(db.Model, BaseModel):
    __tablename__ = 'wx_app_mch'
    appid = db.Column(db.String(24), primary_key=True)
    appsecret = db.Column(db.String(32))
    mchid = db.Column(db.String(20))
    key = db.Column(db.String(32))

class WxMchModel(db.Model, BaseModel):
    __tablename__ = 'wx_mch'
    mchid = db.Column(db.String(20), primary_key=True)
    key = db.Column(db.String(32))
