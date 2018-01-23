#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/19
"""



import uuid
import hashlib
from common.core.base import Base

from models.users import TokenModel
from datetime import datetime, timedelta
from common.core.utils.utils import epoch


from common.core.logger import logging as log


class UserToken(Base):
    def __init__(self, pk):
        super(UserToken, self).__init__(pk)
        self.object = None

    @classmethod
    def get(cls, token):
        try:
            access_token = ErpUserTokenModel.objects.get(token=token)
            return cls(access_token.id)
        except ErpUserTokenModel.DoesNotExist:
            log.info("无法识别身份: %s" % token)
            raise erptokenerror.APITokenNotExistException

    def get_object(self):
        if self.object is None:
            access_token = ErpUserTokenModel.objects.get(id=self.id)
            self.object = {
                "id": self.id,
                "token": access_token.token,
                "expires": access_token.expires,
                "user_id": access_token.user_id,
                "client_id": access_token.client_id,
                "is_active": access_token.is_active
            }
        return self.object

    @classmethod
    def create(cls, user_id, client_id, mpop=True):
        """ mpop: 多点登录,True 允许多点点登录 """

        if mpop is False:
            token_set = ErpUserTokenModel.objects.filter(user_id=user_id, client_id=client_id)
            for row in token_set:
                row.delete()

        expires = datetime.now() + timedelta(minutes=11)
        erp_user_token = ErpUserTokenModel()
        erp_user_token.user_id = user_id
        erp_user_token.token = ErpUserToken.make_token()
        erp_user_token.expires = expires
        erp_user_token.client_id = client_id
        erp_user_token.save()
        return cls(erp_user_token.id)

    def read(self):
        self.get_object()
        return self.object

    @staticmethod
    def make_token():
        hash = hashlib.sha1(uuid.uuid4().hex)
        hash.update(settings.SECRET_KEY)
        return hash.hexdigest()

    def new_token(self):
        token = ErpUserToken.make_token()

    @classmethod
    def logout_all(cls, user_id):
        ErpUserTokenModel.objects.filter(user_id=user_id).update(is_active=False)

    @classmethod
    def logout_token(cls, token):
        ErpUserTokenModel.objects.filter(token=token).update(is_active=False)

    @classmethod
    def logout(cls, token, logout_all=True):
        """ token: 用户token; all: true删除用户所有的token """
        erp_token = cls.get(token)
        user_id = erp_token.user_id
        if logout_all:
            cls.logout_all(user_id=user_id)
        else:
            cls.logout_token(token=token)

    @property
    def is_expires(self):
        """ False 没到期; True 到期 """
        now = datetime.now()
        expires = self.expires
        if expires > now:
            return False
        return True

    @property
    def is_active(self):
        self.get_object()
        log.info("self.object.get('is_active')")
        log.info(self.object.get('is_active'))
        log.info(type(self.object.get('is_active')))
        return self.object.get('is_active')

    @property
    def token_usable(self):
        self.get_object()
        return self.is_expires is False and self.is_active

    @property
    def expires(self):
        self.get_object()
        return self.object.get('expires')

    @property
    def token(self):
        self.get_object()
        return self.object.get('token')

    @property
    def user_id(self):
        self.get_object()
        return self.object.get('user_id')
