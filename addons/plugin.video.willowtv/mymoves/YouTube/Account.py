from TurtleContainer import AddonContext
from common import AddonUtils, HttpUtils, XBMCInterfaceUtils
import time
import re
import xbmcgui, xbmc  # @UnresolvedImport
import sys
import cookielib
import mechanize
from mechanize import ParseResponse


LOGIN_URL = 'https://accounts.google.com/ServiceLogin?service=youtube&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26feature%3Dsign_in_button%26hl%3Den_US%26next%3D%252F%26nomobiletemp%3D1&hl=en_US&uilel=3&passive=true'
COOKIES_FILENAME = 'YTCookieStore'

def login(request_obj, response_obj):
    cookieStore = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonProfile, extraDirPath=AddonUtils.ADDON_SRC_DATA_FOLDER, filename=COOKIES_FILENAME, makeDirs=True)
     
    success = True
    relogin = AddonContext().addon.getSetting('relogin') == 'true'
    if not relogin:
        relogin = __checkAndLoadCookieStore__(cookieStore)
    if relogin:
        success = __loginAndSaveCookieStore__(cookieStore)
 
    if ((not request_obj.get_params().has_key('data')) or request_obj.get_params()['data'] == ''):
        request_obj.set_data({})
    if success:
        request_obj.get_data()['isLoginSuccess'] = True
    else:
        request_obj.get_data()['isLoginSuccess'] = False
    AddonContext().addon.setSetting('relogin', 'false')
    
    
def __checkAndLoadCookieStore__(cookieStore):
    relogin = False
    if AddonUtils.doesFileExist(cookieStore):
        HttpUtils.HttpClient().loadCookiesFromFile(cookieStore)
        HttpUtils.HttpClient().enableCookies()
        now = time.time()
        for cookie in HttpUtils.HttpClient().get_cookiejar():
            if cookie.is_expired(now):
                relogin = True
    else:
        relogin = True
    return relogin
        
    
def __loginAndSaveCookieStore__(cookieStore):
    AddonUtils.deleteFile(cookieStore)
    email = AddonContext().addon.getSetting('yt_email')
    password = AddonContext().addon.getSetting('yt_password')
    if email == None or email == '' or password == None or password == '':
        d = xbmcgui.Dialog()
        d.ok('Welcome to Willow TV', 'Watch LIVE CRICKET on your favorite Willow TV.', 'Please provide your login details for YouTube Account.')
        AddonContext().addon.openSettings(sys.argv[ 0 ])
        return False
    successInd = __loginYouTube__(LOGIN_URL, email, password)
    if successInd:
        HttpUtils.HttpClient().saveCookiesToFile(cookieStore)
    else:
        raise Exception(ExceptionHandler.DONOT_DISPLAY_ERROR);
    return successInd
    

def __loginYouTube__(url, email, pwd):
    try:
        if (not email or email == '') or (not pwd or pwd == ''):
            d = xbmcgui.Dialog()
            d.ok('Provide YouTube account details', 'To watch LIVE CRICKET on your favorite Willow TV,', 'please provide your login details for YouTube account linked to Willow TV.')
            AddonContext().addon.openSettings(sys.argv[ 0 ])
            return False
        
        HttpUtils.HttpClient().enableCookies()
        response = HttpUtils.HttpClient().getResponse(url)
        br = mechanize.Browser(factory=mechanize.RobustFactory())
        br.set_response(response)
        forms = list(br.forms())
        response.close()
        form = forms[0]
        form['Passwd'] = pwd
        form['Email'] = email
        req = form.click()
        response = HttpUtils.HttpClient().getResponseForRequest(req)
        br = mechanize.Browser(factory=mechanize.RobustFactory())
        br.set_response(response)
        br.select_form("verifyForm")
        if br.find_control("smsUserPin"):
            forms = list(br.forms())
            form = forms[0]
            keyb = xbmc.Keyboard()
            keyb.setHeading('Please provide 2-step verification PIN:')
            keyb.doModal()
            code = None
            if (keyb.isConfirmed()):
                    code = keyb.getText()
            if code is None:
                    d = xbmcgui.Dialog()
                    d.ok('YouTube login failed', 'Cannot proceed without verification code.', 'Process has been cancelled by user.')
                    return None
            form["smsUserPin"] = code
            req = form.click()
            response = HttpUtils.HttpClient().getResponseForRequest(req)
            forms = ParseResponse(response, backwards_compat=False)
            response.close()
            form = forms[0]
            req = form.click()
            response = HttpUtils.HttpClient().getResponseForRequest(req)
            web = response.read()
            print web
        while re.search('<title>Redirecting</title>', web):
            
            redirect_re = re.compile('<meta http-equiv="refresh" content="0; url=\&\#39;(.+?)\&\#39;"')
            # check for redirect meta tag
            match = redirect_re.search(web)
            if match:
                    url = redirect_re.findall(web)[0].replace('&amp;', '&')
            else:
                    url = None
                    break
            response = HttpUtils.HttpClient().getResponse(url)
            web = response.read()
            print web
            response.close()
        return True
    except Exception,e:
        raise
        print e
        d = xbmcgui.Dialog()
        d.ok('YouTube login failed', 'Please opt for 2-step authentication method of google', 'You should check if you have provided correct username and password')
        return False

