#!/usr/bin/python3

import re
from . import generalcfg
from . import download



def exhtest(htmlContent):
   pattern = re.compile(r"id1")
   usefulCookies = False
   if re.match(pattern, htmlContent):
      usefulCookies = True
   return usefulCookies
   
def Grossdataspider(htmlcontent, searchopt):
   # separate the htmlcontent(str) to shorter strs  
   pattern1 = re.compile(r"id1")
   matchs1 = pattern1.finditer(htmlcontent)
   beginlist = []
   pattern2 = re.compile(r"id44")
   matchs2 = pattern2.finditer(htmlcontent)
   endlist = []
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

   pagefilteroff = searchopt.pagefilteroff
   if searchopt.manga == True:
      truecount = 0   # Count the amount of true values in the searchcatedict
      for searchcate in searchcatedict.items():
   
         if searchcate[1] == True:
            truecount += 1
      if truecount >= 2:
         pagefilteroff = True
   else:
      pagefilteroff = True



   for match in matchs1:
      beginlist.append(match.span()[1])
 
   for match in matchs2:
      endlist.append(match.span()[0])
	 
   loopcounter = 0
   urlsdict = {}
   while loopcounter < len(beginlist):
      substr = htmlcontent[beginlist[loopcounter]: endlist[loopcounter]]
      linkpattern = re.compile(r'''div class="id2"><a href="(https://.+\.org/g/\w+/\w+/)">(.+)</a></div><div class="id3" style=''')
      matchs3 = linkpattern.search(substr)
      filepattern = re.compile(r"(\d+) files")
      matchs5 = filepattern.search(substr)
      if pagefilteroff == False:
         if any(lang in matchs3.group(2) for lang in generalcfg.langkeys):
            pass
         elif matchs3.group(2).find('Anthology') != -1:
            if int(matchs5.group(1)) > 50:
               urlsdict.update({matchs3.group(2): matchs3.group(1)})
            else:
               pass
         else: 
            if int(matchs5.group(1)) > 100 and int(matchs5.group(1)) < 280:
               urlsdict.update({matchs3.group(2): matchs3.group(1)})
            else:
               pass
      else:
         if any(lang in matchs3.group(2) for lang in generalcfg.langkeys):
            pass
         else:
            urlsdict.update({matchs3.group(2): matchs3.group(1)})
      loopcounter += 1
   return urlsdict
   
   
   
def tagfilter(female_tags, male_tags, misc_tags):
   
   keeptag = True
   if any(female in female_tags for female in generalcfg.unwantedfemale):
      keeptag = False
   if any(male in male_tags for male in generalcfg.unwantedmale):
      keeptag = False
   if any(misc in misc_tags for misc in generalcfg.unwantedmisc):
      keeptag = False
   # Rule out the unwanted tags

   if any(female in female_tags for female in generalcfg.wantedfemale):
      keeptag = True
   if any(male in male_tags for male in generalcfg.wantedmale):
      keeptag = True
   if any(misc in misc_tags for misc in generalcfg.wantedmisc):
      keeptag = True
   # See whether the tags contain some interesting content and keep them
   return keeptag    


def artistmatch(artist, artistkeys):  #should rewrite to support multiple groups/artist
   #Match the exact artist or group
   ismatch = False
   if len(artistkeys) != 0:
      for artistkey in artistkeys:
         if artistkey.find("_") != -1:
            artistkey = artistkey.replace("_", " ")
         else:
            pass
         artistrule = ""
         artistrule = "^" + artistkey + "$"
         for a in artist:
            if a.find("_") != -1:
               a = a.replace("_", " ")
               matchartist = bool(re.match(artistrule, a, re.I))
               if matchartist == True:
                  ismatch = True
               else:
                  pass
            else:
               matchartist = bool(re.match(artistrule, a, re.I))
               if matchartist == True:
                  ismatch = True
               else:
                  pass

   else:
      ismatch = True
   return ismatch
   
   
def genmangainfo(htmlcontent, url, searchopt, mangasession, path):   
   url = url
   entitlepattern = re.compile(r'''div id="gd2"><h1 id="gn">(.+)</h1><h1 id="gj">''')
   entitlres = entitlepattern.finditer(htmlcontent)
   entitle =[]
#    print ("----------title eng----------")
   for match in entitlres:
      # print (match.group(1))
      entitle.append(match.group(1))
   
   jptitlepattern = re.compile(r'''<h1 id="gj">(.+)</h1></div>''')
   jptitleres = jptitlepattern.finditer(htmlcontent)
   jptitle = []
#    print ("----------title jp----------")
   for match in jptitleres:
         # print (match.group(1))
      jptitle.append(match.group(1))
#    print (jptitle)
   parodypattern = re.compile(r'''<div id="td_parody:([A-Za-z0-9_ -]+)" class=''')
   parodyres = parodypattern.finditer(htmlcontent)
   parody = []
   for match in parodyres:
      # print (match.group(1))
      parody.append(match.group(1))

   characterpattern = re.compile(r'''<div id="td_character:([A-Za-z0-9_ -]+)" class=''')
   characterres = characterpattern.finditer(htmlcontent)
   character = []
   for match in characterres:
      # print (match.group(1))
      character.append(match.group(1))
   
   langpattern = re.compile(r'''Language:</td><td class="gdt2">(\w+) ''')
   langres = langpattern.finditer(htmlcontent)
   lang = []
#    print ("----------language----------")
   for match in langres:
      # print (match.group(1))
      lang.append(match.group(1))
   
   pagespattern = re.compile(r'''Length:</td><td class="gdt2">(\d+) pages''')
   pageres = pagespattern.finditer(htmlcontent)
   length = []
#    print ("----------length----------")
   for match in pageres:
      # print (match.group(1))
      length.append(match.group(1))
   
   artistpattern = re.compile(r'''<div id="td_artist:([A-Za-z0-9_ -]+)" class=''')
   artistres = artistpattern.finditer(htmlcontent)
   artist = []
#    print ("----------artist----------")
   for match in artistres:
      # print (match.group(1))
      artist.append(match.group(1))

   femalepattern = re.compile(r'''<div id="td_female:([A-Za-z0-9_ -]+)" class''')

   femaleres = femalepattern.finditer(htmlcontent)
   female_tags = []
#    print ("----------female tags----------")
   for match in femaleres:
      # print (match.group(1))
      female_tags.append(match.group(1))
   
   malepattern = re.compile(r'''<div id="td_male:([A-Za-z0-9_ -]+)" class''')
   maleres = malepattern.finditer(htmlcontent)
   male_tags = []
#    print ("----------male tags----------")
   for match in maleres:
      # print (match.group(1))
      male_tags.append(match.group(1))
   
   miscpattern = re.compile(r'''<div id="td_([A-Za-z0-9_ -]+)" class=''')
   miscres = miscpattern.finditer(htmlcontent)
   misc_tags =[]
#    print ("----------misc tags----------")
   for match in miscres:
      # print (match.group(1))
      misc_tags.append(match.group(1))
   
   
   grouppattern = re.compile(r'''div id="td_group:([A-Za-z0-9_ -]+)" class=''')
   groupres = grouppattern.finditer(htmlcontent)
   group = []
#    print ("----------group----------")
   for match in  groupres:
      # print (match.group(1))
      group.append(match.group(1))

#    print ("----------manga info end----------")
   keeptag = tagfilter(female_tags = female_tags, male_tags = male_tags, misc_tags = misc_tags)
   if len(searchopt.artist) != 0:
      artistismatch = artistmatch(artist=artist, artistkeys=searchopt.artist)
   else:
      artistismatch = True
   if len(searchopt.group) != 0:
      groupismatch = artistmatch(artist=group, artistkeys=searchopt.group)
   else:
      groupismatch = True
   internaldict = {"entitle": entitle, 
                   "jptitle": jptitle, 
                   "artist": artist, 
                   "lang": lang, 
                   "length": length,
                   "female": female_tags,
                   "male": male_tags,
                   "misc":  misc_tags,
                   "group": group,
                   "parody": parody,
                   "character": character,
                   }
   mangainfo = {url: {}}

   if keeptag == True and artistismatch == True and groupismatch == True:
      for item in internaldict.items():
         if item[1]:
            mangainfo[url].update({item[0]: item[1]})
            print ("----------{0}----------".format(item[0]))
            for i in item[1]:
               print (i)
      print ("----------mangainfo end----------")
      # The function download.Previewdl would download the first img's small version. 
      imageDict = {}   # Store the image object in memory and send them to spider
      if searchopt.nopreviewimg == False:
         imagepattern = re.compile(r'''(https://[a-z0-9]*\.*\w+\.org/[a-z0-9]+/[a-z0-9]+/[a-z0-9]+/[a-z0-9_-]+)\.(\w{3,4})''')
         previewimages = imagepattern.finditer(htmlcontent)
         previewimg = {}
         imagePatternBig = re.compile(r'''href="(https://[a-z-]+\.org/[a-z0-9]/[a-z0-9]+/[a-z0-9]+\-1)"''')
         previewImagesBig = imagePatternBig.finditer(htmlcontent)
         for match in previewimages:
            previewimg.update({'imageurlSmall': match.group()})
            # print (match.group())
            previewimg.update({'imageForm': match.group(2)})
            # print (previewimg['imageForm'])
            # print (match.group(2))
         for match in previewImagesBig:
            previewimg.update({'imageurlBig': match.group(1)})
            # print (match.group(1))
         if generalcfg.dlFullPreviewImage == True:
            if previewimages:  
               print ("----------Full preview image download start----------")
               if jptitle:
                  filename = "{0}.{1}".format(jptitle[0], previewimg['imageForm'])
                  previewimg.update({'filename': filename})
                  tempDict = download.previewDlToMemoryBig(previewimg=previewimg,
                                                           mangasession=mangasession
                                                           )
                  # Pass the dict previewimage itself to download relating functions
                  imageDict.update(tempDict)
               elif entitle:
                  filename = "{0}.{1}".format(entitle[0], previewimg['imageForm'])
                  previewimg.update({'filename': filename})
                  # filename ="{0}.{1}".format(entitle[0], previerimg['imageForm'])
                  tempDict = download.previewDlToMemoryBig(previewimg=previewimg,
                                                           mangasession=mangasession
                                                           )
                  imageDict.update(tempDict)
               else: 
                  pass
         else: 
            if previewimg:
               print ("----------Preview image download start----------")
               if jptitle:
                  filename = "{0}.{1}".format(jptitle[0], previewimg['imageForm'])
            #       filename = jptitle[0] + '.' + previerimg[1]
                  previewimg.update({'filename': filename})
                  # previewurl = previewimg['imageurlSmall']
                  tempDict = download.previewdltomenory(previewimg=previewimg, 
                                                        mangasession=mangasession, 
                                                       )
                  imageDict.update(tempDict)
               elif entitle:
                  filename = "{0}.{1}".format(entitle[0], previewimg['imageForm'])
                  previewimg.update({'filename': filename})
                  # previewurl = previewimg['imageurlSmall']
                  tempDict = download.previewdltomenory(previewimg=previewimg, 
                                                        mangasession=mangasession,
                                                       )  
                  imageDict.update(tempDict)
               else:
                  pass
            else:
               pass
      else:
         print ("----------Preview image download DISABLE----------")
      mangainfo.update({"imageDict": imageDict})
   else:
      mangainfo ={}
      print ("Artist or group DOES NOT MATCH user input, DISCARD")
   return mangainfo