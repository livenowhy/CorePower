#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/17
"""


import uuid
import time

from flask import g
from models.users import AuthUserModel
from common.core.base import Base
from common.core.utils.security.password import password_md5_encrypt

import commonware.log
log = commonware.log.getLogger("manage.users.auth_user")


class AuthUser(Base):
    def __init__(self, user_uuid):
        super(AuthUser, self).__init__(user_uuid)

    @classmethod
    def create(cls, user_uuid, user_name, salt_password, salt, email):
        """ 数据库创建用户 """
        auth_user = AuthUserModel(id=user_uuid, password=salt_password, user_name=user_name,
                                  salt=salt, email=email, is_superuser=False, is_active=False)
        g.db_session.add(auth_user)
        g.db_session.commit()
        return cls(auth_user.id)

    @classmethod
    def user_create(cls, user_name, password, email, code_id=None, code_str=None):
        # 验证码验证
        # 用户名无重复验证
        # 邮箱无重复验证
        # 短信验证码验证
        user_uuid = str(uuid.uuid4())
        salt = str(uuid.uuid4())[-11:-1]
        salt_password = password_md5_encrypt(user_name, password, salt)
        cls.create(user_uuid, user_name, salt_password, salt, email)


