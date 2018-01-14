#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2017/11/27
"""

import hashlib
import xmltodict

from common.core.weixin.config import WxPayConfig
import commonware.log
log = commonware.log.getLogger('common.core.weixin.data')


class Payload(object):
    def __init__(self):
        self.data = {}
        self.key = WxPayConfig.KEY

    def to_url_params(self):
        data = self.data
        slist = sorted(data)
        buff = map(lambda k: "{0}={1}".format(k, str(data[k]).encode("utf-8")), slist)
        buff = "&".join(buff)

        return buff

    def sha1(self):
        buff = self.to_url_params()
        buff = hashlib.sha1(buff).hexdigest()
        return buff

    def make_sign(self, using_key=True):
        """ 签名 """
        buff = self.to_url_params()
        if using_key:
            buff = "{0}&key={1}".format(buff, self.key)

        buff = hashlib.md5(buff).hexdigest()
        ret = buff.upper()
        return ret

    def to_xml(self):
        xml = "<xml>"
        for (key, val) in self.data.items():
            xml += "<%s>%s</%s>" % (key, str(val).encode("utf-8"), key)
        xml += "</xml>"
        return xml

    def set_sign(self):
        """ 设置签名 """
        sign = self.make_sign()
        self.data["sign"] = sign
        return sign

    def get_sign(self):
        return self.data.get('sign')

    def is_sign_set(self):
        """ 判断签名 """
        return self.data.get("sign", None) is not None

    def set_key(self, key):
        self.key = key

    def from_xml(self, xml):
        """ xml转字典 """
        self.data = xmltodict.parse(xml).get("xml")
        return self.data


class UnifiedOrder(Payload):

    @property
    def appid(self):
        return self.data.get('appid')

    @appid.setter
    def appid(self, value):
        self.data['appid'] = value

    def is_appid_set(self):
        return self.appid is not None

    @property
    def mch_id(self):
        return self.data.get('mch_id')

    @mch_id.setter
    def mch_id(self, value):
        self.data['mch_id'] = value

    def is_mch_id_set(self):
        return self.mch_id is not None

    @property
    def device_info(self):
        return self.data.get('device_info')

    @device_info.setter
    def device_info(self, value):
        self.data['device_info'] = value

    def is_device_info_set(self):
        return self.device_info is not None

    @property
    def nonce_str(self):
        return self.data.get('nonce_str')

    @nonce_str.setter
    def nonce_str(self, value):
        self.data['nonce_str'] = value

    def is_nonce_str_set(self):
        return self.nonce_str is not None

    @property
    def body(self):
        return self.data.get('body')

    @body.setter
    def body(self, value):
        self.data['body'] = value

    def is_body_set(self):
        return self.body is not None

    @property
    def detail(self):
        return self.data.get('detail')

    @detail.setter
    def detail(self, value):
        self.data['detail'] = value

    def is_detail_set(self):
        return self.detail is not None

    @property
    def attach(self):
        return self.data.get('attach')

    @attach.setter
    def attach(self, value):
        self.data['attach'] = value

    def is_attach_set(self):
        return self.attach is not None

    @property
    def out_trade_no(self):
        return self.data.get('out_trade_no')

    @out_trade_no.setter
    def out_trade_no(self, value):
        self.data['out_trade_no'] = value

    def is_out_trade_no_set(self):
        return self.out_trade_no is not None

    @property
    def total_fee(self):
        return self.data.get('total_fee')

    @total_fee.setter
    def total_fee(self, value):
        self.data['total_fee'] = value

    def is_total_fee_set(self):
        return self.total_fee is not None

    @property
    def spbill_create_ip(self):
        return self.data.get('spbill_create_ip')

    @spbill_create_ip.setter
    def spbill_create_ip(self, value):
        self.data['spbill_create_ip'] = value

    def is_spbill_create_ip_set(self):
        return self.spbill_create_ip is not None

    @property
    def notify_url(self):
        return self.data.get('notify_url')

    @notify_url.setter
    def notify_url(self, value):
        self.data['notify_url'] = value

    def is_notify_url_set(self):
        return self.notify_url is not None

    @property
    def trade_type(self):
        return self.data.get('trade_type')

    @trade_type.setter
    def trade_type(self, value):
        self.data['trade_type'] = value

    def is_trade_type_set(self):
        return self.trade_type is not None

    @property
    def product_id(self):
        return self.data.get('product_id')

    @product_id.setter
    def product_id(self, value):
        self.data['product_id'] = value

    def is_product_id_set(self):
        return self.product_id is not None

    @property
    def openid(self):
        return self.data.get('openid')

    @openid.setter
    def openid(self, value):
        self.data['openid'] = value

    def is_openid_set(self):
        return self.openid is not None


class WxPayOrderQuery(Payload):
    @property
    def appid(self):
        return self.data.get('appid')

    @appid.setter
    def appid(self, appid):
        self.data['appid'] = appid

    def is_appid_set(self):
        return self.appid is not None

    @property
    def mch_id(self):
        return self.data.get('mch_id')

    @mch_id.setter
    def mch_id(self, mch_id):
        self.data['mch_id'] = mch_id

    def is_mch_id_set(self):
        return self.mch_id is not None

    @property
    def transaction_id(self):
        return self.data.get('transaction_id')

    @transaction_id.setter
    def transaction_id(self, transaction_id):
        self.data['transaction_id'] = transaction_id

    def is_transaction_id_set(self):
        return self.transaction_id is not None

    @property
    def out_trade_no(self):
        return self.data.get('out_trade_no')

    @out_trade_no.setter
    def out_trade_no(self, out_trade_no):
        self.data['out_trade_no'] = out_trade_no

    def is_out_trade_no_set(self):
        return self.out_trade_no is not None

    @property
    def nonce_str(self):
        return self.data.get('nonce_str')

    @nonce_str.setter
    def nonce_str(self, nonce_str):
        self.data['nonce_str'] = nonce_str

    def is_nonce_str_set(self):
        return self.nonce_str is not None


class WxPayResults(Payload):
    def check_sign(self):
        if self.is_sign_set():
            raise Exception("签名错误")

        sign = self.make_sign()

        if self.get_sign() == sign:
            return True

        raise Exception("签名错误")

    @classmethod
    def results(cls, xml):
        results = cls()
        results.from_xml(xml)
        if 'SUCCESS' == results.data.get('return_code'):
            return results.data
        return results.data


class Authorize(Payload):
    @property
    def appid(self):
        return self.data.get('appid')

    @appid.setter
    def appid(self, value):
        self.data['appid'] = value

    def is_appid_set(self):
        return self.appid is not None

    @property
    def redirect_uri(self):
        return self.data.get('redirect_uri')

    @redirect_uri.setter
    def redirect_uri(self, value):
        self.data['redirect_uri'] = value

    def is_redirect_uri_set(self):
        return self.redirect_uri is not None

    @property
    def response_type(self):
        return self.data.get('response_type')

    @response_type.setter
    def response_type(self, value):
        self.data['response_type'] = value

    def is_response_type_set(self):
        return self.response_type is not None

    @property
    def scope(self):
        return self.data.get('scope')

    @scope.setter
    def scope(self, value):
        self.data['scope'] = value

    @property
    def state(self):
        return self.data.get('state')

    @state.setter
    def state(self, value):
        self.data['state'] = value


class AccessTokenPayload(Payload):
    @property
    def appid(self):
        return self.data.get('appid')

    @appid.setter
    def appid(self, value):
        self.data['appid'] = value

    @property
    def secret(self):
        return self.data.get('secret')

    @secret.setter
    def secret(self, value):
        self.data['secret'] = value

    @property
    def code(self):
        return self.data.get('code')

    @code.setter
    def code(self, value):
        self.data['code'] = value

    @property
    def grant_type(self):
        return self.data.get('grant_type')

    @grant_type.setter
    def grant_type(self, value):
        self.data['grant_type'] = value


class TicketPayload(Payload):
    @property
    def access_token(self):
        return self.data.get('access_token')

    @access_token.setter
    def access_token(self, value):
        self.data['access_token'] = value

    @property
    def type(self):
        return self.data.get('type')

    @type.setter
    def type(self, value):
        self.data['type'] = value


class UserInfoPayload(Payload):
    def __init__(self):
        super(UserInfoPayload, self).__init__()
        self.data['lang'] = 'zh_CN'

    @property
    def access_token(self):
        return self.data.get('access_token')

    @access_token.setter
    def access_token(self, value):
        self.data['access_token'] = value

    @property
    def openid(self):
        return self.data.get('openid')

    @openid.setter
    def openid(self, value):
        self.data['openid'] = value


class JSTicketPayload(Payload):
    @property
    def noncestr(self):
        return self.data.get('noncestr')

    @noncestr.setter
    def noncestr(self, value):
        self.data['noncestr'] = value

    @property
    def jsapi_ticket(self):
        return self.data.gt('jsapi_ticket')

    @jsapi_ticket.setter
    def jsapi_ticket(self, value):
        self.data['jsapi_ticket'] = value

    @property
    def timestamp(self):
        return self.data.get('timestamp')

    @timestamp.setter
    def timestamp(self, value):
        self.data['timestamp'] = value

    @property
    def url(self):
        return self.data.get('url')

    @url.setter
    def url(self, value):
        self.data['url'] = value


class MobilePayload(Payload):
    def __init__(self):
        super(MobilePayload, self).__init__()
        self.data['package'] = 'Sign=WXPay'

    @property
    def appid(self):
        return self.data.get('appid')

    @appid.setter
    def appid(self, value):
        self.data['appid'] = value

    @property
    def partnerid(self):
        return self.data.get('partnerid')

    @partnerid.setter
    def partnerid(self, value):
        self.data['partnerid'] = value

    @property
    def prepayid(self):
        return self.data.get('prepayid')

    @prepayid.setter
    def prepayid(self, value):
        self.data['prepayid'] = value

    @property
    def noncestr(self):
        return self.data.get('noncestr')

    @noncestr.setter
    def noncestr(self, value):
        self.data['noncestr'] = value

    @property
    def timestamp(self):
        return self.data.get('timestamp')

    @timestamp.setter
    def timestamp(self, value):
        self.data['timestamp'] = value


class RefundPayload(Payload):
    @property
    def appid(self):
        return self.data.get('appid')

    @appid.setter
    def appid(self, value):
        self.data['appid'] = value

    @property
    def mch_id(self):
        return self.data.get('mch_id')

    @mch_id.setter
    def mch_id(self, value):
        self.data['mch_id'] = value

    @property
    def noncestr(self):
        return self.data.get('nonce_str')

    @noncestr.setter
    def noncestr(self, value):
        self.data['nonce_str'] = value

    @property
    def out_trade_no(self):
        return self.data.get('out_trade_no')

    @out_trade_no.setter
    def out_trade_no(self, value):
        self.data['out_trade_no'] = value

    @property
    def out_refund_no(self):
        return self.data.get('out_refund_no')

    @out_refund_no.setter
    def out_refund_no(self, value):
        self.data['out_refund_no'] = value

    @property
    def total_fee(self):
        return self.data.get('total_fee')

    @total_fee.setter
    def total_fee(self, value):
        self.data['total_fee'] = value

    @property
    def refund_fee(self):
        return self.data.get('refund_fee')

    @refund_fee.setter
    def refund_fee(self, value):
        self.data['refund_fee'] = value

    @property
    def op_user_id(self):
        return self.data.get('op_user_id')

    @op_user_id.setter
    def op_user_id(self, value):
        self.data['op_user_id'] = value
