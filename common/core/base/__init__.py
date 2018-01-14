#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/9
"""


class Base(object):
    def __init__(self, pk):
        if type(pk) == str:
            pk = pk.replace('-', '')
        self.__id = pk

    @property
    def id(self):
        return self.__id

    @classmethod
    def create(cls, **kwargs):
        raise Exception

    def read(self):
        raise Exception

    @staticmethod
    def count(**kwargs):
        raise Exception

    @classmethod
    def filter(cls, **kwargs):
        raise Exception

    def update(self, **kwargs):
        raise Exception

    def delete(self):
        raise Exception