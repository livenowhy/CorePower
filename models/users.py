#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2017/11/29
"""

from datetime import datetime

from . import db
from models.base import BaseModel


class UserModel(db.Model, BaseModel):
    """ 用户 """
    __tablename__ = 'users'
    id = db.Column(db.String(64), primary_key=True, nullable=False, name='user_uuid')
    user_name = db.Column(db.String(64))   # 用户名
    password = db.Column(db.String(128))

    fullname = db.Column(db.String(30), default='')
    nickname = db.Column(db.String(30))

    birthday = db.Column(db.DateTime, nullable=True)
    sex = db.Column(db.SmallInteger, default=0)

    email = db.Column(db.String(60))

    address_id = db.Column(db.Integer, default=0)               # 用户默认地址
    avatar_url = db.Column(db.String(255), default='')
    user_type = db.Column(db.SmallInteger, default=0)           # 用户类型
    block_balance = db.Column(db.Numeric, name='frozen_money')  # max_digits=7, decimal_places=2 冻结的余额
    balance = db.Column(db.Numeric, name='user_money')          # max_digits=7, decimal_places=2 余额
    is_old = db.Column(db.Boolean, default=False)


class AuthUserModel(db.Model, BaseModel):
    """ 后台管理用户 """
    __tablename__ = 'auth_users'
    id = db.Column(db.String(64), primary_key=True, nullable=False, name='user_uuid')
    password = db.Column(db.String(128))

    user_name = db.Column(db.String(64), unique=True)  # 用户名
    first_name = db.Column(db.String(64))  # 用户名
    salt = db.Column(db.String(64))  # 密码盐
    last_name = db.Column(db.String(64))  # 最后一次登录时间
    email = db.Column(db.String(64), unique=True)  # 用户邮箱
    last_login = db.Column(db.DateTime, default=datetime.now)
    is_superuser = db.Column(db.SmallInteger, default=0)  # 是否是超级用户
    is_active = db.Column(db.SmallInteger, default=0)  # 是否激活


class TokensModel(db.Model, BaseModel):
    __tablename__ = 'auth_tokens'
    id = db.Column(db.String(64), primary_key=True, nullable=False, name='token_uuid')
    token = db.Column(db.String(128))
    user_uuid = db.Column(db.String(64), unique=True)
    team_uuid = db.Column(db.String(64), unique=True)
    project_uuid = db.Column(db.String(64), unique=True)
    expiry_time = db.Column(db.DateTime)   # 过期时间

    is_active = db.Column(db.SmallInteger, default=0)  # 是否有效
