#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/16
"""


from datetime import datetime

from . import db
from models.base import BaseModel


class ResourcesAclModel(db.Model, BaseModel):
    """ 资源权限访问 """
    __tablename__ = 'resources_acl'
    resource_uuid = db.Column(db.String(64), primary_key=True)
    resource_type = db.Column(db.String(64))
    admin_uuid = db.Column(db.String(64))
    project_uuid = db.Column(db.String(64))
    user_uuid = db.Column(db.String(64))
