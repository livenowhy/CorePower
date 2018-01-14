#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 18/1/13 下午8:19
"""

import string
import random
from urllib import quote
import hashlib
import urllib
import requests
import datetime
from xml.etree.ElementTree import tostring

from common.core.trade import Price
from common.core.utils.xml import dict_to_xml

try:
    from xml.etree import cElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET

from common.core.utils.utils import epoch

import commonware.log
log = commonware.log.getLogger('common.core.trade.payment.weixin')


class WeiXinXml(object):
    def __init__(self, x):
        if isinstance(x, (str, unicode)):
            self.root = ET.fromstring(x)
        else:
            self.root = ET.parse(x)

    def get(self, name):
        try:
            return self.root.find(name).text
        except Exception as msg:
            return None


class WeixinPayment(object):
    def __init__(self, appid, mch_id, api_secret, app_secret):
        self.appid = appid
        self.mch_id = mch_id
        self.api_secret = api_secret
        self.app_secret = app_secret

        self.unifiedorder_url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'

    def get_nonce_str(self, length=32):
        return ''.join([random.choice(string.ascii_lowercase + string.digits) for _ in range(length)])

    def get_param_str(self, data):
        slist = sorted(data)
        param_list = map(lambda k: "{0}={1}".format(k, str(data[k]).encode('utf-8')), slist)
        param_str = '&'.join(param_list)
        return param_str

    def get_sign(self, data):
        param_str = self.get_param_str(data)
        param_str = '{0}&key={1}'.format(param_str, self.api_secret)
        param_str = hashlib.md5(param_str).hexdigest()
        ret = param_str.upper()
        return ret

    def get_prepay_id(self, out_trade_no, total_fee, body, openid, notify_url):
        data = {
            'appid': self.appid,
            'mch_id': self.mch_id,
            'body': body, # 商品描述
            'nonce_str': self.get_nonce_str(),  # 随机数
            'notify_url': notify_url,
            'out_trade_no': out_trade_no,  # 商户订单号
            'trade_type': 'JSAPI',  # 交易类型
            'total_fee': total_fee,  # 订单总金额, 分为单位
            'spbill_create_ip': '127.0.0.1',
            'openid': openid
        }
        data['sign'] = self.get_sign(data)  # 签名
        data_xml = dict_to_xml(data)
        payload = tostring(data_xml)
        log.info('trade requests xml: %s' % payload)
        headers = {
            'Content-Type': 'application/xml'
        }
        ret = requests.post(self.unifiedorder_url, data=payload, headers=headers)
        xml_res = WeiXinXml(ret.text)
        return_code = xml_res.get('return_code')

        if return_code is not None and return_code.lower() == 'success':
            prepay_id = xml_res.get('prepay_id')
            return prepay_id
        return None