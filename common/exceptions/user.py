#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2017/11/30
"""

class APIEmailUsernameNoneException(Exception):
    status_code = 1101
    default_detail = "email and username 不能同时为空"


class APIUsernameEmailNotRegisterException(Exception):
    status_code = 1102
    default_detail = "用户不存在"


class APIUsernameAndPasswordErrorException(Exception):
    status_code = 1103
    default_detail = "用户名或者密码错"


class APIEmailNotRegisterException(Exception):
    status_code = 1104
    default_detail = "邮箱未注册"


class APIUseridNotRegisterException(Exception):
    status_code = 1105
    default_detail = "用户id不存在"


class APIUserNameNoneException(Exception):
    status_code = 1105
    default_detail = "登录用户名不能为空"