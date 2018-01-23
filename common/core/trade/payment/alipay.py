#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 18/1/13 下午8:50
"""

import hashlib
import types
import requests
from urllib import urlencode

from common.core.trade import Price


from common.core.logger import logging as log

class AliService(object):
    WAP = 'alipay.wap.create.direct.pay.by.user'
    WEB = 'create_direct_pay_by_user'


def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s

    if not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                return ' '.join([smart_str(arg, encoding, strings_only,
                                           errors) for arg in s])
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s


class AliPayment(object):
    def __init__(self, partner, key, service=AliService.WAP, sign_type='MD5'):
        self.partner = partner
        self.key = key
        self.service = service
        self.sign_type = sign_type

        self.gateway = 'https://mapi.alipay.com/gateway.do?'
        self.api_site = 'http://www.livenowhy.com'


    def get_param_str(self, params):
        ks = params.keys()
        ks.sort()
        newparams = {}
        prestr = ''
        for k in ks:
            v = params[k]
            k = smart_str(k, 'utf-8')
            if k not in ('sign', 'sign_type') and v != '':
                newparams[k] = smart_str(v, 'utf-8')
                prestr += '{0}={1}&'.format(k, newparams[k])
        prestr = prestr[:-1]
        log.info(prestr)
        return newparams, prestr

    def get_sign(self, prestr):
        sign_param = hashlib.md5(prestr + self.key).hexdigest()
        return sign_param

    def pay(self, out_trade_no, total_fee, show_url, return_url=None):
        total_fee = Price(total_fee).__str__()

        data = {
            'service': self.service,
            'partner': self.partner,
            '_input_charset': 'utf-8',
            'out_trade_no': out_trade_no,
            'subject': out_trade_no,
            'total_fee': total_fee,
            'seller_id': self.partner,
            'payment_type': 1,
            'show_url': show_url,
            'notify_url': "{0}/v4/orders/payments/ali".format(self.api_site),
        }

        if self.service == AliService.WEB:
            data['qr_pay_mode'] = 2
            if return_url:
                data['return_url'] = return_url

        params, prestr = self.get_param_str(data)
        params['sign'] = self.get_sign(prestr)
        params['sign_type'] = self.sign_type
        return self.gateway + urlencode(params)

    def verify_url(self, data):
        partner = data.get('seller_id')
        notify_id = data.get('notify_id')

        log.info('正在验证支付宝通知....%s' % notify_id)
        payload = {
            'service': 'notify_verify',
            'partner': partner,
            'notify_id': notify_id
        }
        ret = requests.get(self.gateway, payload)
        result = ret.text
        log.info('正在验证支付宝通知%s : %s' % (notify_id, result))

        if result.upper() == 'TRUE':
            return True
        return False