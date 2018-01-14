#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2017/11/26
@fun: 第三方交易系统返回的日志
"""


from flask import g
from common.core.base import Base
from models.trade import AliTradeLogModel, WxTradeLogModel


class AliTradeLog(Base):
    """ ali pay log """
    def __init__(self, pk):
        super(AliTradeLog, self).__init__(pk)
        self.object = None

    @classmethod
    def create(cls, out_trade_no, total_fee, trade_status, trade_no, payment_type, notify_type, buyer_email=''):
        log_base = AliTradeLogModel(out_trade_no=out_trade_no,
                                    total_fee=total_fee,
                                    trade_status=trade_status,
                                    trade_no=trade_no,
                                    payment_type=payment_type,
                                    notify_type=notify_type,
                                    buyer_email=buyer_email)
        g.db_session.add(log_base)
        g.db_session.commit()
        return cls(pk=log_base.id)

    @classmethod
    def find(cls, out_trade_no=None, trade_no=None,
             total_fee=None, trade_status=None, payment_type=None,
             notify_type=None, buyer_email=None, offset=0, count=30, is_page=True):
        """ is_page: 是否分页 """

        hdl = g.db_session.query(AliTradeLogModel)

        if out_trade_no is not None:
            hdl = hdl.filter(AliTradeLogModel.out_trade_no == out_trade_no)

        if trade_no is not None:
            hdl = hdl.filter(AliTradeLogModel.trade_no == trade_no)

        if total_fee is not None:
            hdl = hdl.filter(AliTradeLogModel.total_fee == total_fee)

        if trade_status is not None:
            hdl = hdl.filter(AliTradeLogModel.trade_status == trade_status)

        if payment_type is not None:
            hdl = hdl.filter(AliTradeLogModel.payment_type == payment_type)

        if notify_type is not None:
            hdl = hdl.filter(AliTradeLogModel.notify_type == notify_type)

        if buyer_email is not None:
            hdl = hdl.filter(AliTradeLogModel.buyer_email == buyer_email)

        hdl = hdl.all()
        if is_page:
            hdl = hdl[offset: offset + count]

        obj_list = [cls(_m.id) for _m in hdl]
        return obj_list

    def get_obj(self):
        hdl = g.db_session.query(AliTradeLogModel).get(self.id)
        return hdl

    @classmethod
    def filter_transaction(cls, out_trade_no):
        hdl = g.db_session.query(AliTradeLogModel).filter(AliTradeLogModel.trade_status.in_(('TRADE_SUCCESS', 'TRADE_FINISHED'))
                                                          ).filter(AliTradeLogModel.out_trade_no == out_trade_no)
        return hdl

    @classmethod
    def transaction(cls, out_trade_no):
        m_list = cls.filter_transaction(out_trade_no)
        if len(m_list) > 0:
            m = m_list[0]
            return cls(m.pk, )
        return None

    def read(self):
        if self.object is None:
            _m = self.get_obj()
            self.object = {
                'id': self.id,
                'out_trade_no': _m.out_trade_no,
                'trade_no': _m.trade_no,
                'total_fee': _m.total_fee,
                'trade_status': _m.trade_status
            }
        return self.object

    @property
    def out_trade_no(self):
        obj = self.read()
        out_trade_no = obj.get('out_trade_no')
        return out_trade_no

    @property
    def trade_no(self):
        obj = self.read()
        trade_no = obj.get('trade_no')
        return trade_no

    @property
    def total_fee(self):
        obj = self.read()
        total_fee = obj.get('total_fee')
        return total_fee

    @property
    def trade_status(self):
        obj = self.read()
        trade_status = obj.get('trade_status')
        return trade_status

    def is_success(self):
        return self.trade_status in ('TRADE_SUCCESS', 'TRADE_FINISHED')


class WxTradeLog(Base):
    def __init__(self, pk):
        super(WxTradeLog, self).__init__(pk)
        self.__object = None

    @classmethod
    def create(cls, out_trade_no, total_fee, result_code, transaction_id, trade_type, fee_type, appid='', mch_id=''):
        log_base = WxTradeLogModel(out_trade_no=out_trade_no, total_fee=total_fee,
                                   result_code=result_code, transaction_id=transaction_id,
                                   trade_type=trade_type, fee_type=fee_type,
                                   appid=appid, mch_id=mch_id)
        g.db_session.add(log_base)
        g.db_session.commit()
        return cls(pk=log_base.id)

    def get_obj(self):
        hdl = g.db_session.query(WxTradeLogModel).get(self.id)
        return hdl

    @classmethod
    def filter_transaction(cls, out_trade_no, trade_status='SUCCESS'):
        hdl = g.db_session.query(WxTradeLogModel).filter(WxTradeLogModel.result_code==trade_status).filter(WxTradeLogModel.out_trade_no==out_trade_no)
        return hdl

    @classmethod
    def transaction(cls, out_trade_no, trade_status='SUCCESS'):
        m_list = cls.filter_transaction(out_trade_no, trade_status=trade_status)
        if len(m_list) > 0:
            m = m_list[0]
            return cls(m.pk)
        return None

    def read(self):
        if self.__object is None:
            _m = self.get_obj()
            self.__object = {
                'id': self.id,
                'out_trade_no': _m.out_trade_no,
                'total_fee': _m.total_fee,
                'trade_status': _m.result_code,
                'appid': _m.appid,
                'mch_id': _m.mch_id
            }
        return self.__object

    @property
    def out_trade_no(self):
        obj = self.read()
        out_trade_no = obj.get('out_trade_no')
        return out_trade_no

    @property
    def total_fee(self):
        obj = self.read()
        total_fee = obj.get('total_fee')
        return total_fee

    @property
    def trade_status(self):
        obj = self.read()
        trade_status = obj.get('trade_status')
        return trade_status

    @property
    def appid(self):
        obj = self.read()
        appid = obj.get('appid')
        return appid

    @property
    def is_success(self):
        return self.trade_status == 'SUCCESS'
