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

from Products.CMFCore.utils import getToolByName

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
            ptool = getToolByName(self, 'plone_utils', None)
            normalized_login = ptool.normalizeString(credentials['eid_nr'])
            
            print self.REQUEST.SESSION
            if self.REQUEST.SESSION.has_key('eid_nr'):
                #we already check in users if the actual user exist, we return it
                #we return the user
                return self.REQUEST.SESSION.get('eid_username'), self.REQUEST.SESSION.get('eid_username')
            else:
                #lookup user national register in registered users
                self.REQUEST.SESSION.set('eid_nr', credentials['eid_nr'])
                user_name = self.getUserNameFromNR(self.REQUEST.SESSION.get('eid_nr'))
                if user_name:
                    self.REQUEST.SESSION.set('eid_username', user_name)
                #we will return None if the user has not be found in the database
                return user_name, user_name
        else:
            return None


    security.declarePrivate('extractCredentials')
    def extractCredentials(self, request):
        """ 
            Extract eid userinfo from request 
            These informations will be used by authenticateCredentials as it receive them as parameter
        """
        if request.SESSION.has_key('eid_nr'):
            #we already parsed 'HTTP_SSL_CLIENT_S_DN', we use 'eid_name' stored in SESSION object
            creds = {}
            creds.update({'eid_nr':request.SESSION.get('eid_nr'),
                          'eid_from_http':1})
            return creds
        else:
            #we play with 'HTTP_SSL_CLIENT_S_DN'
            from_http = request.get('HTTP_SSL_CLIENT_S_DN')
            if from_http:
                nr = self.getClientData(from_http)
                if nr:
                    creds = {}
                    creds.update({'eid_nr':nr,
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
            datas = corrected_string.split('/')
            #search for SN, GN and serialNumber
            for data in datas:
                if data[:12] == "serialNumber":
                    nr = data[13:]
     
        except Error:
            #if we encoutered an error doing this, we have to stop here
            return None
        
        return nr


    security.declarePrivate('getUserNameFromNR')
    def getUserNameFromNR(self, nr):
        """
            Lookup the user in the User Manager with is National Register
        """
        for user in self.acl_users.getUsers():
            props = self.acl_users.mutable_properties.getPropertiesForUser(user)._properties
            if props['nationalregister'] == nr:
                return user.getId()
        
        return None


classImplements(BelgianEidAuthPlugin, IAuthenticationPlugin, IExtractionPlugin)

InitializeClass(BelgianEidAuthPlugin)