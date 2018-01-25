#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/19
"""

import uuid
import time

from flask import g
from models.users import UserModel
from common.core.base import Base
from common.core.utils.security.password import password_md5_encrypt

from manage.token.token import UserToken


from common.core.logger import logging as log


class User(Base):
    def __init__(self, user_uuid):
        super(User, self).__init__(user_uuid)
        self.object = None

    @classmethod
    def create(cls, user_name, password, email):
        """ 数据库创建用户 """
        salt = str(uuid.uuid4())[-11:-1]
        salt_password = password_md5_encrypt(user_name, password, salt)
        auth_user = UserModel(password=salt_password, user_name=user_name,
                              salt=salt, email=email, is_superuser=False, is_active=False)
        g.db_session.add(auth_user)
        g.db_session.commit()
        return cls(auth_user.id)

    @classmethod
    def user_create(cls, user_name, password, email):
        # 验证码验证
        # 用户名无重复验证
        # 邮箱无重复验证
        # 短信验证码验证
        cls.create(user_name, password, email)

    def get_obj_by_id(self):
        return g.db_session.query(UserModel).get(self.id)

    # usererror.APIUseridNotRegisterException


    @classmethod
    def get_obj_by_username(cls, user_name):
        return g.db_session.query(UserModel).get(user_name=user_name)

    # usererror.APIUsernameEmailNotRegisterException

    @classmethod
    def get_obj_by_email(cls, email):
        return g.db_session.query(UserModel).get(email=email)

    # usererror.APIEmailNotRegisterException


    @classmethod
    def get_object_by_type(cls, user_name, sign_in_type):
        if sign_in_type == 'email':
            return cls.get_obj_by_email(user_name)
        elif sign_in_type == 'user_name':
            return cls.get_obj_by_username(user_name)

    def get_object(self):
        if self.object is None:
            erp_user = self.get_obj_by_id()

            self.object = {
                'user_id': erp_user.id,
                'password': erp_user.password,
                'salt': erp_user.salt,
                'username': erp_user.username,
                'first_name': erp_user.first_name,
                'last_name': erp_user.last_name,
                'email': erp_user.email,
                'is_superuser': erp_user.is_superuser,
                'is_active': erp_user.is_active,
                'last_login': erp_user.last_login,
            }
        return self.object

    def read(self):
        data = {
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_superuser': self.is_superuser,
            'is_active': self.is_active,
            'last_login': self.last_login,
        }
        return data

    @property
    def user_id(self):
        _obj = self.get_object()
        return _obj.get('user_id')

    @property
    def password(self):
        _obj = self.get_object()
        return _obj.get('password')

    @property
    def salt(self):
        _obj = self.get_object()
        return _obj.get('salt')

    @property
    def username(self):
        _obj = self.get_object()
        return _obj.get('username')

    @property
    def first_name(self):
        _obj = self.get_object()
        return _obj.get('first_name')

    @property
    def last_name(self):
        _obj = self.get_object()
        return _obj.get('last_name')

    @property
    def email(self):
        _obj = self.get_object()
        return _obj.get('email')

    @property
    def is_superuser(self):
        _obj = self.get_object()
        return _obj.get('is_superuser')

    @property
    def is_active(self):
        _obj = self.get_object()
        return _obj.get('is_active')

    @property
    def last_login(self):
        _obj = self.get_object()
        return _obj.get('last_login')

    @classmethod
    def create(cls, email, user_name, password):
        salt = str(uuid.uuid4())[-11:-1]
        salt_password = password_md5_encrypt(user_name, password, salt)
        user = UserModel(user_name=user_name, email=email, password=salt_password, salt=salt)
        g.db_session.add(user)
        g.db_session.commit()
        return cls(user.id)

    def check_password(self, password):
        salt_password = password_md5_encrypt(self.username, password, self.salt)
        return salt_password == self.password

    @classmethod
    def sign_in(cls, user_name, password):
        if '@' in user_name:
            sign_in_type = 'email'
        else:
            sign_in_type = 'user_name'

        user_model_obj = cls.get_object_by_type(user_name=user_name, sign_in_type=sign_in_type)
        user_obj = User(user_model_obj.id)
        if user_obj.check_password(password):
            erp_token = UserToken.create(user_obj.user_id, client_id='1')
            return erp_token
            # else:
            # raise usererror.APIUsernameAndPasswordErrorException


