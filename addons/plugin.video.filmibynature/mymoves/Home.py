'''
Created on Nov 20, 2012

@author: ajju
'''
from TurtleContainer import AddonContext
from common.DataObjects import ListItem
import xbmcgui #@UnresolvedImport
from common import AddonUtils


def displayMenuItems(request_obj, response_obj):
    # TV Shows item
    movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('Movie')
    xbmcListItem = xbmcgui.ListItem(label='Movie', iconImage=movie_icon_filepath, thumbnailImage=movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # LIVE TV item
    youtube_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='YouTube_V1.png')
    item = ListItem()
    item.set_next_action_name('YouTube')
    xbmcListItem = xbmcgui.ListItem(label='YouTube', iconImage=youtube_icon_filepath, thumbnailImage=youtube_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)


