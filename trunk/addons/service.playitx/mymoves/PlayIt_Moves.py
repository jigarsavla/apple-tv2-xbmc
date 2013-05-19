'''
Created on Dec 27, 2011

@author: ajju
'''
from TurtleContainer import Container
from common import XBMCInterfaceUtils, Logger, HttpUtils
from common.DataObjects import ListItem
from moves import SnapVideo
from urllib2 import HTTPError
import re
import xbmcgui # @UnresolvedImport

def ping(request_obj, response_obj):
    print request_obj.get_data()
    response_obj.addServiceResponseParam("response", "pong")
    response_obj.addServiceResponseParam("message", "Hi there, I am PlayIt")

    item = ListItem()
    item.set_next_action_name('pong')
    response_obj.addListItem(item)
    

def playHostedVideo(request_obj, response_obj):
    pbType = int(Container().getAddonContext().addon.getSetting('playbacktype'))
    if pbType == 2 and XBMCInterfaceUtils.isPlayingVideo():
        response_obj.addServiceResponseParam("status", "error")
        response_obj.addServiceResponseParam("message", "XBMC is already playing a video. Your this request is ignored.")
        item = ListItem()
        item.set_next_action_name('respond')
        response_obj.addListItem(item)
    else:
        if pbType == 0:
            XBMCInterfaceUtils.stopPlayer()
            
        video_url = request_obj.get_data()['videoLink']
        if video_url.startswith('http://goo.gl/'):
            Logger.logDebug('Found google short URL = ' + video_url)
            video_url = HttpUtils.getRedirectedUrl(video_url)
            Logger.logDebug('After finding out redirected URL = ' + video_url)
            request_obj.get_data()['videoLink'] = video_url
        try:
            if __check_media_url(video_url):
                response_obj.set_redirect_action_name('play_direct')
            else:
                video_hosting_info = SnapVideo.findVideoHostingInfo(video_url)
                if video_hosting_info is None:
                    response_obj.addServiceResponseParam("status", "error")
                    response_obj.addServiceResponseParam("message", "Video URL is currently not supported by PlayIt")
                    item = ListItem()
                    item.set_next_action_name('respond')
                    response_obj.addListItem(item)
                else:
                    response_obj.addServiceResponseParam("status", "success")
                    if not XBMCInterfaceUtils.isPlayingVideo():
                        response_obj.addServiceResponseParam("message", "Enjoy your video!")
                    else:
                        response_obj.addServiceResponseParam("message", "Your video has been added to player queue.")
                    response_obj.set_redirect_action_name('play_it')
                    request_obj.get_data()['videoTitle'] = 'PlayIt Video'
        except HTTPError:
            response_obj.addServiceResponseParam("status", "error")
            response_obj.addServiceResponseParam("message", "Video URL is not valid one! Please check and try again.")
            item = ListItem()
            item.set_next_action_name('respond')
            response_obj.addListItem(item)
        
    
def playRawVideo(request_obj, response_obj):
    video_url = request_obj.get_data()['videoLink']
    
    item = ListItem()
    item.get_moving_data()['videoStreamUrl'] = video_url
    item.set_next_action_name('Play')
    xbmcListItem = xbmcgui.ListItem(label='Streaming Video')
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    response_obj.addServiceResponseParam("status", "success")
    response_obj.addServiceResponseParam("message", "Enjoy the video!")
    
    
def playZappyVideo(request_obj, response_obj):
    Logger.logDebug(request_obj.get_data());
    
    video_id = request_obj.get_data()['videoId']
    port = request_obj.get_data()['port']
    ipaddress = request_obj.get_data()['client_ip']
    video_url = "http://" + ipaddress + ":" + str(port) + "/?videoId=" + video_id
    item = ListItem()
    item.get_moving_data()['videoStreamUrl'] = video_url
    item.set_next_action_name('Play')
    xbmcListItem = xbmcgui.ListItem(label='Streaming Video')
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    response_obj.addServiceResponseParam("status", "success")
    response_obj.addServiceResponseParam("message", "Enjoy the video!")


APPLICATION_MEDIA_TYPES = ['application/octet-stream', 'application/x-mpegURL', 'application/ogg']
def __check_media_url(video_url):
    import urllib2
    request = urllib2.Request(video_url)
    request.get_method = lambda : 'HEAD'
    response = urllib2.urlopen(request)
    content_type = response.info().gettype()
    try:
        return (APPLICATION_MEDIA_TYPES.index(content_type) >= 0)
    except ValueError:
        return re.search('[video|audio]/', content_type)
    
        
