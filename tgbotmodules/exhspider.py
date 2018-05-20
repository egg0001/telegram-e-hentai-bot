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
   def __init__(self, urls, mangasession, searchopt, path=None):
      self.urls=urls #list
      self.mangasession = mangasession #obj
      self.searchopt = searchopt
      self.path = path
   
   def pagedownload(self):
      mangasession = self.mangasession
      stop = generator.Sleep(sleepstr=self.searchopt.rest)
      urlsdict = {}
      tempList = accesstoehentai(method='get', 
                                 mangasession=self.mangasession,
                                 stop=stop,
                                 urls=self.urls)
      if tempList:
         for tl in tempList:
            urlsdict.update(datafilter.Grossdataspider(htmlcontent=tl))
      # print (urlsdict)
      return urlsdict
      
   def mangaanalysis(self):
      mangasession = self.mangasession
      urlSeparateList = [] # separate urls (list) to sublist containing 24 urls in each element
      tempList = []
      tempDict = {} # transfer internal data
      outDict = {}# return the information
      strList = [] # contain the message strs.
      strDict = {} #For generate information to the user
      userInfoDict = {} # Dump information to file
      imageObjDict = {} # Get the image objects 
      download.userfiledetect(path=self.path)
      with open("{0}.mangalog".format(self.path), "r") as fo:
         mangaDict =  json.load(fo)
      for url in mangaDict:   # Rule out the redundant gerally
      #    print (url)
         try:
            self.urls.remove(url)
         except ValueError:
            pass
         else:
            print ("{0} is redundant, discard.".format(url))
      subUrlList = []
      internalCounter = 0
      for url in self.urls:
         subUrlList.append(url)
         internalCounter += 1
         if (internalCounter %24 ) == 0:
            urlSeparateList.append(subUrlList)
            subUrlList = []
      if subUrlList:
         urlSeparateList.append(subUrlList)
      apiStop = generator.Sleep('2-3')
      for usl in urlSeparateList:
         tempList.extend(accesstoehentai(method='post', 
                                         mangasession=mangasession,
                                         stop=apiStop,
                                         urls=usl,
                                         searchopt=self.searchopt))
      # print (tempList)
      tempDict = datafilter.genmangainfoapi(resultJsonDict=tempList, searchopt=self.searchopt)
      for url in tempDict:
         imageDict = previewImageDL(mangaUrl=url, 
                                    mangaInfo=tempDict[url], 
                                    mangasession=mangasession)
                                    
      #    print (imageDict)
         tempDict[url].update({'imageDict': imageDict})
      #    print (tempDict[url])
      if tempDict:
         for url in tempDict:
            if tempDict[url]:
            #    print (tempDict)
               if tempDict[url]["jptitle"]:
                  outjptitle = tempDict[url].get("jptitle")[0]
                  strDict.update({outjptitle: url})
                  if tempDict[url]["imageDict"]:
                     imageObjDict.update(tempDict[url]["imageDict"])
                     del tempDict[url]["imageDict"]
                  else:
                     pass
                  #    print ("Image missed")
                  # print ("----------jptitle updated----------")
                  userInfoDict.update({url:tempDict[url]})
               elif generalcfg.noEngOnlyGallery == False or tempDict[url]['lang'] == None:   # Say goodbye to all mind fucking English galleries.
                  if tempDict[url].get("entitle") != None:
                     outentitle = tempDict[url].get("entitle")[0]
                     strDict.update({outentitle: url})
                     if tempDict[url]["imageDict"]:
                        imageObjDict.update(tempDict[url]["imageDict"])
                        del tempDict[url]["imageDict"]
                     else:
                        pass
                        # print ("Image missed")
                  #    print ("----------entitle updated----------")
                     userInfoDict.update({url:tempDict[url]})
                  else:
                     pass
               elif generalcfg.noEngOnlyGallery == True:
                  # print (tempDict)
                  if any(i in tempDict[url]['lang'] for i in generalcfg.langkeys):
                     pass
                  elif tempDict[url]["entitle"]:
                     outentitle = tempDict[url].get("entitle")[0]
                     strDict.update({outentitle: url})
                     if tempDict[url]["imageDict"]:
                        imageObjDict.update(tempDict[url]["imageDict"])
                        del tempDict[url]["imageDict"]
                     else:
                        pass
                        # print ("Image missed")
                  #    print ("----------entitle updated----------")
                     userInfoDict.update({url: tempDict[url]})
                  else:
                     pass
               else:
                  pass    
            else:
               pass 
         else:
            pass  
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

def previewImageDL(mangaUrl, mangaInfo, mangasession):
   if mangaInfo["jptitle"]:
      title = mangaInfo["jptitle"][0]
   elif mangaInfo["entitle"]:
      title = mangaInfo["entitle"]
   else:
      title = ""
   previewimg = {'imageurlSmall': mangaInfo["imageurlSmall"], 
                 'imageForm': mangaInfo["imageForm"], 
                 'title': title,
                 'imageurlBig': ''}
   if generalcfg.dlFullPreviewImage == True:
      imagePatternBig = re.compile(r'''href="(https://[a-z-]+\.org/[a-z0-9]/[a-z0-9]+/[a-z0-9]+\-1)"''')
      tdHtmlContent = accesstoehentai(method='get',
                                      mangasession=mangasession,
                                      stop=generator.Sleep(2),
                                      urls=[mangaUrl])
      
      imageMatchBig = imagePatternBig.search(tdHtmlContent[0])
      if imageMatchBig:
         previewimg.update({'imageurlBig': imageMatchBig.group(1)})
      imageDict = download.previewDlToMemoryBig(previewimg=previewimg, mangasession=mangasession)
   else:
      imageDict = download.previewdltomenory(previewimg=previewimg, mangasession=mangasession)
   return imageDict

   
      


def accesstoehentai(method, mangasession, stop, urls=None, searchopt=None):
#    print (urls)
   resultList = []
   if method == 'get':
      inputInfo = urls
   elif method == 'post':
      tokenPattern = re.compile(r'''https://.+\.org/g/([0-9a-z]+)\/([0-9a-z]+)\/''')
      mangaJsonPayload = {
                          "method": "gdata",
                          "gidlist": [],
                          "namespace": 1
                         }
      for url in urls:
         mangaTokenMatch = tokenPattern.search(url)
         mangaJsonPayload["gidlist"].append([mangaTokenMatch.group(1), mangaTokenMatch.group(2)])

      inputInfo = [mangaJsonPayload]
   else:
      inputInfo = ''
   for ii in inputInfo:
      err = 0
      for err in range(generalcfg.timeoutRetry):
         try:
            if method == 'get':
               r = mangasession.get(ii)
               resultList.append(r.text)
            else:
               if searchopt.eh == True:
                  r = mangasession.post('https://api.e-hentai.org/api.php', json=ii)
               else:
                  r = mangasession.post('https://api.exhentai.org/api.php', json=ii)
               mangaDictMeta = r.json()
               resultList.extend(mangaDictMeta['gmetadata'])
         except:
            err += 1
            generator.Sleep.Havearest(stop)
         else:
            generator.Sleep.Havearest(stop)
            err = 0
            break
      else:
         print ("network issue")
         err = 0
   return resultList
   

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
   return mangasession

def Spidercontrolasfunc(searchopt, cookies, path):
   mangasession = Sessiongenfunc(searchopt=searchopt, 
                                 cookies=cookies)
   urls = generator.urlgenerate(searchopt)
   manga = MangaSpider(urls=urls, 
                       mangasession=mangasession,
                       searchopt=searchopt
                      ) 
   urlsdict = MangaSpider.pagedownload(manga)
   analysisUrls = list(urlsdict.values())
   manga2 = MangaSpider(urls=analysisUrls, 
                        mangasession=mangasession,
                        searchopt=searchopt,
                        path=path
                       )
   outDict = MangaSpider.mangaanalysis(manga2)
   outDict.update({'cookiesDict': requests.utils.dict_from_cookiejar(mangasession.cookies)})
   del mangasession
   return outDict


      
