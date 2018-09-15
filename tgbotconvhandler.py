#!/usr/bin/python3
import json
import logging
from ast import literal_eval
from tgbotmodules import userdatastore
from tgbotmodules import replytext
from tgbotmodules.spidermodules import generator # use the sleep function
from tgbotmodules import exhspider
from tgbotmodules import userdatastore
from tgbotmodules.spidermodules import generalcfg
from tgbotmodules import searchoptgen 
from io import BytesIO 


  
def verify(inputStr, user_data, chat_data, logger):
   outputTextList = []
   if inputStr == generalcfg.passcode:
      statusdict = userdatastore.userfiledetect()
      if statusdict['isfile'] == False:
         logger.error("Missied userdata, created new one at verify.")
      elif statusdict['iscorrect'] == False:
         logger.error("Userdata is corrupted, backuped and created new one at verify.")
      else:
         logger.info("Userdata checked at verify.")
      logger.info("Identity of %s verified", user_data['actualusername'])
      chat_data.update({"fromadvcreate": False, "fromedit": False, "fromguide": False})
      currentuserdata = userdatastore.dataretrive(actusername=user_data['actualusername'])
      outputTextGeneralInfo = replytext.GeneralInfo.format(len(currentuserdata), generalcfg.maxiumprofile)
      outputTextList.append(outputTextGeneralInfo)
      if len(currentuserdata) >= generalcfg.maxiumprofile:
         logger.info("User %s has %d profile(s), excess or equal to the maxium profiles limitation.", user_data['actualusername'], len(currentuserdata))
         outputTextProfileExcessVerify = replytext.ProfileExcessVerify.format(generalcfg.maxiumprofile) 
         outputTextList.append(outputTextProfileExcessVerify)
         chat_data.update({'profileover': True, 'state': 'advance'})
      else:
        outputTextToUserCookies = replytext.ToUserCookies
        outputTextList.append(outputTextToUserCookies)
        chat_data.update({'state': 'usercookies'})
   else:
      outputTextVerifyFail = replytext.VerifyFail
      outputTextList.append(outputTextVerifyFail)
      logger.error("Identity of %s could not be verified", user_data['actualusername']) 
      chat_data.update({'state': 'verify'}) 
   outputDict = {"outputTextList": outputTextList,
                 "outputChat_data": chat_data, 
                 "outputUser_data": user_data
                }
   return outputDict  

def usercookies(inputStr, user_data, chat_data, logger):
   outputTextList = []
   if inputStr == 'ADVANCE':
      outputTextCookiesToADV = replytext.CookiesToADV
      outputTextList.append(outputTextCookiesToADV)
      chat_data.update({'state': 'advance'})
   else: 
      try:
         cookies = literal_eval(inputStr)
      except (SyntaxError, TypeError, ValueError):
         logger.error("The INCORRECT cookies of user %s is %s.", user_data['actualusername'], inputStr)
         outputTextCookiesError = replytext.CookiesError
         outputTextList.append(outputTextCookiesError)
         chat_data.update({'state': 'usercookies'})
      else:
         logger.info("The cookies of user %s is %s.", user_data['actualusername'], str(cookies))
         outputTextToUserKey = replytext.ToUserKey
         outputTextList.append(outputTextToUserKey)
         user_data.update({'usercookies': cookies})
         chat_data.update({'state': 'userkey'})
   outputDict = {"outputTextList": outputTextList,
                 "outputChat_data": chat_data, 
                 "outputUser_data": user_data
                }
#    print (user_data)
#    print (chat_data)
   return outputDict

def userkey(inputStr, user_data, chat_data, logger):
   outputTextList = []
   if inputStr == 'RETURN':
      logger.info("User %s has returned to usercookies.", user_data['actualusername'])
      outputTextReturnToCookies = replytext.ReturnToCookies 
      outputTextList.append(outputTextReturnToCookies)
      chat_data.update({'state': 'usercookies'})
   else:
      chat_data.update({'state': 'userranges'})
      if inputStr == 'EMPTY':
         user_data.update({"userkey": ""})
         logger.info("The search key of user %s is empty.", user_data['actualusername'])
      else:
         user_data.update({"userkey": inputStr,})
         logger.info("The search key of user %s is %s.", user_data['actualusername'], inputStr)
      outputTextToUserRange = replytext.ToUserRange
      outputTextList.append(outputTextToUserRange)
   outputDict = {"outputTextList": outputTextList,
                 "outputChat_data": chat_data, 
                 "outputUser_data": user_data
                }
#    print (user_data)
#    print (chat_data)
   return outputDict

def userranges(inputStr, user_data, chat_data, logger):
   outputTextList = []
   if inputStr == 'RETURN':
      logger.info("User %s has returned to usercookies.", user_data['actualusername'])
      outputTextReturnToKey = replytext.ReturnToKey
      outputTextList.append(outputTextReturnToKey)
      chat_data.update({'state': 'userkey'})
   else:
      try:
         ranges = int(inputStr)
      except ValueError:
         logger.info("The INCORRECT input of user %s is %s.", user_data['actualusername'], inputStr)
         outputTextRangeError = replytext.RangeError
         outputTextList.append(outputTextRangeError)
         chat_data.update({'state': 'userranges'})
      else:
        if ranges > generalcfg.userPageLimit:
           ranges = generalcfg.userPageLimit
        user_data.update({"userranges": ranges})
        outputTextToUserCate = replytext.ToUserCate
        outputTextList.append(outputTextToUserCate)
        chat_data.update({'state': 'usercate'})
        logger.info("The search range of user %s is %s.", user_data['actualusername'], str(ranges))
   outputDict = {"outputTextList": outputTextList,
                 "outputChat_data": chat_data, 
                 "outputUser_data": user_data
                }
#    print (user_data)
#    print (chat_data)
   return outputDict

def usercate(inputStr, user_data, chat_data, logger):
   outputTextList = []
   if inputStr == 'RETURN':
      logger.info("User %s has returned to userranges.", user_data['actualusername'])
      outputTextReturnToRange = replytext.ReturnToRange
      outputTextList.append(outputTextReturnToRange)
      chat_data.update({'state': 'userranges'})
   else:
      catechecklist = ['doujinshi', 'manga', 'artistcg', 'gamecg', 'western', 'non-h', 'imageset', 'asianporn', 'misc', 'cosplay']
      catelist = inputStr.split(' ')
      if set(catelist).issubset(catechecklist) == True:
         user_data.update({'usercate': catelist})
         chat_data.update({'state': 'userresult'})
         logger.info("The correct search categories of user %s are %s.", user_data['actualusername'], inputStr)
         outputTextList.append(replytext.ToUserResult.format((int(generalcfg.interval)/3600)))
      else:
         chat_data.update({'state': 'usercate'})
         logger.info("The INCORRECT search categories of user %s are %s, return to usercate", user_data['actualusername'], inputStr)
         outputTextCateError = replytext.CateError
         outputTextList.append(outputTextCateError)
   outputDict = {"outputTextList": outputTextList,
                 "outputChat_data": chat_data, 
                 "outputUser_data": user_data
                }
#    print (user_data)
#    print (chat_data)
   return outputDict  

def userresult(inputStr, user_data, chat_data, logger):
   outputTextList = []
   if inputStr == 'RETURN':
      logger.info("User %s has returned to usercate.", user_data['actualusername'])
      outputTextReturnToCate = replytext.ReturnToCate
      outputTextList.append(outputTextReturnToCate)
      chat_data.update({'state': 'usercate'})
   elif inputStr == 1 or inputStr == "1":
      user_data.update({"resultToChat": True, "userpubchenn": False})
      logger.info("User %s would receive his/her result in the chat.", user_data['actualusername'])
      chat_data.update({'state': 'username'})
      outputTextList.append(replytext.ToVirtualUsername)
   elif inputStr == 2 or inputStr == "2":
      user_data.update({"resultToChat": False, "userpubchenn": True})
      logger.info("User %s would receive his/her result in the public channel.", user_data['actualusername'])
      chat_data.update({'state': 'username'})
      outputTextList.append(replytext.ToVirtualUsername)
   elif inputStr == 3 or inputStr == "3":
      user_data.update({"resultToChat": True, "userpubchenn": True})
      logger.info("User %s would receive his/her result in both the chat and public channel.", user_data['actualusername'])   
      chat_data.update({'state': 'username'})
      outputTextList.append(replytext.ToVirtualUsername)
   else:
      logger.info("User %s's wrong input is %s",
                   user_data['actualusername'],
                   inputStr)
      outputTextList.append(replytext.ChoiceError)
      chat_data.update({'state': 'userresult'})
   outputDict = {"outputTextList": outputTextList,
                 "outputChat_data": chat_data, 
                 "outputUser_data": user_data
                }
#    print (user_data)
#    print (chat_data)
   return outputDict     

def username(inputStr, user_data, chat_data, logger):
   outputTextList = []
   if inputStr == 'RETURN':
      logger.info("User %s has returned to userpubchenn.", user_data['actualusername'])
      outputTextList.append(replytext.ReturnToUserResult)
      chat_data.update({'state': 'userresult'})
   else:
      chat_data.update({'state': 'storeinfo', "fromadvcreate": False, "fromedit": False, "fromguide": True})
      user_data.update({"virtualusername": inputStr})
      logger.info("Virual username of %s is %s.", user_data['actualusername'], inputStr)
      outputTextToStoreInfo = replytext.ToStoreInfo 
      outputTextList.append(outputTextToStoreInfo)
      del user_data['chat_id']
      outputTextUserInfo = str(user_data)
      outputTextList.append(outputTextUserInfo)
   outputDict = {"outputTextList": outputTextList,
                 "outputChat_data": chat_data, 
                 "outputUser_data": user_data
                }
#    print (user_data)
#    print (chat_data)
   return outputDict     

def storeinfo(inputStr, user_data, chat_data, logger):
   outputTextList = []
   if inputStr == "YES":
      statusdict = userdatastore.userfiledetect()
      if statusdict['isfile'] == False:
         logger.error("Could not find userdate, create new one at storeinfo")
      elif statusdict['iscorrect'] == False:
         logger.error("Userdata is corrupted, backup the broken file and create new one at storeinfo")
      else:
         logger.info("Userdata checked at storeinfo")
      userdata = {user_data["virtualusername"]: user_data}
      chat_data.update({"virtualusername": user_data["virtualusername"]})
      del  userdata[user_data["virtualusername"]]["virtualusername"]
      if chat_data["fromedit"] == True:
         userdatastore.datadelete(chat_data["oldvirusername"])
      IOreportdict = userdatastore.datastore(userdict=userdata)
      if IOreportdict['issaved'] == IOreportdict['nosamename'] == True:
         logger.info("The information of user %s is saved.", user_data['actualusername'])
         outputTextStored = replytext.Stored 
         outputTextList.append(outputTextStored)
         
         chat_data.update({'state': 'END'})
      else:
         logger.error("The information of user %s is NOT saved due to IO issue or name issue.", user_data['actualusername'])
         chat_data.update({'state': 'username'})
         outputTextStoreError = replytext.StoreError
         outputTextList.append(outputTextStoreError)
         if chat_data["fromguide"] == True:
            chat_data.update({'state': 'username'})
            logger.error("User %s has returned to username.", user_data['actualusername'])
         else:
           chat_data.update({'state': 'advcreate'})
           logger.error("User %s has returned to advcreate.", user_data['actualusername'])
   else: 
      if chat_data["fromguide"] == True:
         logger.info("The information of user %s is not saved due to user cancel, return to virtual username.", user_data['actualusername'])
         outputTextReturnToVirtualUsername = replytext.ReturnToVirtualUsername
         outputTextList.append(outputTextReturnToVirtualUsername)
         chat_data.update({'state': "username"})
      else: 
         chat_data.update({'state': 'advcreate'})
         logger.info("The information of user %s is not saved due to user cancel, return to advcreate.", user_data['actualusername'])
         outputTextReturnToAdvCreate = replytext.ReturnToAdvCreate
         outputTextList.append(outputTextReturnToAdvCreate)
   outputDict = {"outputTextList": outputTextList,
                 "outputChat_data": chat_data, 
                 "outputUser_data": user_data
                }
#    print (user_data)
#    print (chat_data)
   return outputDict

def advance(inputStr, user_data, chat_data, logger):
   outputTextList = []
   if inputStr == 'INFO':
      chat_data.update({'state': 'advguide'})
      logger.info("User %s entered advance mode", user_data['actualusername'])
      statusdict = userdatastore.userfiledetect()
      if statusdict['isfile'] == False:
         logger.error("Missied userdata, created new one at advance.")
      elif statusdict['iscorrect'] == False:
         logger.error("Userdata is corrupted, backuped and created new one at advance.")
      else:
         logger.info("Userdata checked at advance.")
      currentuserdata = userdatastore.dataretrive(actusername=user_data['actualusername'])
      outputTextProfileAmount = replytext.ProfileAmount.format(len(currentuserdata))
      outputTextList.append(outputTextProfileAmount)
      for cd in currentuserdata:
         del currentuserdata[cd]['actualusername']
         del currentuserdata[cd]['chat_id']
         outputTextProfileInfo = str(cd) + '\n' + str(currentuserdata[cd])
         outputTextList.append(outputTextProfileInfo)
      outputTextFuncSelect = replytext.FuncSelect
      outputTextList.append(outputTextFuncSelect)
   else:
      chat_data.update({'state': 'advance'})
      outputTextAdvError = replytext.AdvError
      outputTextList.append(outputTextAdvError)
   outputDict = {"outputTextList": outputTextList,
                 "outputChat_data": chat_data, 
                 "outputUser_data": user_data
                }
#    print (user_data)
#    print (chat_data)
   return outputDict    

def advguide(inputStr, user_data, chat_data, logger):
   outputTextList = []
   currentuserdata = userdatastore.dataretrive(actusername=user_data['actualusername'])
   logger.info("User %s entered advguide", user_data['actualusername'])
   if inputStr == 'ADVCREATE':
      statusdict = userdatastore.userfiledetect()
      if statusdict['isfile'] == False:
         logger.error("Missied userdata, created new one.")
      elif statusdict['iscorrect'] == False:
         logger.error("Userdata is broken, backup and created new one.")
      else:
         logger.info("Userdata checked at advguide.")
      if 'profileover' in chat_data:
         logger.info("User %s already has %d profile(s) so could not create new one.", 
                     user_data['actualusername'], 
                     len(currentuserdata)
                     )
         outputTextProfileExcess = replytext.ProfileExcess
         outputTextList.append(outputTextProfileExcess)
         chat_data.update({'state:': 'advguide'})
      else:
         chat_data.update({'state': 'advcreate'})
         outputTextToAdvCreate = replytext.ToAdvCreate
         outputTextList.append(outputTextToAdvCreate)
   elif inputStr == 'ADVEDIT':
      if len(currentuserdata) == 0:
         chat_data.update({'state': 'advguide'})
         logger.info("User %s does not has any profile", user_data['actualusername'])
         outputTextNoProfile = replytext.NoProfile
         outputTextList.append(outputTextNoProfile)
      else:
         chat_data.update({'state': 'advedit'})
         outputTextSelectProfileNameToEdit = replytext.SelectProfileNameToEdit
         outputTextList.append(outputTextSelectProfileNameToEdit)
   elif inputStr == 'DELETE':
      if len(currentuserdata) == 0:
         chat_data.update({'state': 'advguide'})
         outputTextNoProfileToDelete = replytext.NoProfileToDelete
         outputTextList.append(outputTextNoProfileToDelete)
      else:
         chat_data.update({'state': 'delete'})
         outputTextSelectProfileNameToDelete = replytext.SelectProfileNameToDelete
         outputTextList.append(outputTextSelectProfileNameToDelete)
   else:
      chat_data.update({'state': 'advguide'})
      outputTextErrorInput = replytext.ErrorInput
      outputTextList.append(outputTextErrorInput)
   outputDict = {"outputTextList": outputTextList,
                 "outputChat_data": chat_data, 
                 "outputUser_data": user_data
                }
#    print (user_data)
#    print (chat_data)
   return outputDict

def advcreate(inputStr, user_data, chat_data, logger):
   outputTextList = []
   logger.info("User %s has entered advcreate.", user_data['actualusername'])
   try:
      tempuserdata = literal_eval(inputStr)
   except (SyntaxError, TypeError, ValueError):
      chat_data.update({'state': 'advcreate'})
      outputTextErrorSyntax = replytext. ErrorSyntax
      outputTextList.append(outputTextErrorSyntax)
      logger.info("The INCORRECT profile of user %s is %s, return to advcreate", user_data['actualusername'], inputStr)
   else:
      userdatachecklist = ['usercate', 'userranges', 'userkey', 'resultToChat', 'userpubchenn', 'virtualusername', 'usercookies']
      catechecklist = ['doujinshi', 'manga', 'artistcg', 'gamecg', 'western', 'non-h', 'imageset', 'asianporn', 'misc', 'cosplay']
      if set(userdatachecklist) != set(list(tempuserdata.keys())):       
         logger.info("The INCORRECT userdata key of user %s is %s, return to advcreate", user_data['actualusername'], str(tempuserdata.keys()))
         chat_data.update({'state': 'advcreate'})
         outputTextUserDataCheckFail = replytext.UserDataCheckFail
         outputTextList.append(outputTextUserDataCheckFail)

      elif type(tempuserdata['usercate']) != list:
         logger.info("The INCORRECT usercate type of user %s is %s, return to advcreate", user_data['actualusername'], str(type(tempuserdata['usercate']))) 
         chat_data.update({'state': 'advcreate'})
         outputTextUserCateSyntaxError = replytext.UserCateSyntaxError
         outputTextList.append(outputTextUserCateSyntaxError)

      elif set(tempuserdata['usercate']).issubset(catechecklist) == False:
         logger.info("The INCORRECT usercate categories of user %s is %s, return to advcreate", user_data['actualusername'], str(tempuserdata['usercate'])) 
         chat_data.update({'state': 'advcreate'})
         outputTextUserCateCheckFail = replytext.UserCateCheckFail
         outputTextList.append(outputTextUserCateCheckFail)

      elif type(tempuserdata["userranges"]) != int:
         logger.info("The INCORRECT userranges type of user %s is %s, return to advcreate", user_data['actualusername'], str(type(tempuserdata["userranges"]))) 
         chat_data.update({'state': 'advcreate'})
         outputTextUserRangesValueError = replytext.UserRangesValueError
         outputTextList.append(outputTextUserRangesValueError)
      elif tempuserdata["resultToChat"] == False and tempuserdata["userpubchenn"] == False:
         logger.info("User %s does not choice any method to receive the result", user_data['actualusername'])
         outputTextList.append(replytext.UserReceiveResultError)
         chat_data.update({'state': 'advcreate'})
      else:
         if tempuserdata["userranges"] > generalcfg.userPageLimit:
            logger.error("The INCORRECT userranges value of user %s is %d, Limit to %d", user_data['actualusername'], tempuserdata["userranges"], generalcfg.userPageLimit) 
            tempuserdata["userranges"] = generalcfg.userPageLimit
            outputTextRangeExcess = replytext.RangeExcess
            outputTextList.append(outputTextRangeExcess)
         if chat_data["fromedit"] == True:
            logger.info("The correct usedata of user %s from advedit is %s.", user_data['actualusername'], str(tempuserdata))
            chat_data.update({'state': 'storeinfo'})
         else:        
            logger.info("The correct usedata of user %s is %s.", user_data['actualusername'], str(tempuserdata))
            chat_data.update({"fromadvcreate": True, "fromedit": False, "fromguide": False, 'state': 'storeinfo'})
         user_data.update(tempuserdata)
         outputTextUserDataCheckComplete = replytext.UserDataCheckComplete
         outputTextList.append(outputTextUserDataCheckComplete)
   outputDict = {"outputTextList": outputTextList,
                 "outputChat_data": chat_data, 
                 "outputUser_data": user_data
                }
#    print (user_data)
#    print (chat_data)
   return outputDict

def advedit(inputStr, user_data, chat_data, logger):
   outputTextList = []
   tempuserdata = userdatastore.dataretrive(user_data['actualusername'])
   if tempuserdata.get(inputStr, 'None') == 'None':
      chat_data.update({'state': 'advedit'})
      outputTextErrorVirtualUserName = replytext.ErrorVirtualUserName
      outputTextList.append(outputTextErrorVirtualUserName)
   else:
      chat_data.update({"fromadvcreate": False, "fromedit": True, 
                        "fromguide": False, "oldvirusername": inputStr,
                        'state': 'advcreate'})
      logger.info("User %s is going to edit %s", user_data['actualusername'], inputStr)
      tempuserdata = tempuserdata[inputStr]
      tempuserdata.update({"virtualusername": inputStr})
      del tempuserdata["actualusername"]
      del tempuserdata["chat_id"]
      outputTextRetriveProfileSuccess = replytext.RetriveProfileSuccess
      outputTextList.append(outputTextRetriveProfileSuccess)
      outputTextProfileContent = str(tempuserdata)
      outputTextList.append(outputTextProfileContent)
   outputDict = {"outputTextList": outputTextList,
                 "outputChat_data": chat_data, 
                 "outputUser_data": user_data
                }
#    print (user_data)
#    print (chat_data)
   return outputDict      

def delete(inputStr, user_data, chat_data, logger):
   outputTextList = []
   logger.info("User %s has entered delete.", user_data['actualusername'])
   IOreportdict = userdatastore.datadelete(inputStr)
   if IOreportdict["hasdata"] == False:
      chat_data.update({'state': 'delete'})
      logger.error("User %s's virtual userdata %s not found.", 
                   user_data['actualusername'], 
                   inputStr
                  )
      outputTextVirUsernameNotFound = replytext.VirUsernameNotFound
      outputTextList.append(outputTextVirUsernameNotFound)
   else:
      chat_data.update({'state': 'advance'})
      logger.info("User %s's virtual userdata %s has been deleted.", 
                   user_data['actualusername'], 
                   inputStr
                 )
      outputTextDeleteSuccess = replytext.DeleteSuccess.format(inputStr)
      outputTextList.append(outputTextDeleteSuccess)
   outputDict = {"outputTextList": outputTextList,
                 "outputChat_data": chat_data, 
                 "outputUser_data": user_data
                }
#    print (user_data)
#    print (chat_data)
   return outputDict  

def spiderfunction(logger, spiderDict=None):
   '''This function would either exploit the provided user information or the information on
      disk (if user information is not provided) to search the e-h/exh and return several 
      Manga objects. Every Manga object contains all of a gallery's information. This function
      would create a dict like {username1: MangaObjectList1, username2: MangaObjectList2} to 
      handle multiple users' result'''
   if spiderDict == None:
      spiderDict = userdatastore.getspiderinfo()
   else: 
      # print (spiderDict)
      for sD in spiderDict:
         spiderDict[sD].update({'userpubchenn': False, 'resultToChat': True})
   logger.info("Spider is initialing")

   toTelegramDict = {} 
   sendUserResultDict = {} # Determin whether this user has chat_id and channel id to receive the result.
                           # Otherwise the spider would not search this user's information.
   sleep = generator.Sleep(sleepstr=generalcfg.searchInterval)

   for sd in spiderDict:
      tempChat_idList = []
      # print (spiderDict[sd]['resultToChat'])
      if spiderDict[sd]['resultToChat'] == True and spiderDict[sd]['chat_id']:
         tempChat_idList.append(spiderDict[sd]['chat_id'])
      if spiderDict[sd]["userpubchenn"] == True and generalcfg.pubChannelID:
         tempChat_idList.append(generalcfg.pubChannelID)
      sendUserResultDict.update({sd: tempChat_idList})
   for sd in sendUserResultDict: 
      if sendUserResultDict[sd]:
         logger.info("Search user %s's information", str(sd))
         generator.Sleep.Havearest(sleep)
         searchopt = searchoptgen.searchgenerate(generateDict=spiderDict[sd])
         cookies = spiderDict[sd]["usercookies"]
         userResultStorePath = "./searchresult/{0}/{1}/".format(spiderDict[sd]["actualusername"], sd)
         imageObjList = exhspider.Spidercontrolasfunc(searchopt=searchopt, 
                                                      cookies=cookies, 
                                                      path=userResultStorePath,
                                                      logger=logger,
                                                      datastore=userdatastore.datastore,
                                                      spiderDict=spiderDict,
                                                      sd=sd
                                                     ) 
         logger.info("Search of user %s has completed.", str(sd))

         if imageObjList:
            toTelegramDict.update({sd: imageObjList})
      else:
         pass
   return toTelegramDict


def messageanalyze(inputStr=None, user_data=None, chat_data=None, logger=None):
   '''This function controls the interaction between user and bot. The basic working
      method of this function is that the upper layers provide the user input, status
      and user information. Then, this function would exploit a suitable sub function
      to treat these message and return the result. After that, it would return these 
      results to the upper layers.'''
   messageFuncDict = {'verify': verify,
                      'usercookies': usercookies,
                      'userkey': userkey,
                      'userranges': userranges,
                      'usercate': usercate,
                      'userresult': userresult,
                      'username': username,
                      'storeinfo': storeinfo,
                      'advance': advance,
                      'advguide': advguide,
                      'advcreate': advcreate,
                      'advedit': advedit,
                      'delete': delete
                     }
   outputDict = messageFuncDict[chat_data['state']](inputStr=inputStr, 
                                                    user_data=user_data, 
                                                    chat_data=chat_data,
                                                    logger=logger
                                                   )
   return outputDict