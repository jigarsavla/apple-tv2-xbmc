'''
Created on Dec 27, 2011

@author: ajju
'''

import TurtleService
import TurtlePlugin

if __name__ == '__main__':
    
    __addon_id__ = 'service.playit'
    __is_type_service__ = True
    
    if __is_type_service__:
        TurtleService.start(__addon_id__, 'PlayIt', '/PlayIt', 8181, [8100, 8199])
    else:
        TurtlePlugin.start(__addon_id__)
