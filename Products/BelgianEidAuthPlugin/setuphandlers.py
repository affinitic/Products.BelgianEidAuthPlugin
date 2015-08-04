from Products.CMFCore.utils import getToolByName


def setup(context):
    if context.readDataFile('Products.BelgianEidAuthPlugin_various.txt') is None:
        return
    portal = context.getSite()
    install_plugin(portal)
    add_property(portal)
    add_role(portal)


def add_role(portal):
    pas = getToolByName(portal, 'acl_users', None)
    prm = pas.portal_role_manager
    if "MemberWithEid" not in prm.listRoleIds():
        prm.addRole("MemberWithEid", "MemberWithEid", "A member that connect with his eID card")


def add_property(portal):
    portal = getToolByName(portal, 'portal_url').getPortalObject()
    if not portal.portal_properties.site_properties.hasProperty('https_address'):
        portal.portal_properties.site_properties.manage_addProperty('https_address', 'https://change_this_url_but_not_the_extension/logged_in', 'string')


def install_plugin(portal):
    acl = portal.acl_users
    if not hasattr(acl, 'eid'):
        acl.manage_addProduct['BelgianEidAuthPlugin'].manage_addBelgianEidAuthPlugin('eid', title='BelgianEidAuthPlugin')

    plugin_obj = acl.eid
    activatable = []
    try:
        for info in plugin_obj.plugins.listPluginTypeInfo():
            interface = info['interface']
            interface_name = info['id']
            if plugin_obj.testImplements(interface):
                activatable.append(interface_name)
    except AttributeError:
        pass
    plugin_obj.manage_activateInterfaces(activatable)
