from Products.CMFCore.utils import getToolByName

mtool = getToolByName(context, "portal_membership")
member = mtool.getAuthenticatedMember()

#called from choose_connection_mode template
#choose_connection_mode template MUST be called after login !!!
#if user is logged with his eID card, we add him a role called MemberWithEid
if context.REQUEST.SESSION.has_key('eid_nr'):
    context.acl_users.portal_role_manager.assignRoleToPrincipal('MemberWithEid', member.getId())
    return True
else:
    context.acl_users.portal_role_manager.removeRoleFromPrincipal('MemberWithEid', member.getId()) 
    return False