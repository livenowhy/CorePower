#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2017/11/25
"""

import commonware.log
from decimal import Decimal

log = commonware.log.getLogger('core.trade.price')

class Price(object):
    """ 钱 """
    def __init__(self, price, is_cent=False):
        """ 初始化: is_cent=True,表示price是分 """
        if is_cent:
            self.__cent = int(price)
        elif isinstance(price, Price):
            self.__cent = price.__cent
        else:
            _ = '%.2f' % float(price)
            self.__cent = int(''.join(_.split('.')))

    @property
    def cent(self):
        return int(self.__cent)

    def __str__(self):
        return "%.2f" % (self.__cent / float(100))

    def __int__(self):
        return int(self.__cent)

    def __float__(self):
        return float(self.__cent)

    def __check_price(self, price):
        if price == None:
            price = 0
        return int(float(price) * 100)

    def __cmp__(self, price):
        if price is None:
            return 1
        elif isinstance(price, Price):
            return self.__cent.__cmp__(price.__cent)
        else:
            price = self.__check_price(price)
            return self.__cent.__cmp__(price)

    def __lt__(self, price):
        if isinstance(price, Price):
            return self.__cent < price.cent
        else:
            price = self.__check_price(price)
            return self.__cent < price

    def __le__(self, price):
        if self.__lt__(price):
            return True
        if self == price:
            return True
        return False

    def __gt__(self, price):
        if isinstance(price, Price):
            return self.__cent > price.cent
        else:
            price = self.__check_price(price)
            return self.__cent > price

    def __ge__(self, price):
        if self.__gt__(price):
            return True
        if self == price:
            return True
        return False

    def __add__(self, price):
        if isinstance(price, Price):
            price = self.__cent + price.cent
        else:
            price = self.__check_price(price)
            price = self.__cent + price
        price *= 0.01
        return Price(price)

    def __sub__(self, price):
        if isinstance(price, Price):
            price = self.__cent - price.cent
        else:
            price = self.__check_price(price)
            price = self.__cent - price
        price *= 0.01
        return Price

    def __div__(self, price):
        if isinstance(price, Price):
            discount = float(self.__cent) / price.cent
            return discount
        else:
            price = float(price)
            cent = int(round(self.__cent / price))
            return Price(cent, is_cent=True)

    def __mul__(self, discount):
        if isinstance(discount, Price):
            raise Exception("不支持当前操作.")
        else:
            price = int(round(self.__cent * float(discount)))
            price *= 0.01
        return Price(price)

    def __rmul__(self, discount):
        return self.__mul__(discount)

    def __radd__(self, price):
        return self.__add__(price)

    def __rsub__(self, price):
        if isinstance(price, Price):
            price = price.cent - self.__cent
        else:
            price = self.__check_price(price)
            price = price - self.__cent
        price *= 0.01
        return Price(price)

    def __rdiv__(self, price):
        if isinstance(price, Price):
            discount = float(price.cent) / self.__cent
        else:
            price = self.__check_price(price)
            discount = float(price) / self.__cent
        discount = round(discount, 2)
        return discount

    @property
    def YUAN(self):
        return '%.2f' % (self.__cent / float(100))

    @property
    def FEN(self):
        return self.cent