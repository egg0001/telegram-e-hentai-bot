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
    
def mangaanalysis(urls, mangasession, searchopt, logger, path):
   mangasession = mangasession
   urlSeparateList = [] # separate urls (list) to sublist containing 24 urls in each element
   tempList = [] # store the API result from e-h/exh
   tempDict = {} # transfer internal data
   mangaObjList = [] # Store the Manga objects
   executer = ThreadPoolExecutor(max_workers=3) # The ThreadPoolExecutor containing and running the preview image downloading 
                                                # threading.
   q = Queue() # store the image memory objects
   logger.info('Thread containor for downloading preview image initiated.')
   download.userfiledetect(path=path)
   with open("{0}.mangalog".format(path), "r") as fo:
      mangaDict =  json.load(fo)
   discardUrls = 0
   for url in mangaDict:   # Rule out the redundant gerally
      #    print (url)
      try:
         urls.remove(url)
         discardUrls += 1
      except ValueError:
         continue
   logger.info('Discarded {0} redundant gallery(s)'.format(discardUrls))
   subUrlList = []
   internalCounter = 0
   for url in urls:
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
                                               mangasession=mangasession,
                                               stop=apiStop,
                                               urls=usl,
                                                  searchopt=searchopt,
                                               logger=logger
                                              )
                     )
      # print (tempList)
   logger.info("Retrived {0} gallery(s)' information by exploiting e-h api".format(len(tempList)))
   tempDict = datafilter.genmangainfoapi(resultJsonDict=tempList, searchopt=searchopt)
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
         mangaObjList.append(manga)
   logger.info('Filtered {0} gallery(s) containing uncomfortable tags'.format((len(tempList)-len(mangaObjList))))

   futureList = []
   for manga in mangaObjList:
      future = executer.submit(fn=download.previewImageDL, 
                               manga=manga,
                               mangasession=mangasession,
                               logger=logger,
                               q=q)
      futureList.append(future)
   for future in futureList:
      future.result()
   executer.shutdown()
   imageTempDict = {}  # Temporally store the image objs
   logger.info('All preview image download threads has completed.')
   while not q.empty():
      temp = q.get()
      imageTempDict.update(temp)
   logger.info('Image objects retrived.')
#    print (imageTempDict)
   for manga in mangaObjList:
      if imageTempDict.get(manga.url):
         manga.previewImageObj = imageTempDict[manga.url]
      else:
         manga.previewImageObj = None
   for manga in mangaObjList:
      mangaDict.update({manga.url: manga.mangaData})
   with open("{0}.mangalog".format(path), "w") as fo:
      json.dump(mangaDict, fo)
   return mangaObjList

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
   urls = generator.urlgenerate(searchopt)
   urlsdict = pagedownload(urls=urls, 
                           mangasession=mangasession, 
                           searchopt=searchopt, 
                           logger=logger, 
                           path=path)
   analysisUrls = list(urlsdict.values())
   mangaObjList = mangaanalysis(urls=analysisUrls, 
                                mangasession=mangasession, 
                                searchopt=searchopt, 
                                logger=logger, 
                                path=path)
   spiderDict[sd]["usercookies"] = requests.utils.dict_from_cookiejar(mangasession.cookies)
   cookiesUpdateDict = {sd: spiderDict[sd]}
   datastore(userdict=cookiesUpdateDict, fromSpider=True)
   del mangasession
   logger.info('Search completed.')
   return mangaObjList


      
