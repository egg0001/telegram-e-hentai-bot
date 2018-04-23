#!/usr/bin/python3

import logging
import json
import os
import time
import datetime
from ast import literal_eval
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler 
from telegram.ext import Filters
from telegram.ext import ConversationHandler
from tgbotconvhandler import messageanalyze
from tgbotconvhandler import spiderfunction
from tgbotmodules import replytext 
# from tgbotmodules import botconfig
from tgbotmodules.spidermodules import generalcfg
from tgbotmodules import userdatastore
# from tgbotmodules import userdatastore
 
def start(bot, update, user_data, chat_data):
   user_data.clear()
   chat_data.clear()
   user_data.update({"actualusername": str(update.message.from_user.username)})
   logger.info("Actual username is %s.", str(update.message.from_user.username))
   update.message.reply_text(text="Welcome to Nakazawa Bookstore, please show your vip card.")
   chat_data.update({'state': 'verify'})
   return STATE

def state(bot, update, user_data, chat_data):
   inputStr = update.message.text
   outputDict = messageanalyze(inputStr=inputStr, 
                               user_data=user_data, 
                               chat_data=chat_data,
                               logger=logger
                              )
   user_data.update(outputDict["outputUser_data"])
   chat_data.update(outputDict["outputChat_data"])
   for text in outputDict["outputTextList"]:
      update.message.reply_text(text=text)
   if chat_data['state'] != 'END':
      state = STATE 
   else: 
      user_data.clear()
      chat_data.clear()
      logger.info("The user_data and chat_data of user %s is clear.", str(update.message.from_user.username))
      state = ConversationHandler.END
   return state

def searcheh(bot, job):
   logger.info("Search is beginning")
   spiderDict = userdatastore.getspiderinfo()
   toTelegramDict = spiderfunction(logger=logger)
   logger.info("All users' search has been completed, begin to send the result")
   if toTelegramDict:
      for td in toTelegramDict:
         chat_idList = []     
         if spiderDict[td]['userchenn']:
            chat_idList.append(spiderDict[td]['userchenn'])
         if spiderDict[td]["userpubchenn"] == True:
            chat_idList.append(generalcfg.pubChannelID)
         logger.info("Begin to send user %s's result.", td)
         for chat_id in chat_idList:
            messageDict = {"messageCate": "message",
                           "messageContent": ["------This is user {0}'s result------".format(str(td))]}
            channelmessage(bot=bot, messageDict=messageDict, chat_id=chat_id)
            for obj in toTelegramDict[td]['imageObjDict']:
               messageDict = {'messageCate': "photo", "messageContent": [toTelegramDict[td]["imageObjDict"][obj]]}
               channelmessage(bot=bot, messageDict=messageDict, chat_id=chat_id)
               messageDict = {'messageCate': "message", "messageContent": [obj]}
               channelmessage(bot=bot, messageDict=messageDict, chat_id=chat_id)
            messageDict = {'messageCate': "message", "messageContent": toTelegramDict[td]["strList"]}
            channelmessage(bot=bot, messageDict=messageDict, chat_id=chat_id) 
         logger.info("User %s's result has been sent.", td)
      logger.info("All users' result has been sent.")
   else: 
      logger.info("Could not gain any new result to users.")         
      messageDict = {"messageCate": "message", "messageContent": ["We do not have any new result"]}
      channelmessage(bot=bot, messageDict=messageDict, chat_id=generalcfg.pubChannelID)

def channelmessage(bot, messageDict, chat_id): 
   messageContent = messageDict["messageContent"]
   for mC in messageContent:
      err = 0
      for err in range(generalcfg.timeoutRetry):
         try:
            if messageDict['messageCate'] == 'photo':
               mC.seek(0)
               bot.send_photo(chat_id=chat_id, photo=mC)
            else:
               bot.send_message(chat_id=chat_id, text=mC)
         except:
            err += 1
            time.sleep(1)
         else:
            time.sleep(0.5)
            err = 0
            break
      else:
         print ("network issue")
         err = 0

def autoCreateJob(job):
   job.run_repeating(searcheh, interval=generalcfg.interval, first=5)

def cancel(bot, update, user_data, chat_data):  
   update.message.reply_text(text=replytext.UserCancel)
   logger.info("User %s has canceled the process.", str(update.message.from_user.username))
   user_data.clear()
   chat_data.clear()
   logger.info("The user_data and chat_data of user %s has cleared", str(update.message.from_user.username))
   return ConversationHandler.END

def error(bot, update, error):
   logger.warning('Update "%s" caused error "%s"', update, error)

def main():
   updater = Updater(token=generalcfg.token)
   dp =updater.dispatcher
   job=updater.job_queue
   conv_handler = ConversationHandler(
                  entry_points=[CommandHandler('start', start, pass_user_data=True, pass_chat_data=True)],
                  states={STATE: [MessageHandler(Filters.text, state, pass_user_data=True, pass_chat_data=True)]
                  },
                  fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True, pass_chat_data=True)],
   )
   dp.add_handler(conv_handler)
   dp.add_error_handler(error)
   autoCreateJob(job=job)
   updater.start_polling(poll_interval=1.0, timeout=1.0)
   updater.idle()


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
(STATE) = range(1)

if __name__ == '__main__':
   main()