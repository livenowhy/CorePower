#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2017/12/28
"""

from corepower import app
from flask import jsonify, Flask, g


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(data='ddd')