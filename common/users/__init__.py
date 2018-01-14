#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2017/12/28
"""

from models.users import UserModel



class User(object):

    def __init__(self, pk, model_obj=None):
        if isinstance(pk, UserModel):
            super(User, self).__init__(pk.id)
        else:
            super(User, self).__init__(pk)

        self.__user_model_obj = model_obj


    @classmethod
    def create(cls, email, password, platform='web'):
        _user = UserModel()
        _user.email = email
        _user.password = password







    @classmethod
    def creates(cls, email, nickname, platform='ios', channel="", user_type=None):
        __time = epoch(datetime.now())
        __user = MUser()
        __user.username = email
        __user.nickname = nickname
        __user.email = email
        __user.user_type = UserType.get_type(platform)
        __user.reg_time = __time
        __user.last_login = __time
        __user.visit_count = 1
        if user_type != None:
            __user.user_type = user_type
        __user.save()

        user = cls(__user.id)
        RegisterChannel.create(user, channel)
        return user