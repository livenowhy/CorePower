#!/usr/bin/env python
# encoding: utf-8

"""
@author: lzp
@contact: liuzhangpei@126.com
@time: 2018/1/16
"""

import time
import inspect

from .auth_manager import AclManager

import commonware.log

log = commonware.log.getLogger('common.auth.auth_acl_check')








######################


def acl_check(func):
    def _acl_check(*args, **kwargs):
        func_args = inspect.getcallargs(func, *args, **kwargs)
        context = func_args.get('context')

        token = context['token']
        resource_uuid = context['resource_uuid']
        action = context['action']

        user_info = token_auth(token)['result']
        user_uuid = user_info['user_uuid']
        team_uuid = user_info['team_uuid']
        team_priv = user_info['team_priv']
        project_uuid = user_info['project_uuid']
        project_priv = user_info['project_priv']

        cache_context = "%s%s%s%s%s%s%s" % (user_uuid, team_uuid, team_priv,
                                            project_uuid, project_priv, resource_uuid, action)
        log.debug('start ack check, context=%s' % cache_context)
        # 加入缓存
        acl_manager = AclManager()
        ret = acl_manager.resource_acl_check(user_uuid, team_uuid, team_priv,
                                             project_uuid, project_priv,
                                             resource_uuid, action)
        # expire = int(time.time()) + 300

        if 0 == ret:
            try:
                return func(*args, **kwargs)
            except Exception as msg:
                return 'sss'
        else:
            log.warning('Resource acl auth denied: user_uuid = %s, '
                        'team_uuid=%s, team_priv=%s, project_uuid=%s, '
                        'project_priv=%s, resource_uuid=%s, action=%s' % (user_uuid, team_uuid, team_priv,
                                                                          project_uuid, project_priv, resource_uuid, action))
            return '202'

    try:
        return _acl_check
    except Exception as msg:
        log.error('Acl check error, reason=%s' % msg.message)
        return '202'
