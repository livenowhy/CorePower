# *-* coding:utf-8 *-*

import datetime

from common.core.weixin.data import UnifiedOrder, MobilePayload, RefundPayload, WxPayOrderQuery
from common.core.weixin.api import WxPayApi
from common.core.trade.payment.weixin import JSAPIPayment, WxTradeType
from common.core.utils.utils import epoch

from common.core.weixin.config import WxPayConfig, WxPayConfig
from common.exceptions.payment import OrderClosedException, OrderPaidException, OutTradeNoUsedException
from common.core.weixin.wxapp import WxApp


from common.core.logger import logging as log

class WeixinPayment(object):
    def __init__(self, app):
        if app is None:
            app = self.get_default_app()
        self.app = app

    def get_default_app(self):
        app = WxApp.from_appid('--------')
        return app

    def get_wx_payment(self):
        app = self.app
        config = WxPayConfig(app)
        payment = WxPayApi(config=config)
        return payment

    def get_pay_url(self, out_trade_no, total_fee, body, notify_url, **kwargs):
        payment = self.get_wx_payment()
        payload = UnifiedOrder()
        payload.set_out_trade_no(out_trade_no)
        payload.set_body(body)
        payload.set_total_fee(total_fee.FEN)
        payload.set_trade_type(WxTradeType.NATIVE)
        payload.set_notify_url(notify_url)
        payload.set_product_id(kwargs.get('product_id'))
        result = payment.unifiedorder(payload)
        return result.get('code_url')

    def wap_pay(self, out_trade_no, total_fee, body, notify_url, **kwargs):
        code = kwargs.get('code')
        wap_payment = JSAPIPayment()
        wap_payment.set_code(code)
        openid = wap_payment.get_openid()
        prepay_id = wap_payment.get_prepay_id(out_trade_no, total_fee.FEN, body, openid, notify_url)
        wap_payment.set_prepay_id(prepay_id)
        results = wap_payment.get_js_api_parameter()
        return results

    def order_query(self, out_trade_no):
        payload = WxPayOrderQuery()
        payload.set_out_trade_no(out_trade_no)
        results = WxPayApi.order_query(payload)
        return results

    def app_payment(self, out_trade_no, total_fee, body, notify_url, **kwargs):
        payload = UnifiedOrder()
        payload.set_out_trade_no(out_trade_no)
        payload.set_body(body)
        payload.set_total_fee(total_fee.FEN)
        payload.set_trade_type(WxTradeType.APP)
        payload.set_notify_url(notify_url)

        pay_api = self.get_wx_payment()
        ret = pay_api.unifiedorder(payload)
        result_code = ret.get('result_code')
        if result_code == 'SUCCESS':
            mobile_payload = MobilePayload()
            mobile_payload.prepayid = ret.get('prepay_id')
            mobile_payload.timestamp = epoch(datetime.datetime.now())
            results = pay_api.mobile_pay(mobile_payload)
            results['pkg'] = mobile_payload.data['package']
        else:
            err = ret.get('err_code')
            if 'OUT_TRADE_NO_USED' == err:
                raise OutTradeNoUsedException()
            elif 'ORDERPAID' == err:
                raise OrderPaidException()
            elif 'ORDERCLOSED' == err:
                raise OrderClosedException()

        return results

    def refund(self, out_trade_no=None, refund_no=None, total_fee=None, refund_fee=None, appid=None):
        """ 微信退款 """
        self.set_app(appid)
        payload = RefundPayload()
        payload.out_trade_no = out_trade_no
        payload.out_refund_no = refund_no
        payload.total_fee = total_fee
        payload.refund_fee = refund_fee

        pay_api = self.get_wx_payment()
        ret = pay_api.refund(payload)
        return_code = ret.get('return_code')
        return_msg = ret.get('return_msg', '')
        return return_code == 'SUCCESS', return_msg