'''
Created on Mar 16, 2013

@author: ajju
'''
from common import HttpUtils, AddonUtils
from common.DataObjects import ListItem
import xbmcgui  # @UnresolvedImport
from datetime import datetime
import re
import time
import urllib
import calendar
try:
    import json
except ImportError:
    import simplejson as json
    
YU_URL = 'http://ytwidget.willow.tv/ytui.html'

def displaySeries(request_obj, response_obj):
    html = HttpUtils.HttpClient().getHtmlContent(YU_URL)
    seriesDetail = re.compile('WLSeriesDetailsObj = \[(.+?)\];').findall(html)[0]
    seriesDetail = ('[' + urllib.unquote(seriesDetail).decode('utf8') + ']').replace('\t', '').replace('\n', '').replace('\r', '')
    seriesDetailJObj = json.loads(seriesDetail)
    tabType = None
    
    items = []
    for series in seriesDetailJObj:
        name = series['Name']
        start_date_obj = datetime(*(time.strptime(series['StartDate'].replace(' 0:00', ''), "%d %b %Y")[0:6])).date()
        end_date_obj = datetime(*(time.strptime(series['EndDate'].replace(' 0:00', ''), "%d %b %Y")[0:6])).date()
        schedule = start_date_obj.strftime('%b %d %Y') + ' -to- ' + end_date_obj.strftime('%b %d %Y')
        
        if tabType != 'UPCOMING' and series['SeriesShouldRenderInUpcomingTab'] == "1":
            tabType = 'UPCOMING'
            item = ListItem()
            item.set_next_action_name('Nothing')
            xbmcListItem = xbmcgui.ListItem(label='[B][COLOR blue]Upcoming/Ongoing Series[/COLOR][/B]', iconImage='', thumbnailImage='')
            item.set_xbmc_list_item_obj(xbmcListItem)
            items.append(item)
        elif tabType != 'ARCHIVE' and series['SeriesShouldRenderInArchiveTab'] == "1":
            tabType = 'ARCHIVE'
            item = ListItem()
            item.set_next_action_name('Nothing')
            xbmcListItem = xbmcgui.ListItem(label='[B][COLOR orange]Archive Series[/COLOR][/B]', iconImage='', thumbnailImage='')
            item.set_xbmc_list_item_obj(xbmcListItem)
            items.append(item)
            
        item = ListItem()
        item.add_request_data('series', series)
        item.set_next_action_name('Matches')
        xbmcListItem = xbmcgui.ListItem(label=(schedule + ' :: [B]' + name + '[/B]'), label2=schedule, iconImage='', thumbnailImage='')
        item.set_xbmc_list_item_obj(xbmcListItem)
        items.append(item)
    response_obj.set_item_list(items)


def displayMatches(request_obj, response_obj):
    series = request_obj.get_data()['series']
    if not series.has_key('MatchDetails'):
        tabType = None
        regex = None
        if series['SeriesShouldRenderInUpcomingTab'] == "1":
            tabType = 'Upcoming'
            regex = 'HandleWLSeriesDetailsWSForUpcomingTab\((.+?)\);'
        
        elif series['SeriesShouldRenderInArchiveTab'] == "1":
            tabType = 'Archive'
            regex = 'HandleWLSeriesDetailsWSForArchiveTab\((.+?)\);'
        
        url = 'http://www.willow.tv/EventMgmt/webservices/FetchJSONDataForYTUI.asp?SeriesId=' + series['Id'] + '&TabType=' + tabType
        html = HttpUtils.HttpClient().getHtmlContent(url)        
        thisSeriesDetail = re.compile(regex).findall(html)[0]
        thisSeriesDetail = (urllib.unquote(thisSeriesDetail).decode('utf8')).replace('\t', '').replace('\n', '').replace('\r', '')
        series = json.loads(thisSeriesDetail)
    
    items = []
    for match in series['MatchDetails']:
        time_obj = time.strptime(match['StartDate'] + ' GMT', "%d %b %Y %H:%M %Z")
        startDate = time.strftime('%a, %d %b %Y %I:%M %p', time.localtime(calendar.timegm(time_obj)))
        name = ''
        if match['IsMatchLive'] == '1':
            name = '[B][COLOR red]LIVE[/COLOR][/B] '
        name = name + match['Name']
        
        item = ListItem()
        item.add_request_data('match', match)
        item.set_next_action_name('Match_Urls')
        xbmcListItem = xbmcgui.ListItem(label=(startDate + ' :: [B]' + name + '[/B]'), label2=startDate, iconImage='', thumbnailImage='')
        item.set_xbmc_list_item_obj(xbmcListItem)
        items.append(item)
        
    response_obj.set_item_list(items)
                

def displayMatchUrls(request_obj, response_obj):
    match = request_obj.get_data()['match']
    items = []
    for urlDetail in match['UrlDetails']:
        videoId = urlDetail['VideoId']
        if videoId != 'NA':
            name = '[B]' + urlDetail['Type'] + '[/B] : ' + urlDetail['VideoName']
            imageUrl = urlDetail['Thumbnail']
            videoUrl = None
            if videoId.startswith('PL'):
                videoUrl = 'www.youtube.com/playlist?list=' + urlDetail['VideoId'] + '&'
            else:
                videoUrl = 'www.youtube.com/watch?v=' + urlDetail['VideoId'] + '&'
            
            item = ListItem()
            item.add_request_data('videoLink', videoUrl)
            item.add_request_data('videoTitle', urlDetail['VideoName'])
            item.set_next_action_name('Play_URL')
            xbmcListItem = xbmcgui.ListItem(label=name, iconImage=imageUrl, thumbnailImage=imageUrl)
            item.set_xbmc_list_item_obj(xbmcListItem)
            items.append(item)
    response_obj.set_item_list(items)
    

def displayNothing(request_obj, response_obj):
    # Do Nothing
    return
