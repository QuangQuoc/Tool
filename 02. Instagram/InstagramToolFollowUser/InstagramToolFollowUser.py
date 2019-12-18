import argparse
import os
import sys
import random
from enum import Enum, auto
from time import sleep
import pandas as pd
from instabot import Bot

#define
class USERFROM(Enum):
    HASHTAG = auto()
    LOCATION = auto()
    USERNAME = auto()
    POST = auto()

#global variables
followDelayTime = random.randint(100, 120)
bot = Bot(follow_delay=followDelayTime)

#parameters
userName = "" 
passWord = ""
cookieFileName = userName + "_cookie.txt"

hashTag = ""
locationTag = ""
postId = ""
usersFile = ""
userField = ""


users = GetUserFromFile(usersFile, userField)


methodGetUser = USERFROM.HASHTAG

#login
bot.login(username=userName, password=passWord, use_cookie=True, cookie_fname=cookieFileName)


'''
    - Read username from file
    - Return: <list> users
'''
def GetUserFromFile(fileName, userField):
    data = pd.read_excel(fileName)
    return data[userField]

'''
    - Read username from hashTagName
    - Return: <list> users
'''
def GetUsersFromHastag(hashTagName, minLike = 0):
    users = []
    lsMediaId = bot.get_hashtag_medias(hashTagName)
    for mediaId in lsMediaId:
        usersLikeId = bot.get_media_likers(mediaId)
        #TH: Media co so like lon hon minLike
        if len(usersLikeId) > minLike:
            usersCommentId = bot.get_media_commenters(mediaId)
            users.append(usersLikeId)
            users.append(usersCommentId)
            list(dict.fromkeys(users))
