#!/usr/bin/python3


import requests
from tgbotmodules.spidermodules import generalcfg
from tgbotmodules.spidermodules import datafilter
from tgbotmodules.spidermodules import generator
from tgbotmodules.spidermodules import ehlogin
from tgbotmodules.spidermodules import download
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from queue import Queue
import re
import argparse
import json
import random
import time

class Manga():
   __slots__ = ('url', 'title', 'mangaData', 'previewImageObj', 'imageUrlSmall')
      
def pagedownload(urls, mangasession, searchopt, logger, path=None):
   mangasession = mangasession
   stop = generator.Sleep(sleepstr=searchopt.rest)
   urlsdict = {}
   tempList = download.accesstoehentai(method='get', 
                                       mangasession=mangasession,
                                       stop=stop,
                                       urls=urls,
                                       logger=logger)
   if tempList:
      for tl in tempList:
         urlsdict.update(datafilter.Grossdataspider(htmlcontent=tl))
   logger.info("Retrived {0} gallery(s) urls".format(len(urlsdict)))
   return urlsdict
    
class urlAnalysis():
   def __init__(self, urls, path, mangasession, searchopt, logger):
      self.urls = urls
      self.path = path
      self.futureList = []
      self.mangaObjList=[]
      self.mangasession = mangasession
      self.logger = logger
      self.searchopt = searchopt

   def mangaAnalysis(self, executer, q):

      urlSeparateList = [] # separate urls (list) to sublist containing 24 urls in each element
      tempList = [] # store the API result from e-h/exh
      tempDict = {} # transfer internal data
      mangaObjList = [] # Store the Manga objects
 
                                                # threading.

      self.logger.info('Thread containor for downloading preview image initiated.')
      download.userfiledetect(path=self.path)
      with open("{0}.mangalog".format(self.path), "r") as fo:
         mangaDict =  json.load(fo)
      discardUrls = 0
      for url in mangaDict:   # Rule out the redundant gerally
         #    print (url)
         try:
            self.urls.remove(url)
            discardUrls += 1
         except ValueError:
            continue
      self.logger.info('Discarded {0} redundant gallery(s)'.format(discardUrls))
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
         tempList.extend(download.accesstoehentai(method='post', 
                                                  mangasession=self.mangasession,
                                                  stop=apiStop,
                                                  urls=usl,
                                                  logger=self.logger
                                                 )
                        )
      # print (tempList)
      self.logger.info("Retrived {0} gallery(s)' information by exploiting e-h api".format(len(tempList)))
      tempDict = datafilter.genmangainfoapi(resultJsonDict=tempList, searchopt=self.searchopt)
      for url in tempDict:
         manga = Manga()
         addToObj = False
         if generalcfg.noEngOnlyGallery == False:
            addToObj = True
         elif generalcfg.noEngOnlyGallery == True and (tempDict[url]["jptitle"] or (not any(lang in tempDict[url]["lang"] for lang in generalcfg.langkeys))):
            addToObj = True
         else:
            addToObj = False
         if addToObj == True:
            if generalcfg.useEngTitle == False and tempDict[url]["jptitle"]:
               title = tempDict[url]["jptitle"][0]
            else: 
               title = tempDict[url]["entitle"][0]
            manga.title = title
            manga.imageUrlSmall = tempDict[url]["imageurlSmall"]
            del tempDict[url]["imageurlSmall"]
            manga.mangaData = tempDict[url]
            manga.url = url
            self.mangaObjList.append(manga)
      self.logger.info('Filtered {0} gallery(s) containing uncomfortable tags'.format((len(tempList)-len(mangaObjList))))
      for manga in self.mangaObjList:
         future = executer.submit(fn=download.previewImageDL, 
                                  manga=manga,
                                  mangasession=self.mangasession,
                                  logger=self.logger,
                                  q=q)
         self.futureList.append(future)



def mangaSpider(urls, mangasession, searchopt, logger, path=None):
   mangaDict={}
   urlanalysis = urlAnalysis(urls=urls,path=path,mangasession=mangasession,searchopt=searchopt,logger=logger)
   executer = ThreadPoolExecutor(max_workers=generalcfg.dlThreadLimit)
   q = Queue() # store the image memory objects
   urlanalysis.mangaAnalysis(executer=executer,q=q) # The ThreadPoolExecutor containing and running the preview image downloading
   for future in urlanalysis.futureList:
      future.result()
   executer.shutdown()
   imageTempDict = {}  # Temporally store the image objs
   logger.info('All preview image download threads has completed.')
   while not q.empty():
      temp = q.get()
      imageTempDict.update(temp)
   logger.info('Image objects retrived.')
#    print (imageTempDict)
   for manga in urlanalysis.mangaObjList:
      if imageTempDict.get(manga.url):
         manga.previewImageObj = imageTempDict[manga.url]
      else:
         manga.previewImageObj = None
   for manga in urlanalysis.mangaObjList:
      mangaDict.update({manga.url: manga.mangaData})
   with open("{0}.mangalog".format(path), "w") as fo:
      json.dump(mangaDict, fo)
   return urlanalysis.mangaObjList

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

def Sessiongenfunc(searchopt, cookies, logger):
   mangasession = requests.Session()
   if generalcfg.headers:
      mangasession.headers.update(random.choice(generalcfg.headers))
   else:
      mangasession.headers.update({{"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",}})
   if generalcfg.proxy:
      # proxypattern = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5})")
      # proxy = proxypattern.search(random.choice(generalcfg.proxy)).group(1)
      if generalcfg.proxy[0].find('socks5://') != -1:
         proxy = generalcfg.proxy[0].replace('socks5://', 'socks5h://')
      else:
         proxy = generalcfg.proxy[0]
      proxies = {"http": proxy, "https": proxy,}
      # print (proxies)
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
   logger.info('Requests session generated.')
   return mangasession

def Spidercontrolasfunc(searchopt, cookies, path, logger, datastore, spiderDict, sd):
   mangasession = Sessiongenfunc(searchopt=searchopt, 
                                 cookies=cookies,
                                 logger=logger)
   searchUrls = generator.urlgenerate(searchopt)
   urlsdict = pagedownload(urls=searchUrls, 
                           mangasession=mangasession, 
                           searchopt=searchopt, 
                           logger=logger, 
                           path=path)
   urls = list(urlsdict.values())
   mangaObjList = mangaSpider(urls=urls,
                              mangasession=mangasession,
                              searchopt=searchopt,
                              logger=logger,
                              path=path)
#    mangaObjList = mangaanalysis(urls=analysisUrls, 
#                                 mangasession=mangasession, 
#                                 searchopt=searchopt, 
#                                 logger=logger, 
#                                 path=path)
   spiderDict[sd]["usercookies"] = requests.utils.dict_from_cookiejar(mangasession.cookies)
   cookiesUpdateDict = {sd: spiderDict[sd]}
   datastore(userdict=cookiesUpdateDict, fromSpider=True)
   del mangasession
   logger.info('Search completed.')
   return mangaObjList


      
