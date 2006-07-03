"""
BelgianEidAuthPlugin
"""

from AccessControl.Permissions import add_user_folders
from Products.PluggableAuthService.PluggableAuthService import registerMultiPlugin
from BelgianEidAuthPlugin import BelgianEidAuthPlugin, manage_addBelgianEidAuthPlugin, manage_addBelgianEidAuthPluginForm
from Products.CMFCore.DirectoryView import registerDirectory

registerDirectory('skins', globals())
registerDirectory('skins/BelgianEidAuthPlugin', globals())

def initialize(context):
    """ Initialize the BelgianEidAuthPlugin """
    
    registerMultiPlugin(BelgianEidAuthPlugin.meta_type)
    
    context.registerClass( BelgianEidAuthPlugin
                            , permission=add_user_folders
                            , constructors=( manage_addBelgianEidAuthPluginForm
                                        , manage_addBelgianEidAuthPlugin
                                        )
                             , icon='www/chip_eid.gif'
                            , visibility=None
                            )