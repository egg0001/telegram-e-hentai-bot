#!/usr/bin/python3


import requests
from requests import Request, Session




def ehlogin(username, password, mangasession):
   payload = {"UserName": username,
              "PassWord": password,
              'returntype':'8',
               'CookieDate':'1',
               'b':'d',
               'bt':'pone',
             }

   loginurl = "https://forums.e-hentai.org/index.php?act=Login&CODE=01"


   loginres = mangasession.post(loginurl, data=payload)
   htmlcontent = loginres.text
   if htmlcontent.find("incorrect") != -1:
      print ("Username or Password incorrect")
      quit()
   else:
      ehres = mangasession.get("https://e-hentai.org/")
      exhres = mangasession.get("https://exhentai.org/")
      print (mangasession.cookies)
   return mangasession

