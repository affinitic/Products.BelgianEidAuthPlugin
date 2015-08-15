## Controller Python Script "logged_in"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Initial post-login actions
# Products.CMFPlone/skins/plone_login/logged_in.cpy

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

REQUEST = context.REQUEST

membership_tool = getToolByName(context, 'portal_membership')
if membership_tool.isAnonymousUser():
    REQUEST.RESPONSE.expireCookie('__ac', path='/')
    email_login = getToolByName(context, 'portal_properties') \
                    .site_properties.getProperty('use_email_as_login')
    if email_login:
        context.plone_utils.addPortalMessage(
            _(u'Login failed. Both email address and password are case '
              u'sensitive, check that caps lock is not enabled.'),
            'error')
    else:
        context.plone_utils.addPortalMessage(
            _(u'Login failed. Both login name and password are case '
              u'sensitive, check that caps lock is not enabled.'),
            'error')
    return state.set(status='failure')

from DateTime import DateTime
member = membership_tool.getAuthenticatedMember()
login_time = member.getProperty('login_time', '2000/01/01')
if not isinstance(login_time, DateTime):
    login_time = DateTime(login_time)
initial_login = int(login_time == DateTime('2000/01/01'))
state.set(initial_login=initial_login)

must_change_password = member.getProperty('must_change_password', 0)
state.set(must_change_password=must_change_password)

if initial_login:
    state.set(status='initial_login')
elif must_change_password:
    state.set(status='change_password')

membership_tool.loginUser(REQUEST)

#code above come from Plone
#if user is logged with his eID card, we add him a role called MemberWithEid
#a user is known as logged with his eID card when eid_username exist in the SESSION object
#beginning patch -->

#we use the key 'eid_username', because 'eid_from_http' does not mean that the user is connected, but mean that the user try to connect...
#'eid_username' = logged user, eid_from_http could cause breakage if user try to connect with his eID card, is not subscribed and try after to connect using his username and password, we MUST make sure that he do not receive the MemberWithEid role !!!

#if context.REQUEST.SESSION.has_key('eid_username'):
#    context.acl_users.portal_role_manager.assignRoleToPrincipal('MemberWithEid', member.getId())
#else:
#    context.acl_users.portal_role_manager.removeRoleFromPrincipal('MemberWithEid', member.getId())

#this is managed in BelgianEidAuthPlugin.py too
#if not context.REQUEST.SESSION.has_key('eid_logged_in_executed'):
#    context.REQUEST.SESSION.set('eid_logged_in_executed', 1)

#<-- end of patch
return state
