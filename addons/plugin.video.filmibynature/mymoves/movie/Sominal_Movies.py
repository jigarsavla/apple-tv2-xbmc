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
from common.HttpUtils import HttpClient

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
    html = HttpClient().getHtmlContent(url=(BASE_WSITE_URL + "feeds/posts/summary/-/BluRay?max-results=10000&alt=json"))
    jObj = json.loads(html)
    print 'RETRIEVED MOVIE OBJECT'
    print len(jObj["feed"]["entry"])
    for entry in jObj["feed"]["entry"]:
        title = str(entry["title"]["$t"])
        print title
        movieInfo = re.compile("(.+?)\((\d+)\) (.*)").findall(title)
        title = movieInfo[0][0].rstrip()
        year = movieInfo[0][1]
        quality = movieInfo[0][2]
        moviePageUrl = ""
        movieInfoUrl = ""
        for link in entry["link"]:
            if link["rel"] == "self":
                movieInfoUrl = link["href"]
            elif link["rel"] == "alternate":
                moviePageUrl = link["href"]
                
        item = ListItem()
        item.add_moving_data('movieTitle', title)
        item.add_moving_data('movieYear', year)
        item.add_request_data('movieInfoUrl', movieInfoUrl)
        item.set_next_action_name('Movie_Streams')
        xbmcListItem = xbmcgui.ListItem(label=title, label2='(' + year + ') - ' + quality)
        item.set_xbmc_list_item_obj(xbmcListItem)
        response_obj.addListItem(item)
        
        
def retieveMovieStreams(request_obj, response_obj):
    html = HttpClient().getHtmlContent(url=(request_obj.get_data()['movieInfoUrl'] + '?alt=json'))
    jObj = json.loads(html)
    html = jObj['entry']['content']['$t']
    soup = BeautifulSoup.BeautifulSoup(html)
    for aTag in soup.findAll('a', attrs={'href':re.compile('http://www.desionlinetheater.com')}, recursive=True):
        infoLink = str(aTag['href']).replace('http://adf.ly/377117/', '')
        name = aTag.getText()
        
        item = ListItem()
        item.add_moving_data('videoInfoLink', infoLink)
        item.add_request_data('videoTitle', name)
        item.set_next_action_name('Play_Stream')
        xbmcListItem = xbmcgui.ListItem(label=name)
        item.set_xbmc_list_item_obj(xbmcListItem)
        response_obj.addListItem(item)
    items = response_obj.get_item_list()
    XBMCInterfaceUtils.callBackDialogProgressBar(getattr(sys.modules[__name__], '__prepareVideoLink__'), items, 'Retrieving Streaming links', 'Failed to retrieve stream information, please try again later')
    
def __prepareVideoLink__(item):
    url = item.get_moving_data()['videoInfoLink']
    video_link = {}
    contentDiv = BeautifulSoup.SoupStrainer('div', {'class':'left'})
    soup = HttpClient().getBeautifulSoup(url=url, parseOnlyThese=contentDiv)
    child = soup.findChild('embed')
    if child is None:
        child = soup.findChild('iframe')
    video_url = child['src']
    video_hosting_info = SnapVideo.findVideoHostingInfo(video_url)
    video_source_img = video_hosting_info.get_video_hosting_image()
    
    item.add_request_data('videoLink', video_url)
    xbmc_item = item.get_xbmc_list_item_obj()
    xbmc_item.setIconImage(video_source_img)
    xbmc_item.setThumbnailImage(video_source_img)
    
    
