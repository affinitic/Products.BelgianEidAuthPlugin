"""
BelgianEidAuthPlugin
"""

from AccessControl import ClassSecurityInfo

from Globals import InitializeClass
from OFS.Cache import Cacheable

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin

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

        """ 
            See IAuthenticationPlugin.
            o We expect the credentials to be those returned by ILoginPasswordExtractionPlugin.
            o We do not need a password if we receive can access data in the REQUEST
        """
        
        debug = False
        print "BelgianEidAuthPlugin : debug mode is %s" % debug
        
        if debug:
            return "User", "user"
        
        if credentials.has_key('eid_from_http'):
            #we received something, the user is using his eID card, proceed
            debug=True
            #XXX Alpha1 Version
            #As test, we must have a created user with name from credentials['eid_name']
            return credentials['eid_name'], credentials['eid_name']
            
            #XXX Beta version -->
            #we lookup if the user has already been logged
            #we search for nr in the existing users
        else:
            return None


    security.declarePrivate('extractCredentials')
    def extractCredentials(self, request):
        """ 
            Extract eid userinfo from request 
            These informations will be used by authenticateCredentials as it receive them as parameter
        """
        
        from_http = request.get('HTTP_SSL_CLIENT_S_DN')
        print "from_http : %s" % from_http
        
        if from_http:
            name, name2, nr = self.getClientData(from_http)
            if name and name2 and nr:
                creds = {}
                creds.update({'eid_name':name,
                              'eid_name2':name2,
                              'eid_nr':nr,
                              'eid_from_http':1
                             })
            return creds
        else:
            #If we can not get this from the REQUEST, we are not in a correctly configured HTTPS mode
            return None

    
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
        return "Gauthier", "Bastien", "123456789"
                    
classImplements(BelgianEidAuthPlugin, IAuthenticationPlugin, IExtractionPlugin)

InitializeClass(BelgianEidAuthPlugin)
