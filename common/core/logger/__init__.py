#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/23
"""

import logging

log_level = logging.INFO
log_file = '/var/flask.log'

logging.basicConfig(
    level=log_level,
    filename=log_file,
    format=('%(asctime)s '
            '[%(levelname)s] '
            '[%(filename)s line:%(lineno)d] '
            '%(message)s'),
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='a'
    )