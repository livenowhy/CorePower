#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/9
"""
from flask import g

from common.core.base import Base
from common.core.trade import Price

from models.trade import TradeModel, TradeRefundModel

from common.constants.transaction.payment import TradeStatus, PayType

#
# from .data import TransactionRefundData
# from common.payment.payment import PaymentService
#

import commonware.log
log = commonware.log.getLogger("trade.Trade")


class Trade(Base):
    def __init__(self, trade_no, trade_info={}):
        super(Trade, self).__init__(trade_no)
        self.trade_info = trade_info
        self.__service = None
        self.__refund_info_list = None

    @classmethod
    def read_info(cls, trade_obj):
        if isinstance(trade_obj, TradeModel) is False:
            return {}

        info = dict()
        info['id'] = trade_obj.id
        info['trade_no'] = trade_obj.trade_no
        info['pay_id'] = trade_obj.pay_id
        info['pay_name'] = trade_obj.pay_name
        info['trade_amount'] = trade_obj.trade_amount
        info['trade_status'] = trade_obj.trade_status
        info['user_uuid'] = trade_obj.user_uuid
        info['trade_type'] = trade_obj.trade_type
        info['body'] = trade_obj.body
        return info

    @classmethod
    def create(cls, user_id, pay_id, pay_name, trade_amount, body, trade_type):
        trade_obj = TradeModel(user_id=user_id,
                               pay_id=pay_id,
                               pay_name=pay_name,
                               trade_amount=trade_amount,
                               body=body,
                               trade_type=trade_type)
        g.db_session.add(trade_obj)
        g.db_session.commit()
        trade_info = cls.read_info(trade_obj)
        return cls(trade_obj.trade_no, trade_info=trade_info)

    @classmethod
    def find(cls, trade_no=None, pay_id=None, trade_status=None, user_id=None,
             trade_type=None, offset=0, count=None, start=None, end=None):

        qs = g.db_session.query(TradeModel)

        if trade_no is not None:
            qs = qs.filter(TradeModel.trade_no == trade_no)

        if pay_id is not None:
            qs = qs.filter(TradeModel.pay_id == pay_id)

        if trade_status is not None:
            qs = qs.filter(TradeModel.trade_status == trade_status)

        if user_id is not None:
            qs = qs.filter(TradeModel.user_id == user_id)

        if trade_type is not None:
            qs = qs.filter(TradeModel.trade_type == trade_type)

        if start is not None:
            qs = qs.filter(TradeModel.start >= start)

        if end is not None:
            qs = qs.filter(TradeModel.end <= end)

        qs = qs.all()
        total_count = qs.count()
        if offset is not None and count is not None:
            qs = qs[offset: offset + count]
        trade_obj_list = [lambda _m: cls(_m.trade_no, cls.read_info(_m)), qs]
        return trade_obj_list, total_count

    def get_obj(self):
        hdl = g.db_session.query(TradeModel).get(trade_no=self.id)
        return hdl
    
    def __confirm_model_info(self):
        if self.trade_info is {}:
            __model_obj = self.get_obj()
            self.trade_info = self.read_info(__model_obj)
            
    @property
    def user_id(self):
        self.__confirm_model_info()
        return self.__confirm_model_info['user_id']

    # @property
    # def refund_amount(self):
    #     refund_info_list = self.get_refund_list()
    #     refund_amount = Price()
    #     for refund_info in refund_info_list:
    #         refund_amount += refund_info.get("refund_amount")
    #     return refund_amount

    @property
    def trade_amount(self):
        self.__confirm_model_info()
        return self.__confirm_model_info['trade_amount']

    @property
    def trade_no(self):
        self.__confirm_model_info()
        return self.__confirm_model_info['trade_no']

    # @property
    # def residual_amount(self):
    #     return self.trade_amount - self.refund_amount

    @property
    def pay_name(self):
        self.__confirm_model_info()
        return self.__confirm_model_info['pay_name']

    @property
    def pay_id(self):
        self.__confirm_model_info()
        return self.__confirm_model_info['pay_id']

    @property
    def pay_type(self):
        self.__confirm_model_info()
        pay_type = PayType.online_type().get(self.pay_id)
        return pay_type

    @property
    def is_success(self):
        self.__confirm_model_info()
        return self.__confirm_model_info['trade_status'] == TradeStatus.PAID

    def pay(self, paid_amount):
        self.__confirm_model_info()
        if self.trade_amount != paid_amount:
            raise Exception("交易金额与支付金额不符")
        if self.is_success is False:
            self.update(trade_status=TradeStatus.PAID)
            self.payoff()
    
    ###########
            
            


    def __confirm_pay_service(self):
        self.__confirm_model_info()
        if self.__service is None:
            self.__service = PaymentService.create_payment(self.pay_type)





    def __prepare_pay(self, notify_url, return_url=None):
        self.__confirm_pay_service()
        self.__service.set_notify_url(notify_url)
        if return_url is not None:
            self.__service.set_return_url(return_url)

    def _app_pay(self, notify_url, return_url=None, **kwargs):
        self.__prepare_pay(notify_url, return_url=return_url)
        results = self.__service.app_payment(self.__model_obj.body,
                self.__model_obj.trade_no, self.__model_obj.trade_amount,
                return_url=return_url, **kwargs)
        return results

    def _qr_pay(self, notify_url, return_url=None, **kwargs):
        self.__prepare_pay(notify_url, return_url=return_url)
        ret = self.__service.qr_code_pay(self.__model_obj.body,
                self.__model_obj.trade_no, self.__model_obj.trade_amount)
        results = dict()
        results["url"] = ret
        return results

    def _wap_pay(self, notify_url, return_url=None, **kwargs):
        self.__prepare_pay(notify_url, return_url=return_url)
        results = self.__service.wap_pay(self.__model_obj.body,
                self.__model_obj.trade_no, self.__model_obj.trade_amount, **kwargs)
        return results

    def _mini_pay(self, notify_url, return_url=None, **kwargs):
        self.__prepare_pay(notify_url, return_url=return_url)
        results = self.__service.mini_pay(self.__model_obj.body,
                self.__model_obj.trade_no, self.__model_obj.trade_amount, **kwargs)
        return results

    # 新零售 支付方式(收银台现金或汇聚支付)
    def _cashier_pay(self, notify_url, return_url=None, **kwargs):
        self.__prepare_pay(notify_url, return_url=return_url)
        results = self.__service.joinpay_pay(self.__model_obj.body,
                self.__model_obj.trade_no, self.__model_obj.trade_amount, **kwargs)
        return results

    def apply_pay(self, method, notify_url, return_url=None, **kwargs):
        """ 申请支付
        目前支持支付方式
        1. QR支付 （用户PC端扫码支付）
        2. 手机支付
        3. WAP支付 （用户H5目前的支付方案）
        4. 线下支付 （线下新零售支付方案）
        """
        if self.is_success() is True:
            raise Exception("此次交易已支付, 请勿重复支付")
        mtd = getattr(self, "_%s_pay" % (method), None)
        if not callable(mtd):
            raise Exception("当前无法支付的支付方式[%s]" % method)
        kwargs.update(user_id=str(self.user_id))
        results = mtd(notify_url, return_url=return_url, **kwargs)
        return results

    def payoff(self):
        """
        交易成功支付之后逻辑处理，需要按具体模块业务需求实现
        """
        pass





    def refund(self, amount):
        self.__confirm_model_info()
        self.__confirm_pay_service()
        if amount > self.residual_amount:
            raise Exception("退款金额大于交易可退余额")
        log.info('core.trade.refund')
        refund_data = TransactionRefundData(self.__model_obj.trade_no, amount)
        refund_no, is_success, err = self.__service.refund(refund_data)

        if is_success is True:
            TradeRefundModel.objects.create(trade_no=self.id, refund_amount=amount,
                    refund_no=refund_no)
            self.__refund_info_list = None
        return refund_no, is_success, err

    def get_refund_list(self):
        if self.__refund_info_list is None:
            trade_refund_model_obj_list = TradeRefundModel.objects.filter(trade_no=self.id)
            self.__refund_info_list = map(lambda _m:_m.to_dict(), trade_refund_model_obj_list)
        return self.__refund_info_list

    def read(self):
        self.__confirm_model_info()
        return self.__model_obj.to_dict()

    def query(self):
        self.__confirm_model_info()
        self.__confirm_pay_service()
        results = self.__service.order_query(self.trade_no)
        return results

