from Infrastructures.Database.DriverMysql import DriverMysql
from Variables import DatabaseVariables as dbVar
from Models.User import User
from Models.Follower import Follower

driver = DriverMysql(dbVar.host, dbVar.user, dbVar.password, dbVar.dbName)

def ReadFollowers(hashtagId):
    sql = f"SELECT * FROM Followers WHERE HashTagId={str(hashtagId)!r}"
    data = driver.SelectAll(sql)
    if len(data) > 0:
        flwers = []
        for row in data:
            flwer = Follower(id = row["Id"], userName = row["UserName"], 
                             userId = row["UserId"], hashtagId = row["HashtagId"])
            flwers.append(flwer)
        return flwers
    return data

def AddFollower(flwer):
    if flwer.UserName != None:
        sql = f"INSERT \
               INTO Followers (UserName, UserId, HashTagId) \
               VALUES ({flwer.UserName!r}, {str(flwer.UserId)!r}, {str(flwer.HashtagId)!r})"
    else:
        sql = f"INSERT \
               INTO Followers (UserId, HashTagId) \
               VALUES ({str(flwer.UserId)!r}, {str(flwer.HashtagId)!r})"
    driver.Insert(sql)