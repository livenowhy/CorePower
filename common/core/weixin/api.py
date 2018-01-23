#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2017/11/28
"""

import requests
import string
import random
from common.core.weixin.config import WxPayConfig
from common.core.weixin.data import WxPayResults



from common.core.logger import logging as log



class WxPayApi(object):
    def __init__(self, config, ip='127.0.0.1'):
        self.__config = config
        self.__ip = ip

    @staticmethod
    def get_nonce_str(length=32):
        return ''.join([random.choice(string.ascii_lowercase + string.digits) for _ in range(length)])

    def unifiedorder(self, payload, timeout=6):
        """ 统一下单 """
        
        url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        
        if not payload.is_out_trade_no_set():
            raise Exception("缺少统一支付接口必填参数out_trade_no")
        
        if not payload.is_body_set():
            raise Exception("缺少统一支付接口必填参数body")
        
        if not payload.is_total_fee_set():
            raise Exception("缺少统一支付接口必填参数total_fee")
        
        if not payload.is_trade_type_set():
            raise Exception("缺少统一支付接口必填参数trade_type")

        if 'JSAPI' == payload.trade_type and not payload.is_openid_set():
            raise Exception("统一支付接口中，缺少必填参数openid！trade_type为JSAPI时，openid为必填参数！")

        if 'NATIVE' == payload.trade_type and not payload.is_product_id_set():
            raise Exception("统一支付接口中，缺少必填参数product_id！trade_type为JSAPI时，product_id为必填参数！")

        if not payload.is_notify_url_set():
            payload.set_notify_url()

        config = self.__config
        payload.appid(config.get_appid())
        payload.mch_id(config.get_mchid())
        payload.spbill_create_ip(self.__ip)
        payload.nonce_str(WxPayApi.get_nonce_str())
        payload.set_sign()

        xml = payload.to_xml()

        headers = {'Content-Type': 'application/xml'}
        log.info(xml)

        ret = requests.post(url, data=xml, headers=headers)
        log.info(ret)
        results = WxPayResults.results(ret.text)
        return results

    def refund(self, payload, timeout=6):
        url = 'https://api.mch.weixin.qq.com/secapi/pay/refund'
        config = self.__config
        payload.appid = config.get_appid()
        payload.mch_id = config.get_mchid()
        payload.noncestr = WxPayApi.get_nonce_str()
        payload.op_user_id = config.get_mchid()  # ???
        payload.set_key(config.get_key())
        payload.set_sign()
        xml = payload.to_xml()
        log.info(xml)

        headers = {
            'Content-Type': 'application/xml'
        }
        log.info(config.get_apiclient_cert())
        ret = requests.post(url, data=xml, headers=headers, verify=True,
                            cert=(config.get_apiclient_cert(), config.get_apiclient_key()))
        log.info(ret)
        results = WxPayResults.results(ret.text)
        return requests

    def mobile_pay(self, payload):
        config = self.__config
        payload.appid = config.get_appid()
        payload.partnerid = config.get_mchid()
        payload.noncestr = WxPayApi.get_nonce_str()
        payload.set_sign()
        return payload.data

    @staticmethod
    def order_query(payload, timeout=6):
        """
        查询订单
        :param payload: WxPayOrderQuery input
        :param timeout: request time out
        :return: WxPayResults
        """
        url = 'https://api.mch.weixin.qq.com/pay/orderquery'
        if not payload.is_out_trade_no_set() and payload.is_transaction_id_set():
            raise Exception('订单查询接口中, out_trade_no、transaction_id 至少填一个')

        payload.set_appid(WxPayConfig.APPID)
        payload.set_mch_id(WxPayConfig.MCHID)
        payload.set_nonce_str(WxPayApi.get_nonce_str())
        payload.set_sign()

        xml = payload.to_xml()
        headers = {
            'Content-Type': 'application/xml'
        }

        ret = requests.post(url, data=xml, headers=headers)
        results = WxPayResults.results(ret.text)
        return results


class WeiXinOpenApi(object):
    def __init__(self, appid):
        self.appid = appid

    @staticmethod
    def authorize(payload, appid):
        """ 用户授权获取code """
        url = 'https://open.weixin.qq.com/connect/oauth2/authorize'
        payload.appid = appid
        url_params = payload.to_url_params()
        ret_url = '{url}?{url_params}#wechat_redirect'.format(url=url, url_params=url_params)
        return ret_url

    @staticmethod
    def access_token(payload):
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
        payload.appid = ''
        payload.secret = ''
        payload.grant_type = 'authorization_code'

        url_params = payload.to_url_params()
        ret_url = '{url}?{url_params}'.format(url=url, url_params=url_params)
        return ret_url

    @staticmethod
    def getticket(payload):
        url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket'
        url_params = payload.to_url_params()
        ret_url = '{url}?{url_params}'.format(url=url, url_params=url_params)
        return ret_url

    @staticmethod
    def token(payload):
        url = 'https://api.weixin.qq.com/cgi-bin/token'
        payload.appid = ''
        payload.secret = ''
        payload.grant_type = 'client_credential'
        url_params = payload.to_url_params()
        ret_url = '{url}?{url_params}'.format(url=url, url_params=url_params)
        return ret_url

    @staticmethod
    def user_info_sns(payload):
        url = 'https://api.weixin.qq.com/sns/userinfo'
        url_params = payload.to_url_params()
        ret_url = '{url}?{url_params}'.format(url=url, url_params=url_params)
        return ret_url

    @staticmethod
    def user_info(payload):
        url = 'https://api.weixin.qq.com/cgi-bin/user/info'
        url_params = payload.to_url_params()
        ret_url = '{url}?{url_params}'.format(url=url, url_params=url_params)
        return ret_url

    def jscode_to_session(self, secret, js_code, grant_type='authorization_code'):
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        params = '&'.join(['appid=%s' % self.appid, 'secret=%s' % secret, 'js_code=%s' % js_code, 'grant_type=%s' % grant_type])
        url = '?'.join([url, params])
        ret = requests.get(url)
        return ret.json()