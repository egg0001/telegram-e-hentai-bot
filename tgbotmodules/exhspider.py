#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from tgbotmodules.spidermodules import generalcfg
from tgbotmodules.spidermodules import datafilter
from tgbotmodules.spidermodules import generator
from tgbotmodules.spidermodules import ehlogin
from tgbotmodules.spidermodules import download
import re
import argparse
import json
import random
import time

class MangaSpider():
   def __init__(self, urls, mangasession, stop, searchopt, path=None):
      self.urls=urls #list
      self.mangasession = mangasession #obj
      self.searchopt = searchopt
      self.stop = stop #Pause obj
      self.path = path

         
   
   def pagedownload(self):
      mangasession = self.mangasession
      urlsdict = {}
      for url in self.urls: 
         
         r = mangasession.get(url)
         htmlcontent = r.text
         urlsdict.update(datafilter.Grossdataspider(htmlcontent=htmlcontent, 
                                                    searchopt=self.searchopt))
      #    print (urlsdict)
         print ("Now have a rest")
         generator.Sleep.Havearest(self.stop)
         print ("Continue")
      return urlsdict
      
   def mangaanalysis(self):
      mangasession = self.mangasession
      outDict = {}# return the information
      strList = [] # contain the message strs.
      strDict = {} #For generate information to the user
      userInfoDict = {} # Dump information to file
      imageObjDict = {} # Get the image objects 
      download.userfiledetect(path=self.path)
      with open("{0}.mangalog".format(self.path), "r") as fo:
         mangaDict =  json.load(fo)
      for url in mangaDict:   # Rule out the redundant gerally
         print (url)
         try:
            self.urls.remove(url)
         except ValueError:
            pass
         else:
            print ("{0} is redundant, discard.".format(url))
      for url in self.urls:
         r = mangasession.get(url)
         htmlcontent = r.text
         tempdict = datafilter.genmangainfo(htmlcontent=htmlcontent, 
                                            url=url, 
                                            searchopt=self.searchopt, 
                                            mangasession=mangasession,
                                            path=self.path)

         if tempdict:
            if tempdict[url]:
               print (tempdict)
               if tempdict[url].get("jptitle") != None:
                  outjptitle = tempdict[url].get("jptitle")[0]
                  strDict.update({outjptitle: url})
                  imageObjDict.update(tempdict["imageDict"])
                  del tempdict["imageDict"]
                  print ("----------jptitle updated----------")
                  userInfoDict.update(tempdict)
               elif generalcfg.noEngOnlyGallery == False:   # Say goodbye to all mind fucking English galleries.
                  if tempdict[url].get("entitle") != None:
                     outentitle = tempdict[url].get("entitle")[0]
                     strDict.update({outentitle: url})
                     imageObjDict.update(tempdict["imageDict"])
                     del tempdict["imageDict"]
                     print ("----------entitle updated----------")
                     userInfoDict.update(tempdict)
                  else:
                     pass
               else: 
                  pass
            else:
               pass 
         else:
            pass  
         print ("Now have a rest")
         generator.Sleep.Havearest(self.stop)
         print ("Continue")
      if strDict:
         outStr = ""
         internalCount = 0
         for key in strDict:  #Separate the result strings to be more appealing
            outStr += "{0} \n{1}\n ".format(key, strDict[key])
            internalCount += 1
            if internalCount == 7:
               outStr += '/././././././././' +"\n "
               internalCount = 0
         strList += outStr.split('/././././././././')
         outDict.update({"strList": strList, "imageObjDict": imageObjDict})
      mangaDict.update(userInfoDict)
      with open("{0}.mangalog".format(self.path), "w") as fo:
         json.dump(mangaDict, fo)
      return outDict
      
         



      

# def Sessiongen():
#    mangasession = requests.Session()
#    if len(generalcfg.headers) != 0:
#       mangasession.headers.update(generalcfg.headers)
#    else:
#       headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",}
#       mangasession.headers.update(headers)
#    proxypattern = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5})")
#    if len(searchopt.proxy) != 0:
#       proxy = proxypattern.search(searchopt.proxy).group(1)
#       proxies = {"http": proxy, "https": proxy,}
#       mangasession.proxies = proxies
#    elif len(generalcfg.proxy) != 0:
#       proxy = proxypattern.search(generalcfg.proxy).group(1)
#       proxies = {"http": proxy, "https": proxy,}
#       mangasession.proxies = proxies
#       print (proxies)
#    else:
#       pass
     
#    if searchopt.eh == False:
#       if len(searchopt.username) != 0 and len(searchopt.password) != 0:
#           mangasession = ehlogin.ehlogin(username=searchopt.username, 
#                                          password=searchopt.password,
#                                          mangasession=mangasession
#                                          )
                                               
#       else:                                                         
#          if generalcfg.cookies:
#             requests.utils.add_dict_to_cookiejar(mangasession.cookies, generalcfg.cookies)
#          else:
#             print ("Required cookies to access exhentai")
#             quit()
#    else:
#       pass
#    return mangasession


def exhcookiestest(mangasessionTest, cookies, forceCookiesEH=False):   #Evaluate whether the cookies could access exh
   requests.utils.add_dict_to_cookiejar(mangasessionTest.cookies, cookies)
   usefulCookiesDict = {'e-h': False, 'exh': False}
   if forceCookiesEH == False:
      r = mangasessionTest.get("https://exhentai.org/")
      htmlContent = r.text
      usefulCookiesDict['exh'] = datafilter.exhtest(htmlContent=htmlContent)
      time.sleep(random.uniform(3,5))   
   else:
      r = mangasessionTest.get("https://exhentai.org/")
      htmlContent = r.text
      usefulCookiesDict['exh'] = datafilter.exhtest(htmlContent=htmlContent)
      time.sleep(random.uniform(3,5))
      if usefulCookiesDict['exh'] == False:
         r = mangasessionTest.get("https://e-hentai.org/")
         htmlContent = r.text
         usefulCookiesDict['e-h'] = datafilter.exhtest(htmlContent=htmlContent)      
         time.sleep(random.uniform(3,5))  # If access exh too fast, it would activate the anti-spider mechanism
      else: 
         pass
   return usefulCookiesDict



def Sessiongenfunc(searchopt, cookies):
   mangasession = requests.Session()
   if generalcfg.headers:
      mangasession.headers.update(random.choice(generalcfg.headers))
   else:
      mangasession.headers.update({{"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",}})
   if generalcfg.proxy:
      proxypattern = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5})")
      proxy = proxypattern.search(random.choice(generalcfg.proxy)).group(1)
      proxies = {"http": proxy, "https": proxy,}
      mangasession.proxies = proxies
   else:
      pass
   if cookies:
         forceCookiesEH = searchopt.forcecookieseh
         
         usefulCookiesDict = exhcookiestest(mangasessionTest=mangasession, 
                                            cookies=cookies, 
                                            forceCookiesEH=forceCookiesEH
                                           )
         if usefulCookiesDict['exh'] == True:
            requests.utils.add_dict_to_cookiejar(mangasession.cookies, cookies)
         elif usefulCookiesDict['exh'] == False and usefulCookiesDict['e-h'] == True:
            requests.utils.add_dict_to_cookiejar(mangasession.cookies, cookies)
            searchopt.eh = True
         else:
            searchopt.eh = True
   else:
      searchopt.eh = True
      requests.utils.add_dict_to_cookiejar(mangasession.cookies, {"sl": "dm_1"})
   return mangasession      


    
  


# def Spidercontrol(searchopt):
#    mangasession = Sessiongen()
#    stop = generator.Sleep(sleepstr=searchopt.rest)
#    print (mangasession.headers)
#    urls = generator.urlgenerate(searchopt)
#    manga = MangaSpider(urls=urls, 
#                        mangasession=mangasession, 
#                        stop=stop, 
#                        searchopt=searchopt)
#    urlsdict = MangaSpider.pagedownload(manga)
#    print (urlsdict)
#    analysisurls = urlsdict.values()
#    manga2 = MangaSpider(urls=analysisurls, 
#                         mangasession=mangasession, 
#                         searchopt=searchopt, 
#                         stop=stop, 
#                         path="./result/")
#    outDict = MangaSpider.mangaanalysis(manga2)
#    del outDict["imageObjDict"]
#    print (outDict)
#    generator.shgenerate(outputdict=outDict, searchopt=searchopt)
#    return

def Spidercontrolasfunc(searchopt, cookies, path):
   mangasession = Sessiongenfunc(searchopt=searchopt, 
                                 cookies=cookies)
   stop = generator.Sleep(sleepstr=searchopt.rest)
   urls = generator.urlgenerate(searchopt)
   manga = MangaSpider(urls=urls, 
                       mangasession=mangasession,
                       searchopt=searchopt, 
                       stop=stop
                      ) 
   urlsdict = MangaSpider.pagedownload(manga)
   analysisUrls = list(urlsdict.values())
   manga2 = MangaSpider(urls=analysisUrls, 
                        mangasession=mangasession,
                        searchopt=searchopt, 
                        stop=stop,
                        path=path
                       )
   outDict = MangaSpider.mangaanalysis(manga2)


   del mangasession
   return outDict




   

# def searchinfo():
#    parser = argparse.ArgumentParser(description='Search settings')
#    parser.add_argument('-k', "--keyword", action='store', dest='keyword', default="", type=str, help='General keywords (might contain unexpected result)')
#    parser.add_argument('-p', "--pages", action='store', dest='pages',default=5, type=int, help='Pages Limitation')
#    parser.add_argument('-d', "--doujin", action='store_true', default=False, dest='doujinshi', help='Search doujin category')
#    parser.add_argument('-m', "--manga", action='store_true', default=False, dest='manga', help='Search manga category')
#    parser.add_argument("--artistcg", action='store_true', default=False, dest='artistcg', help='Search artistcg category')
#    parser.add_argument("--gamecg", action='store_true', default=False, dest='gamecg', help='Search gamecg category')
#    parser.add_argument("--western", action='store_true', default=False, dest='western', help='Search western category')
#    parser.add_argument("--non_h", action='store_true', default=False, dest='non_h', help='Search non_h category')
#    parser.add_argument("--cosplay", action='store_true', default=False, dest='cosplay', help='Search cosplay category')
#    parser.add_argument("--asianporn", action='store_true', default=False, dest='asianporn', help='Search asianporn category')
#    parser.add_argument("--imageset", action='store_true', default=False, dest="imageset", help="Search imageset category")
#    parser.add_argument("--cate_misc", action='store_true', default=False, dest='cate_misc', help='Search misc category')
#    parser.add_argument("--pagefilteroff", action='store_true', default=False, dest='pagefilteroff', help="Disable the pagefilter sorting the dankoubon in manga category, this filter's default is ON while users ONLY SEARCH manga category and would automatically TURN OFF while search containing other categories")
#    parser.add_argument("--eh", action='store_true', default=False, dest='eh', help='Search the e-hentai instead of exhentai (do not require cookies, username and password)')
#    parser.add_argument('-a', "--artist", action='append', dest='artist', default=[], help='Artist keyword')
#    parser.add_argument('-g', "--group", action='append', dest='group', default=[], help='Group keyword')
#    parser.add_argument("--male", action='append', dest='male', default=[], help="Male's tags")
#    parser.add_argument("--parody", action='append', dest='parody', default=[], help="Parody's tags")
#    parser.add_argument("--character", action='append', dest='character', default=[], help="Character's tags")
#    parser.add_argument("--female", action='append', dest='female', default=[], help="Female's tags")
#    parser.add_argument("--misc", action='append', dest='misc', default=[], help="Misc's tags")
#    parser.add_argument("--username", action='store', dest='username', default="", type=str, help='Exploit username and password instead of cookies in the cfg file to login exh, however exploiting the cookies is recommended')
#    parser.add_argument("--password", action='store', dest='password', default="", type=str, help='Exploit username and password instead of cookies in the cfg file to login exh, however exploiting the cookies is recommended')
#    parser.add_argument("--proxy", action='store', dest='proxy', type=str, default="", help="Exploit proxy to access the site(example 'http://host:port'")
#    parser.add_argument("--full_gallery", action='store_true', default=False, dest='fulgal', help='Let the xeH download the full gallery (might consume huge amount of date)')
#    parser.add_argument("--rest", action='store', default="3-8", dest='rest', help='Pause between every request to simulate human active, defult is 3-8 sec(example 3 or 3-8)')
#    parser.add_argument("--nopreviewimg", action='store_true', default=False, dest='nopreviewimg', help='Disable the preview image download function(if the net connection is unpromising, use this parament')
#    parser.add_argument("--forcecookieseh", action='store_true', default=False, dest='forcecookieseh', help="Try to Exploit users' cookies to search e-h if this cookies could not search exh.")
#    searchopt = parser.parse_args()
#    return searchopt

# if __name__ == "__main__":
#    searchopt = searchinfo()
#    Spidercontrol(searchopt)


      
