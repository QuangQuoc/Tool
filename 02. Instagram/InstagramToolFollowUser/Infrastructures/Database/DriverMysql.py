import pymysql

class DriverMysql(object):
    """description of class"""
    def __init__(self, host, user, password, dbname, charset='utf8mb4'):
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.charset = charset
        self.cursors = pymysql.cursors.DictCursor


        '''
        Sử dụng để tạo kết nối đến database
        '''
    def GetConnect(self):
        connection = None
        try:
            connection = pymysql.connect(host=self.host,
                                         user=self.user,
                                         password=self.password,
                                         db=self.dbname,
                                         charset=self.charset,
                                         cursorclass=self.cursors)
            print("Kết nối database thành công!")
        except Exception as e:
            print("Lỗi kết nối Db: " + e)
        finally:
            return connection

    def Execute(self, sql):
        connection = self.GetConnect()
        data = None
        if connection != None:
            cursor = connection.cursor()
            try:
                cursor.execute(sql)
                data = cursor
            except Exception as e:
                print(e)
            finally:
                connection.close()
                return data

    def Insert(self, sql):
        connection = self.GetConnect()
        data = None
        if connection != None:
            cursor = connection.cursor()
            try:
                cursor.execute(sql)
                connection.commit()
            except Exception as e:
                print(e)
            finally:
                connection.close()

    def SelectOne(self, sql):
        connection = self.GetConnect()
        data = None
        if connection != None:
            cursor = connection.cursor()
            try:
                cursor.execute(sql)
                data = cursor.fetchone()
            except Exception as e:
                print(e)
            finally:
                connection.close()
                return data

    def SelectAll(self, sql):
        connection = self.GetConnect()
        data = None
        if connection != None:
            cursor = connection.cursor()
            try:
                cursor.execute(sql)
                data = cursor.fetchall()
            except Exception as e:
                print(e)
            finally:
                connection.close()
                return data
    
    def Update(self, sql):
        connection = self.GetConnect()
        data = None
        if connection != None:
            cursor = connection.cursor()
            try:
                cursor.execute(sql)
                connection.commit()
            except Exception as e:
                print(e)
            finally:
                connection.close()

