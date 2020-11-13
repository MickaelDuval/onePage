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
hoteDebug = "localhost"
repInstall = "D:/prj/onePage"
repPages = "pages"
pageIndex = "_index_"

# contient les pages 'techniques', messages d'erreurs, page 404 etc
repHtmlTechnique = "defautHtml"
"""

sys.path.append(config.repInstall) 
os.chdir(config.repInstall)

import onePage
    
application = onePage.OnePage()

if __name__ == '__main__':
    application.debug()
