#! /usr/bin/python3
#coding:utf-8

################################################################################
#                                Mickaël DUVAL
#                                13/11/2020
################################################################################

import sys
import os
import config

exempleConfig = """
portDebug = 9875
repInstall = "D:/prj/webaventure"
repPages = "pages"
pageIndex = "_index_"
"""

sys.path.append(config.repInstall) 
os.chdir(config.repInstall)

import onePage
    
application = onePage.OnePage()

if __name__ == '__main__':
    application.debug()
