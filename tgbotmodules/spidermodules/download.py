#!/usr/bin/python3


import os
import requests
import time
import json
from PIL import Image
import io



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

def previewdltomenory(url, mangasession, filename):
   fileNameList = filename.split(".")
   previewimage = mangasession.get(url)
   previewimage.content
   i = Image.open(io.BytesIO(previewimage.content))
   bio = io.BytesIO()
   bio.name = filename
   i.save(bio)
   imageDict = {filename: bio}
   return imageDict
   
   

