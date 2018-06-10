#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Sid.
# https://github.com/yoavram/Sid

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Yoav Ram <yoav@yoavram.com>

from __future__ import absolute_import

__license__ = u'MIT'
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

## comment out due because libmmd.dll was not found during installation
# trick to get Ctrl-C to behave: http://stackoverflow.com/questions/15457786/ctrl-c-crashes-python-after-importing-scipy-stats
# import sys
# if sys.platform == 'win32':
# 	import os
# 	import imp
# 	import ctypes
# 	import thread
# 	import win32api

# 	# Load the DLL manually to ensure its handler gets
# 	# set before our handler.
# 	basepath = imp.find_module('numpy')[1]
# 	ctypes.CDLL(os.path.join(basepath, 'core', 'libmmd.dll'))
# 	ctypes.CDLL(os.path.join(basepath, 'core', 'libifcoremd.dll'))

# 	# Now set our handler for CTRL_C_EVENT. Other control event 
# 	# types will chain to the next handler.
# 	def handler(dwCtrlType, hook_sigint=thread.interrupt_main):
# 	    if dwCtrlType == 0: # CTRL_C_EVENT
# 	        hook_sigint()
# 	        return 1 # don't chain to the next handler
# 	    return 0 # chain to the next handler

# 	win32api.SetConsoleCtrlHandler(handler, 1)
# end of trick

import os
CI = os.environ.get('CI', 'false').lower() == 'true'
if CI:
  import matplotlib
  matplotlib.use('Agg')

from . import take_cover

# http://www.text-image.com/convert/ascii.html
__logo__ = """                      smddms`                     
                     oN.  /Mo                     
                   /hm/    -mh-                   
                  oN+`      `oN+                  
                 `Mo          oh                  
                 :Mmsyysssyys/mN-                 
                `Nmdo.`````./hdNy                 
                 Nh`         ``ms                 
                 hm``        `-M/                 
                 +Mmm+     `hmNN`                 
                  :+my     .Mds-                  
              .:oyyys.      :oyyyo/-`             
            /hhs:.`            `.:oyds.           
           /M/`                     .dd           
           hd                        :M.          
          `N/                         N+          
          :M`   +.              `y.   yh          
          sm   +N`               om`  +M`         
          my  .N+                `my  .M:         
         `M:  yd                  /M:  ds         
         :m   od/`              `:hh-  sd         
         oN-`  -hds+oyy+``/yhssyhh:  `.dm         
       .+mNmho:.`-+++NMMmmMMMo-:-`./ohddNy-`      
    `/ydo-  ./ohhy+:+NMMMMMMMo+sydds/.  -oddo-`   
  -sds:         `-:///////////::-`         -odh+` 
.yd/`                                         -ym:
md                                              sN
hm-`                                           -dh
 +hmmddddhhhhhhhhhhhhhhhhhhhhhyyyyyyyyyyyyyyhhhy/ """
