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

from zLOG import LOG, PROBLEM
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
    """ PAS plugin for using BelgianEid credentials to log in. """

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
            
            XXX We should not use the lookup if we receive valid HTTPS credentials and the user has not been found once, because the user could connect using his username/passwd and we could check to many times
        """
        #print "credentials = ", credentials
        debug = False
        #print "BelgianEidAuthPlugin : debug mode is %s" % debug
        
        if debug:
            return "User", "user"
            
        if credentials.has_key('eid_from_http'):
            #we received something, the user is using his eID card, proceed
            
            if self.REQUEST.SESSION.has_key('eid_username'):
                #we already check in users if the actual user exist, we return it
                #we return the user
                print "return the already connected user"
                #if we come from logged_out, login_success, ... we need to call the logged_in script
                #these URL are not redirected by login_next
                #see login_next.cpy from CMFPlone for more informations
                if not self.REQUEST.SESSION.has_key('eid_logged_in_executed'):
                    self.REQUEST.SESSION.set('eid_logged_in_executed', 1)
                    portal = getToolByName(self, 'portal_url').getPortalObject()
                    self.REQUEST.RESPONSE.redirect(portal.portal_properties.site_properties.getProperty('https_address') + '?came_from=%s' % self.REQUEST.get('URL'))
                return self.REQUEST.SESSION.get('eid_username'), self.REQUEST.SESSION.get('eid_username')
            else:
                #lookup user national register in registered users
                print "lookup user"
                user_name = self.getUserNameFromNR(credentials['eid_nr'])
                if user_name:
                    #we force the redirection to logged_in to be sure that logged_in.cpy where we manage the MemberWithEid role is executed
                    #we do not call logged_in here if the url is not redirectable (see login_next.cpy in CMFPlone)
                    if not self.REQUEST.SESSION.has_key('eid_logged_in_executed'):
                        not_redirectable_urls = ['login', 'login_success', 'login_password', 'login_failed',
                                               'login_form', 'logged_in', 'logged_out', 'logout', 'registered',
                                               'mail_password', 'mail_password_form', 'join_form',
                                               'require_login', 'member_search_results'] 
                        redirectable = True
                        for not_redirectable_url in not_redirectable_urls:
                            if not_redirectable_url in self.REQUEST.get('URL'):
                                redirectable = False
                                
                        if redirectable:
                            self.REQUEST.SESSION.set('eid_logged_in_executed', 1)                                
                            self.REQUEST.RESPONSE.redirect(portal.portal_properties.site_properties.getProperty('https_address') + '?came_from=%s' % self.REQUEST.get('URL'))
                    
                    self.REQUEST.SESSION.set('eid_username', user_name)
                    return user_name, user_name                    
                
                #we will return None if the user has not be found in the database
                return None
        else:
            #if credentials is not None, it means that extractCredentials returned something without the 'eid_from_http' key, it should not happen...
            print "return None"
            return None


    security.declarePrivate('extractCredentials')
    def extractCredentials(self, request):
        """ 
            Extract eid userinfo from request 
            These informations will be used by authenticateCredentials as it receive them as parameter
        """
        #if the user try to connect using his eID card and that the getClientData has returned the 'eid_nr'
        #we could suppose that we have eid_from_http but not 'eid_nr' altought it should not happen...
        
        creds = {}
        #we know that we have already extracted the credentials only if :
        #--> 'eid_from_http' is set in SESSION --> we have already encountered the HTTPS support
        #--> 'eid_nr' is set in SESSION --> we have successfully extracted nr from 'HTTP_SSL_CLIENT_S_DN' with the getClientData method
        #--> 'HTTP_SSL_CLIENT_S_DN' is in the REQUEST --> Apache still send the SSL var
        #--> 'HTTP_SSL_CLIENT_S_DN' in REQUEST is equal to 'eid_http_ssl_client_s_dn' in SESSION wich means that the user as not changed
        
        if request.SESSION.has_key('eid_from_http') and request.get('HTTP_SSL_CLIENT_S_DN') and request.get('HTTP_SSL_CLIENT_S_DN') == request.SESSION.get('eid_http_ssl_client_s_dn'):
                #we still check if 'HTTP_SSL_CLIENT_S_DN' is in the REQUEST because Apache could remove it
                #we already parsed 'HTTP_SSL_CLIENT_S_DN', we use 'eid_nr' stored in SESSION object
                #as we just manage cached vars in SESSION, we do not need delete 'eid_username' from SESSION
                creds.update({'eid_nr':request.SESSION.get('eid_nr'),
                            'eid_from_http':1,
                            'eid_http_ssl_client_s_dn': request.get('HTTP_SSL_CLIENT_S_DN')})
                return creds
        else:
            #we play with 'HTTP_SSL_CLIENT_S_DN'
            from_http = request.get('HTTP_SSL_CLIENT_S_DN')
            if from_http:
                #we search the national register number in the request send from Apache
                nr = self.getClientData(from_http)
                if nr:
                    creds.update({'eid_nr':nr,
                                  'eid_from_http':1,
                                  'eid_http_ssl_client_s_dn': from_http
                                })
                    request.SESSION.set('eid_nr', creds['eid_nr'])
                    request.SESSION.set('eid_from_http', creds['eid_from_http'])
                    #we save the 'HTTP_SSL_CLIENT_S_DN' in the SESSION to see if it is always the same send by Apache
                    request.SESSION.set('eid_http_ssl_client_s_dn', creds['eid_http_ssl_client_s_dn'])
                    #we try to remove 'eid_username' from SESSION to force AuthenticateCredentials to do the authentication again if it had already been done
                    try:
                        del request.SESSION['eid_username']
                    except KeyError:
                        pass
                    return creds
                else:
                    creds.update({'eid_from_http':0})
            else:
                creds.update({'eid_from_http':0})
                    
        #If we can not get this from the REQUEST, we are not in a correctly configured HTTPS mode
        #we remove the keys from SESSION !!!
        #--> 'eid_from_http' in creds == 0 if from_hhtp is None or if nr returned by getClientData is None
        
        #XXX performance problem at trying to delete the keys from SESSION when not using eID card???  The plugin will always do this try/catch...
        if creds['eid_from_http'] == 0:
            try:
                del request.SESSION['eid_nr']
                del request.SESSION['eid_from_http']
                del request.SESSION['eid_http_ssl_client_s_dn']
                del request.SESSION['eid_username']
            except KeyError:
                #if 'eid_nr' or 'eid_from_hhtp' or 'eid_http_ssl_client_s_dn' or 'eid_username' does not exist in SESSION, we pass, they already have been deleted
                pass
        
        return None
        

    security.declarePrivate('getClientData')
    def getClientData(self, from_http):
        """ 
        We receive a String, we need to parse it to return the name, first_name and nr (national register number)
        """
        #there can be UTF/ISO encoding problems with OpenSSL/Apache, so we do what we have to to correct this
        #UTF-8 codes are not passed as codes but as string
        #"é" should be '\xc3\xa9' but it is returned as '\\xc3\\xa9'
        nr = None
        
        try:
            #we need to correct the string if we wish to retrieve CN/SN/GN datas from fro_http
            #corrected_string = eval("u'" + from_http + "'")
            #corrected_string = corrected_string.encode('latin1')
            #corrected_string = unicode(corrected_string, 'utf-8')
            #datas = corrected_string.split('/')
            
            datas = from_http.split('/')
            #search for SN, GN and serialNumber
            for data in datas:
                if data[:12] == "serialNumber":
                    nr = data[13:]
            #a belgian national register number is 11 digits long
            if len(nr) != 11:
                nr = None

        except:
            #if we encoutered an error doing this, we have to stop here
            #we should not have errors here, so we LOG
            LOG("BelgianEidAuthPlugin :", PROBLEM, "Failed to extract datas from from_http in getClientData(self, from_http).")
            return None
        
        return nr


    security.declarePrivate('getUserNameFromNR')
    def getUserNameFromNR(self, nr):
        """
            Lookup the user in the User Manager with is National Register
        """
        for user in self.acl_users.getUsers():
            props = self.acl_users.mutable_properties.getPropertiesForUser(user)._properties
            
            #the property 'nationalregister' could not exist, so we try and catch
            try:
                if props['nationalregister'] == nr:
                    return user.getId()
            except KeyError:
                pass
        
        return None


classImplements(BelgianEidAuthPlugin, IAuthenticationPlugin, IExtractionPlugin)

InitializeClass(BelgianEidAuthPlugin)