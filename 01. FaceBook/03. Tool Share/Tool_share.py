import random
import re
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pickle
import os
from pathlib import Path, PureWindowsPath
 
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
# 1:allow, 2:block 
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(executable_path = chromedriver_path, options=chrome_options)
driver.implicitly_wait(15) # seconds

def login(usr, pwd):
    print("----------login: "+usr+"----------")
    # biến kiểm tra live cookies
    checkCookies = ""
    # lấy cookies ra
    cookieFileName = str(pathDirFacebook) + "/02. Cookies/" + usr + "cookies.pkl"
    try:
        # Go to facebook.com
        driver.get("https://www.facebook.com/")

        # Login using cookies
        try:
            cookies = pickle.load(open(cookieFileName, "rb"))
        except:
            cookies = ""
        if len(cookies) != 0:
            for cookie in cookies:
                if 'expiry' in cookie:
                    del cookie['expiry']
                driver.add_cookie(cookie)  
            driver.get("https://www.facebook.com/")    
            checkCookies = driver.get_cookies()
            if len(checkCookies) != 10:
                cookies = ""
        if len(cookies) == 0:
            pickle.dump("" , open(cookieFileName,"wb"))
            # Enter user email
            try:
                elem = driver.find_element_by_id("email")
            except:
                elem = driver.find_element_by_name("email")
            elem.send_keys(usr)
            # Enter user password
            try:
                elem = driver.find_element_by_id("pass")
            except:
                elem = driver.find_element_by_name("pass")
            elem.send_keys(pwd)
            # Login
            elem.send_keys(Keys.RETURN)
            sleep(40)
            # Get Cookies sau khi dang nhap
            pickle.dump(driver.get_cookies() , open(cookieFileName,"wb"))
        driver.get("https://mbasic.facebook.com")
        print("------------------------------------------------------------login: Hoàn thành")
    except:
        print("LỖI: login "+usr)


# Lướt newfeed facebook  
# n: số lần lướt
def luot_newFeed(n):
    try:
        print("----------luot_newFeed----------")
        driver.get("https://mbasic.facebook.com/")
        sleep(5)
        try:
            # Ckick nút chuyển tiếp luot_newFeed đầu tiên
            driver.find_element_by_xpath("//*[@id=\"m_newsfeed_stream\"]/a").click()
        except:
            print("Chưa có nút chuyển tiếp luot_newFeed đầu tiên") 
        # Thực hiện n lần lướt
        for i in range(n):
            # Lấy chiều dài của thanh cuốn
            last_height = driver.execute_script("return document.body.scrollHeight")
            sleep(random.randint(7, 10))
            # kéo thanh cuốn xuống 1 khoảng = last_height/random.randint(0, 4))
            driver.execute_script("window.scrollTo(0," + str(int(last_height/random.randint(0, 4))) + ")")
            sleep(random.randint(7, 10))
            try:
                url = driver.current_url
                # Like bài viết đầu tiên trên newfeed
                driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[1]/div[3]/div[2]/div[2]/div[2]/span[1]/a[2]").click()
                # load lại trang newfeed trước khi like
                driver.get(url)
                # Ckick nút chuyển tiếp luot_newFeed
                driver.find_element_by_xpath("//*[@id=\"root\"]/div[1]/a").click()
            except:
                break
        # Đi đến bảng thông báo 
        driver.get("https://mbasic.facebook.com/notifications")
        # Click xem tất cả thông báo
        driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[1]/div/div/h2/a[1]").click()
        print("------------------------------------------------------------luot_newFeed: hoàn thành")    
    except:
        print("----------LỖI: luot_newFeed----------")        
    
# Kết Bạn theo gợi ý của facebook
# n: số lần kết bạn theo gợi ý
# timeSleep: thời gian dừng sau mỗi lần kết bạn
def ket_ban_theo_goi_y(n, timeSleep): 
    try:
        print("----------ket_ban_theo_goi_y----------")
        # Load vào trang kết bạn theo gợi ý
        driver.get("https://mbasic.facebook.com/friends/center/suggestions")
        # Thực hiện n lần kết bạn theo gợi ý
        for i in range(n):
            # Dùng thanh cuốn kiểm tra xem còn bao nhiêu lượt kết bạn theo gợi ý trên trang (Tối đa 10/10)
            height = (driver.execute_script("return document.body.scrollHeight")-197.4)/116.2
            if  height < 1:
                print("Không có theo kết bạn gợi ý")
                break
            # Click kết bạn người đầu tiên
            driver.find_element_by_xpath("//*[@id=\"friends_center_main\"]/div[1]/div[1]/table/tbody/tr/td[2]/div[2]/table/tbody/tr/td/div[1]").click()
            # Load lại trang kết bạn theo gợi ý để phục hồi lượt kết bạn đầu tiên trên trang
            driver.get("https://mbasic.facebook.com/friends/center/suggestions")
            # Sleep
            sleep(random.randint(timeSleep/2, timeSleep + timeSleep/2))
            print("Đã kết bạn theo gợi ý: "+str(i+1))
        print("------------------------------------------------------------ket_ban_theo_goi_y: hoàn thành")    
    except:
        print("Lỗi kết bạn theo gợi ý")

# Huỷ các yêu cầu kết bạn mà không được chấp nhận
# n: số lần huỷ
def huy_loi_ket_ban(n):  
    try:
        print("----------huy_loi_ket_ban----------")
        # load vào trang ĐÃ GỬI LỜI MỜI kết bạn
        driver.get("https://mbasic.facebook.com/friends/center/requests/outgoing")
        # thực hiện n lần huỷ kết bạn
        for i in range(n):
            # kiểm tra xem còn 1 yêu cầu đã gửi lời mời kết bạn nào k
            height = (driver.execute_script("return document.body.scrollHeight")-219.8)/62.6
            if  height < 1:
                print("Không có yêu cầu đã gửi lời mời kết bạn")
                break
            # load lại vào trang ĐÃ GỬI LỜI MỜI kết bạn
            driver.get("https://mbasic.facebook.com/friends/center/requests/outgoing")
            # Click vào nút huỷ lời mời
            driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[1]/div[1]/div[1]/table/tbody/tr/td[2]/div[2]/a").click()
    except:
        print("LỖI: huy_loi_ket_ban")

# Chấp nhận lời mời Kết Bạn
# n: số lần chấp nhận lời mời kết bạn
# timeSleep: thời gian dừng sau mỗi lời chấp nhận kết bạn
def chap_nhan_ket_ban(n,timeSleep):
    try:
        # Load trang chấp nhận lời mời Kết Bạn
        print("----------Chap_nhan_ket_ban----------")
        driver.get("https://mbasic.facebook.com/friends/center/requests")
        # Thực hiện n lần chấp nhận kết bạn
        for i in range(n):
            # Dùng thanh cuốn kiểm tra xem còn bao nhiêu lượt chấp nhận kết bạn trên trang (Tối đa 5/5)
            height = (driver.execute_script("return document.body.scrollHeight")-219.8)/62.6
            if  height < 1:
                print("Không có lời mời nào")
                break
            else:
                # Load lại trang chấp nhận kết bạn để phục hồi lượt chấp nhận đầu tiên trên trang
                driver.get("https://mbasic.facebook.com/friends/center/requests")
                # Click chấp nhận kết bạn người đầu tiên
                driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[1]/div[1]/div[1]/table/tbody/tr/td[2]/div[2]/a[1]").click()
                sleep(timeSleep)
                print("Đã chấp nhận kết bạn: "+str(i+1))
        print("------------------------------------------------------------chap_nhan_ket_ban: hoàn thành") 
    except:
        print("Lỗi kết bạn theo lời mời")   

# Kiểm tra trang thái nhóm
#  + "Tham gia nhóm": chưa tham gia --> gửi yêu cầu tham gia
#  + "Đã yêu cầu tham gia nhóm": đợi duyệt --> lâu quá thì chuyển nhóm khác
#  + "Nhóm đã được tham gia - sẵn sàng share": đã được tham gia --> sẵn sàng share
# groupId: id của nhóm
def add_check_group(groupId):
    try:
        print("----------add_check_group: " +str(int(groupId))+ " ----------")
        # Load vào trang group
        driver.get("https://mbasic.facebook.com/" +str(int(groupId))+ "?view=info")
        # textstatus: lấy text kiểm tra trạng thái nhóm
        try:
            textstatus = driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[1]/div[3]/ul/li[8]/table/tbody/tr/td[1]/a")
        except:
            textstatus = driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[1]/div[4]/ul/li[8]/table/tbody/tr/td[1]/a")
        status = textstatus.text
        print("Trạng thái group: "+status)
        if status == "Tham gia nhóm":
            textstatus.click()
        print("------------------------------------------------------------add_check_group: Hoàn thành")
    except:
        print("LỖI: add_check_group: "+str(int(groupId)))
    # Trả về trạng thái group
    return status

# share bài vào group
# groupId: id nhóm cần share
# postId: id bài cần share
# status: trạng thái của group đó đã đc tham gia chưa
def share_group(groupId, postId, status):
    try:
        print("----------share_group: " +str(int(groupId))+ "," + str(int(postId)) + " ----------")
        # kiểm tra group có đủ điều kiện share chưa
        if status == "Chỉnh sửa cài đặt thông báo":
            # load link share
            driver.get("https://mbasic.facebook.com/composer/mbasic/?c_src=share&referrer=feed&sid="+str(postId)+"&m=group&target="+str(groupId))
            # click vào nút đăng bài
            driver.find_element_by_xpath("/html/body/div/div/div[2]/div/table/tbody/tr/td/div/form/input[17]").click()
            # lấy thông tin trên link: idUser-idShare-idGroup
            BaiDaDang = re.findall("\d+", driver.current_url)
            BaiDaDang.append(str(int(groupId)))
            print("------------------------------------------------------------Share_group: Hoàn thành")  
    except:
        print("LỖI: Share_group " + str(int(groupId)))
    # Trả về trạng thái share group
    return BaiDaDang

# Xoá bài đã share
# BaiDaDang: idUser-idShare-idGroup bài đã share
def xoa_bai_share(BaiDaDang):
    try:
        print("----------xoa_bai_share: " +str(BaiDaDang[1])+ " ----------")
        # load vào bài cần xoá
        driver.get("https://mbasic.facebook.com/" + BaiDaDang[1])
        # click vào nút xoá bài
        driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[1]/div[1]/div/div[1]/div[1]/table/tbody/tr/td[2]/div/div/a[2]").click()
        # click vào nút xác nhận xoá bài
        driver.find_element_by_xpath("/html/body/div/div/div[2]/div[2]/div[1]/form/input[3]").click()
        print("------------------------------------------------------------xoa_bai_share: Hoàn thành")
    except:
        print("LỖI: xoa_bai_share " + str(BaiDaDang))

# Up cmt bài đã share
# BaiDaDang: idUser-idShare-idGroup bài đã share
def up_cmt(BaiDaDang):
    try:
        print("----------up_bai: " +str(BaiDaDang)+ " ----------")
        # Nuội dung cmt
        icon = [":)",":D",":P","O:)","3:)",";)",">:O",":*","^_^","8-)","8|",">:(",":v",":3","(y)",":|]"]
        # Đi đến bài viết cần up cmt
        driver.get("https://mbasic.facebook.com/" + BaiDaDang[1])
        # Điền nội dung cmt
        driver.find_element_by_xpath("//*[@id=\"composerInput\"]").send_keys(icon[ random.randint(0, len(icon))])
        # Click vào nút cmt
        driver.find_element_by_xpath("//*[@id=\"u_0_6\"]/tbody/tr/td[2]/div").click()
        print("------------------------------------------------------------up_cmt: Hoàn Thành")
    except:
        print("LỖI: up_cmt")
    
def like_cmt(postId):
    print("----------like_cmt: " +str(int(postId))+ " ----------")
    cmt = ["Giá sao bạn", "Ib tư vấn mình với ạ", "Mình ở địa chỉ nào ạ","có ship tận nhà không ạ", "Ib mình với", "Rep ib mình với"]
    driver.get("https://mbasic.facebook.com/"+str(int(postId)))
    try:
        driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[1]/div[2]/div/div[1]/table/tbody/tr/td[1]/a").click()
        #driver.get("https://mbasic.facebook.com/"+str(int(postId)))
        #driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[1]/div[2]/div/div[6]/form[1]/table/tbody/tr/td[1]/div/table/tbody/tr/td/textarea").send_keys(cmt[ random.randint(0, len(cmt))])
        #driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[1]/div[2]/div/div[6]/form[1]/table/tbody/tr/td[2]/div").click()
    except:
        print("Lỗi like up")
    print("------------------------------------------------------------")

#3121
#login("100045332020378", "quocsang199698") #459470627407885 #184085025268369
login("nguyen.robert.5680", "quocsang199698") #1103048153082966
#login("minhquoc.truong.927", "quocsang199698") #108757516583030
#login("ho.thanhtuyen.98", "quocsang199698") #256506321136779
#-------
#3122
#login("tran.anhtuyet.35977", "quocsang199698") #1983835191701296
#login("le.kimhue.9026", "quocsang199698") #479843565793652
#login("ho.huuphuoc.35", "quocsang199698") #123116161619507
#login("quan.duongminh.33046", "quocsang199698") #264846833886893
#-----
#3124
#login("truong.thaoly.568", "quocsang199698") #131942476971113
#login("tran.vanthanh.984", "quocsang199698") #1826787617399125
#login("thaovan.huynh.39948", "quocsang199698") #131942476971113
#login("ho.thanhdanh.31", "quocsang199698") #307963623358864
#-----
#3126
#login("thienhieu.nguyenthi", "quocsang199698") #1362279090456478
#login("thienhieu.nguyenthi", "quocsang199698") #1573166649377023

#driver.get("https://www.facebook.com/")
luot_newFeed(10)
#like_cmt(837285500065805)
a = add_check_group(1103048153082966)
b = share_group(1103048153082966, 2493773520877849, a)
#print(a)
sleep(100)
ket_ban_theo_goi_y(5,180)
up_cmt(b)
chap_nhan_ket_ban(5,30)






#https://mbasic.facebook.com/groups/459470627407885?view=permalink&id=3078080212213567&_rdr
#https://mbasic.facebook.com/groups/100045332020378?view=permalink&id=3078080212213567&_rdr
#a=driver.find_element_by_xpath("//*[@id=\"root\"]/div[1]/div[4]")
#print(a.get_attribute("data-ft")) 116.2 194.4

    



