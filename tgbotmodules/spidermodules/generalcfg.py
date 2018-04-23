#-----------------------bot config session----------------------

token = ""  #The token of the Telegram bot.

maxiumprofile = 3   #The maximun profiles number every actual user could own. 

passcode = 'This is a test passcode.'  # The passcode to verify user and allow them to use this service.

adminID = 'This is a test adminID.'

pubChannelID = "" #Public channel ID, admin could send the result to this channel if the user allow.

interval = (3600*6)  #The interval between every run of spiderfunction.

timeoutRetry = 10  #Retry times to deal with the timeout issue.

forceCookiesEH = True

rest = "3-8" #The interval of every page of the exh/eh for every user
searchInterval = '10-15'  #The search interval between every user
                          # Example 60 or 60-90


#------------------------spider session-------------------------
headers = [{"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",}]  
      
langkeys = ['RUS', 'Indonesian', 'Osomatsu-san', 'English', 'Korean', 'korean', 'Thai', 'Spanish', 'Vietnamese', 'Russian', 'French', 'Italian', 'Portuguese', 'Chinese', 'German'] 
#Rule out unwanted translation


noEngOnlyGallery = True  # Discard all the gerallies only containing English title and not suitable to Eastern users.

proxy = [] # This test proxy setting is ONLY avaliable for the spider modules (PLEASE KEEP IT AS A EMPTY LIST) 


unwantedfemale = ['ssbbw']
unwantedmale = ['males_only'] 
unwantedmisc = []

wantedfemale = []
wantedmale = ['tomgirl']
wantedmisc = []

#Rule out the unwanted tags and keep the wanted tags
#If the gallery's all tags contain unwanted and wanted tags simultaneously, the program would keep the gallery 
#Please use underline to replace space
