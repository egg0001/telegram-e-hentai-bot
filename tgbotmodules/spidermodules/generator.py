#!/usr/bin/python3

from . import generalcfg
import time
import random

def urlgenerate(searchopt):  #put this function to the specify module later
   SearchKey = searchopt.keyword  # The general keywords 
   searchcatedict = {"&f_doujinshi=1": searchopt.doujinshi,
                     "&f_manga=1": searchopt.manga,
                     "&f_artistcg=1": searchopt.artistcg,
                     "&f_gamecg=1": searchopt.gamecg,
                     "&f_western=1": searchopt.western,
                     "&f_non-h=1": searchopt.non_h,
                     "&f_cosplay=1": searchopt.cosplay,
                     "&f_asianporn=1": searchopt.asianporn,
                     "&f_misc=1": searchopt.cate_misc,
                     "f_imageset=1": searchopt.imageset,
                    }



   if searchopt.artist:
      for a in searchopt.artist:
         SearchKey = SearchKey + "+artist:" + a
   
   if searchopt.group:
      for g in searchopt.group:
         SearchKey = SearchKey + "+group:" + g
   
   if searchopt.parody:
      for p in searchopt.parody:
         SearchKey = SearchKey + "+parody:" + p

   if searchopt.character:
      for c in searchopt.character:
         SearchKey = SearchKey + "+character:" + c
   
   if searchopt.male:
      for m in searchopt.male:
         SearchKey = SearchKey + "+male:" + m

   if searchopt.female:
      for f in searchopt.female:
         SearchKey = SearchKey + "+female:" + f
      
   if searchopt.misc:
      for mi in searchopt.misc:
         SearchKey = SearchKey + "+misc:" + mi

   if searchopt.eh == False:
      inputurl = "https://exhentai.org/?page=%d"
   else:
      inputurl = "https://e-hentai.org/?page=%d"

   for searchcate in searchcatedict.items():
      if searchcate[1] == True:
         inputurl = inputurl + searchcate[0]

   inputurl = inputurl + "&f_search=KEY&f_apply=Apply+Filter"
   if searchopt.eh == True:
      inputurl = inputurl +'&inline_set=dm_t'
   inputurl_list = [inputurl.replace("KEY", SearchKey) % i for i in range(searchopt.pages)]
   return inputurl_list
   
   
def shgenerate(outputdict, searchopt):
   fo = open("forxeH.sh", "w")
   xeh = "xeH "
   if len(searchopt.username) != 0 and  len(searchopt.password) !=0:
      xeh = xeh + "-u '" + searchopt.username + "' " + "-k '" + searchopt.password + "' "
   if len(searchopt.proxy) != 0:
      xeh = xeh + "--proxy '" + searchopt.proxy + "' "
   elif len(generalcfg.proxy) != 0:
      xeh = xeh + "--proxy '" + generalcfg.proxy + "' "
   if searchopt.fulgal == False:
      xeh = xeh + "--download-range " + "'1' "
   urls = outputdict.values()
   for u in urls:
      xeh = xeh + u + " "
   fo.write(xeh)
   fo.write("\n")
   parelist = outputdict.items()
   for pare in parelist:
      fo.write("#" + pare[1] + ' ')
      fo.write(pare[0])
      fo.write("\n")
   fo.close()
   return


   
   
class Sleep():   #Just a sleep function
   minsleep = 0
   maxsleep = 0
   def __init__(self, sleepstr):
      self.sleepstr = str(sleepstr)
      if self.sleepstr.find("-") != -1:
         sleeptime = self.sleepstr.split("-")
         Sleep.minsleep = int(sleeptime[0])
         Sleep.maxsleep = int(sleeptime[1])
      else:
         Sleep.minsleep = int(self.sleepstr)
         Sleep.maxsleep = int(self.sleepstr)
   
   def Havearest(self):
      time.sleep(random.uniform(Sleep.minsleep, Sleep.maxsleep))
