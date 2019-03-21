#!/usr/bin/python3

from . import generalcfg
import time
import random

def urlgenerate(searchopt):  #put this function to the specify module later
   SearchKey = searchopt.keyword  # The general keywords 
   searchcatedict = {"doujinshi": searchopt.doujinshi,
                     "manga": searchopt.manga,
                     "artistcg": searchopt.artistcg,
                     "gamecg": searchopt.gamecg,
                     "western": searchopt.western,
                     "non-h": searchopt.non_h,
                     "cosplay": searchopt.cosplay,
                     "asianporn": searchopt.asianporn,
                     "misc": searchopt.cate_misc,
                     "imageset": searchopt.imageset,
                    }

   categoryValue = {'doujinshi': 2, 
                    'manga': 4,
                    'artistcg': 8,
                    'gamecg': 16,
                    'western': 512,
                    'non-h': 256,
                    'imageset': 32,
                    'cosplay': 64,
                    'asianporn': 128,
                    'misc': 1
                    }

   category = 1023
   for searchcate in searchcatedict.items():
      if searchcate[1] == True:
         category = category ^ categoryValue[searchcate[0]]



   # if searchopt.artist:
   #    for a in searchopt.artist:
   #       SearchKey = SearchKey + "+artist:" + a
   
   # if searchopt.group:
   #    for g in searchopt.group:
   #       SearchKey = SearchKey + "+group:" + g
   
   # if searchopt.parody:
   #    for p in searchopt.parody:
   #       SearchKey = SearchKey + "+parody:" + p

   # if searchopt.character:
   #    for c in searchopt.character:
   #       SearchKey = SearchKey + "+character:" + c
   
   # if searchopt.male:
   #    for m in searchopt.male:
   #       SearchKey = SearchKey + "+male:" + m

   # if searchopt.female:
   #    for f in searchopt.female:
   #       SearchKey = SearchKey + "+female:" + f
      
   # if searchopt.misc:
   #    for mi in searchopt.misc:
   #       SearchKey = SearchKey + "+misc:" + mi

   if searchopt.eh == False:
      inputurl = "https://exhentai.org/?page=%d&f_cats={0}&f_search={1}&f_apply=Apply+Filter"
   else:
      inputurl = "https://e-hentai.org/?page=%d&f_cats={0}&f_search={1}&f_apply=Apply+Filter"



   # inputurl = inputurl + "&f_search=KEY&f_apply=Apply+Filter"
   # if searchopt.eh == True:
   #    inputurl = inputurl +'&inline_set=dm_t'
   inputurl_list = [inputurl.format(category, SearchKey) % i for i in range(searchopt.pages)]
   # print (inputurl_list)
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
