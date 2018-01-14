#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2017/11/30
"""


from rest_framework.exceptions import APIException


class MobileAlreadyRegistered(APIException):
    status_code = 1000
    detail = ""


class MobileNotRegistered(APIException):
    status_code = 1001
    detail = ""
    

class MobileGetCodeException(APIException):
    status_code = 1002
    detail = ""


class RequestTooFrequently(APIException):
    status_code = 1003
    detail = ""


class NewMobileUserRequestTooFrequently(APIException):
    status_code = 1004
    detail = ""


class CodeNotMatch(APIException):
    status_code = 1005
    detail = ""


class AppAlreadyRegistered(APIException):
    status_code = 1006
    detail = ""


class OnceSignLimited(APIException):
    status_code = 1007
    detail = ""


class InvalidInviteCodeException(APIException):
    status_code = 1008
    detail = ""


class InvitationGiftJusSupportMobileException(APIException):
    status_code = 1009
    detail = ""


class HasGetInvitationGiftException(APIException):
    status_code = 1010
    detail = ""


class AshesUserNoInvitationGiftException(APIException):
    status_code = 1011
    detail = ""


class IllegalUserInMergeAddressException(APIException):
    status_code = 1012
    detail = ""


class AssociatedMobileNotMatchException(APIException):
    status_code = 1013
    detail = ""


class AlreadyAssociatedWithCurrentMobileException(APIException):
    status_code = 1014
    detail = ""


class MobileAlreadyAssociatedWithAnotherUserException(Exception):
    status_code = 1015
    detail = ""


class AlreadyAssociatedWithWeixinException(APIException):
    status_code = 1016
    detail = ""


class WeixinAlreadyAssociatedWithAnotherUserException(APIException):
    status_code = 1017
    detail = ""

class AlreadyAssociatedWithWeiboException(APIException):
    status_code = 1018
    detail = ""


class WeiboAlreadyAssociatedWithAnotherUserException(APIException):
    status_code = 1019
    detail = ""

class AlreadyAssociatedWithQQException(APIException):
    status_code = 1020
    detail = ""


class QQAlreadyAssociatedWithAnotherUserException(APIException):
    status_code = 1021
    detail = ""


class UserCouldBeCombinedException(APIException):
    status_code = 1022
    detail = ""


class EmailAlreadyAssociatedWithAnotherUserException(APIException):
    status_code = 1023
    detail = ""


class AssociatedEmailNotMatchException(APIException):
    status_code = 1024
    detail = ""


class AlreadyAssociatedWithCurrentEmailException(APIException):
    status_code = 1025
    detail = ""


class BirthdayNotAllowEditException(APIException):
    status_code = 1026
    detail = ""