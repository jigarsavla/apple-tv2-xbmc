'''
Created on Oct 29, 2011

@author: ajju
'''
from common import HttpUtils, Logger
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD, \
    VIDEO_QUAL_HD_720, VIDEO_QUAL_HD_1080, VIDEO_QUAL_LOW
import re
import urllib
try:
    import json
except ImportError:
    import simplejson as json

VIDEO_HOSTING_NAME = 'Dailymotion'
def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://press.dailymotion.com/fr/wp-content/uploads/logo-Dailymotion.png')
    video_hosting_info.set_video_hosting_name(VIDEO_HOSTING_NAME)
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_link = 'http://www.dailymotion.com/video/' + str(video_id)
        html = HttpUtils.HttpClient().getHtmlContent(url=video_link)
        HttpUtils.HttpClient().disableCookies()
        sequence = re.compile('"sequence":"(.+?)"').findall(html)
        if(len(sequence) == 0):
            sequence = re.compile('"sequence",  "(.+?)"').findall(html)
            newseqeunce = urllib.unquote(sequence[0]).decode('utf8').replace('\\/', '/')
            imgSrc = re.compile('og:image" content="(.+?)"').findall(html)
            if(len(imgSrc) == 0):
                imgSrc = re.compile('/jpeg" href="(.+?)"').findall(html)
            dm_low = re.compile('"sdURL":"(.+?)"').findall(newseqeunce)
            dm_high = re.compile('"hqURL":"(.+?)"').findall(newseqeunce)
            
            video_info.set_video_image(imgSrc[0])
            video_info.set_video_stopped(False)
            
            if(len(dm_high) == 0 and len(dm_low) == 1):
                video_info.add_video_link(VIDEO_QUAL_SD, dm_low[0])
            elif(len(dm_low) == 0 and len(dm_high) == 1):
                video_info.add_video_link(VIDEO_QUAL_HD_720, dm_high[0])
            else:
                video_info.add_video_link(VIDEO_QUAL_SD, dm_low[0])
                video_info.add_video_link(VIDEO_QUAL_HD_720, dm_high[0])
        else:
            
            newseqeunce = urllib.unquote(sequence[0]).decode('utf8').replace('\\/', '/')
            
            jObj = json.loads(newseqeunce)
            for sequenceItem in jObj['sequence'][0]['layerList'][0]['sequenceList']:
                if sequenceItem['name'] == 'main' or sequenceItem['name'] == 'reporting':
                    for layerItem in sequenceItem['layerList']:
                        if layerItem['name'] == 'reporting' and layerItem['type'] == 'Reporting':
                            video_info.set_video_name((layerItem['param']['extraParams']['videoTitle']).replace('+', ' '))
                        elif layerItem['name'] == 'video' and layerItem['type'] == 'VideoFrame':
                            params = layerItem['param']
                            if not params.has_key('sdURL') and not params.has_key('hqURL'):
                                autoURL = params['autoURL']
                                videoData = HttpUtils.HttpClient().getHtmlContent(url=autoURL)
                                jVideoData = json.loads(videoData)
                                dm_SD = None
                                dm_720 = None
                                dm_1080 = None
                                for alternate in jVideoData['alternates']:
                                    if alternate['name'] == '380' and dm_SD == None:
                                        dm_SD = alternate['template'].replace('mnft', 'mp4')
                                    elif alternate['name'] == '480':
                                        dm_SD = alternate['template'].replace('mnft', 'mp4')
                                    elif alternate['name'] == '720':
                                        dm_720 = alternate['template'].replace('mnft', 'mp4')
                                    elif alternate['name'] == '1080':
                                        dm_1080 = alternate['template'].replace('mnft', 'mp4')
                                
                                if dm_SD is not None:
                                    video_info.add_video_link(VIDEO_QUAL_SD, dm_SD, addReferer=True, refererUrl=video_link)
                                if dm_720 is not None:
                                    video_info.add_video_link(VIDEO_QUAL_HD_720, dm_720, addReferer=True, refererUrl=video_link)
                                if dm_1080 is not None:
                                    video_info.add_video_link(VIDEO_QUAL_HD_1080, dm_1080, addReferer=True, refererUrl=video_link)
                                video_info.set_video_stopped(False)
                            else:
                                if params.has_key('IdURL'):
                                    video_info.add_video_link(VIDEO_QUAL_LOW, params['IdURL'])
                                if params.has_key('sdURL'):
                                    video_info.add_video_link(VIDEO_QUAL_SD, params['sdURL'])
                                if params.has_key('hqURL'):
                                    video_info.add_video_link(VIDEO_QUAL_SD, params['hqURL'])
                                if params.has_key('hd720URL'):
                                    video_info.add_video_link(VIDEO_QUAL_HD_720, params['hd720URL'])
                                video_info.set_video_stopped(False)
                        elif layerItem['name'] == 'relatedBackground' and layerItem['type'] == 'Background':
                            params = layerItem['param']
                            video_info.set_video_image(params['imageURL'])
    except Exception, e:
        Logger.logError(e)
        video_info.set_video_stopped(True)
    return video_info


def retrievePlaylistVideoItems(playlistId):
    html = HttpUtils.HttpClient().getHtmlContent(url='https://api.dailymotion.com/playlist/' + playlistId + '/videos')
    playlistJsonObj = json.loads(html)
    videoItemsList = []
    for video in playlistJsonObj['list']:
        videoItemsList.append('http://www.dailymotion.com/video/' + str(video['id']))
    return videoItemsList

