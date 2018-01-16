#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/16
"""

from flask import g

from common.core.base import Base
from models.weixin import WxMchModel, WxAppMchModel
from .mch import WxMch


class WxApp(Base):
    def __init__(self, pk):
        super(WxApp, self).__init(pk)
        self.object = None

    @classmethod
    def create(cls, appid, appsecret, mchid=None):
        if mchid is None:
            wxappmch = WxAppMchModel(appid=appid, appsecret=appsecret)
        else:
            wxappmch = WxAppMchModel(appid=appid, appsecret=appsecret, mchid=mchid)
        g.db_session.add(wxappmch)
        g.db_session.commit()
        return cls(pk=wxappmch.pk)

    def cache_key(self):
        return 'wx:app:%s' % self.id

    def get_obj(self):
        hdl = g.db_session.query(WxAppMchModel).get(self.id)
        return hdl

    def get_object(self):
        """ 加入缓存 """
        if self.object is None:
            _m = self.get_obj()
            self.object = {
                'appid': _m.appid,
                'appsecret': _m.appsecret,
                'mchid': _m.mchid
            }
        return self.object

    @classmethod
    def from_appid(cls, appid):
        try:
            hdl = g.db_session.query(WxAppMchModel).get(pk=appid)
            return cls(hdl.pk)
        except :
            return None

    @property
    def appid(self):
        obj = self.get_object()
        appid = obj.get('appid')
        return appid

    @property
    def appsecret(self):
        obj = self.get_object()
        secret = obj.get('appsecret')
        return secret

    @property
    def mch(self):
        obj = self.get_object()
        mchid = obj.get('mchid')
        if not mchid:
            return None
        return WxMch(mchid)