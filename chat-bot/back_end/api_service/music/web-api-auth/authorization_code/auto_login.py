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

def music():
    subprocess.call("node /Users/erikzhou/Desktop/9900_project/chat-bot/back_end/api_service/music/web-api-auth/authorization_code/app.js",shell = True)
    time.sleep(1) 

    #now can start the login thread



def login():
    options = Options()
    #options.add_argument('--headless')

    driver = webdriver.Chrome('./chromedriver',chrome_options = options)
    driver.get('http://localhost:8888/login')

    # #get will wait until page loaded
    # #get the loging user name and password form field
    username = driver.find_element_by_id("login-username")
    password = driver.find_element_by_id("login-password")
    login_btn = driver.find_element_by_id("login-button")

    #send the username and password
    username.send_keys("erikxiangzhou@gmail.com")
    password.send_keys("Zhou512388!")
    login_btn.click()


    #minimise the window
    driver.minimize_window()

    #wait the refresh token appears and click then very 20 mins
    wait = WebDriverWait(driver, 10)
    refresh = wait.until(EC.element_to_be_clickable((By.ID, "obtain-new-token")))

    time.sleep(3) 
    refresh.click()


music_t = threading.Thread(target=music)
login_t = threading.Thread(target=login)
music_t.start()
login_t.start()







