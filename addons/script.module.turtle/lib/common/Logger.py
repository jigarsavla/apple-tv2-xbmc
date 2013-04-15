
import xbmc  # @UnresolvedImport
import traceback
import sys
import logging

def logInfo(message):
    if type(message) is not str:
        message = str(message)
    xbmc.log(message, xbmc.LOGINFO)

def logDebug(message):
    if type(message) is not str:
        message = str(message)
    xbmc.log(message, xbmc.LOGDEBUG)
    
def logError(message):
    if type(message) is not str:
        if type(message) is Exception:
            logging.exception(message)
            return
        message = str(message)
    xbmc.log(message, xbmc.LOGERROR)
    
def logFatal(message):
    if type(message) is not str:
        if type(message) is Exception:
            logging.exception(message)
            return
        message = str(message)
    xbmc.log(message, xbmc.LOGFATAL)
    
def logNotice(message):
    if type(message) is not str:
        message = str(message)
    xbmc.log(message, xbmc.LOGNOTICE)
    
def logSevere(message):
    if type(message) is not str:
        if type(message) is Exception:
            logging.exception(message)
            return
        message = str(message)
    xbmc.log(message, xbmc.LOGSEVERE)

def logWarning(message):
    if type(message) is not str:
        if type(message) is Exception:
            logging.exception(message)
            return
        message = str(message)
    xbmc.log(message, xbmc.LOGWARNING)
        

