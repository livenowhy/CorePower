#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2017/11/27
"""


class WxPayConfig(object):
    """
    APPID: 绑定支付的APPID
    MCHID: 商户号
    KEY: 商户支付密钥
    APPSECRET: 公共账号secret (JSAPI支付的时候需要配置)
    """

    # DEBUG
    APPID = ''
    MCHID = ''
    KEY = ''
    APPSECRET = ''


class AbsWxPayConfig(object):
    def get_appid(self):
        raise NotImplementedError('微信支付必须配置APPID')

    def get_mchid(self):
        raise NotImplementedError('微信支付必须配置商户ID')

    def get_key(self):
        raise NotImplementedError('微信支付必须配置密钥')

    def get_appsecret(self):
        raise NotImplementedError('微信支付必须配置APP SECRET')

    def get_appclient_key(self):
        raise NotImplementedError('微信支付操作必须使用CA证书key')

    def get_appclient_cert(self):
        raise NotImplementedError('微信支付操作必须使用CA证书')
