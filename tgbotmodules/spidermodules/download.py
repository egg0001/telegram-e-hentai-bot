#!/usr/bin/python3


import os
import requests
import time
import json
from PIL import Image
import io
import re
import random
from . import generalcfg
from . import generator



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
      

def previewImageDL(mangaUrl, mangaInfo, mangasession, logger, q, threadQ):
   logger.info('Begin to retrive preview image of {0}.'.format(mangaUrl))
   if mangaInfo["jptitle"]:
      title = mangaInfo["jptitle"][0]
   elif mangaInfo["entitle"]:
      title = mangaInfo["entitle"]
   else:
      title = ""
   previewimg = {'imageurlSmall': mangaInfo["imageurlSmall"], 
                 'imageForm': mangaInfo["imageForm"], 
                 'title': title,
                 'imageurlBig': '',
                 'imageurlBigReload': '',
                 'mangaUrl': mangaUrl}
   if generalcfg.dlFullPreviewImage == True:
      imagePatternBig = re.compile(r'''href="(https://[a-z-]+\.org/[a-z0-9]/[a-z0-9]+/[a-z0-9]+\-1)"''')
      tdHtmlContent = accesstoehentai(method='get',
                                      mangasession=mangasession,
                                      stop=generator.Sleep(2),
                                      urls=[mangaUrl],
                                      logger=logger)
      
      imageMatchBig = imagePatternBig.search(tdHtmlContent[0])
      if imageMatchBig:
         previewimg.update({'imageurlBig': imageMatchBig.group(1)})
      imageDict = previewDlToMemoryBig(previewimg=previewimg, mangasession=mangasession, logger=logger)
   else:
      imageDict = previewdltomenory(previewimg=previewimg, mangasession=mangasession, logger=logger)
   imageDict = {mangaUrl: imageDict}
   q.put(imageDict)
   threadQ.task_done()

   
      


def accesstoehentai(method, mangasession, stop, logger, urls=None, searchopt=None):
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
            #    if searchopt.eh == True:
               r = mangasession.post('https://api.e-hentai.org/api.php', json=ii)
            #    else:
            #       r = mangasession.post('https://api.exhentai.org/api.php', json=ii)
               mangaDictMeta = r.json()
               resultList.extend(mangaDictMeta['gmetadata'])
         except Exception as error:
            logger.error('Encountered an error while access e-h/exh - {0}'.format(str(error)))
            err += 1
            generator.Sleep.Havearest(stop)
         else:
            generator.Sleep.Havearest(stop)
            err = 0
            break
      else:
         logger.error('Retry limitation reached {0} times, discarded'.format(generalcfg.dlRetry))
         err = 0
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
            contentTypeList = previewimage.headers['Content-Type'].split('/')
            previewimg['imageForm'] = contentTypeList[1]
            if previewimg['imageForm'] == ('jpg' or 'JPG'):
               previewimg.update({'imageForm': 'jpeg'})
            previewimg.update({'filename': '{0}.{1}'.format(previewimg['title'], previewimg['imageForm'])})
            if len(previewimage.content) != int(previewimage.headers['content-length']):
               raise jpegEOIError('Image is corrupted.')
            i = Image.open(io.BytesIO(previewimage.content))
            bio = io.BytesIO()
            bio.name = previewimg['filename']
            i.save(bio)
            imageDict = {previewimg['filename']: bio}
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

   return imageDict


def previewdltomenory(previewimg, mangasession, logger):
   imageDict = {}
   if previewimg['imageForm']:
      pass
   else:
      previewimg['imageForm'] = 'jpg'
   if previewimg['imageurlSmall']:

      imageDict = imageDownload(previewimg=previewimg,
                                mangasession=mangasession,
                                logger=logger
                                )
   else:
      pass
   return imageDict

def previewDlToMemoryBig(previewimg, mangasession, logger):
   imageDict = {}
   if previewimg['imageForm']:
      pass
   else:
      previewimg['imageForm'] = 'jpg'
   if previewimg['imageurlBig']:
      imageDict = imageDownload(previewimg=previewimg,
                                mangasession=mangasession,
                                logger=logger,
                                fromBig=True
                               )
   else:
      pass
   if imageDict:
      pass
   elif previewimg['imageurlSmall']:
      logger.warning('Download full preview image of {0} failed, try to download small image.'.format(previewimg['mangaUrl']))
      imageDict = imageDownload(previewimg=previewimg,
                                mangasession=mangasession,
                                logger=logger
                                )
   else:
      pass
   return imageDict
   
      
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
