#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/9
"""
from . import db
from models.base import BaseModel


class ScholarModel(db.Model, BaseModel):
    """ 作者表 """
    __tablename__ = 'scholar'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64))
    dynasty = db.Column(db.String(16))


class LiteratureModel(db.Model, BaseModel):
    """ 作品 """
    __tablename__ = 'literature'
    id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.String(64), primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.String(16))