#!/usr/bin/python3

from tgbotmodules import userdatastore
import json

with open('./userdata/userdata', 'r') as fo:
   userdata = json.load(fo)

for ud in userdata:
   if userdata[ud].get("userchenn"):
      del userdata[ud]["userchenn"]
   userdata[ud].update({'resultToChat': False, "chat_id": ''})

with open('./userdata/userdata', 'w') as fo:
   json.dump(userdata, fo)


