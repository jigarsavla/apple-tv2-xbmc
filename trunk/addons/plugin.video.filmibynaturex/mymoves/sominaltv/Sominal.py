'''
Created on Nov 20, 2012

@author: ajju
'''
from TurtleContainer import Container
from common.DataObjects import ListItem
import xbmcgui  # @UnresolvedImport
from common import AddonUtils, Logger, EnkDekoder
import base64
import re
import sys
import BeautifulSoup
from moves import SnapVideo
from snapvideo import Dailymotion, YouTube, GoogleDocs
from common import XBMCInterfaceUtils
try:
    import json
except ImportError:
    import simplejson as json
from common import HttpUtils


PREFERRED_DIRECT_PLAY_ORDER = [GoogleDocs.VIDEO_HOSTING_NAME, Dailymotion.VIDEO_HOSTING_NAME, YouTube.VIDEO_HOSTING_NAME]
BASE_WSITE_URL = base64.b64decode('aHR0cDovL3d3dy5zb21pbmFsdHZmaWxtcy5jb20v')
pageDict = {0:25, 1:50, 2:100}
TITLES_PER_PAGE = pageDict[int(Container().getAddonContext().addon.getSetting('moviesPerPage'))]



def listMovies(request_obj, response_obj):
    categoryUrlSuffix = request_obj.get_data()['categoryUrlSuffix']
    page = None
    if request_obj.get_data().has_key('page'):
        page = int(request_obj.get_data()['page'])
    
    titles = Container().getAddonContext().cache.cacheFunction(retrieveMovies, categoryUrlSuffix)
    
    count = -1
    start = 0
    current_page = -1
    total_pages = -1
    if len(titles) > TITLES_PER_PAGE:
        count = 0
        current_page = 1
        total_pages = int(len(titles) / TITLES_PER_PAGE)
        if len(titles) % TITLES_PER_PAGE:
            total_pages = total_pages + 1
        if page is not None:
            current_page = int(page)
            start = (current_page - 1) * TITLES_PER_PAGE
    end = start + TITLES_PER_PAGE
    items = []
    for entry in titles:
        if count > -1:
            if count < start:
                count = count + 1
                continue
            elif count >= end:
                break
            else:
                count = count + 1
        titleInfo = entry['info']
        
        if re.compile('Hindi Dubbed').findall(titleInfo) is not None:
            titleInfo = titleInfo.replace('(Hindi Dubbed)', '').replace('Hindi Dubbed', '')
        
        movieInfo = re.compile("(.+?)\((\d+)\) (.*)").findall(titleInfo)
        if(len(movieInfo) == 0):
            movieInfo = re.compile("(.+?)\((\d+)\)").findall(titleInfo)
        if(len(movieInfo) == 0):
            movieInfo = [[titleInfo]]
        title = unicode(movieInfo[0][0].rstrip()).encode('utf-8')
        year = ''
        if(len(movieInfo[0]) >= 2):
            year = unicode(movieInfo[0][1]).encode('utf-8')
        quality = ''
        if categoryUrlSuffix != 'BluRay':
            if(len(movieInfo[0]) >= 3):
                quality = unicode(movieInfo[0][2]).encode('utf-8').strip()
                if quality == '*BluRay*' or quality == '*BluRay* (Hindi Dubbed)' or quality == '*BluRay* Hindi Dubbed':
                    quality = '[COLOR red]*HD*[/COLOR]'
                elif quality == 'DVD' or quality == 'DVD (Hindi Dubbed)' or quality == 'DVD Hindi Dubbed':
                    quality = '[COLOR orange]DVD[/COLOR]'
                quality = ' :: ' + quality
                
        movieInfoUrl = entry['link']
        movieLabel = '[B]' + title + '[/B]' + ('(' + year + ')' + quality if (year != '') else '')
        item = ListItem()
        item.add_moving_data('movieTitle', title)
        item.add_moving_data('movieYear', year)
        item.add_request_data('movieInfoUrl', movieInfoUrl)
        item.set_next_action_name('Movie_Streams')
        xbmcListItem = xbmcgui.ListItem(label=movieLabel, label2='(' + year + ') :: ' + quality)
        item.set_xbmc_list_item_obj(xbmcListItem)
        items.append(item)
        response_obj.addListItem(item)
    
    if current_page > 0 and current_page < total_pages:
        next_page = current_page + 1
        item = ListItem()
        item.add_request_data('page', next_page)
        item.add_request_data('categoryUrlSuffix', request_obj.get_data()['categoryUrlSuffix'])
        item.set_next_action_name('Next_Page')
        xbmcListItem = xbmcgui.ListItem(label='  ---- next page ----  #' + str(next_page) + ' ->')
        item.set_xbmc_list_item_obj(xbmcListItem)
        response_obj.addListItem(item)
    
    response_obj.set_xbmc_content_type('movies')
    
'''
Cached function to retrieve HD movies
'''
def retrieveMovies(categoryUrlSuffix):
    html = HttpUtils.HttpClient().getHtmlContent(url=(BASE_WSITE_URL + "feeds/posts/summary/-/" + categoryUrlSuffix + "?max-results=99999&alt=json"))
    jObj = json.loads(html)
    titles = []
    for entry in jObj["feed"]["entry"]:
        titleInfo = str(entry["title"]["$t"])
        movieInfoUrl = ""
        for link in entry["link"]:
            if link["rel"] == "self":
                movieInfoUrl = str(link["href"])
                break
        
        title = {}
        title['info'] = titleInfo
        title['link'] = movieInfoUrl
        titles.append(title)
    return titles


def retieveTrailerStream(request_obj, response_obj):
    soup = None
    title = None
    if request_obj.get_data().has_key('movieInfoUrl'):
        html = HttpUtils.HttpClient().getHtmlContent(url=(request_obj.get_data()['movieInfoUrl'] + '?alt=json'))
        jObj = json.loads(html)
        html = jObj['entry']['content']['$t']
        title = jObj['entry']['title']['$t']
        soup = BeautifulSoup.BeautifulSoup(html)
    elif request_obj.get_data().has_key('moviePageUrl'):
        contentDiv = BeautifulSoup.SoupStrainer('div', {'dir':'ltr'})
        soup = HttpUtils.HttpClient().getBeautifulSoup(url=request_obj.get_data()['moviePageUrl'], parseOnlyThese=contentDiv)
    if soup == None:
        return
    paramTag = soup.findChild('param', attrs={'name':'movie'}, recursive=True)
    videoLink = None
    if paramTag is not None:
        videoLink = paramTag['value']
    else:
        videoLink = soup.findChild('embed', recursive=True)['src']
    request_obj.set_data({'videoLink': videoLink, 'videoTitle':title})


def retieveMovieStreams(request_obj, response_obj):
    soup = None
    if request_obj.get_data().has_key('movieInfoUrl'):
        html = HttpUtils.HttpClient().getHtmlContent(url=(request_obj.get_data()['movieInfoUrl'] + '?alt=json'))
        jObj = json.loads(html)
        html = jObj['entry']['content']['$t']
        soup = BeautifulSoup.BeautifulSoup(html)
    elif request_obj.get_data().has_key('moviePageUrl'):
        contentDiv = BeautifulSoup.SoupStrainer('div', {'dir':'ltr'})
        soup = HttpUtils.HttpClient().getBeautifulSoup(url=request_obj.get_data()['moviePageUrl'], parseOnlyThese=contentDiv)
    if soup == None:
        return
    videoSources = []
    videoSourceLinks = None
    divTags = []
    loadLastTags(soup, 'div', divTags)
    
    for divTag in divTags:
        if re.search('^(Source|ONLINE)', divTag.getText(), re.IGNORECASE):
            if videoSourceLinks is not None and len(videoSourceLinks) > 0:
                videoSources.append(videoSourceLinks)
            videoSourceLinks = []
        else:
            aTag = divTag.findChild('a', attrs={'href':re.compile('(desionlinetheater.com|wp.me)')}, recursive=True)
            if aTag is not None:
                infoLink = str(aTag['href']).replace('http://adf.ly/377117/', '')
                if videoSourceLinks == None:
                    videoSourceLinks = []
                videoSourceLinks.append(infoLink)
    if videoSourceLinks is not None and len(videoSourceLinks) > 0:
        videoSources.append(videoSourceLinks)
    new_items = []
    sourceCount = 0
    for videoSource in videoSources:
        sourceCount = sourceCount + 1
        new_items.extend(__prepareVideoSourceLinks__(videoSource, str(sourceCount)))
    
    if(request_obj.get_data().has_key('videoInfo')):
        __addVideoInfo__(new_items, request_obj.get_data()['videoInfo'])
    response_obj.set_item_list(new_items)
    
    playNowItem = __findPlayNowStream__(response_obj.get_item_list())
    if playNowItem is not None:
        request_obj.set_data({'videoPlayListItems': playNowItem.get_request_data()['videoPlayListItems']})
    
    XBMCInterfaceUtils.displayDialogMessage('Do you know?', 'The content of this add-on is from www.sominaltvfilms.com.','Please help SomnialTV by visiting his website regularly.','AJ has no relation with www.sominaltvfilms.com. OK to proceed!',msgType='[B]INFO & REQUEST: [/B]')
    
    
def __addVideoInfo__(video_items, videoInfo):
    for video_item in video_items:
        video_item.add_request_data('videoInfo', videoInfo)
    
    
def loadLastTags(soup, findTag, tags):
    childs = soup.findAll(findTag, recursive=False)
    if childs is None or len(childs) == 0:
        tags.append(soup)
    else:
        for newSoup in childs:
            loadLastTags(newSoup, findTag, tags)
    
    
def __findPlayNowStream__(new_items):
    selectedIndex = None
    selectedSource = None
    for item in new_items:
        if item.get_moving_data().has_key('isContinuousPlayItem') and item.get_moving_data()['isContinuousPlayItem']:
            try:
                preference = PREFERRED_DIRECT_PLAY_ORDER.index(item.get_moving_data()['videoSourceName'])
                if preference == 0:
                    selectedSource = item
                    selectedIndex = 0
                    break
                elif selectedIndex is None or selectedIndex > preference:
                    selectedSource = item
                    selectedIndex = preference
            except ValueError:
                continue
    return selectedSource
    
    
def __preparePlayListItem__(video_items, source):
    video_playlist_items = []
    video_source_img = None
    video_source_name = None
    for item in video_items:
        video_item = {}
        video_item['videoLink'] = item.get_request_data()['videoLink']
        video_item['videoTitle'] = item.get_request_data()['videoTitle']
        video_playlist_items.append(video_item)
        video_source_img = item.get_moving_data()['videoSourceImg']
        video_source_name = item.get_moving_data()['videoSourceName']
    Logger.logDebug('IMAGE :: ')
    Logger.logDebug(video_source_img)
    Logger.logDebug(type(video_source_img))
    item = ListItem()
    item.add_request_data('videoPlayListItems', video_playlist_items)
    item.add_moving_data('isContinuousPlayItem', True)
    item.add_moving_data('videoSourceName', video_source_name)
    item.set_next_action_name('Play_AllStreams')
    xbmcListItem = xbmcgui.ListItem(label='[COLOR blue]' + AddonUtils.getBoldString('Continuous Play') + '[/COLOR]' + ' | ' + 'Source #' + source + ' | ' + 'Parts = ' + str(len(video_playlist_items)) , iconImage=video_source_img, thumbnailImage=video_source_img)
    item.set_xbmc_list_item_obj(xbmcListItem)
    return item
    
    
def __prepareVideoSourceLinks__(videoSourceLinks, source):
    new_items = XBMCInterfaceUtils.callBackDialogProgressBar(getattr(sys.modules[__name__], '__prepareVideoLink__'), videoSourceLinks, 'Retrieving streaming links for source #' + source, 'Failed to retrieve stream information, please try again later')
    if len(new_items) == 0:
        XBMCInterfaceUtils.displayDialogMessage('No video items found!', 'Unable to resolve video items from source #' + source, 'Continuing with next source...')
        return []
    
    count = 0
    for item in new_items:
        xbmcItem = item.get_xbmc_list_item_obj()
        count = count + 1
        xbmcItem.setLabel('Source #' + source + ' | ' + xbmcItem.getLabel() + str(count))
    new_items.append(__preparePlayListItem__(new_items, source))
    return new_items
    
    
def __prepareVideoLink__(videoSourceLink):
    new_items = []
    url = videoSourceLink
    if re.search('wp.me', url, re.I):
        url = HttpUtils.getRedirectedUrl(url)
    Logger.logDebug(url)
#     contentDiv = BeautifulSoup.SoupStrainer('div', {'class':'left_articles'})
#     soup = BeautifulSoup.BeautifulSoup(html, contentDiv)
    html = HttpUtils.HttpClient().getHtmlContent(url)
    dek = EnkDekoder.dekode(html)
    if dek is not None:
        html = dek
        
    html = html.replace('\n\r', '').replace('\r', '').replace('\n', '')
    children = re.compile('<embed(.+?)>').findall(html)
    if children is None or len(children) == 0:
        children = re.compile('<iframe(.+?)>').findall(html)
    Logger.logDebug(children)
    for child in children:
        video_url = re.compile('src="(.+?)"').findall(child)[0]
        if(re.search('http://ads', video_url, re.I) or re.search('http://ax-d', video_url, re.I)):
            continue
        if video_url.startswith('http://goo.gl/'):
            Logger.logDebug('Found google short URL = ' + video_url)
            video_url = HttpUtils.getRedirectedUrl(video_url)
            Logger.logDebug('After finding out redirected URL = ' + video_url)
        video_hosting_info = SnapVideo.findVideoHostingInfo(video_url)
        video_source_img = video_hosting_info.get_video_hosting_image()
        
        new_item = ListItem()
        new_item.add_request_data('videoTitle', 'Part #')
        new_item.add_request_data('videoLink', video_url)
        new_item.add_moving_data('videoSourceImg', video_source_img)
        new_item.add_moving_data('videoSourceName', video_hosting_info.get_video_hosting_name())
        new_item.set_next_action_name('Play_Stream')
        xbmcListItem = xbmcgui.ListItem(label='Part #', iconImage=video_source_img, thumbnailImage=video_source_img)
        new_item.set_xbmc_list_item_obj(xbmcListItem)
        new_items.append(new_item)
    
    return new_items


