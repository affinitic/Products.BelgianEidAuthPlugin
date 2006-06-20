from Products.CMFCore.TypesTool import ContentFactoryMetadata
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
import string

from Products.BelgianEidAuthPlugin.config import *

def install(self):
    """Register password reset skins and add the tool"""
    directory_name = 'BelgianEidAuthPlugin'
    
    out = StringIO()

    # Setup the skins
    skinstool = getToolByName(self, 'portal_skins')
    if directory_name not in skinstool.objectIds():
        # We need to add Filesystem Directory Views for any directories
        # in our skins/ directory.  These directories should already be
        # configured.
        addDirectoryViews(skinstool, 'skins', product_globals)
        out.write("Added %s directory view to portal_skins\n" % directory_name)
    
    
    #By default we could also remove the portlet_login from left_slots and right_slots   
    #but this is to restrictive so we just show in doc how to do it
    #Update action linked to the "connect" link
    #change "login_form" to "choose_connection_mode"
    mtool = getToolByName(self, "portal_membership", None)
    #we remove the "join" action and we add another one
    if mtool:
        actions = mtool._actions
        filtered = [action for action in actions if action.id != "login"]
        if len(actions) != len(filtered):
            mtool._actions = tuple(filtered)
            mtool.addAction(id="login",
                            name="Log in",
                            action="string:${portal_url}\choose_connection_mode",
                            condition="not: member",
                            permission="View",
                            category="user",
                            visible=1,
                            REQUEST=None
                        )

    return out.getvalue()
