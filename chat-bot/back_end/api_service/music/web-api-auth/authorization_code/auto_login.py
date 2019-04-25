from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import subprocess
import threading
import psutil

p=""
flag = 1

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

def music():
    global p
    #this will be called from the backend 
    cmd = "node ./app.js" 
    #cmd = "node ./api_service/music/web-api-auth/authorization_code/app.js"
    p = subprocess.Popen(cmd, shell=True)
    #subprocess.call("node ./api_service/music/web-api-auth/authorization_code/app.js",shell = True)
    time.sleep(1) 

    #now can start the login thread

def login():
    options = Options()
    #options.add_argument('--headless')


    #driver = webdriver.Chrome("./api_service/music/web-api-auth/authorization_code/chromedriver",chrome_options = options)
    driver = webdriver.Chrome('./chromedriver',chrome_options = options)
    driver.get('http://localhost:8888/login')

    # #get will wait until page loaded
    # #get the loging user name and password form field
    username = driver.find_element_by_id("login-username")
    password = driver.find_element_by_id("login-password")
    login_btn = driver.find_element_by_id("login-button")

    #send the username and password
    username.send_keys("erikxiangzhou@gmail.com")
    password.send_keys("12345!")
    login_btn.click()


    #minimise the window
    driver.minimize_window()

    #wait the refresh token appears and click then very 20 mins
    wait = WebDriverWait(driver, 10)
    try:
        refresh = wait.until(EC.element_to_be_clickable((By.ID, "obtain-new-token")))
    except:
        return 

    global flag
    counter = 0
    while flag: #auto refresh every 20 mins
         time.sleep(1) 
         counter += 1
         if counter > 1000:
            refresh.click()
            counter = 0
         if not flag: #close the webpage
            driver.close()


music_t = threading.Thread(target=music)
login_t = threading.Thread(target=login)

music_t.start()
login_t.start()

time.sleep(8)
print("Now to kill the process....")
kill(p.pid)
print("now killed")
music_t.join()
print("music joined ")
flag = 0
login_t.join()
print("login joined")







