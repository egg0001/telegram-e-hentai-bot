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
      

def previewImageDL(mangaUrl, mangaInfo, mangasession, q):
#    print ('{0} image DL has started.'.format(mangaUrl))
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
      imageDict = previewDlToMemoryBig(previewimg=previewimg, mangasession=mangasession)
   else:
      imageDict = previewdltomenory(previewimg=previewimg, mangasession=mangasession)
   imageDict = {mangaUrl: imageDict}
   q.put(imageDict)

   
      


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


def imageDownload(mangasession, previewimg, fromBig=False):
   err = 0
   previewimg.update({'filename': '{0}.{1}'.format(previewimg['title'], previewimg['imageForm'])})
   imageDict = {}
   previewimgUrl = ""
   if fromBig == True:
      # print ("Try to access the first image url in the gallery.")
      # print (previewimg['imageurlBig'])
      time.sleep(random.uniform(1, 2))
      for err in range(generalcfg.dlRetry):
         try:
            tempUrl = previewimg['imageurlBig']
            # print (tempUrl)
            r = mangasession.get(tempUrl)
            # print ("Accessed to the first page")
            # print (r)
            htmlcontent = r.text
            # print (htmlcontent)
            imagepattern = re.compile(r'''src=\"(http://[0-9:\.]+\/[a-zA-Z0-9]\/[a-zA-Z0-9-]+\/keystamp=[a-zA-Z0-9-]+;fileindex=[a-zA-Z0-9]+;xres=[a-zA-Z0-9]+\/.+\.[a-zA-Z]+)" style=''')
            matchUrls = imagepattern.search(htmlcontent)
            previewimgUrl = matchUrls.group(1)
            # print (previewimgUrl)
         except:
            print ('Access error.')
            err += 1
            time.sleep(0.5)
         else:
            # print ('Access complete.')
            # print (previewimgUrl)
            time.sleep(0.5)
            err = 0
            break
      else:
         print ('Newwork issue')
         err = 0
         previewimgUrl = previewimg['imageurlSmall']
   else:
      previewimgUrl = previewimg['imageurlSmall']

   if previewimgUrl:
      for err in range(generalcfg.dlRetry):
         try:
            previewimage = mangasession.get(previewimgUrl)
            previewimage.content
            i = Image.open(io.BytesIO(previewimage.content))
            bio = io.BytesIO()
            bio.name = previewimg['filename']
            i.save(bio)
            imageDict = {previewimg['filename']: bio}
         except:
            err += 1
            time.sleep(0.5)
         else:
            err = 0
            break
      else:
         print ('Network issue')
         err = 0
   return imageDict


def previewdltomenory(previewimg, mangasession):
   imageDict = {}
   if previewimg['imageForm']:
      pass
   else:
      previewimg['imageForm'] = 'jpg'
   if previewimg['imageurlSmall']:

      imageDict = imageDownload(previewimg=previewimg,
                                mangasession=mangasession
                                )
   else:
      pass
   return imageDict

def previewDlToMemoryBig(previewimg, mangasession):
   imageDict = {}
   if previewimg['imageForm']:
      pass
   else:
      previewimg['imageForm'] = 'jpg'
   if previewimg['imageurlBig']:
      imageDict = imageDownload(previewimg=previewimg,
                                mangasession=mangasession,
                                fromBig=True
                               )
   else:
      pass
   if imageDict:
      pass
   elif previewimg['imageurlSmall']:
      imageDict = imageDownload(previewimg=previewimg,
                                mangasession=mangasession
                                )
   else:
      pass
   return imageDict
   
      
   

