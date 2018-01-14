#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/11
"""


class ConstantBase(object):
    @classmethod
    def dict(cls):
        return {}

    @classmethod
    def value_to_text(cls, value):
        _dict = cls.dict()
        if value in _dict:
            return _dict[value]
        return None
