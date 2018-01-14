#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/9
"""

from xml.etree.ElementTree import Element


def dict_to_xml(data, tag='xml'):
    """ 字典转成 xml 格式数据 """
    elem = Element(tag)
    for key, val in data.items():
        child = Element(key)
        child.text = str(val).encode('utf-8')
        elem.append(child)
    return elem