import os
from pathlib import Path, PureWindowsPath
from time import sleep
from selenium import webdriver

fileDir = os.path.dirname(os.path.realpath('__file__'))
fileDirWin = PureWindowsPath(fileDir)
pathDirTool = fileDirWin.parents[1].as_posix()
pathDirFacebook = fileDirWin.parents[0].as_posix()

preferences = {
    "webrtc.ip_handling_policy" : "disable_non_proxied_udp",
    "webrtc.multiple_routes_enabled": False,
    "webrtc.nonproxied_udp_enabled" : False
}

chromedriver_path = str(pathDirTool) + '/03. Software/Chrome/chromedriver.exe'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-rtc-smoothness-algorithm")
chrome_options.add_argument("--disable-javascript")
chrome_options.add_argument("--disable-async-dns")
chrome_options.add_argument("--disable-background-networking")
chrome_options.add_argument("--disable-webrtc-encryption[13]")
chrome_options.add_argument("--disable-webrtc-hw-decoding[13]")
chrome_options.add_argument("--disable-webrtc-hw-encoding[13]")
chrome_options.add_argument("--disable-webrtc-multiple-routes[13]")
#chrome_options.add_experimental_option("prefs", preferences)
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko)")
# 1:allow, 2:block 
prefs = {"profile.default_content_setting_values.notifications": 2,
        "webrtc.ip_handling_policy" : "disable_non_proxied_udp",
        "webrtc.multiple_routes_enabled": False,
        "webrtc.nonproxied_udp_enabled" : False}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path = chromedriver_path, options=chrome_options)

#Store it in a variable and print the value
agent = driver.execute_script("return navigator.userAgent")
print(agent)
#directly print the value
#print driver.execute_script("return navigator.userAgent")
#Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko)
