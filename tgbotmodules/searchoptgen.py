#!/usr/bin/env python

import argparse
# from . import botconfig
from tgbotmodules.spidermodules import generalcfg


def searchparser():
   parser = argparse.ArgumentParser(description='Search settings')
   parser.add_argument('-k', "--keyword", action='store', dest='keyword', default="", type=str, help='General keywords (might contain unexpected result)')
   parser.add_argument('-p', "--pages", action='store', dest='pages',default=5, type=int, help='Pages Limitation')
   parser.add_argument('-d', "--doujinshi", action='store_true', default=False, dest='doujinshi', help='Search doujin category')
   parser.add_argument('-m', "--manga", action='store_true', default=False, dest='manga', help='Search manga category')
   parser.add_argument("--artistcg", action='store_true', default=False, dest='artistcg', help='Search artistcg category')
   parser.add_argument("--gamecg", action='store_true', default=False, dest='gamecg', help='Search gamecg category')
   parser.add_argument("--western", action='store_true', default=False, dest='western', help='Search western category')
   parser.add_argument("--non_h", action='store_true', default=False, dest='non_h', help='Search non_h category')
   parser.add_argument("--cosplay", action='store_true', default=False, dest='cosplay', help='Search cosplay category')
   parser.add_argument("--asianporn", action='store_true', default=False, dest='asianporn', help='Search asianporn category')
   parser.add_argument("--cate_misc", action='store_true', default=False, dest='cate_misc', help='Search misc category')
   parser.add_argument("--pagefilteroff", action='store_true', default=False, dest='pagefilteroff', help="Disable the pagefilter sorting the dankoubon in manga category, this filter's default is ON while users ONLY SEARCH manga category and would automatically TURN OFF while search containing other categories")
   parser.add_argument("--imageset", action='store_true', default=False, dest="imageset", help="Search imageset category")
   parser.add_argument("--eh", action='store_true', default=False, dest='eh', help='Search the e-hentai instead of exhentai (do not require cookies, username and password)')
   parser.add_argument('-a', "--artist", action='append', dest='artist', default=[], help='Artist keyword')
   parser.add_argument('-g', "--group", action='append', dest='group', default=[], help='Group keyword')
   parser.add_argument("--male", action='append', dest='male', default=[], help="Male's tags")
   parser.add_argument("--parody", action='append', dest='parody', default=[], help="Parody's tags")
   parser.add_argument("--character", action='append', dest='character', default=[], help="Character's tags")
   parser.add_argument("--female", action='append', dest='female', default=[], help="Female's tags")
   parser.add_argument("--misc", action='append', dest='misc', default=[], help="Misc's tags")
   parser.add_argument("--username", action='store', dest='username', default="", type=str, help='Exploit username and password instead of cookies in the cfg file to login exh, however exploiting the cookies is recommended')
   parser.add_argument("--password", action='store', dest='password', default="", type=str, help='Exploit username and password instead of cookies in the cfg file to login exh, however exploiting the cookies is recommended')
   parser.add_argument("--proxy", action='store', dest='proxy', type=str, default="", help="Exploit proxy to access the site(example 'http://host:port'")
   parser.add_argument("--full_gallery", action='store_true', default=False, dest='fulgal', help='Let the xeH download the full gallery (might consume huge amount of date)')
   parser.add_argument("--rest", action='store', default="3-8", dest='rest', help='Pause between every request to simulate human active, defult is 3-8 sec(example 3 or 3-8)')
   parser.add_argument("--nopreviewimg", action='store_true', default=False, dest='nopreviewimg', help='Disable the preview image download function(if the net connection is unpromising, use this parament')
   parser.add_argument("--forcecookieseh", action='store_true', default=False, dest='forcecookieseh', help="Try to Exploit users' cookies to search e-h if this cookies could not search exh.")
   searchopt = parser.parse_args()
   return searchopt


def searchgenerate(generateDict):    
   searchopt = searchparser()
#    print (generateDict)
   if generateDict['userkey']:
      searchopt.keyword = generateDict['userkey']
   if 'non-h' in generateDict['usercate']:
      generateDict['usercate'].remove('non-h')
      generateDict['usercate'].append('non_h')
#    print (generateDict['usercate'])
   for gd in generateDict['usercate']:
      searchopt.__setattr__(gd, True)
   searchopt.pages = generateDict["userranges"]
   searchopt.pagefilteroff = True
   if generateDict["usercookies"] == None:
      searchopt.eh = True
   else:
      searchopt.eh = False
   searchopt.forcecookieseh = generalcfg.forceCookiesEH
   return searchopt








   