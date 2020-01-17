import os
import re
import json 
import random
import pickle
import pandas as pd
import urllib.request
from time import sleep
from selenium import webdriver
from pathlib import Path, PureWindowsPath
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

 
PROXY = "192.168.99.100:3121"
fileDir = os.path.dirname(os.path.realpath('__file__'))
fileDirWin = PureWindowsPath(fileDir)
pathDirTool = fileDirWin.parents[1].as_posix()
pathDirFacebook = fileDirWin.parents[0].as_posix()

chromedriver_path = str(pathDirTool) + '/03. Software/Chrome/chromedriver.exe'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko)")
# 1:allow, 2:block 
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)

#driver = webdriver.Chrome(executable_path = chromedriver_path, options=chrome_options)
#driver.implicitly_wait(5) # seconds

api_key = "BTaKJG45nKYfNrYIqYX_MQt6f"

pwd = "quocsang199698"

# kiểm tra xem api còn sống và số tiền lập facebook có còn k
# api_key: api của simthue
# n: số lần thực hiện dịch vụ facebook
def check_api_simthue(api_key, n):
    print("----------check_api_simthue----------")
    try:
        # request json
        response = urllib.request.urlopen("http://api.pvaonline.net/balance?key=" +api_key)
        data = json.loads(response.read())
        print(data)
        # kiểm tra xem api còn sống và còn đủ tiền thực hiện dịch vụ hay không
        if data["success"]:
            print("api_key live")
            # Kiểm tra xem số tiền có đủ thực hiện n lần dịch vụ
            if data["balance"]//1500 >= n:
                result = True
                print("số lần thực hiện dịch vụ tối đa: " + str(data["balance"]//1500))
            else:
                print("số lần thực hiện dịch vụ nhỏ hơn n = " + str(n) + ": " + str(data["balance"]//1500))
                result = False
        else:
            print("api_key die")
            result = False
        print("---------------------------------check_api_simthue: Hoàn thành")        
        return result
    except:
        print("LỖI: check_api_simthue")

# Tạo yêu cầu nhận code facebook từ simthue.com
# status: trạng thái của api kiểm tra ở check_api_simthue, true or false
# api_key: api của simthue
# service_id: id dịch vụ facebook: 9
def create_request(api_key, service_id, status):
    try:
        print("----------create_request----------")
        if status:
            # request json
            response = urllib.request.urlopen("http://api.pvaonline.net/request/create?key=" + api_key + "&service_id=" + str(service_id))
            data = json.loads(response.read())
            print(data)
            # lấy giá trị id trả về
            id = data["id"]
        print("---------------------------------create_request: Hoàn thành")    
        return id
    except:
        print("LỖI: create_request")

# Lấy sdt để lập facebook
# api_key: api của simthue
# request_id: id của lần yêu cầu đó
def get_numberphone(api_key, request_id):
    try:
        print("----------get_numberphone----------")
        # request json
        response = urllib.request.urlopen("http://api.pvaonline.net/request/check?key=" + api_key + "&id=" + request_id)
        data = json.loads(response.read())
        # Kiểm tra có sdt chưa
        while 1:
            if data["number"] != '':
                break
        print(data)
        #  lấy sdt và time sdt tồn tại
        number = data["number"]
        timeleft = data["timeleft"]
        print("number phone: " + str(number) + ", " + "time left: " + str(timeleft))
        print("---------------------------------get_numberphone: Hoàn thành")
        return number
    except:
        print("LỖI: get_numberphone")

# Lấy sms: code trả về từ facebook
# api_key: api của simthue
# request_id: id của lần yêu cầu đó
def get_sms(api_key, request_id):
    try:
        print("----------get_sms----------")
        # request json
        response = urllib.request.urlopen("http://api.pvaonline.net/request/check?key=" + api_key + "&id=" + request_id)
        data = json.loads(response.read())
        timeleft = data["timeleft"]
        # Kiểm tra xem có sms chưa
        while 1:
            if data["sms"] != []:
                sms = re.findall("\d+", data["sms"][0])
                code = sms[1]
                print("Mã code: " + code)
                break
            elif data["timeleft"] == 0:
                code = ""
                print("Không có sms")
                break
        print("---------------------------------get_sms: Hoàn thành")    
        return code
    except:
        print("LỖI: get_sms")

def create_account():
    try:
        ho = ['Nguyễn','Trương','Trần','Lê','Đinh','Hồ','Phan','Phạm','Lý','Đinh','Đặng','Đỗ','Bùi','Ngô','Võ','Hoàng','Tôn']
        tenNu = ['Cẩm Hạnh', 'Cẩm Hiền', 'Cẩm Hường', 'Cẩm Liên', 'Cẩm Linh', 'Cẩm Ly', 'Cẩm Nhi', 'Cẩm Nhung', 'Cam Thảo', 'Cẩm Thúy', 'Cẩm Tú', 'Cẩm Vân', 'Cẩm Yến', 'Cát Cát', 'Cát Linh', 'Cát Ly', 'Cát Tiên', 'Chi Lan', 'Chi Mai', 'Ái Hồng', 'Ái Khanh', 'Ái Linh', 'Ái Nhân', 'Ái Nhi', 'Dã Lan', 'Dạ Lan', 'Dạ Nguyệt', 'Dã Thảo', 'Dạ Thảo', 'Dạ Thi', 'Dạ Yến', 'Ðan Khanh', 'Đan Linh', 'Ðan Quỳnh', 'Đan Thư', 'Ðan Thu', 'Di Nhiên', 'Diễm Châu', 'Diễm Chi', 'Diễm Hằng', 'Diễm Hạnh', 'Diễm Hương', 'Diễm Khuê', 'Diễm Kiều', 'Diễm Liên', 'Diễm Lộc', 'Diễm My', 'Diễm Phúc', 'Diễm Phước', 'Diễm Phương', 'Diễm Phượng', 'Diễm Quyên', 'Diễm Quỳnh', 'Diễm Thảo', 'Diễm Thư', 'Diễm Thúy', 'Diễm Trang', 'Diễm Trinh', 'Diễm Uyên', 'Diên Vỹ', 'Diệp Anh', 'Diệp Vy', 'Diệu Ái', 'Diệu Anh', 'Diệu Hằng', 'Diệu Hạnh', 'Diệu Hiền', 'Diệu Hoa', 'Diệu Hồng', 'Diệu Hương', 'Diệu Huyền', 'Diệu Lan', 'Diệu Linh', 'Diệu Loan', 'Diệu Nga', 'Diệu Ngà', 'Diệu Ngọc', 'Diệu Nương', 'Diệu Thiện', 'Diệu Thúy', 'Diệu Vân', 'Duy Hạnh', 'Duy Mỹ', 'Duy Uyên', 'Duyên Hồng', 'Duyên My', 'Duyên Mỹ', 'Duyên Nương', 'Hà Giang', 'Hà Liên', 'Hà Mi', 'Hà My', 'Hà Nhi', 'Hà Phương', 'Hạ Phương', 'Hà Thanh', 'Hà Tiên', 'Hạ Tiên', 'Hạ Uyên', 'Hạ Vy', 'Hạc Cúc', 'Hải Ân', 'Hải Anh', 'Hải Châu', 'Hải Ðường', 'Hải Duyên', 'Hải Miên', 'Hải My', 'Hải Mỹ', 'Hải Ngân', 'Hải Nhi', 'Hải Phương', 'Hải Phượng', 'Hải San', 'Hải Sinh', 'Hải Thanh', 'Hải Thảo', 'Hải Uyên', 'Hải Vân', 'Hải Vy', 'Hải Yến', 'Hàm Duyên', 'Hàm Nghi', 'Hàm Thơ', 'Hàm Ý', 'Hằng Anh', 'Hạnh Chi', 'Hạnh Dung', 'Hạnh Linh', 'Hạnh My', 'Hạnh Nga', 'Hạnh Phương', 'Hạnh San', 'Hạnh Thảo', 'Hạnh Trang', 'Hạnh Vi', 'Hảo Nhi', 'Hiền Chung', 'Hiền Hòa', 'Hiền Mai', 'Hiền Nhi', 'Hiền Nương', 'Hiền Thục', 'Hiếu Giang', 'Hiếu Hạnh', 'Hiếu Khanh', 'Hiếu Minh', 'Hiểu Vân', 'Hồ Diệp', 'Hoa Liên', 'Hoa Lý', 'Họa Mi', 'Hoa Thiên', 'Hoa Tiên', 'Hoài An', 'Hoài Giang', 'Hoài Hương', 'Hoài Phương', 'Hoài Thương', 'Hoài Trang', 'Hoàn Châu', 'Hoàn Vi', 'Hoàng Cúc', 'Hoàng Hà', 'Hoàng Kim', 'Hoàng Lan', 'Hoàng Mai', 'Hoàng Miên', 'Hoàng Oanh', 'Hoàng Sa', 'Hoàng Thư', 'Hoàng Yến', 'Hồng Anh', 'Hồng Bạch Thảo', 'Hồng Châu', 'Hồng Ðào', 'Hồng Diễm', 'Hồng Ðiệp', 'Hồng Hà', 'Hồng Hạnh', 'Hồng Hoa', 'Hồng Khanh', 'Hồng Khôi', 'Hồng Khuê', 'Hồng Lâm', 'Hồng Liên', 'Hồng Linh', 'Hồng Mai', 'Hồng Nga', 'Hồng Ngân', 'Hồng Ngọc', 'Hồng Như', 'Hồng Nhung', 'Hồng Oanh', 'Hồng Phúc', 'Hồng Phương', 'Hồng Quế', 'Hồng Tâm', 'Hồng Thắm', 'Hồng Thảo', 'Hồng Thu', 'Hồng Thư', 'Hồng Thúy', 'Hồng Thủy', 'Hồng Vân', 'Hồng Xuân', 'Huệ An', 'Huệ Hồng', 'Huệ Hương', 'Huệ Lâm', 'Huệ Lan', 'Huệ Linh', 'Huệ My', 'Huệ Phương', 'Huệ Thương', 'Hương Chi', 'Hương Giang', 'Hương Lâm', 'Hương Lan', 'Hương Liên', 'Hương Ly', 'Hương Mai', 'Hương Nhi', 'Hương Thảo', 'Hương Thu', 'Hương Thủy', 'Hương Tiên', 'Hương Trà', 'Hương Trang', 'Hương Xuân', 'Huyền Anh', 'Huyền Diệu', 'Huyền Linh', 'Huyền Ngọc', 'Huyền Nhi', 'Huyền Thoại', 'Huyền Thư', 'Huyền Trâm', 'Huyền Trân', 'Huyền Trang', 'Huỳnh Anh', 'Ái Thi', 'Ái Thy', 'Ái Vân', 'An Bình', 'An Di', 'An Hạ', 'An Hằng', 'An Nhàn', 'An Nhiên', 'Anh Chi', 'Anh Ðào', 'Ánh Dương', 'Ánh Hoa', 'Ánh Hồng', 'Anh Hương', 'Ánh Lệ', 'Ánh Linh', 'Anh Mai', 'Ánh Mai', 'Ánh Ngọc', 'Ánh Nguyệt', 'Anh Phương', 'Anh Thảo', 'Anh Thi', 'Anh Thơ', 'Ánh Thơ', 'Anh Thư', 'Anh Thy', 'Ánh Trang', 'Ánh Tuyết', 'Ánh Xuân', 'Bạch Cúc', 'Bạch Hoa', 'Bạch Kim', 'Bạch Liên', 'Bạch Loan', 'Bạch Mai', 'Bạch Quỳnh', 'Bạch Trà', 'Bạch Tuyết', 'Bạch Vân', 'Bạch Yến', 'Ban Mai', 'Băng Băng', 'Băng Tâm', 'Bảo Anh', 'Bảo Bình', 'Bảo Châu', 'Bảo Hà', 'Bảo Hân', 'Bảo Huệ', 'Bảo Lan', 'Bảo Lễ', 'Bảo Ngọc', 'Bảo Phương', 'Bảo Quyên', 'Bảo Quỳnh', 'Bảo Thoa', 'Bảo Thúy', 'Bảo Tiên', 'Bảo Trâm', 'Bảo Trân', 'Bảo Trúc', 'Bảo Uyên', 'Bảo Vân', 'Bảo Vy', 'Bích Châu', 'Bích Chiêu', 'Bích Ðào', 'Bích Ðiệp', 'Bích Duyên', 'Bích Hà', 'Bích Hải', 'Bích Hằng', 'Bích Hạnh', 'Bích Hảo', 'Bích Hậu', 'Bích Hiền', 'Bích Hồng', 'Bích Hợp', 'Bích Huệ', 'Bích Lam', 'Bích Liên', 'Bích Loan', 'Bích Nga', 'Bích Ngà', 'Bích Ngân', 'Bích Ngọc', 'Bích Như', 'Bích Phượng', 'Bích Quân', 'Bích Quyên', 'Bích San', 'Bích Thảo', 'Bích Thoa', 'Bích Thu', 'Bích Thủy', 'Bích Ty', 'Bích Vân']   
        tenNam =
        print("----------create_account----------")
        driver.get("https://mbasic.facebook.com/reg")
        # Họ
        driver.find_element_by_xpath("//*[@id=\"firstname\"]/div/input").send_keys(ho[random.randint(0, len(ho))])
        # Tên
        driver.find_element_by_xpath("//*[@id=\"firstname\"]/div/div/input").send_keys(ten[random.randint(0, len(ten))])
        # Số điện thoại hoặc email
        driver.find_element_by_xpath("//*[@id=\"contactpoint_step_input\"]")
        # Giới tính Nữ
        driver.find_element_by_xpath("/html/body/div/div/div[2]/div[2]/table/tbody/tr/td/form/div[3]/div/div[2]/div/table/tbody/tr/td[1]/label/input")
        # Giới tính nam
        driver.find_element_by_xpath("/html/body/div/div/div[2]/div[2]/table/tbody/tr/td/form/div[3]/div/div[2]/div/table/tbody/tr/td[2]/label/input")
        # pass
        driver.find_element_by_xpath("//*[@id=\"password_step_input\"]").send_keys(pwd).send_keys(Keys.RETURN)

    except:    
        print("LỖI: create_account")


# a = check_api_simthue(api_key = api_key, n = 1)
# b = create_request(api_key = api_key, service_id = 9, status = a)
# c = get_numberphone(api_key = api_key, request_id = "RMns-Zrg_16V")
# get_sms(api_key = api_key, request_id = "RMns-Zrg_16V")

