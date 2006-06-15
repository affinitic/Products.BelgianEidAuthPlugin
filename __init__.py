"""
BelgianEidAuthPlugin
"""

from AccessControl.Permissions import add_user_folders
from Products.PluggableAuthService.PluggableAuthService import registerMultiPlugin
from BelgianEidAuthPlugin import BelgianEidAuthPlugin, manage_addBelgianEidAuthPlugin, manage_addBelgianEidAuthPluginForm

def initialize(context):
    """ Initialize the GMailAuthPlugin """
    registerMultiPlugin(BelgianEidAuthPlugin.meta_type)

    context.registerClass( BelgianEidAuthPlugin
                            , permission=add_user_folders
                            , constructors=( manage_addBelgianEidAuthPluginForm
                                        , manage_addBelgianEidAuthPlugin
                                        )
                            #, icon=''
                            , visibility=None
                            )