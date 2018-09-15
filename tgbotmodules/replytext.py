#!/usr/bin/python3

#-----------------------verify section---------------------------------------

startMessage = "Welcome to Nakazawa Bookstore, please show your vip card."


GeneralInfo = ("You have {0} profile(s) on this service. \n" +
               "If you have more than {1} profiles on this service, "  +
               "you would not allow to create new one. \n" +
               "This bot ONLY SUPPORT ASCII input. \n" +
               "You can type RETURN to return to previous step (only works in guiding mode) or /cancel to exit. \n" +
               "If the whole process stocks for a while (caused bytimeout), " +
               "please enter the same value again or type RETURN to back to previous step. \n" +
               "If you want to browse, modify, delete your profile(s) or use advance profile create mode, " +
               "please type ADVANCE. \n"
              )

ProfileExcessVerify = ("Oops, you already have {0} profiles, " +
                       "We would guide you to advance mode and please type INFO to get information \n" 
                      )

ToUserCookies = ("Please input your cookies as the begining of profile creation \n" + 
                 "(example: {'key1': 'value1', 'key2': 'value2',...,}); \n" +
                 "otherwise if you only want to search e-hentai, please inpute {}."
                )

VerifyFail = "Oops, your vip card is INCORRECT, please show another one."

#----------------------usercookies section------------------------------------

CookiesToADV = ('Now you have entered advance mode. \n' +
                'Please type INFO to get information.'
               )

CookiesError = "Oops, you enter a wrong cookies dict, please check it and enter again."

ToUserKey = ("Now please input your search keyword, " +
             "notice that e-hentai and exhentai only support AND as well as NOT logic." +
             "You can input EMPTY to set a empty keyword"
            )

#--------------------userkey section-----------------------------------------

ReturnToCookies = 'Return to pervious step (enter cookies).' 

ToUserRange = "Now please input your search range (pages), maximum is FIVE PAGES."

#--------------------userrange section---------------------------------------

ReturnToKey = 'Return to pervious step (enter search keyword).'

RangeError = 'Oops, you should enter a NUMBER, please enter again'

ToUserCate = ("Now please input your search categories and use comma to separate them " +
              "(example: doujinshi or doujinshi manga); "+ 
              "notice that an error category input would cause a empty search result"
             )

#--------------------search cateoury section----------------------------------------

ReturnToRange = 'Return to pervious step (enter range).'

CateError = 'Oops, you have enter a wrong categories list, please check it and retry.'

ToUserResult = ("Please type the option number to choice a method receiving your search result "
               "in every {0} hours. \n" +
               "Typing '1' indicates you would receive your result in this chat. \n" +
               "Typing '2' indicates you would receive your result in the channel of this bot's admin. \n" +
               "Typing '3' indicates you would receive your result in both this chat and the channel of" +
               "this bot's admin."
              )

#--------------------userresult section---------------------------------------

ReturnToCate = 'Return to pervious step (enter search categories).'

ToVirtualUsername = ("Lastly, please enter your virtual username. " + 
                     "This username would be exploited to show the result on the public chennal " +
                     "if you have allowed this on the pervious step. "
                    )
ChoiceError = ("Oops, you have typed some strange things, please retry.")

#--------------------virtualusername section-------------------------------------

ReturnToUserResult = 'Return to pervious step (how to send your result).'

ToStoreInfo = ("You have entered all the necessary information, " +
               "let us show it to you. \n" +
               "If all kinds of the information are correct, you can type YES to store them " +
               "and other input would be considered as NO and you will return to pervious step."
              )

#--------------------storeinfo section-----------------------------------------

Stored = "Great, your information is stored and this bot would begin to work!"

StoreError = ('Oops, your information is not saved due to some issues, ' +
              'like the virtual username has been used, ' +
              'please try a new virtual username again. \n' +
              'If you continually encounter this message, please contect admin'
)

ReturnToVirtualUsername = "Return to input virtual username."

ReturnToAdvCreate = "Return to edit, please input the new userdata again."

#-------------------advance section---------------------------------------------

ProfileAmount = "You have {0} profile(s) on this service. \n"

FuncSelect = ('Typing ADVCREATE would allow you to use advance mode to create profile by ONLY ONE step \n' +
              'Typing ADVEDIT would allow you to edit existed profile(s). \n' +
              'Typing DELETE would allow you to delete your existed profile(s) \n' +
              'Typing HELP would show your profile(s) information as well as this message again.'
             )

AdvError = ("Oops, you have typed some strange things, please try again. " +
            "If this message is appearring repeatedly, please type INFO again."
           )

#-------------------advguide section---------------------------------------------

ProfileExcess = ('Oops, you have too many profiles and CANNOT create more, ' +
                 'please select other functions.'
                )

ToAdvCreate = ('Exploiting advance creating mode indicates you would use ' +
                                        'our template to create your profile. \n' +
                                        'This is the template. \n' +
                                        '''{
                                            "usercate": ["CATE1", "CATE2", "..."], 
                                            "resultToChat": True, 
                                            "userranges": RANGE(INT),
                                            "userkey": "USERKEY", 
                                            "userpubchenn": False,
                                            "virtualusername": "VIRTUALUSERNAME", 
                                            "usercookies": {
                                                            "KEY1": "VALUE1", 
                                                            "KEY2": "VALUE2"
                                                            }
                                            }'''
               )

NoProfile = ("You do not have any profile on this service so " +
             "could not delete them, please choice other functions"
            )

SelectProfileNameToEdit = "Please input the virtual username you want to edit."

NoProfileToDelete = ("You do not have any profile on this service so " +
                    "could not delete them, please choice other functions"
                    )

SelectProfileNameToDelete = "Now please type the virtual username you want to delete"

ErrorInput = ('Oops, you have typed some strange things, please try again. ' +
              'If this message is appearring repeatedly , please select the function again.'
             )

#--------------------advcreate section--------------------------------------------

ErrorSyntax = ('Oops, it seems that you have enter a wrong profile, '+
               'please check it and enter again.'
              )

UserDataCheckFail = ('Oops, it seems that you are trying something wired in the user ' +
                     'profile, please check it and enter again.'
                    )

UserCateSyntaxError = ('Oops, the usercate must be list rather than other categories, ' +
                       'please check it and enter again.'
                      )

UserCateCheckFail = ('Oops, it seems that you have entered some wrong search categories, ' +
                     'please check it and enter again.'
                    ) 

UserRangesValueError = ('Oops, it seems that you have entered a wrong userranges, ' +
                        '(should be int), please check it and enter again.'
                       )

UserReceiveResultError = ('Oops, you should choice at least ONE method to receive your result, ' +
                          'please try again.')

RangeExcess = ('It seems that you have entered a search range more than, ' +
                '5 pages, limit to 5 pages'
              )

UserDataCheckComplete = ('Your profile looks great! ' +
                         'If this profile does not have any issue, ' +
                         'please type YES to store it and other typing would be considered as NO.' 
                        )

#----------------------advedit section--------------------------------------------

ErrorVirtualUserName = ("Oops, it seems that you have input a wrong virtual username, " +
                        "please check it and try again"
                       )

RetriveProfileSuccess = ("Let us show the userdata you want to edit, " +
                         "Please copy this userdata and edit it \n"
                        )

#----------------------delete section----------------------------------------------

VirUsernameNotFound = ("Oops, it seems that you have enter a worng virtual username, " +
                       "please retry."
                      )

DeleteSuccess = ("Virtual username profile {0} " +
                 "has been successfully deleted. Now back to ADVANCE, " +
                 "please type INFO to get more information."
                )

#----------------------------cancel---------------------
UserCancel = "You have canceled the process."