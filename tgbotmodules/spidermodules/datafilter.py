#!/usr/bin/python3

import re
from . import generalcfg
from . import download



def exhtest(htmlContent):
   pattern = re.compile(r"Front")
   usefulCookies = False
   if bool(re.search(pattern, htmlContent)):
      usefulCookies = True
   return usefulCookies
   
def Grossdataspider(htmlcontent):
   # patternThumb = re.compile(r"Show List")
   # matchThumb = patternThumb.search(htmlcontent)
   # if matchThumb:
   urlsdict = GrossdataspiderThumbnail(htmlcontent=htmlcontent)
   # else:
   #    urlsdict = GrossdataspiderList(htmlcontent=htmlcontent)
   return urlsdict
 
def GrossdataspiderList(htmlcontent):
   patternBegin = re.compile(r"itdc")
   matchesBegin = patternBegin.finditer(htmlcontent)
   beginList = []
   patternEnd = re.compile(r"itu")
   matchesEnd = patternEnd.finditer(htmlcontent)
   endList = []
   for match in matchesBegin:
      beginList.append(match.span()[1])

   for match in matchesEnd:
      endList.append(match.span()[0])

   loopCounter = 0
   urlsDict = {}
   linkPattern = re.compile(r'''class="it5"><a href="(https://.+\.org/g/\w+/\w+/)" onmouseover="[a-zA-Z0-9_()]+" onmouseout="[a-zA-Z0-9_()]+">(.+)</a></div>''')
   while loopCounter < len(beginList):
      substr = htmlcontent[beginList[loopCounter]: endList[loopCounter]]
      matchesLinkInfo = linkPattern.search(substr)
      if matchesLinkInfo:
         if any(lang in matchesLinkInfo.group(2) for lang in generalcfg.langkeys):
            pass
         else:      
            urlsDict.update({matchesLinkInfo.group(2): matchesLinkInfo.group(1)})
      else:
         pass
      loopCounter += 1
   return urlsDict


def GrossdataspiderThumbnail(htmlcontent):
   patternBegin = re.compile(r'''class="gl1''')
   matchesBegin = patternBegin.finditer(htmlcontent)
   beginList = []
   patternEnd = re.compile(r'''class="gl3''')
   matchesEnd = patternEnd.finditer(htmlcontent)
   endList = []
   for match in matchesBegin:
      beginList.append(match.span()[1])
 
   for match in matchesEnd:
      endList.append(match.span()[0])
   # print (beginList)
   # print (endList)
   loopCounter = 0
   urlsDict = {}
   linkPattern = re.compile(r'''<a href="(https://.+\.org/g/\w+/\w+/)"><div class="gl4[a-zA-Z0-9\s]+">(.+)</div></a>''')
   while loopCounter < len(beginList):
      substr = htmlcontent[beginList[loopCounter]: endList[loopCounter]]
      matchesLinkInfo = linkPattern.search(substr)
      if matchesLinkInfo:
         if any(lang in matchesLinkInfo.group(2) for lang in generalcfg.langkeys):
            pass
         else:
            urlsDict.update({matchesLinkInfo.group(2): matchesLinkInfo.group(1)})
      else:
         pass
      loopCounter += 1
   # print (urlsDict)
   return urlsDict
   
   
   
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
   


def genmangainfoapi(resultJsonDict, searchopt):
   mangaInfo = {}
   resultDict = {}
   for gmd in resultJsonDict:
      male_tags = []
      female_tags = []
      artist = []
      group = []
      character = []
      parody = []
      misc_tags = []
      lang = []
      entitle = []
      jptitle = []
      length = []
      category = []
      imageurlSmall = ""
      imageForm = ""
      if searchopt.eh == True:
         galleryUrl = 'https://e-hentai.org/g/{0}/{1}/'.format(gmd['gid'], gmd['token'])
      else:
         galleryUrl = 'https://exhentai.org/g/{0}/{1}/'.format(gmd['gid'], gmd['token'])
      if gmd.get('title'):
         entitle.append(gmd['title'])
      if gmd.get('title_jpn'):
         jptitle.append(gmd['title_jpn'])
      if gmd.get('filecount'):
         length.append(gmd['filecount'])
      if gmd.get('category'):
         category.append(gmd['category'])
      if gmd.get('thumb'):
         imageurlSmall = gmd['thumb']
      #    print (imageurlSmall)
      #    imageMatch = re.search(r'''(https://[a-z0-9\.]+\.org\/[a-z0-9]+\/[a-z0-9]+\/[a-z0-9_-]+)\.(\w{3,4})''', imageurlSmall)
      #    imageForm = imageMatch.group(2)
      if gmd.get('tags'):
         for tag in gmd['tags']:
            parodyMatch = re.search(r'''parody:(.+)''', tag)
            femaleMatch = re.search(r'''female:(.+)''', tag)
            maleMatch = re.search(r'''male:(.+)''', tag)
            artistMatch = re.search(r'''artist:(.+)''', tag)
            groupMatch = re.search(r'''group:(.+)''', tag)
            characterMatch = re.search(r'''character:(.+)''', tag)
            languageMatch = re.search(r'''language:(.+)''', tag)
            if parodyMatch:
               parody.append(parodyMatch.group(1))
            elif femaleMatch:
               female_tags.append(femaleMatch.group(1))
            elif maleMatch:
               male_tags.append(maleMatch.group(1))
            elif artistMatch:
               artist.append(artistMatch.group(1))
            elif groupMatch:
               group.append(groupMatch.group(1))
            elif characterMatch:
               character.append(characterMatch.group(1))
            elif languageMatch:
               lang.append(languageMatch.group(1))
            else:
               misc_tags.append(tag)
      if lang:
         pass
      else:
         lang.append('Japanese')
      mangaInfo.update({galleryUrl:
                      {"entitle": entitle, 
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
                       "imageurlSmall": imageurlSmall,
                      }})
#    print (mangaInfo)
   for mi in mangaInfo:
      if any(lang in mangaInfo[mi]['lang'] for lang in generalcfg.langkeys):
         langKeep = False
      else:
         langKeep = True
      keepTag = tagfilter(female_tags=mangaInfo[mi]['female'],
                          male_tags=mangaInfo[mi]['male'],
                          misc_tags=mangaInfo[mi]['misc']
                        )
      if searchopt.artist:
         isMatchArtist = artistmatch(artist=mangaInfo[mi]['artist'], 
                                     artistkeys=searchopt.artist)
      else:
         isMatchArtist = True

      if searchopt.group:
         isMatchGroup = artistmatch(artist=mangaInfo[mi]['group'], 
                                    artistkeys=searchopt.artist)
      else:
         isMatchGroup = True

      if keepTag == True and isMatchArtist == True and isMatchGroup == True and langKeep == True:
         resultDict.update({mi: mangaInfo[mi]})
#    print (resultDict)
   return resultDict


     

# def genmangainfo(htmlcontent, url, searchopt, mangasession, path):   
#    url = url
#    entitlepattern = re.compile(r'''div id="gd2"><h1 id="gn">(.+)</h1><h1 id="gj">''')
#    entitlres = entitlepattern.finditer(htmlcontent)
#    entitle =[]
# #    print ("----------title eng----------")
#    for match in entitlres:
#       # print (match.group(1))
#       entitle.append(match.group(1))
   
#    jptitlepattern = re.compile(r'''<h1 id="gj">(.+)</h1></div>''')
#    jptitleres = jptitlepattern.finditer(htmlcontent)
#    jptitle = []
# #    print ("----------title jp----------")
#    for match in jptitleres:
#          # print (match.group(1))
#       jptitle.append(match.group(1))
# #    print (jptitle)
#    parodypattern = re.compile(r'''<div id="td_parody:([A-Za-z0-9_ -]+)" class=''')
#    parodyres = parodypattern.finditer(htmlcontent)
#    parody = []
#    for match in parodyres:
#       # print (match.group(1))
#       parody.append(match.group(1))

#    characterpattern = re.compile(r'''<div id="td_character:([A-Za-z0-9_ -]+)" class=''')
#    characterres = characterpattern.finditer(htmlcontent)
#    character = []
#    for match in characterres:
#       # print (match.group(1))
#       character.append(match.group(1))
   
#    langpattern = re.compile(r'''Language:</td><td class="gdt2">(\w+) ''')
#    langres = langpattern.finditer(htmlcontent)
#    lang = []
# #    print ("----------language----------")
#    for match in langres:
#       # print (match.group(1))
#       lang.append(match.group(1))
   
#    pagespattern = re.compile(r'''Length:</td><td class="gdt2">(\d+) pages''')
#    pageres = pagespattern.finditer(htmlcontent)
#    length = []
# #    print ("----------length----------")
#    for match in pageres:
#       # print (match.group(1))
#       length.append(match.group(1))
   
#    artistpattern = re.compile(r'''<div id="td_artist:([A-Za-z0-9_ -]+)" class=''')
#    artistres = artistpattern.finditer(htmlcontent)
#    artist = []
# #    print ("----------artist----------")
#    for match in artistres:
#       # print (match.group(1))
#       artist.append(match.group(1))

#    femalepattern = re.compile(r'''<div id="td_female:([A-Za-z0-9_ -]+)" class''')

#    femaleres = femalepattern.finditer(htmlcontent)
#    female_tags = []
# #    print ("----------female tags----------")
#    for match in femaleres:
#       # print (match.group(1))
#       female_tags.append(match.group(1))
   
#    malepattern = re.compile(r'''<div id="td_male:([A-Za-z0-9_ -]+)" class''')
#    maleres = malepattern.finditer(htmlcontent)
#    male_tags = []
# #    print ("----------male tags----------")
#    for match in maleres:
#       # print (match.group(1))
#       male_tags.append(match.group(1))
   
#    miscpattern = re.compile(r'''<div id="td_([A-Za-z0-9_ -]+)" class=''')
#    miscres = miscpattern.finditer(htmlcontent)
#    misc_tags =[]
# #    print ("----------misc tags----------")
#    for match in miscres:
#       # print (match.group(1))
#       misc_tags.append(match.group(1))
   
   
#    grouppattern = re.compile(r'''div id="td_group:([A-Za-z0-9_ -]+)" class=''')
#    groupres = grouppattern.finditer(htmlcontent)
#    group = []
# #    print ("----------group----------")
#    for match in  groupres:
#       # print (match.group(1))
#       group.append(match.group(1))

# #    print ("----------manga info end----------")
#    keeptag = tagfilter(female_tags = female_tags, male_tags = male_tags, misc_tags = misc_tags)
#    if len(searchopt.artist) != 0:
#       artistismatch = artistmatch(artist=artist, artistkeys=searchopt.artist)
#    else:
#       artistismatch = True
#    if len(searchopt.group) != 0:
#       groupismatch = artistmatch(artist=group, artistkeys=searchopt.group)
#    else:
#       groupismatch = True
#    internaldict = {"entitle": entitle, 
#                    "jptitle": jptitle, 
#                    "artist": artist, 
#                    "lang": lang, 
#                    "length": length,
#                    "female": female_tags,
#                    "male": male_tags,
#                    "misc":  misc_tags,
#                    "group": group,
#                    "parody": parody,
#                    "character": character,
#                    }
#    mangainfo = {url: {}}

#    if keeptag == True and artistismatch == True and groupismatch == True:
#       for item in internaldict.items():
#          if item[1]:
#             mangainfo[url].update({item[0]: item[1]})
#             print ("----------{0}----------".format(item[0]))
#             for i in item[1]:
#                print (i)
#       print ("----------mangainfo end----------") 
#       imageDict = {}   # Store the image object in memory and send them to spider
#       if searchopt.nopreviewimg == False:
#          imagepattern = re.compile(r'''(https://[a-z0-9]*\.*\w+\.org/[a-z0-9]+/[a-z0-9]+/[a-z0-9]+/[a-z0-9_-]+)\.(\w{3,4})''')
#          previewimages = imagepattern.search(htmlcontent)
#          previewimg = {'imageurlSmall': '', 
#                        'imageForm': '', 
#                        'title': '',
#                        'imageurlBig': ''}  # Store different kinds of data for the download functions.
#          imagePatternBig = re.compile(r'''href="(https://[a-z-]+\.org/[a-z0-9]/[a-z0-9]+/[a-z0-9]+\-1)"''')
#          previewImagesBig = imagePatternBig.search(htmlcontent)
#          if previewimages:
#             previewimg['imageurlSmall'] = previewimages.group()
#             # print (previewimages.group())
#             previewimg['imageForm'] = previewimages.group(2)
#             # print (previewimg['imageForm'])
#             # print (previewimages.group(2))
#          if previewImagesBig:
#             previewimg['imageurlBig'] = previewImagesBig.group(1)
#             # print (previewImagesBig.group(1))
#          if generalcfg.dlFullPreviewImage == True and previewimg:
#             print ("----------Full preview image download start----------")
#             if jptitle:
#                previewimg['title'] = jptitle[0]
#                tempDict = download.previewDlToMemoryBig(previewimg=previewimg,
#                                                         mangasession=mangasession
#                                                        )
#             elif entitle:
#                if generalcfg.noEngOnlyGallery == True and any(i in lang for i in generalcfg.langkeys):
#                   tempDict = {}
#                else:
#                   previewimg['title'] = entitle[0]
#                   tempDict = download.previewDlToMemoryBig(previewimg=previewimg,
#                                                         mangasession=mangasession
#                                                        )
#             else: 
#                tempDict = {}
#             imageDict.update(tempDict)
#          elif previewimg: 
#             print ("----------Preview image download start----------")
#             if jptitle:
#                previewimg['title'] = jptitle[0]
#                tempDict = download.previewdltomenory(previewimg=previewimg, 
#                                                      mangasession=mangasession, 
#                                                     )
#             elif entitle:
#                if generalcfg.noEngOnlyGallery == True and any(i in lang for i in generalcfg.langkeys):
#                   tempDict = {}
#                else:
#                   previewimg['title'] = entitle[0]
#                   tempDict = download.previewdltomenory(previewimg=previewimg, 
#                                                         mangasession=mangasession,
#                                                        )
#             else:
#                tempDict = {}
#             imageDict.update(tempDict)
#          else:
#             pass
#       else:
#          print ("----------Preview image download DISABLE----------")
#       mangainfo.update({"imageDict": imageDict})
#    else:
#       mangainfo ={}
#       print ("Artist or group DOES NOT MATCH user input, DISCARD")
#    return mangainfo