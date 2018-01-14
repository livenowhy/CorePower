#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/8
@支付模块
"""

from datetime import datetime

from . import db
from models.base import BaseModel

from models.fields import PriceType


class AliTradeLogModel(db.Model):
    """ ali异步通知日志 """
    __tablename__ = 'ali_trade_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    out_trade_no = db.Column(db.String(64))
    trade_no = db.Column(db.String(64))
    total_fee = db.Column(db.String(16))
    trade_status = db.Column(db.String(20))
    payment_type = db.Column(db.String(3))
    notify_type = db.Column(db.String(32))
    created = db.Column(db.DateTime, default=datetime.now)  # 记录日志不需要修改时间
    buyer_email = db.Column(db.String(64), nullable=True)


class WxTradeLogModel(db.Model):
    """ 微信交易异步通知日志 """
    __tablename__ = 'wx_trade_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    out_trade_no = db.Column(db.String(64))
    result_code = db.Column(db.String(16))
    fee_type = db.Column(db.String(10))
    trade_type = db.Column(db.String(10))
    transaction_id = db.Column(db.String(64))
    appid = db.Column(db.String(64), default='')
    mch_id = db.Column(db.String(32), default='')
    total_fee = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now)


class TradeModel(db.Model, BaseModel):
    """ 最低层交易数据 """
    __tablename__ = 'trade'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trade_no = db.Column(db.String(32), unique=True)
    pay_id = db.Column(db.Integer, index=True)
    pay_name = db.Column(db.String(32))
    trade_amount = db.Column(PriceType, default=0)   # PriceField
    trade_status = db.Column(db.Integer, default=0, index=True)
    user_uuid = db.Column(db.String(64), default=0)
    trade_type = db.Column(db.Integer, default=0)
    body = db.Column(db.String(256))


class TradeRefundModel(db.Model, BaseModel):
    """ 交易退款记录 """
    __tablename__ = 'trade_refund'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    refund_no = db.Column(db.String(32))
    trade_no = db.Column(db.String(32))
    refund_amount = db.Column(PriceType, default=0)  # PriceField


class RefundSheetModel(db.Model, BaseModel):
    """ 退款单:方便财务审核 """
    __tablename__ = 'refund_sheet'
    refund_sheet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    refund_sheet_sn = db.Column(db.String(32))
    trade_no = db.Column(db.String(32))
    pay_id = db.Column(db.Integer, index=True)
    refund_category = db.Column(db.Integer, index=True)
    order_id = db.Column(db.Integer, index=True)
    sub_order_id = db.Column(db.Integer, index=True, default=0)
    sub_order_item_id = db.Column(db.Integer, index=True, default=0)
    refund_amount = db.Column(PriceType, default=0)  # PriceField
    refund_sheet_status = db.Column(db.Integer, default=0)
    user_uuid = db.Column(db.String(64), default=0)
    applicant = db.Column(db.String(16), default=0)
    reason = db.Column(db.String(1024), default=0)


class RefundSheetOperationModel(db.Model, BaseModel):
    """ 退款单操作记录 """
    __tablename__ = 'refund_sheet_operation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    refund_sheet_id = db.Column(db.Integer)
    last_status = db.Column(db.Integer)
    current_status = db.Column(db.Integer)
    op_user = db.Column(db.String(64))
    user_uuid = db.Column(db.String(64), default=0)
    op_desc = db.Column(db.String(1024), default=0)


class RefundActionLogModel(db.Model, BaseModel):
    """ 退款操作日志 """
    __tablename__ = 'refund_action_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    refund_sheet_sn = db.Column(db.String(32))

    refund_no = db.Column(db.String(32))
    trade_no = db.Column(db.String(32))
    refund_status = db.Column(db.Boolean, default=False)
    msg = db.Column(db.String(128))


class OrderTradeRefundModel(db.Model, BaseModel):
    """ 订单交易退款 """
    __tablename__ = 'order_trade_refund'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    refund_no = db.Column(db.String(32))
    trade_no = db.Column(db.String(32))
    refund_amount = db.Column(PriceType, default=0)  # PriceField
    order_id = db.Column(db.Integer, index=True)
    sub_order_id = db.Column(db.Integer, index=True, default=0)