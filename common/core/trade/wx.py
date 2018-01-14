# *-* coding:utf-8 *-*

from weixin.core.data import UnifiedOrder, MobilePayload, RefundPayload
from weixin.core.data import WxPayOrderQuery
from weixin.core.api import WxPayApi

import datetime

from common.core.trade.payment import JSAPIPayment
from common.utils.utils import epoch
from common.exception.payment import OutTradeNoUsedException
from common.exception.payment import OrderPaidException
from common.exception.payment import OrderClosedException

from common.wechat.config import PayConfig
from common.wechat.app import WxApp

import commonware.log
log = commonware.log.getLogger("weixin.payment")

class WxTradeType(object):
    NATIVE = "NATIVE"
    APP = "APP"


class WeixinPayment(object):
    def __init__(self, app):
        if app is None:
            app = self.__get_default_app()
        self.app = app

    def __get_default_app(self):
        app = WxApp.from_appid("wxaf251f7ccf232cff")
        return app

    def __set_app(self, appid=None):
        if appid is not None:
            app = WxApp.from_appid(appid)
            self.app = app

    def __get_wx_payment(self):
        app = self.app
        config = PayConfig(app)
        payment = WxPayApi(config)
        return payment



    def get_pay_url(self, out_trade_no,
            total_fee, body, notify_url, **kwargs):

        payment = self.__get_wx_payment()

        payload = UnifiedOrder()
        payload.set_out_trade_no(out_trade_no)
        payload.set_body(body)
        payload.set_total_fee(total_fee.FEN)
        payload.set_trade_type(WxTradeType.NATIVE)
        payload.set_notify_url(notify_url)
        payload.set_product_id(kwargs.get("product_id"))

        results = payment.unifiedorder(payload)
        return results.get("code_url")

    def wap_pay(self, out_trade_no, total_fee, body, notify_url, **kwargs):
        code = kwargs.get("code")
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

    def app_payment(self, out_trade_no, total_fee,
            body, notify_url, **kwargs):
        payload = UnifiedOrder()
        payload.set_out_trade_no(out_trade_no)
        payload.set_body(body)
        payload.set_total_fee(total_fee.FEN)
        payload.set_trade_type(WxTradeType.APP)
        payload.set_notify_url(notify_url)

        pay_api = self.__get_wx_payment()
        ret = pay_api.unifiedorder(payload)
        log.info(ret)
        result_code = ret.get("result_code")
        if result_code == "SUCCESS":
            mobile_payload = MobilePayload()
            mobile_payload.prepayid = ret.get("prepay_id")
            mobile_payload.timestamp = epoch(datetime.datetime.now())
            results = pay_api.mobile_pay(mobile_payload)
            results["pkg"] = mobile_payload.data["package"]
        else:
            err = ret.get("err_code")
            if err == "OUT_TRADE_NO_USED":
                raise OutTradeNoUsedException()
            elif err == "ORDERPAID":
                raise OrderPaidException()
            elif err == "ORDERCLOSED":
                raise OrderClosedException()

        return results

    def refund(self, **kwargs):
        """
        微信退款
        """
        out_trade_no = kwargs.get("out_trade_no", None)
        refund_no = kwargs.get("refund_no", None)
        total_fee = kwargs.get("total_fee", None)
        refund_fee = kwargs.get("refund_fee", None)
        appid = kwargs.get("appid", None)

        self.__set_app(appid)

        payload = RefundPayload()
        payload.out_trade_no = out_trade_no
        payload.out_refund_no = refund_no
        payload.total_fee = total_fee
        payload.refund_fee = refund_fee

        pay_api = self.__get_wx_payment()
        ret = pay_api.refund(payload)
        log.info(ret)
        return_code = ret.get("return_code")
        return_msg = ret.get("return_msg", "")
        return return_code=="SUCCESS", return_msg
