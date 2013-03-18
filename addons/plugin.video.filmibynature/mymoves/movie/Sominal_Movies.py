'''
Created on Nov 20, 2012

@author: ajju
'''
from TurtleContainer import AddonContext
from common.DataObjects import ListItem
import xbmcgui  # @UnresolvedImport
from common import AddonUtils
import base64
import re
import sys
import BeautifulSoup
from moves import SnapVideo
from snapvideo import Dailymotion, YouTube, GoogleDocs
from common import XBMCInterfaceUtils
import TurtlePlugin
try:
    import json
except ImportError:
    import simplejson as json
from common import HttpUtils
try:
    import StorageServer
except:
    import storageserverdummy as StorageServer


PREFERRED_DIRECT_PLAY_ORDER = [GoogleDocs.VIDEO_HOSTING_NAME, Dailymotion.VIDEO_HOSTING_NAME, YouTube.VIDEO_HOSTING_NAME]
BASE_WSITE_URL = base64.b64decode('aHR0cDovL3d3dy5zb21pbmFsdHZmaWxtcy5jb20v')
pageDict = {0:25, 1:50, 2:100}
TITLES_PER_PAGE = pageDict[int(AddonContext().addon.getSetting('moviesPerPage'))]

def displayMainMenu(request_obj, response_obj):
    # HD Movies
    hd_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='HD_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('listMovies')
    item.add_request_data('categoryUrlSuffix', 'BluRay')
    xbmcListItem = xbmcgui.ListItem(label='HD MOVIES', iconImage=hd_movie_icon_filepath, thumbnailImage=hd_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # A-Z Movies
    az_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='AZ_Dir_V1.png')
    item = ListItem()
    item.set_next_action_name('AZ')
    xbmcListItem = xbmcgui.ListItem(label='A - to - Z INDEX', iconImage=az_movie_icon_filepath, thumbnailImage=az_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
#    response_obj.addListItem(item)
    
    # Hindi Movies
    hindi_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Hindi_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('listMovies')
    item.add_request_data('categoryUrlSuffix', 'Hindi%20Movies')
#    item.add_request_data('infoUrl', BASE_WSITE_URL + '2010/11/hindi-movies.html')
    xbmcListItem = xbmcgui.ListItem(label='HINDI', iconImage=hindi_movie_icon_filepath, thumbnailImage=hindi_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Telugu Movies
    telugu_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Telugu_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('listMovies')
    item.add_request_data('categoryUrlSuffix', 'Telugu')
#    item.add_request_data('infoUrl', BASE_WSITE_URL + '2010/11/telugu-movies.html')
    xbmcListItem = xbmcgui.ListItem(label='TELUGU', iconImage=telugu_movie_icon_filepath, thumbnailImage=telugu_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Tamil Movies
    tamil_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Tamil_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('listMovies')
    item.add_request_data('categoryUrlSuffix', 'Tamil')
#    item.add_request_data('infoUrl', BASE_WSITE_URL + '2010/11/tamil-movies.html')
    xbmcListItem = xbmcgui.ListItem(label='TAMIL', iconImage=tamil_movie_icon_filepath, thumbnailImage=tamil_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Punjabi Movies
    punjabi_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('listMovies')
    item.add_request_data('categoryUrlSuffix', 'Punjabi')
#    item.add_request_data('infoUrl', BASE_WSITE_URL + '2011/08/punjabi-movies.html')
    xbmcListItem = xbmcgui.ListItem(label='PUNJABI', iconImage=punjabi_movie_icon_filepath, thumbnailImage=punjabi_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Malayalam Movies
    malayalam_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Malayalam_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('listMovies')
    item.add_request_data('categoryUrlSuffix', 'Malayalam')
#    item.add_request_data('infoUrl', BASE_WSITE_URL + '2010/11/hindi-movies.html')
    xbmcListItem = xbmcgui.ListItem(label='MALAYALAM', iconImage=malayalam_movie_icon_filepath, thumbnailImage=malayalam_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Bengali Movies
    bengali_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Bengali_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('listMovies')
    item.add_request_data('categoryUrlSuffix', 'Bengali')
#    item.add_request_data('infoUrl', BASE_WSITE_URL + '2010/11/hindi-movies.html')
    xbmcListItem = xbmcgui.ListItem(label='BENGALI', iconImage=bengali_movie_icon_filepath, thumbnailImage=bengali_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)


def displayUC(request_obj, response_obj):
    print 'UNDER CONSTRUCTION'
    XBMCInterfaceUtils.displayDialogMessage(heading='UNDER Construction', line1='Please wait for update!!', line2='Enjoy HD movies for the time being.', line3='')

def listMovies(request_obj, response_obj):
    cache = StorageServer.StorageServer(TurtlePlugin.__addon_id__, 12)
    titles = cache.cacheFunction(retrieveMovies, request_obj.get_data()['categoryUrlSuffix'])
    
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
        if request_obj.get_data().has_key('page'):
            current_page = int(request_obj.get_data()['page'])
            start = (current_page - 1) * TITLES_PER_PAGE
    end = start + TITLES_PER_PAGE
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
        print titleInfo
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
        if request_obj.get_data()['categoryUrlSuffix'] != 'BluRay':
            if(len(movieInfo[0]) >= 3):
                quality = unicode(movieInfo[0][2]).encode('utf-8')
                if quality == '*BluRay*':
                    quality = '[COLOR red]' + quality + '[/COLOR]'
                elif quality == 'DVD':
                    quality = '[COLOR orange]' + quality + '[/COLOR]'
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
    print 'RETRIEVED MOVIE OBJECT'
    print len(jObj["feed"]["entry"])
    for entry in jObj["feed"]["entry"]:
        titleInfo = str(entry["title"]["$t"])
        print titleInfo
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


'''

@deprecated: Using the method listMovies
'''
def listCategoryMovies(request_obj, response_obj):
    cache = StorageServer.StorageServer(TurtlePlugin.__addon_id__, 12)
    titles = cache.cacheFunction(retrieveCategoryMovies, request_obj.get_data()['infoUrl'])
    
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
        if request_obj.get_data().has_key('page'):
            current_page = int(request_obj.get_data()['page'])
            start = (current_page - 1) * TITLES_PER_PAGE
    end = start + TITLES_PER_PAGE
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
        movieInfo = re.compile("(.+?)\((\d+)\)").findall(titleInfo)
        title = unicode(movieInfo[0][0].rstrip()).encode('utf-8')
        year = unicode(movieInfo[0][1]).encode('utf-8')
        moviePageUrl = entry['link']
                
        item = ListItem()
        item.add_moving_data('movieTitle', title)
        item.add_moving_data('movieYear', year)
        item.add_request_data('moviePageUrl', moviePageUrl)
        item.set_next_action_name('Movie_Streams')
        xbmcListItem = xbmcgui.ListItem(label=title, label2='(' + year + ')')
        item.set_xbmc_list_item_obj(xbmcListItem)
        response_obj.addListItem(item)
        
    if current_page > 0 and current_page < total_pages:
        next_page = current_page + 1
        item = ListItem()
        item.add_request_data('page', next_page)
        item.add_request_data('infoUrl', request_obj.get_data()['infoUrl'])
        item.set_next_action_name('Next_Page')
        xbmcListItem = xbmcgui.ListItem(label='  ---- next page ----  #' + str(next_page) + ' ->')
        item.set_xbmc_list_item_obj(xbmcListItem)
        response_obj.addListItem(item)
        
    response_obj.set_xbmc_content_type('movies')

'''
Cached function to retrieve category specific movies

@deprecated: Using the method retrieveMovies
'''
def retrieveCategoryMovies(infoUrl):
    titles = []
    contentDiv = BeautifulSoup.SoupStrainer('div', {'dir':'ltr'})
    soup = HttpUtils.HttpClient().getBeautifulSoup(url=infoUrl, parseOnlyThese=contentDiv)
    for aTag in soup.findAll('a', {'href':re.compile('http://www.sominaltv(theater|films).com(.+?).html')}):
        if not re.search('^(?!\()', aTag.getText()):
            continue
        titleInfo = aTag.getText()
        movieInfo = re.compile("(.+?)\((\d+)\)").findall(titleInfo)
        if not len(movieInfo) > 0:
            continue
        moviePageUrl = aTag['href']
        title = {}
        title['info'] = titleInfo
        title['link'] = moviePageUrl
        titles.append(title)
    return titles


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
    for divTag in soup.findAll('div', attrs={'class':'separator'}, recursive=True):
        if re.search('^(Source|ONLINE)', divTag.getText(), re.IGNORECASE):
            if videoSourceLinks is not None and len(videoSourceLinks) > 0:
                videoSources.append(videoSourceLinks)
            videoSourceLinks = []
        else:
            aTag = divTag.findChild('a', attrs={'href':re.compile('(desionlinetheater.com|wp.me)')}, recursive=True)
            if aTag is not None:
                infoLink = str(aTag['href']).replace('http://adf.ly/377117/', '')
                name = aTag.getText()
                if videoSourceLinks == None:
                    videoSourceLinks = []
                videoSourceLinks.append(infoLink)
    if videoSourceLinks is not None and len(videoSourceLinks) > 0:
        videoSources.append(videoSourceLinks)
    
    new_items = XBMCInterfaceUtils.callBackDialogProgressBar(getattr(sys.modules[__name__], '__prepareVideoSourceLinks__'), videoSources, 'Resolving links for source', 'Failed to retrieve stream information, please try again later')
    response_obj.set_item_list(new_items)
    
    playNowItem = __findPlayNowStream__(response_obj.get_item_list())
    if playNowItem is not None:
        request_obj.set_data({'videoPlayListItems': playNowItem.get_request_data()['videoPlayListItems']})
    
    
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
    
    
def __preparePlayListItem__(video_items):
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
    
    item = ListItem()
    item.add_request_data('videoPlayListItems', video_playlist_items)
    item.add_moving_data('isContinuousPlayItem', True)
    item.add_moving_data('videoSourceName', video_source_name)
    item.set_next_action_name('Play_AllStreams')
    xbmcListItem = xbmcgui.ListItem(label='[COLOR blue]' + AddonUtils.getBoldString('Continuous Play') + '[/COLOR]' + ' | ' + 'Parts = ' + str(len(video_playlist_items)) , iconImage=video_source_img, thumbnailImage=video_source_img)
    item.set_xbmc_list_item_obj(xbmcListItem)
    return item
    
    
def __prepareVideoSourceLinks__(videoSourceLinks):
    print videoSourceLinks
    new_items = XBMCInterfaceUtils.callBackDialogProgressBar(getattr(sys.modules[__name__], '__prepareVideoLink__'), videoSourceLinks, 'Retrieving streaming links for source', 'Failed to retrieve stream information, please try again later')
    count = 0
    for item in new_items:
        xbmcItem = item.get_xbmc_list_item_obj()
        count = count + 1
        xbmcItem.setLabel(xbmcItem.getLabel() + str(count))
    new_items.append(__preparePlayListItem__(new_items))
    return new_items
    
    
def __prepareVideoLink__(videoSourceLink):
    new_items = []
    url = videoSourceLink
    print 'Going to look for video links in ' + url
    if re.search('wp.me', url, re.I):
        url = HttpUtils.getRedirectedUrl(url)
    video_link = {}
    contentDiv = BeautifulSoup.SoupStrainer('div', {'class':'left'})
    soup = HttpUtils.HttpClient().getBeautifulSoup(url=url, parseOnlyThese=contentDiv)
    children = soup.findChildren('embed')
    if children is None or len(children) == 0:
        children = soup.findChildren('iframe')
    for child in children:
        video_url = child['src']
        if(re.search('http://ads', video_url, re.I) or re.search('http://ax-d', video_url, re.I)):
            continue
        video_hosting_info = SnapVideo.findVideoHostingInfo(video_url)
        video_source_img = video_hosting_info.get_video_hosting_image()
        
        new_item = ListItem()
        new_item.add_request_data('videoTitle', 'Video Part #')
        new_item.add_request_data('videoLink', video_url)
        new_item.add_moving_data('videoSourceImg', video_source_img)
        new_item.add_moving_data('videoSourceName',  video_hosting_info.get_video_hosting_name())
        new_item.set_next_action_name('Play_Stream')
        xbmcListItem = xbmcgui.ListItem(label='Video Part #', iconImage=video_source_img, thumbnailImage=video_source_img)
        new_item.set_xbmc_list_item_obj(xbmcListItem)
        new_items.append(new_item)
    
    return new_items
