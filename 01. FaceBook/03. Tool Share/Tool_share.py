import random
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
 
def main():
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    fileDirWin = PureWindowsPath(fileDir)
    pathDirTool = fileDirWin.parents[1].as_posix()
    pathDirFacebook = fileDirWin.parents[0].as_posix()
    #Read data from excel
    dataFileName = str(pathDirFacebook) + "/01. Data/" + "nhom_share.xlsx"
    df = pd.read_excel(dataFileName)
    # Your Facebook account user and password
    # Doc User tu file excel
    usr = "copmapmap22@gmail.com"
    pwd = "Copmapmap_@222"
    cookieFileName = str(pathDirFacebook) + "/02. Cookies/" + usr + "cookies.pkl"
    message = "https://www.facebook.com/totokids.quanaotreem/posts/113499553458620"
    #chromedriver_path = "E:/05. Software/Chrome/chromedriver.exe"
    chromedriver_path = str(pathDirTool) + '/03. Software/Chrome/chromedriver.exe'
    chrome_options = webdriver.ChromeOptions()
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
    else:
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
        sleep(120)
        # Get Cookies sau khi dang nhap
        pickle.dump(driver.get_cookies() , open(cookieFileName,"wb"))
    group_links = [
        "phongtrodanang/",
        "chovieclamdanang/"
    ]
    sleep(20)
    while(1):
        for group in df['Group_copMapMap']:
        #for group in group_links:
            try:
                groupId = str(int(group))
                print(groupId)
                # Go to the Facebook Group
                driver.get("https://mbasic.facebook.com/groups/"+str(groupId))
                # Tìm khung đăng bài trong group
                post_box=driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[1]/div[3]/form/table/tbody/tr/td[2]/div/textarea")
                post_box.click()
                sleep(2)
                
                #send link share
                ActionChains(driver).send_keys(message).perform()
    
                # Tìm nút đăng bài trong group
                buttons = driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[1]/div[3]/form/table/tbody/tr/td[3]/div/input")
                sleep(2)
                buttons.click()

                print("Share OK")
                print("------------------------")
                #random sleep 10p->15p
                x=random.randint(200,300)
                print(x)
                sleep(x)
            except:
                print("Group loi " + str(groupId))
                print("------------------------")
            # driver.close()
 
if __name__ == '__main__':
  main()
