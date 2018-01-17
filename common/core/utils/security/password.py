#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/17
"""

from .md5 import md5_encrypt


def password_md5_encrypt(user_name, password, salt):
    user_name_salt = '%s%s' % (str(user_name), str(salt))
    str1 = md5_encrypt(user_name_salt)[0:8]
    str2 = md5_encrypt(str1)[8:16]
    str3 = md5_encrypt(str2)[16:24]
    str4 = md5_encrypt(str3)[24:32]
    str5 = '%s%s%s' % (str(password), str4, str(salt))
    return md5_encrypt(str5)
