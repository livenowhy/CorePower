#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/16
"""

from flask import g

from common.core.base import Base
from models.weixin import WxMchModel


class WxMch(Base):
    def __init__(self, pk):
        super(WxMch, self).__init__(pk)
        self.object = None

    @classmethod
    def create(cls, mchid, key):
        wxmch = WxMchModel(mchid=mchid, key=key)
        g.db_session.add(wxmch)
        g.db_session.commit()
        return cls(pk=wxmch.pk)

    def cache_key(self):
        return 'wx:mch:%s' % self.id

    def get_obj(self):
        hdl = g.db_session.query(WxMchModel).get(self.id)
        return hdl

    def get_object(self):
        """ 考虑加入缓存 """
        if self.object is None:
            _m = self.get_obj()
            self.object = {
                'mchid': _m.mchid,
                'key': _m.key
            }

        return self.object

    @property
    def mchid(self):
        obj = self.get_object()
        mchid = obj.get('mchid')
        return mchid

    @property
    def key(self):
        obj = self.get_object()
        key = obj.get('key')
        return key