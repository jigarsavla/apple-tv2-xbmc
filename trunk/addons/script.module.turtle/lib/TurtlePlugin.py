'''
Created on Oct 16, 2011

@author: ajju
'''
from TurtleContainer import Container
from common import ExceptionHandler, Logger, HttpUtils
import sys
import xbmcplugin  # @UnresolvedImport

__addon_id__ = None

def start(addon_id):
    try:
        global __addon_id__
        __addon_id__ = addon_id
        
        containerObj = Container(addon_id=addon_id)
        action_id = containerObj.getTurtleRequest().get_action_id()
        containerObj.performAction(action_id)
        cleanUp()
    except Exception, e:
        Logger.logFatal(e)
        ExceptionHandler.handle(e)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def cleanUp():
    containerObj = Container()
    containerObj.cleanUp()
    del containerObj
    httpClient = HttpUtils.HttpClient()
    httpClient.cleanUp()
    del httpClient
