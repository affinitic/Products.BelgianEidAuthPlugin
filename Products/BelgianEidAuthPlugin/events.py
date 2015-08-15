# -*- coding: utf-8 -*-
"""
Products.BelgianEidAuthPlugin
-----------------------------

Created by mpeeters
:license: GPL, see LICENCE.txt for more details.
"""

from plone import api
from zope.globalrequest import getRequest


def user_logged_in(event):
    request = getRequest()
    portal = api.portal.get()
    role_manager = portal.acl_users.portal_role_manager
    if 'eid_username' in request.SESSION.keys():
        role_manager.assignRoleToPrincipal('MemberWithEid',
                                           event.principal.getId())
    else:
        role_manager.removeRoleFromPrincipal('MemberWithEid',
                                             event.principal.getId())

    if 'eid_logged_in_executed' not in request.SESSION.keys():
        request.SESSION.set('eid_logged_in_executed', 1)
