import User

class GetUsers(object):
    """description of class"""
    def __init__(self, _bot):
        self.bot = _bot
    
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
            user = User.User(userId, userName)
            users.append(user)
        return users

    '''
    - Read username from hashTagName
    - Return: <list> users
    '''
    def GetUsersFromHastag(self, hashTagName, minLike = 0):
        lsMediaId = self.bot.get_hashtag_medias(hashTagName)
        users = self.GetUsersFromLsMediaId(lsMediaId, minLike)
        return users

    # Đọc list User(userId, userName) từ 1 LocationTag (geoTag)
    def GetUsersFromLocation(self, locationTag, minLike):
        lsMediaId = self.bot.get_hashtag_medias(locationTag)
        users = self.GetUsersFromLsMediaId(lsMediaId, minLike)
        return users

    # Đọc list User(userId, userName) từ 1 bài MediaId
    def GetUsersFromMediaId(self, mediaId):
        usersId = self.GetUsersIdFromMediaId(mediaId)
        users = self.GetUsersFromUsersId(usersId)
        return users

    # Đọc list User(userId, UserName) từ list MediaId
    def GetUsersFromLsMediaId(self, lsMediaId, minLike):
        usersId = []
        for mediaId in lsMediaId:
            usersId += self.GetUsersIdFromMediaId(mediaId, minLike)
            list(dict.fromkeys(usersId))
        users = self.GetUsersFromUsersId(usersId)
        return users

    # Đọc list UserId từ 1 bài đăng Media
    def GetUsersIdFromMediaId(self, mediaId, minLike = 0):
        usersId = []
        usersLikeId = self.bot.get_media_likers(mediaId)
        if len(usersLikeId) > minLike:
            usersCommentId = self.bot.get_media_commenters(mediaId)
            usersId += usersLikeId
            usersId += usersCommentId
            list(dict.fromkeys(usersId))
        return usersId

    # Đọc UserObject(userId, userName) từ UserId
    def GetUserFromUserId(self, userId):
        userName = self.bot.get_username_from_user_id(userId)
        user = User.User(userId, userName)
        return user

    # Đọc list UserObject(userId, userName) từ list UserId
    def GetUsersFromUsersId(self, usersId):
        users = []
        list(dict.fromkeys(usersId))
        for userId in usersId:
            user = self.GetUserFromUserId(userId)
            users.append(user)
        return users

