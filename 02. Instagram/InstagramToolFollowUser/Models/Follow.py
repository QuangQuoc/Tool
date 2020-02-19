from Models.Account import Account
from Models.Follower import Follower
class Follow(object):
    """description of class"""
    def __init__(self, id = None, accountId = None, followerId = None, 
                 status = None, followDate = None, unFollowDate = None):
        self.Id = id
        self.Account = Account()
        self.AccountId = accountId
        self.Follower = Follower()
        self.FollowerId = followerId
        self.Status = status
        self.FollowDate = followDate
        self.UnFollowDate = unFollowDate