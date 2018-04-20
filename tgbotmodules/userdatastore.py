#!/usr/bin/env python

import json
from ast import literal_eval
import os
import time


def userfiledetect():
   statusdict = {'isfile': True, 'iscorrect': True,}
   if os.path.exists("./userdata") == False:
      os.mkdir("./userdata")
      statusdict['isfile'] = False
      userdict = {}
      with open('./userdata/userdata', 'w') as fo:
         json.dump(userdict, fo)

   elif os.path.isfile('./userdata/userdata') == False:
      statusdict['isfile'] = False
      userdict = {}
      with open('./userdata/userdata', 'w') as fo:
         json.dump(userdict, fo)
   else:
      pass
   with open('./userdata/userdata', 'r') as fo:
         try:
            usersdict = json.load(fo)
         except json.decoder.JSONDecodeError:
            statusdict['iscorrect'] = False
            broken_file = os.path.join('./userdata', 'userdata')
            bkm = 'userdata.broken.TIME'
            backup_file_name = bkm.replace('TIME', str(time.asctime(time.localtime())))
            backup_file_name = backup_file_name.replace(":", ".")
            backup_file = os.path.join('./userdata', backup_file_name)
            os.rename(broken_file, backup_file)
            userdict = {}
            with open('./userdata/userdata', 'w') as fo:
               json.dump(userdict, fo)

   return statusdict

def datastore(userdict):

   IOreportdict = {'issaved': False, 'nosamename': True,}

   with  open('./userdata/userdata', 'r') as fo:
      Usersdict = json.load(fo)
      
   for usd in Usersdict:
      if usd == list(userdict.keys())[0]:
         
         IOreportdict['nosamename'] = False

   if IOreportdict['nosamename'] == True:  
      Usersdict.update(userdict)
      with  open('./userdata/userdata', 'w') as fo:
         json.dump(Usersdict, fo)
      IOreportdict['issaved'] = True
         # IOreport = "Usersdata file was updated successfully."
   return IOreportdict

def dataretrive(actusername):   #must use actual username

   with open('./userdata/userdata', 'r') as fo:
      retrivedata = json.load(fo)
   userdata = {}
   for rd in retrivedata.items():     
      if rd[1]['actualusername'] == actusername:
         userdata.update({rd[0]: rd[1],})

   return userdata

def datadelete(virusername):   #must input virtual username
   IOreportdict = {'isdelete': False, 'hasdata': True}
   with open('./userdata/userdata', 'r') as fo:
      retrivedata = json.load(fo)
   try:
      del retrivedata[virusername]
   except KeyError:
      IOreportdict['hasdata'] = False
   else:
      with open('./userdata/userdata', 'w') as fo:
         json.dump(retrivedata, fo)
         IOreportdict['isdelete'] = True
   return IOreportdict

def getspiderinfo():
   spiderInfoDict = {}
   userfiledetect()
   with open('./userdata/userdata', 'r') as fo:
      spiderInfoDict.update(json.load(fo))
   return spiderInfoDict
    