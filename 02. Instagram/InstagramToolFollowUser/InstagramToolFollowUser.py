import argparse
import os
import sys
import random
from enum import Enum, auto
from time import sleep
import pandas as pd
from instabot import Bot
from Models.User import User
import GetUsers
from Controllers import FollowController as flwCtrl
from Models.Account import Account
from Models.Hashtag import Hashtag
from Infrastructures.Repositories import AccountsRepository as accRepo
#define
class USERFROM(Enum):
    HASHTAG = auto()
    LOCATION = auto()
    USER_FILE = auto()
    POST = auto()

#-----------------------------Global Variables------------------------------
followDelayTime = random.randint(200, 300)
#bot = Bot(follow_delay=followDelayTime)
bot = Bot()

# Main Function => Run file

def main():
    #-----------------------------Input Parameters------------------------------
    #- UserInfo
    userName = "hoian_handmadetailoring"
    userId = "29845994399"
    password = "AB21121995"
    cookieFileName = userName + "_cookie.txt"
    # Kiểm tra Account đã có chưa
    acc = accRepo.ReadAccount(userName)
    if acc == None:
        acc = Account(userName=userName, password=password, userId=userId)
        acc = accRepo.AddAccount(acc)
    #- DataInput for GetMethod
    hashtags = ["hoiantailoring", "hoiancustommade", "customtailoring", "hoiantailor", "Hoianshopping", "travelclothes", "travelclothesforwomen", "hoiantrip"]
    hashtagName = "hoiancustomtailor"
    locationTag = ""
    postId = ""
    usersFile = ""
    userNameField = ""
    userIdField = ""
    hashtag = Hashtag(name = hashtagName)
    
    #- Follow Method
    getUserMethod = USERFROM.HASHTAG
    #- Giới hạn số like của 1 bài viết muốn lấy Liker và Commenter
    minLike = 10 
    #users = GetUserFromFile(usersFile, userField)
    #----------------------------------Login--------------------------------------
    bot.login(username=acc.UserName, password=acc.Password, use_cookie=True, cookie_fname=cookieFileName)
    getUsers = GetUsers.GetUsers(bot)
    
    #testController
    for htName in hashtags:
        htag = Hashtag(name = htName)
        flwCtrl.FollowHashTag(acc, htag, bot)
    #---------------------------------Follow--------------------------------------
    # Get list User(userId, userName)
    if getUserMethod == USERFROM.HASHTAG:
        users = getUsers.GetUsersFromHastag(hashTag, minLike)
    elif getUserMethod == USERFROM.LOCATION:
        users = getUsers.GetUsersFromLocation(locationTag, minLike)
    elif getUserMethod == USERFROM.POST:
        users = getUsers.GetUsersFromMediaId(postId)
    elif getUserMethod == USERFROM.USER_FILE:
        users = getUsers.GetUsersFromFile(usersFile, userNameField, userIdField)
    # Follow user
    if len(users) > 0:
        for i in range(0, len(users)):
            bot.follow(users[i].userId)
            # Lưu User vào file excel


if __name__ == "__main__":
    main()


'''
    - Read username from file
    - Return: <list> users
    DOING
'''
def GetUsersFromFile(fileName, userNameField, userIdField):
    users = []
    colsName = [userIdField, userNameField]
    df = pd.read_excel(fileName, names = colsName)
    for cell in df:
        userName = df[userNameField]
        userId = df[userIdField]
        user = User(userId, userName)
        users.append(user)
    return users
    

'''
    - Read username from hashTagName
    - Return: <list> users
'''
def GetUsersFromHastag(hashTagName, minLike = 0):
    lsMediaId = bot.get_hashtag_medias(hashTagName)
    users = GetUsersFromLsMediaId(lsMediaId)
    return users

# Đọc list User(userId, userName) từ 1 LocationTag (geoTag)
def GetUsersFromLocation(locationTag, minLike):
    lsMediaId = bot.get_hashtag_medias(locationTag)
    users = GetUsersFromLsMediaId(lsMediaId)
    return users

# Đọc list User(userId, userName) từ 1 bài MediaId
def GetUsersFromMediaId(mediaId):
    usersId = GetUsersIdFromMediaId(mediaId)
    users = GetGetUsersFromUsersId(usersId)
    return users

# Đọc list User(userId, UserName) từ list MediaId
def GetUsersFromLsMediaId(lsMediaId):
    usersId = []
    for mediaId in lsMediaId:
        usersId += GetUsersIdFromMediaId(mediaId, minLike)
        list(dict.fromkeys(usersId))
    users = GetUsersFromUsersId(usersId)
    return users

# Đọc list UserId từ 1 bài đăng Media
def GetUsersIdFromMediaId(mediaId, minLike = 0):
    usersId = []
    usersLikeId = bot.get_media_likers(mediaId)
    if len(usersLikeId) > minLike:
        usersCommentId = bot.get_media_commenters(mediaId)
        usersId += usersLikeId
        usersId += usersCommentId
        list(dict.fromkeys(users))
    return usersId

# Đọc UserObject(userId, userName) từ UserId
def GetUserFromUserId(userId):
    userName = bot.get_username_from_user_id(userId)
    user = User(userId, userName)
    return user

# Đọc list UserObject(userId, userName) từ list UserId
def GetUsersFromUsersId(usersId):
    users = []
    list(dict.fromkeys(users))
    for userId in usersId:
        user = GetUserFromUserId(userId)
        users.append(user)
    return users
