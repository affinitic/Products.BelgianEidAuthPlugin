"""
BelgianEidAuthPlugin
"""

from AccessControl import ClassSecurityInfo

from Globals import InitializeClass
from OFS.Cache import Cacheable

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin

from zLOG import LOG
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

manage_addBelgianEidAuthPluginForm = PageTemplateFile(
    'www/BelgianEidAdd', globals(), __name__='manage_addBelgianEidAuthPluginForm' )

def manage_addBelgianEidAuthPlugin(dispatcher, id, title=None, REQUEST=None):
    """ Add a BelgianEidAuthPlugin to a Pluggable Auth Service. """

    obj = BelgianEidAuthPlugin(id, title)
    dispatcher._setObject(obj.getId(), obj)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(
                                '%s/manage_workspace'
                                '?manage_tabs_message='
                                'BelgianEidAuthPlugin+added.'
                            % dispatcher.absolute_url())

class BelgianEidAuthPlugin(BasePlugin, Cacheable):

    """ PAS plugin for using BelgianEid credentials to log in.
    """

    meta_type = 'BelgianEidAuthPlugin'

    security = ClassSecurityInfo()

    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title


    #
    #   IAuthenticationPlugin implementation
    #
    security.declarePrivate('authenticateCredentials')
    def authenticateCredentials(self, credentials):

        """ See IAuthenticationPlugin.

        o We expect the credentials to be those returned by ILoginPasswordExtractionPlugin.
        o We do not need a password if we receive can access data in the REQUEST
        """
        debug = True
        print "BelgianEidAuthPlugin : debug mode is %s" % debug

        if debug:
            fake_username, fake_login = "user", "user"
            print "BelgianEidAuthPlugin : debug mode is returning '%s', '%s'" % (fake_username, fake_login)
            return "user", "56789"
        
        if credentials:
            #we received something, the user is using his eID card, proceed
            debug=True
            name, name2, nr = self.getClientData(from_hhtp)
            #we lookup if the user has already been logged
            #we search for nr in the existing users
            return name, name
        else:
            return None


    security.declarePrivate('extractCredentials')
    def extractCredentials(self, request):
        """ Extract eid userinfo from request 
            These informations will be used by authenticateCredentials as it receive them as parameter
        """
        
        from_http = credentials.get('HTTP_SSL_CLIENT_S_DN')
        print "from_http : %s" % from_http
        creds = {}
        name, name2, nr = self.getClientData(from_hhtp)
        
        if name and name2 and nr:
            creds.update({'eid_name':name,
                          'eid_name2':name2,
                          'eid_nr':nr,
                          'eid_from_http':1
                         }
                        )
        return creds

        
    security.declarePrivate('getClientData')
    def getClientData(self, from_http):
        """ 
        We receive a String, we need to parse it to return the name, first_name and nr (national register number)
        """
        #there can be UTF/ISO encoding problems with OpenSSL/Apache, so we do what we have to to correct this
        #UTF-8 codes are not passed as codes but as string
        #"é" should be '\xc3\xa9' but it is returned as '\\xc3\\xa9'
        try:
            corrected_string = eval("u'" + from_http + "'")
            corrected_string = corrected_string.encode('latin1')
            corrected_string = unicode(corrected_string, 'utf-8')
        except Error:
            #if we encoutered an error doing this, we have to stop here
            return None, None, None
        #the string is corrected, we can parse it to retrieve the informations we want
        #we parse                
        return None, None, None 
                    
classImplements(BelgianEidAuthPlugin, IAuthenticationPlugin)

InitializeClass(BelgianEidAuthPlugin)
