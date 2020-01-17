class FollowUsers(object):
    """description of class"""
    def __init__(self, _bot):
        self.bot = _bot

    def FollowAndSaveUser(self, userId):
        self.bot.follow(userId)


