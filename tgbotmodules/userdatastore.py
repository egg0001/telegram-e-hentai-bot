#!/usr/bin/env python

import json
from ast import literal_eval
import os
import time


def userfiledetect():
   '''By exploiting this function, other parts of the program would detect the status of the  
      file storing the users' information. If this file does not exist or corrupted, this 
      function would create a brand new file and backup the broken file (if has) for further
      analysis.'''
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

def datastore(userdict, fromSpider=False):
   '''The user data store function containing in the tgbotconvhandler would exploit this function
      to store the user information/settings in to the file. and the program would exploit the 
      information in this file to search e-h/exh recursively. Moreover, the spider would also 
      exploit this function to store the most updated user cookies.'''
   IOreportdict = {'issaved': False, 'nosamename': True,}

   with  open('./userdata/userdata', 'r') as fo:
      Usersdict = json.load(fo)
   if fromSpider == False:
      for usd in Usersdict:
         if usd == list(userdict.keys())[0]:
         
            IOreportdict['nosamename'] = False
   else:
      pass
   if IOreportdict['nosamename'] == True:  
      Usersdict.update(userdict)
      with  open('./userdata/userdata', 'w') as fo:
         json.dump(Usersdict, fo)
      IOreportdict['issaved'] = True
   return IOreportdict

def dataretrive(actusername):   #must use actual username
   '''By providing the real telegram username, this function would return all the virtual
      username containing this actual username.'''
   with open('./userdata/userdata', 'r') as fo:
      retrivedata = json.load(fo)
   userdata = {}
   for rd in retrivedata.items():     
      if rd[1]['actualusername'] == actusername:
         userdata.update({rd[0]: rd[1],})

   return userdata

def datadelete(virusername):   #must input virtual username
   '''By providing a virtual username, this function would delete the information of this
      virtual username.'''
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
   '''The spiderfunction would exploit this function to retrive all the user information
      from file preparing to search.'''
   spiderInfoDict = {}
   userfiledetect()
   with open('./userdata/userdata', 'r') as fo:
      spiderInfoDict.update(json.load(fo))
   return spiderInfoDict
    