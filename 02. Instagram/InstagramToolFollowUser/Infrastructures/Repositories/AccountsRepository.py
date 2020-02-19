from Infrastructures.Database.DriverMysql import DriverMysql
from Variables import DatabaseVariables as dbVar
from Models.User import User
from Models.Account import Account

driver = DriverMysql(dbVar.host, dbVar.user, dbVar.password, dbVar.dbName)
tableName = "Accounts"

def AddAccount(account): 
    sql = f"INSERT \
           INTO {tableName} (UserName, UserId, Password) \
           VALUES ({account.UserName!r}, {account.UserId!r}, {account.Password!r})"
    driver.Insert(sql)
    sqlsl = f"SELECT * \
              FROM {tableName} \
              WHERE UserName={account.UserName!r}"
    data = driver.SelectOne(sqlsl)
    acc = Account(id=data["Id"], userName=data["UserName"], 
                  userId=data["UserId"], password=data["Password"])
    return acc

def ReadAccount(userName):
    sql = f"SELECT * \
          FROM {tableName} \
          WHERE UserName={userName!r}"
    data = driver.SelectOne(sql)
    if data != None:
        acc = Account(id=data["Id"], userName=data["UserName"],
                      userId=data["UserId"], password=data["Password"])
        return acc
    return data