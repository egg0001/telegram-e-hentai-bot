#!/usr/bin/python3


import os
import requests
import time
import json
import io
import re
import random
from . import generalcfg
from . import generator
from .theLogger import loggerGene



def userfiledetect(path):
   if os.path.exists(path) == False:
      os.makedirs(path, exist_ok=True)
      userdict = {}
      with open("{0}.mangalog".format(path), 'w') as fo:
         json.dump(userdict, fo)
   elif os.path.isfile("{0}.mangalog".format(path)) == False:
      userdict = {}
      with open("{0}.mangalog".format(path), 'w') as fo:
         json.dump(userdict, fo)
   else:
      with open("{0}.mangalog".format(path), 'r') as fo:
         try:
            usersdict = json.load(fo)
         except json.decoder.JSONDecodeError:
            broken_file = os.path.join(path, '.mangalog')
            bkm = 'userdata.broken.TIME'
            backup_file_name = bkm.replace('TIME', str(time.asctime(time.localtime())))
            backup_file_name = backup_file_name.replace(":", ".")
            backup_file = os.path.join(path, backup_file_name)
            os.rename(broken_file, backup_file)
            userdict = {}
            with open("{0}.mangalog".format(path), 'w') as fo:
               json.dump(userdict, fo)
         else:
            pass
      

def previewImageDL(manga, mangasession, logger, q):
   logger.info('Begin to retrive preview image of {0}.'.format(manga.url))
#    if mangaInfo["jptitle"]:
#       title = mangaInfo["jptitle"][0]
#    elif mangaInfo["entitle"]:
#       title = mangaInfo["entitle"]
#    else:
#       title = ""
   previewimg = {'imageurlSmall': manga.imageUrlSmall,
                 'title': manga.title,
                 'imageurlBig': '',
                 'imageurlBigReload': '',
                 'mangaUrl': manga.url}
   if generalcfg.dlFullPreviewImage == True:
      imagePatternBig = re.compile(r'''href="(https://[a-z-]+\.org/[a-z0-9]/[a-z0-9]+/[a-z0-9]+\-1)"''')
      tdHtmlContent = accesstoehentai(method='get',
                                      mangasession=mangasession,
                                      stop=generator.Sleep(2),
                                      urls=[manga.url],
                                      logger=logger)
      
      imageMatchBig = imagePatternBig.search(tdHtmlContent[0])
      if imageMatchBig:
         previewimg.update({'imageurlBig': imageMatchBig.group(1)})
      bio = imageDownload(previewimg=previewimg, mangasession=mangasession, logger=logger, fromBig=True)
   else:
      bio = imageDownload(previewimg=previewimg, mangasession=mangasession, logger=logger)
   imageDict = {manga.url: bio}
#    print (imageDict)
   q.put(imageDict)

         
      


def retryDocorator(func, logger=loggerGene(), retry=generalcfg.timeoutRetry):
   '''This simple retry decorator provides a try-except looping to the accesstoehentai function for
      overcoming network fluctuation.'''
   def wrapperFunction(*args, **kwargs):
      err = 0 
      for err in range(retry):
         try:
            resultList = func(*args, **kwargs)
            break
         except Exception as error:
           err += 1
           logger.warning(str(error))
      else:
         logger.warning('Retry limitation reached')
         resultList = []
      return resultList
   return wrapperFunction

@retryDocorator
def accesstoehentai(method, mangasession, stop, logger, urls=None):
   ''' Most of the parts of the  program would use this function to retrive the htmlpage, and galleries'
       information by using e-h's API. It provides two methods to access e-hentai/exhentai. The GET 
       methot would return the htmlpage; and the POST method would extract the gallery ID and gallery
       key to generate the json payload sending exploit e-h's API then return the API's result.'''
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
      if method == 'get':
         r = mangasession.get(ii)
         resultList.append(r.text)
      else:
         r = mangasession.post('https://api.e-hentai.org/api.php', json=ii)
         mangaDictMeta = r.json()
         resultList.extend(mangaDictMeta['gmetadata'])
   return resultList


def imageDownload(mangasession, previewimg, logger, fromBig=False):

   err = 0
   imageDict = {}
   if fromBig == True:
      logger.info('Begin to download full preview image of {0}.'.format(previewimg['mangaUrl']))
   else:
      logger.info('Begin to download small preview image of {0}.'.format(previewimg['mangaUrl']))
   for err in range(generalcfg.dlRetry):
      try:
         if fromBig == True:
            if err != 0 and previewimg['imageurlBigReload']:
               r = mangasession.get(previewimg['imageurlBigReload'])
            else:
               r = mangasession.get(previewimg['imageurlBig'])
            downloadUrlsDict = mangadlhtmlfilter(htmlContent=r.text, url=previewimg['imageurlBig'])
            previewimg.update({'imageurlBigReload': downloadUrlsDict['reloadUrl']})
            if downloadUrlsDict['imageUrl']:
               previewimgUrl = downloadUrlsDict['imageUrl']
            else:
               previewimgUrl = previewimg['imageurlSmall']
         else:
            logger.warning('Could not retrive full image downloading url of {0}, try to download small one.'.format(previewimg['mangaUrl']))
            previewimgUrl = previewimg['imageurlSmall']
         previewimage = mangasession.get(previewimgUrl)
         if previewimage.status_code == 200:
            bio = io.BytesIO(previewimage.content)
            bio.name = previewimg['title']
            if bio.getbuffer().nbytes != int(previewimage.headers['content-length']):
               raise jpegEOIError('Image is corrupted.')            
         else:
            raise downloadStatusCodeError('Error status code.')
      except Exception as error:
         logger.error('Encountered an error while downloading image {0} - {1}'.format(previewimg['mangaUrl'], str(error)))
         err += 1
         time.sleep(0.5)
      else:
         err = 0
         break    
   else:
      err = 0
      logger.error('Error limitation while download {0} is reached, stop this thread.'.format(previewimg['mangaUrl']))
      bio = None
   return bio
      
def mangadlhtmlfilter(htmlContent, url):
   downloadUrlsDict = {'imageUrl': "", 'reloadUrl': ''}
   imagePattern = re.compile('''<img id="img" src="(http://.+)" style="''')
   matchUrls = imagePattern.search(htmlContent)
   reloadPattern = re.compile(r'''id\=\"loadfail\" onclick\=\"return nl\(\'([0-9\-]+)\'\)\"''')
   reloadUrl = reloadPattern.search(htmlContent)
   if matchUrls:                     # This block still has some strange issues..... 
      downloadUrlsDict['imageUrl'] = matchUrls.group(1)
   if reloadUrl:
      downloadUrlsDict['reloadUrl'] = '{0}?nl={1}'.format(url, reloadUrl.group(1))
   return downloadUrlsDict  

#-------------Several personalized Exceptions----------------------

class jpegEOIError(Exception):
   pass

class htmlPageError(Exception):
   pass

class downloadStatusCodeError(Exception):
   pass
