#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/8
"""


from common.core.trade import Price
from sqlalchemy.types import Integer

# 参考 http://docs.sqlalchemy.org/en/rel_0_9/core/custom_types.html#creating-new-types

class PriceType(Integer):
    def bind_processor(self, dialect):
        def process(value):
            if isinstance(value, Price):
                value = value.cent
            elif isinstance(value, int):
                value = int(value)
            else:
                value = Price(value).cent
            return value

        return process

    def to_python(self, value):
        if value is None:
            return None
        try:
            value = int(value)
            return Price(value, is_cent=True)
        except (TypeError, ValueError):
            raise ValueError("Do not nest ARRAY types; ARRAY(basetype) ")

    def result_processor(self, dialect, coltype):
        """ Return a conversion function for processing result row values. """
        return self.to_python
