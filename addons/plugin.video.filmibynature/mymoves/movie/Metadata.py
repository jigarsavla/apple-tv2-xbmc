
from metahandler import metahandlers, metacontainers  # @UnresolvedImport
import xbmcgui, xbmcplugin  # @UnresolvedImport
from common import XBMCInterfaceUtils
import sys


    
def retieveMovieInfoAndAddItem(request_obj, response_obj):
    items = response_obj.get_item_list()
    XBMCInterfaceUtils.callBackDialogProgressBar(getattr(sys.modules[__name__], '__addMovieInfo_in_item'), items, 'Retrieving MOVIE info', 'Failed to retrieve movie information, please try again later')

global metaget
metaget = metahandlers.MetaData()

def __addMovieInfo_in_item(item):
    title = str(item.get_moving_data()['movieTitle'])
    year = str(item.get_moving_data()['movieYear'])
    meta = metaget.get_meta('movie', title, year=year)
    xbmc_item = item.get_xbmc_list_item_obj()
    
    if(meta is not None):
        xbmc_item.setIconImage(meta['thumb_url'])
        xbmc_item.setThumbnailImage(meta['cover_url'])
        xbmc_item.setInfo('video', {'genre':meta['genre'], 'title':meta['title'], 'year':meta['year'], 'rating':meta['rating'], 'tagline':meta['tagline'], 'writer':meta['writer'] , 'director':meta['director'], 'cast':meta['cast'], 'raiting':meta['rating'], 'votes':meta['votes'], 'plot':meta['plot'], 'duration':meta['duration'], 'mpaa':meta['mpaa'], 'studio':meta['studio'] , 'premiered':meta['premiered'], 'trailer_url':meta['trailer_url']})
        xbmc_item.setProperty('fanart_image', meta['backdrop_url'])
    else:
        xbmc_item.setInfo('video', {'title':title, 'year':year})

