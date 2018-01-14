#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2017/12/28
"""


# 数据库
DATABASES = {
    'default': {
        'MYSQL_DATABASE_DB': 'registry',
        'MYSQL_DATABASE_HOST': '127.0.0.1',
        'MYSQL_DATABASE_PORT': '3306',
        'MYSQL_DATABASE_USER': 'root',
        'MYSQL_DATABASE_PASSWORD': 'root123root',
        'MYSQL_DATABASE_CHARSET': 'utf8'
    },
}


SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{password}@{host}:{port}/{dbname}?charset=utf8'.format(
    user=DATABASES['default']['MYSQL_DATABASE_USER'],
    password=DATABASES['default']['MYSQL_DATABASE_PASSWORD'],
    host=DATABASES['default']['MYSQL_DATABASE_HOST'],
    port=DATABASES['default']['MYSQL_DATABASE_PORT'],
    dbname=DATABASES['default']['MYSQL_DATABASE_DB']
)


SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_MIGRATE_REPO = '/Users/zhangpei.liu/Desktop/share/CorePower/apps/db'