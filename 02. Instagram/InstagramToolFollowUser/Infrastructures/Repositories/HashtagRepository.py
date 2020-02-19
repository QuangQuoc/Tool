from Infrastructures.Database.DriverMysql import DriverMysql
from Variables import DatabaseVariables as dbVar
from Models.Hashtag import Hashtag

driver = DriverMysql(dbVar.host, dbVar.user, dbVar.password, dbVar.dbName)

tableName = "Hashtags"

def AddHashtag(hashtag):
    # Lưu hashtag mới vào database
    sql = f"Insert \
           into {tableName} (Name, Title) \
           Values ({hashtag.Name!r}, {hashtag.Title!r})"
    driver.Insert(sql)
    # Đọc lại hashtag mới thêm vào để trả về
    sqlsl = f"SELECT * \
             FROM {tableName} \
             WHERE Name={hashtag.Name!r}"
    data = driver.SelectOne(sqlsl)
    htg = Hashtag(id = data["Id"], name = data["Name"], title = data["Title"])
    return htg

def ReadHashtagId(hashtagName):
    param = "'"+ hashtagName +"'"
    sql = f"SELECT Id FROM Hashtags WHERE Name={hashtagName!r}"
    data = driver.SelectOne(sql)
    if data != None:
        data = data["Id"]
    return data