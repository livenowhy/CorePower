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


class WxPayConfig(AbsWxPayConfig):
    def __init__(self, wx_app):
        self.wx_app = wx_app

        self.wx_pay_apiclient_key = ''
        self.wx_pay_apiclient_cert = ''

    def get_appid(self):
        app = self.wx_app
        appid = app.appid
        return appid

    def get_mch(self):
        app = self.wx_app
        mch = app.mch
        if mch is None:
            raise Exception('请为APP配置商户信息')
        return mch

    def get_mchid(self):
        app = self.wx_app
        mch = self.get_mch()
        mchid = mch.mchid
        return mchid

    def get_key(self):
        app = self.wx_app
        mch = self.get_mch()
        key = mch.key
        return key

    def get_appsecret(self):
        app = self.wx_app
        secret = app.appsecret
        return secret

    def get_appclient_key(self):
        mch = self.wx_app.mch
        key_path = self.wx_pay_apiclient_cert % mch.mchid
        return key_path

    def get_appclient_cert(self):
        mch = self.wx_app.mch
        cert_path = self.wx_pay_apiclient_cert % mch.mchid
        return cert_path
