'''
Created on Oct 29, 2011

@author: ajju
'''
from common import HttpUtils, XBMCInterfaceUtils, Logger
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_LOW, \
    VIDEO_QUAL_SD, VIDEO_QUAL_HD_720, VIDEO_QUAL_HD_1080
import re
import urllib

VIDEO_HOSTING_NAME = 'YouTube'
def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://www.automotivefinancingsystems.com/images/icons/socialmedia_youtube_256x256.png')
    video_hosting_info.set_video_hosting_name(VIDEO_HOSTING_NAME)
    return video_hosting_info

def retrieveVideoInfo(video_id):
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        
        HttpUtils.HttpClient().enableCookies()
        video_info.set_video_image('http://i.ytimg.com/vi/' + video_id + '/default.jpg')
        html = HttpUtils.HttpClient().getHtmlContent(url='http://www.youtube.com/get_video_info?video_id=' + video_id + '&asv=3&el=detailpage&hl=en_US')
        stream_map = None
        
        html = html.decode('utf8')
        html = html.replace('\n', '')
        html = html.replace('\r', '')
        html = unicode(html + '&').encode('utf-8')
        if re.search('status=fail', html):
            XBMCInterfaceUtils.displayDialogMessage('Video info retrieval failed', 'Reason: ' + ((re.compile('reason\=(.+?)\.').findall(html))[0]).replace('+', ' ') + '.')
            video_info.set_video_stopped(True)
            return video_info
        
        Logger.logDebug(html)
        title = urllib.unquote_plus(re.compile('title=(.+?)&').findall(html)[0]).replace('/\+/g', ' ')
        video_info.set_video_name(title)
        stream_info = None
        if not re.search('url_encoded_fmt_stream_map=&', html):
            stream_info = re.compile('url_encoded_fmt_stream_map=(.+?)&').findall(html)
        stream_map = None
        if (stream_info is None or len(stream_info) == 0) and re.search('fmt_stream_map": "', html):
            stream_map = re.compile('fmt_stream_map": "(.+?)"').findall(html)[0].replace("\\/", "/")
        elif stream_info is not None:
            stream_map = stream_info[0]
            
        if stream_map is None:
            params = HttpUtils.getUrlParams(html)
            Logger.logDebug('ENTERING live video scenario...')
            for key in params:
                Logger.logDebug(key + " : " + urllib.unquote_plus(params[key]))
            hlsvp = urllib.unquote_plus(params['hlsvp'])
            playlistItems = HttpUtils.HttpClient().getHtmlContent(url=hlsvp).splitlines()
            qualityIdentified = None
            for item in playlistItems:
                Logger.logDebug(item)
                if item.startswith('#EXT-X-STREAM-INF'):
                    if item.endswith('1280x720'):
                        qualityIdentified = VIDEO_QUAL_HD_720
                    elif item.endswith('1080'):
                        qualityIdentified = VIDEO_QUAL_HD_1080
                    elif item.endswith('854x480'):
                        qualityIdentified = VIDEO_QUAL_SD
                    elif item.endswith('640x360'):
                        qualityIdentified = VIDEO_QUAL_LOW
                elif item.startswith('http') and qualityIdentified is not None:
                    videoUrl = HttpUtils.HttpClient().addHttpCookiesToUrl(item, extraExtraHeaders={'Referer':'https://www.youtube.com/watch?v=' + video_id})
                    video_info.add_video_link(qualityIdentified, videoUrl)
                    qualityIdentified = None
            video_info.set_video_stopped(False)
            return video_info
        
        stream_map = urllib.unquote_plus(stream_map)

        
        formatArray = stream_map.split(',')
        for formatContent in formatArray:
            if formatContent == '':
                continue
            formatUrl = ''
            try:
                formatUrl = urllib.unquote(re.compile("url=([^&]+)").findall(formatContent)[0]) + "&title=" + urllib.quote_plus(title)   
            except Exception, e:
                Logger.logFatal(e)     
            if re.search("rtmpe", stream_map):
                try:
                    conn = urllib.unquote(re.compile("conn=([^&]+)").findall(formatContent)[0]);
                    host = re.compile("rtmpe:\/\/([^\/]+)").findall(conn)[0];
                    stream = re.compile("stream=([^&]+)").findall(formatContent)[0];
                    path = 'videoplayback';
                    
                    formatUrl = "-r %22rtmpe:\/\/" + host + "\/" + path + "%22 -V -a %22" + path + "%22 -f %22WIN 11,3,300,268%22 -W %22http:\/\/s.ytimg.com\/yt\/swfbin\/watch_as3-vfl7aCF1A.swf%22 -p %22http:\/\/www.youtube.com\/watch?v=" + video_id + "%22 -y %22" + urllib.unquote(stream) + "%22"
                except Exception, e:
                    Logger.logFatal(e)
            if formatUrl == '':
                continue
            if(formatUrl[0: 4] == "http" or formatUrl[0: 2] == "-r"):
                formatQual = re.compile("itag=([^&]+)").findall(formatContent)[0]
                if not re.search("signature=", formatUrl):
                    formatUrl += "&signature=" + re.compile("sig=([^&]+)").findall(formatContent)[0]
        
            qual = formatQual
            url = HttpUtils.HttpClient().addHttpCookiesToUrl(formatUrl, extraExtraHeaders={'Referer':'https://www.youtube.com/watch?v=' + video_id})
            Logger.logDebug('quality ---> ' + qual)
            if(qual == '52' or qual == '60'):  # Incorrect stream should be skipped. Causes Svere Crash
                XBMCInterfaceUtils.displayDialogMessage('XBMC Unsupported codec skipped', 'YouTube has started new stream is currently cannot be decoded by XBMC player, causes crash.', 'Skipped this video quality.')
                continue
            if(qual == '13' and video_info.get_video_link(VIDEO_QUAL_LOW) is None):  # 176x144
                video_info.add_video_link(VIDEO_QUAL_LOW, url)
            elif(qual == '5' and video_info.get_video_link(VIDEO_QUAL_LOW) is None):  # 400\\327226 AUDIO ONLY
                video_info.add_video_link(VIDEO_QUAL_LOW, url)
            elif(qual == '6' and video_info.get_video_link(VIDEO_QUAL_LOW) is None):  # 640\\327360 AUDIO ONLY
                video_info.add_video_link(VIDEO_QUAL_LOW, url)
            elif(qual == '17'):  # 176x144
                video_info.add_video_link(VIDEO_QUAL_LOW, url)
            elif(qual == '18'):  # 270p/360p MP4
                video_info.add_video_link(VIDEO_QUAL_LOW, url)
            elif(qual == '22'):  # 1280x720 MP4
                video_info.add_video_link(VIDEO_QUAL_HD_720, url)
            elif(qual == '34'):  # 480x360 FLV
                video_info.add_video_link(VIDEO_QUAL_SD, url)
            elif(qual == '35' and video_info.get_video_link(VIDEO_QUAL_SD) is None):  # 854\\327480 SD
                video_info.add_video_link(VIDEO_QUAL_SD, url)
            elif(qual == '36' and video_info.get_video_link(VIDEO_QUAL_LOW) is None):  # 320x240
                video_info.add_video_link(VIDEO_QUAL_LOW, url)
            elif(qual == '37'):  # 1920x1080 MP4
                video_info.add_video_link(VIDEO_QUAL_HD_1080, url)
            elif(qual == '38' and video_info.get_video_link(VIDEO_QUAL_HD_1080) is None):  # 4096\\3272304 EPIC MP4
                video_info.add_video_link(VIDEO_QUAL_HD_1080, url)
            elif(qual == '43' and video_info.get_video_link(VIDEO_QUAL_LOW) is None):  # 360 WEBM
                video_info.add_video_link(VIDEO_QUAL_LOW, url)
            elif(qual == '44' and video_info.get_video_link(VIDEO_QUAL_SD) is None):  # 480 WEBM
                video_info.add_video_link(VIDEO_QUAL_SD, url)
            elif(qual == '45' and video_info.get_video_link(VIDEO_QUAL_HD_720) is None):  # 720 WEBM
                video_info.add_video_link(VIDEO_QUAL_HD_720, url)
            elif(qual == '46' and video_info.get_video_link(VIDEO_QUAL_HD_1080) is None):  # 1080 WEBM
                video_info.add_video_link(VIDEO_QUAL_HD_1080, url)
            elif(qual == '120'):  # New video qual
                video_info.add_video_link(VIDEO_QUAL_HD_720, url)
                # 3D streams - MP4
                # 240p -> 83
                # 360p -> 82
                # 520p -> 85
                # 720p -> 84
                # 3D streams - WebM
                # 360p -> 100
                # 360p -> 101
                # 720p -> 102
            elif video_info.get_video_link(VIDEO_QUAL_LOW) is None:  # unknown quality
                video_info.add_video_link(VIDEO_QUAL_LOW, url)

            video_info.set_video_stopped(False)
    except Exception, e:
        Logger.logError(e)
        video_info.set_video_stopped(True)
    return video_info


def retrievePlaylistVideoItems(playlistId):
    Logger.logFatal('YouTube Playlist ID = ' + playlistId)
    soupXml = HttpUtils.HttpClient().getBeautifulSoup('http://gdata.youtube.com/feeds/api/playlists/' + playlistId)
    videoItemsList = []
    for media in soupXml.findChildren('media:player'):
        videoUrl = str(media['url'])
        videoItemsList.append(videoUrl)
    return videoItemsList
    
def retrieveReloadedPlaylistVideoItems(playlistId):
    Logger.logFatal('YouTube Reloaded Playlist ID = ' + playlistId)
    soupXml = HttpUtils.HttpClient().getBeautifulSoup('http://gdata.youtube.com/feeds/api/playlists/' + playlistId)
    videoItemsList = []
    for media in soupXml.findChildren('track'):
        videoUrl = media.findChild('location').getText()
        videoItemsList.append(videoUrl)
    return videoItemsList
    
