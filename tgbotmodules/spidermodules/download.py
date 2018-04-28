#!/usr/bin/python3


import os
import requests
import time
import json
from PIL import Image
import io
import re
from . import generalcfg



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
      
def Previewdl(url, mangasession, filename, path):


   os.makedirs(path, exist_ok=True)
   previewimage = mangasession.get(url, stream=True)
   handle = open("{0}{1}".format(path, filename), 'wb')
#    handle = open("./previewimage/FILENAME".replace('FILENAME', filename), "wb")
   for chunk in previewimage.iter_content(chunk_size=512):
      if chunk:
         handle.write(chunk)
   handle.close()
   return

def imageDownload(mangasession, previewimg, fromBig=False):
   err = 0
   imageDict = {}
   previewimgUrl = ""
   if fromBig == True:
      print ("Try to access the first image url in the gallery.")
      print (previewimg['imageurlBig'])
      time.sleep(1)
      for err in range(generalcfg.dlRetry):
         try:
            tempUrl = previewimg['imageurlBig']
            print (tempUrl)
            r = mangasession.get(tempUrl)
            print ("Accessed to the first page")
            print (r)
            htmlcontent = r.text
            print (htmlcontent)
            imagepattern = re.compile(r'''src=\"(http://[0-9:\.]+\/[a-zA-Z0-9]\/[a-zA-Z0-9-]+\/keystamp=[a-zA-Z0-9-]+;fileindex=[a-zA-Z0-9]+;xres=[a-zA-Z0-9]+\/.+\.[a-zA-Z]+)" style=''')
            matchUrls = imagepattern.search(htmlcontent)
            previewimgUrl = matchUrls.group(1)
            print (previewimgUrl)
         except:
            print ('Access error.')
            err += 1
            time.sleep(0.5)
         else:
            print ('Access complete.')
            print (previewimgUrl)
            time.sleep(0.5)
            err = 0
            break
      else:
         print ('Newwork issue')
         err = 0
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
#    previewimage = mangasession.get(previewimg['imageurlSmall'])
#    previewimage.content
#    i = Image.open(io.BytesIO(previewimage.content))
#    bio = io.BytesIO()
#    bio.name = previewimg['filename']
#    i.save(bio)
#    imageDict = {previewimg['filename']: bio}
   imageDict = imageDownload(previewimg=previewimg,
                             mangasession=mangasession
                             )
   return imageDict

def previewDlToMemoryBig(previewimg, mangasession):
#    previewImage= mangasession.get(previewimg['imageurlBig'])
#    htmlcontent = previewImage.text
#    imagepattern = re.compile(r"src=\"(http://[0-9:\.]+\/[a-z0-9]\/[a-z0-9-]+\/keystamp=[a-z0-9-]+;fileindex=[a-z0-9]+;xres=[0-9/]+\.[a-z]+)\"")
#    imageUrl = imagepattern.finditer(htmlcontent)
#    time.sleep(0.5)
#    previewimage = mangasession.get(imageUrl)
#    previewimage.content
#    i = Image.open(io.BytesIO(previewimage.content))
#    bio = io.BytesIO()
#    bio.name = previewimg['filename']
#    i.save(bio)
#    imageDict = {previewimg['filename']: bio}
   print ('This is big image download.')
   imageDict = imageDownload(previewimg=previewimg,
                             mangasession=mangasession,
                             fromBig=True
                            )
   if imageDict:
      pass
   else:
      imageDict = imageDownload(previewimg=previewimg,
                                mangasession=mangasession
                                )
   return imageDict
   
      
   

