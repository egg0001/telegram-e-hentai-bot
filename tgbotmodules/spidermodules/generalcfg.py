#-----------------------bot config session----------------------

token = ""  #The token of the Telegram bot.

maxiumprofile = 3   #The maximun profiles number every actual user could own. 

passcode = 'This is a test passcode.'  # The passcode to verify user and allow them to use this service.

adminID = 'This is a test adminID.'

pubChannelID = "" #Public channel ID, admin could send the result to this channel if the user allow.

interval = (3600*6)  #The interval (second) between every run of spiderfunction.

timeoutRetry = 5 #Retry times to deal with the timeout issue during sending users' searching result.

forceCookiesEH = True # This variable would try to use user's cookies to access e-hentai after these cookies failed to access exhentai.

rest = "3-8" #The interval of every page of the exh/eh for every user

searchInterval = '10-15'  #The search interval between every user
                          # Example 60 or 60-90

userPageLimit = 5 # The pages limitation (integret number) for every user's searching process at every searching cycle.
                  # Since e-hentai/exhentai would not update a huge amount of galleries in the preset time period
                  # (six hours), setting it to a large number is useless and would add some pressure to
                  # e-hentai/exhentai's server.  

#------------------------spider session-------------------------
headers = [{"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",}]  
      
langkeys = ['gay', 'Gay', 'RUS', 'Indonesian', 'Osomatsu-san', 'English', 'Korean', 'korean', 'Thai', 'Spanish', 'Vietnamese', 'Russian', 'French', 'Italian', 'Portuguese', 'German'] 
#This list contains ALL the UNWANTED keywords the bot admin wants to rule out on the titles in the index pages of e-hentai/exhentai.
#Since the history reason, it keeps to be called langkeys.


noEngOnlyGallery = True  # Discard all the gerallies only containing English title and not suitable to Eastern users.

proxy = [] # This test proxy setting is ONLY avaliable for the spider modules.
                           # PLEASE KEEP IT AS AN EMPTY LIST

dlFullPreviewImage = True # This variable would determin whether the bot downloads the first image in the gallery as the preview image sending to channel.
                          # While it would provide a better image qualtry, it would also consume e-hentai image quota.

dlRetry = 3  # This variable determins the retry times of download preview images' function.

unwantedfemale = ['ssbbw']
unwantedmale = ['males_only', 'yaoi'] 
unwantedmisc = []

wantedfemale = []
wantedmale = ['tomgirl']
wantedmisc = []

#Rule out the unwanted tags and keep the wanted tags
#If the gallery's tags contain both unwanted and wanted tags simultaneously, the program would keep the gallery 
#Please use underline to replace space
