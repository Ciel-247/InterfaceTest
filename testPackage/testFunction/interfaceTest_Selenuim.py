# -*- coding:utf-8 -*-
import requests,redis,os,json
from time import sleep
from selenium import webdriver

def initWork():
    chromedriver = "C:\Users\lesq\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
    driver = webdriver.Chrome(chromedriver,chrome_options=options)
    return driver

def handleLogin():
    username = "330100194704074447"
    password = "aa12345678"
    url = "http://192.168.149.135:8082/login-web/login"
    driver.get(url)
    driver.maximize_window()
    DZSWJ_TGC = driver.get_cookie("DZSWJ_TGC")['value']
    JSESSIONID = driver.get_cookie("JSESSIONID")['value']
    print DZSWJ_TGC
    # redis的key值是前面获得的DZSWJ_TGC + '@sessionCache'
    redis_key = DZSWJ_TGC + '@sessionCache'
    sessionCache = re.get(redis_key)
    # 把str转为dict
    sessionCache_dict = (json.loads(sessionCache))
    # 单独取出验证码，因为本身得到的验证码是前后有双引号的，所以切割了[1:5]
    captcha = sessionCache_dict["attributes"]["KAPTCHA_SESSION_KEY"].decode("unicode_escape").encode("utf8")[1:5]
    username_input = driver.find_element_by_id("userName")
    password_input = driver.find_element_by_id("passWord")
    captcha_input = driver.find_element_by_id("captchCode")
    login_btn = driver.find_element_by_id("login")
    sleep(1)
    username_input.send_keys(username)
    password_input.send_keys(password)
    captcha_input.send_keys(captcha)
    login_btn.click()
    sleep(1)
    choose_user_btn = driver.find_element_by_id("companyEnter")
    choose_user_btn.click()
    return DZSWJ_TGC,JSESSIONID

if __name__ == '__main__':
    host = "http://192.168.149.135:8082"
    # 连接redis，来拿到服务器的验证码（后面可以做成可配置的）
    re = redis.Redis(host='192.168.149.93', port=6379, db=0, password='servyou')
    driver = initWork()
    DZSWJ_TGC, JSESSIONID = handleLogin()
    cookies = {"DZSWJ_TGC":DZSWJ_TGC,"JSESSION":JSESSIONID}
    # swjg_dm = "13301089100"
    # getSwjgMc_url = host + "/sbzx-web/api/baseCode/get/getBaseCodeValueByName/DM_GY_SWJG?dm=" + swjg_dm
    # getSwjgMc = requests.get(getSwjgMc_url,cookies = cookies)
    #
    # print getSwjgMc.text

    queryysb_url = host + "/sbzx-web/api/ysbqc/queryysb"
    queryysb = requests.post(queryysb_url,cookies = cookies)
    print  queryysb.text







