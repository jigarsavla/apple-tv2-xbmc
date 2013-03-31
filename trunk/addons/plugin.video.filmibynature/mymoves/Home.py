'''
Created on Nov 20, 2012

@author: ajju
'''
from TurtleContainer import AddonContext
from common.DataObjects import ListItem
import xbmcgui #@UnresolvedImport
from common import AddonUtils


def displayMenuItems(request_obj, response_obj):
    # Movies item
    movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('Movie')
    xbmcListItem = xbmcgui.ListItem(label='Movie', iconImage=movie_icon_filepath, thumbnailImage=movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Trailers
    trailer_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Trailers.png')
    item = ListItem()
    item.set_next_action_name('Trailer')
    item.add_request_data('categoryUrlSuffix', 'Trailers')
    xbmcListItem = xbmcgui.ListItem(label='TRAILERS', iconImage=trailer_movie_icon_filepath, thumbnailImage=trailer_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # A-Z
    az_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='AZ_Dir_V1.png')
    item = ListItem()
    item.set_next_action_name('AZ')
    xbmcListItem = xbmcgui.ListItem(label='A to Z', iconImage=az_movie_icon_filepath, thumbnailImage=az_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # LIVE TV item
    youtube_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='YouTube_V1.png')
    item = ListItem()
    item.set_next_action_name('YouTube')
    xbmcListItem = xbmcgui.ListItem(label='YouTube', iconImage=youtube_icon_filepath, thumbnailImage=youtube_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
#     response_obj.addListItem(item)


