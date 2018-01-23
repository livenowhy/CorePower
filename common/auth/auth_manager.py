#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/16
"""

from flask import g

import inspect
import time

from models.resources_acl import ResourcesAclModel
from common.core.base import Base
from common.core.logger import logging as log


def role_check(action, privilege):
    try:
        if 'create' == action and 'C' in privilege:
            return 0
        elif 'delete' == action and 'D' in privilege:
            return 0
        elif 'update' == action and 'U' in privilege:
            return 0
        elif 'read' == action and 'R' in privilege:
            return 0
        return 1
    except Exception as msg:
        log.warning('Role check error, reason=%s' % msg.message)
        return 1

class AclManager(Base):
    def __init__(self, resource_uuid, object={}):
        super(AclManager, self).__init__(pk=resource_uuid)
        self.object = object

    def get_obj(self):
        hdl = g.db_session.query(ResourcesAclModel).get(resource_uuid=self.id)
        return hdl

    def read(self):
        if self.object is None:
            _m = self.get_obj()
            self.object = {
                'resource_uuid': self.id,
                'resource_type': _m.out_trade_no,
                'admin_uuid': _m.trade_no,
                'project_uuid': _m.total_fee,
                'user_uuid': _m.trade_status
            }
        return self.object

    @property
    def admin_uuid(self):
        """ admin_acl_check """
        self.read()
        return self.object.get('admin_uuid', None)

    @property
    def team_uuid(self):
        """ team_acl_check """
        self.read()
        return self.object.get('admin_uuid', None)

    @property
    def project_uuid(self):
        """ project_acl_check """
        self.read()
        return self.object.get('admin_uuid', None)

    @property
    def user_uuid(self):
        """ user_acl_check """
        self.read()
        return self.object.get('admin_uuid', None)


    @classmethod
    def resource_acl_check(cls, user_uuid, team_uuid, team_priv,
                           project_uuid, project_priv, resource_uuid, action):
        """"""
        resource_acl = cls(resource_uuid)

        try:
            if resource_acl.user_uuid in ('global', user_uuid):
                return 0
        except Exception:
            return 1

        if 0 == role_check(action, project_priv):
            try:
                if resource_acl.project_uuid in ('global', project_uuid):
                    return 0
            except Exception:
                return 1

        if 0 == role_check(action, team_priv):
            try:
                if resource_acl.team_uuid in ('global', team_uuid):
                    return 0
            except Exception:
                return 1

        if 'sysadmin' == user_uuid:
            try:
                if resource_acl.admin_uuid in ('global', user_uuid):
                    return 0
            except Exception:
                return 1

        return 1

