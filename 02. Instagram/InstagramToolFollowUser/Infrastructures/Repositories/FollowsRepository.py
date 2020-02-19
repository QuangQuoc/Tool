from Infrastructures.Database.DriverMysql import DriverMysql
from Variables import DatabaseVariables as dbVar
from Models.User import User
from datetime import datetime
from Models.Follow import Follow

driver = DriverMysql(dbVar.host, dbVar.user, dbVar.password, dbVar.dbName)

def ReadFollowsHtg(accId, hashtagId):
    sql = f"SELECT * \
           FROM Follows \
           INNER JOIN Followers \
           ON Follows.FollowerId = Followers.Id \
           WHERE Followers.HashTagId = {str(hashtagId)!r}\
           AND Follows.AccountId = {str(accId)!r}"
    data = driver.SelectAll(sql)
    if len(data) > 0:
        follows = []
        for row in data:
            fl = Follow(id = row["Id"], accountId = row["AccountId"], 
                        followerId = row["FollowerId"], status = row["Status"], 
                        followDate = row["FollowDate"], unFollowDate = row["UnFollowDate"])
            follows.append(fl)
        return follows
    return data

def ReadFollowsStatus(accId, status):
    sql = f"SELECT * \
           FROM Follows \
           INNER JOIN Followers \
           ON Follows.FollowerId = Followers.Id \
           WHERE Follows.AccountId ={accId!r}\
           AND Follows.Status = {str(status)}"
    data = driver.SelectAll(sql)
    if len(data) > 0:
        follows = []
        for row in data:
            fl = Follow(id = row["Id"], accountId = row["AccountId"], 
                        followerId = row["FollowerId"], status = row["Status"], 
                        followDate = row["FollowDate"], unFollowDate = row["UnFollowDate"])
            fl.Follower.UserId = row["UserId"]
            follows.append(fl)
        return follows
    return data

def AddFollow(follow): 
    sql = f"INSERT \
           INTO Follows \
           (AccountId, FollowerId, Status) \
           VALUES ({follow.AccountId!r}, {follow.FollowerId!r}, {str(follow.Status)})"
    driver.Insert(sql)

def UpdateStatus(followId, status):
    sql = f"UPDATE Follows \
           SET Status = {str(status)} \
           WHERE Id = {followId!r}"
    driver.Update(sql)

def UpdateDateFollow(followId, date):
    sql = f"UPDATE Follows \
            SET FollowDate = {str(date)!r} \
            WHERE Id = {followId!r}"
    driver.Update(sql)