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
from common import XBMCInterfaceUtils
try:
    import json
except ImportError:
    import simplejson as json
from common import HttpUtils

BASE_WSITE_URL = base64.b64decode('aHR0cDovL3d3dy5zb21pbmFsdHZmaWxtcy5jb20v')

def displayMainMenu(request_obj, response_obj):
    # HD Movies
    hd_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='HD_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('Blurays')
    xbmcListItem = xbmcgui.ListItem(label='HD MOVIES', iconImage=hd_movie_icon_filepath, thumbnailImage=hd_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # A-Z Movies
    az_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='AZ_Dir_V1.png')
    item = ListItem()
    item.set_next_action_name('AZ')
    xbmcListItem = xbmcgui.ListItem(label='A - to - Z INDEX', iconImage=az_movie_icon_filepath, thumbnailImage=az_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Hindi Movies
    hindi_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Hindi_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('Hindi')
    xbmcListItem = xbmcgui.ListItem(label='HINDI', iconImage=hindi_movie_icon_filepath, thumbnailImage=hindi_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Telugu Movies
    telugu_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Telugu_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('Telugu')
    xbmcListItem = xbmcgui.ListItem(label='TELUGU', iconImage=telugu_movie_icon_filepath, thumbnailImage=telugu_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Tamil Movies
    tamil_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Tamil_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('Tamil')
    xbmcListItem = xbmcgui.ListItem(label='TAMIL', iconImage=tamil_movie_icon_filepath, thumbnailImage=tamil_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Punjabi Movies
    punjabi_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('Punjabi')
    xbmcListItem = xbmcgui.ListItem(label='PUNJABI', iconImage=punjabi_movie_icon_filepath, thumbnailImage=punjabi_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Malayalam Movies
    malayalam_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Malayalam_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('Malayalam')
    xbmcListItem = xbmcgui.ListItem(label='MALAYALAM', iconImage=malayalam_movie_icon_filepath, thumbnailImage=malayalam_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Bengali Movies
    bengali_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Bengali_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('Bengali')
    xbmcListItem = xbmcgui.ListItem(label='BENGALI', iconImage=bengali_movie_icon_filepath, thumbnailImage=bengali_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)


def displayUC(request_obj, response_obj):
    print 'UNDER CONSTRUCTION'
    XBMCInterfaceUtils.displayDialogMessage(heading='UNDER Construction', line1='Please wait for update!!', line2='Enjoy HD movies for the time being.', line3='')

def listHDMovies(request_obj, response_obj):
    html = HttpUtils.HttpClient().getHtmlContent(url=(BASE_WSITE_URL + "feeds/posts/summary/-/BluRay?max-results=10000&alt=json"))
    jObj = json.loads(html)
    print 'RETRIEVED MOVIE OBJECT'
    print len(jObj["feed"]["entry"])
    for entry in jObj["feed"]["entry"]:
        titleInfo = str(entry["title"]["$t"])
        print titleInfo
        movieInfo = re.compile("(.+?)\((\d+)\) (.*)").findall(titleInfo)
        title = unicode(movieInfo[0][0].rstrip()).encode('utf-8')
        year = unicode(movieInfo[0][1]).encode('utf-8')
        quality = unicode(movieInfo[0][2]).encode('utf-8')
        moviePageUrl = ""
        movieInfoUrl = ""
        for link in entry["link"]:
            if link["rel"] == "self":
                movieInfoUrl = str(link["href"])
            elif link["rel"] == "alternate":
                moviePageUrl = str(link["href"])
                
        item = ListItem()
        item.add_moving_data('movieTitle', title)
        item.add_moving_data('movieYear', year)
        item.add_request_data('movieInfoUrl', movieInfoUrl)
        item.set_next_action_name('Movie_Streams')
        xbmcListItem = xbmcgui.ListItem(label=title, label2='(' + year + ') - ' + quality)
        item.set_xbmc_list_item_obj(xbmcListItem)
        response_obj.addListItem(item)
    response_obj.set_xbmc_content_type('movies')
        
        
def retieveMovieStreams(request_obj, response_obj):
    html = HttpUtils.HttpClient().getHtmlContent(url=(request_obj.get_data()['movieInfoUrl'] + '?alt=json'))
    jObj = json.loads(html)
    html = jObj['entry']['content']['$t']
    soup = BeautifulSoup.BeautifulSoup(html)
    for aTag in soup.findAll('a', attrs={'href':re.compile('(desionlinetheater.com|wp.me)')}, recursive=True):
        infoLink = str(aTag['href']).replace('http://adf.ly/377117/', '')
        name = aTag.getText()
        
        item = ListItem()
        item.add_moving_data('videoInfoLink', infoLink)
        item.add_request_data('videoTitle', name)
        item.set_next_action_name('Play_Stream')
        response_obj.addListItem(item)
    items = response_obj.get_item_list()
    new_items = XBMCInterfaceUtils.callBackDialogProgressBar(getattr(sys.modules[__name__], '__prepareVideoLink__'), items, 'Retrieving Streaming links', 'Failed to retrieve stream information, please try again later')
    response_obj.set_item_list(new_items)
    
def __prepareVideoLink__(item):
    new_items = []
    url = item.get_moving_data()['videoInfoLink']
    if re.search('wp.me', url, re.I):
        url = HttpUtils.getRedirectedUrl(url)
    video_link = {}
    contentDiv = BeautifulSoup.SoupStrainer('div', {'class':'left'})
    soup = HttpUtils.HttpClient().getBeautifulSoup(url=url, parseOnlyThese=contentDiv)
    children = soup.findChildren('embed')
    if children is None or len(children) == 0:
        children = soup.findChildren('iframe', attrs={'class':'iframe-class'})
    name = item.get_request_data()['videoTitle']
    count = 0
    for child in children:
        count = count + 1
        new_name = name
        if(len(children) > 1):
            new_name = name + ' - Part #' + str(count)
        video_url = child['src']
        if(re.search('http://ads', video_url, re.I)):
            return
        video_hosting_info = SnapVideo.findVideoHostingInfo(video_url)
        video_source_img = video_hosting_info.get_video_hosting_image()
        new_item = ListItem()
        new_item.add_request_data('videoTitle', new_name)
        new_item.add_request_data('videoLink', video_url)
        new_item.set_next_action_name('Play_Stream')
        xbmcListItem = xbmcgui.ListItem(label=new_name, iconImage=video_source_img, thumbnailImage=video_source_img)
        new_item.set_xbmc_list_item_obj(xbmcListItem)
        new_items.append(new_item)
        
    return new_items
    
    
