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
                  if tempdict["imageDict"]:
                     imageObjDict.update(tempdict["imageDict"])
                     del tempdict["imageDict"]
                  else:
                     print ("Image missed")
                  print ("----------jptitle updated----------")
                  userInfoDict.update(tempdict)
               elif generalcfg.noEngOnlyGallery == False:   # Say goodbye to all mind fucking English galleries.
                  if tempdict[url].get("entitle") != None:
                     outentitle = tempdict[url].get("entitle")[0]
                     strDict.update({outentitle: url})
                     if tempdict["imageDict"]:
                        imageObjDict.update(tempdict["imageDict"])
                        del tempdict["imageDict"]
                     else:
                        print ("Image missed")
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


      
