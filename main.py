# !/usr/bin/python3
# -*- coding: utf-8 -*-


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
import json

import re
import sendmail
import easygui as g
import ast
#************忽略warning*************
import warnings
warnings.filterwarnings("ignore")
#************忽略warning*************


def cookie_resize(cookies):
    cookies = cookies.replace(': false', ': False')
    cookies = cookies.replace(':false', ':False')
    cookies = cookies.replace(': true', ': True')
    cookies = cookies.replace(':true', ':True')
    cookies = ast.literal_eval(cookies)
    return cookies

chromeOptions = webdriver.ChromeOptions()
is_daili = g.buttonbox(msg="是否需要代理?",title="",choices=("是","否", "默认"))
if is_daili == "是":
    daili = g.enterbox(msg="输入代理ip和端口", title="代理ip和端口")
    chromeOptions.add_argument("--proxy-server={}".format(daili))
elif is_daili == "默认":
    chromeOptions.add_argument("--proxy-server=socks5://127.0.0.1:1080")
if not g.ccbox("是否加载图片",choices=("是","否")):
    prefs = {"profile.managed_default_content_settings.images": 2}
    chromeOptions.add_experimental_option("prefs", prefs)

browser = webdriver.Chrome(chrome_options = chromeOptions)
browser.implicitly_wait(10)

if g.ccbox("是否加载cookie",choices=("是","否")):
    url = g.enterbox(msg="输入网址", title="url")
    cookies = g.enterbox(msg="输入cookie", title="cookie")

    '''
    print(cookies)
    input()
    cookies = cookie_resize(cookies)
    print(cookies)
    input()
    browser.get(url)
    browser.delete_all_cookies()
    for cookie in cookies:
        browser.add_cookie(cookie_dict=cookie)
    '''
    cookies = json.loads(cookies)
    print(cookies)
    browser.get(url)
    browser.delete_all_cookies()
    for cook in cookies:
        # 遍历删除sameSite,注意，旧版chrome可能是没有samesite
        try:
            print("POP sameSite")
            print(cook.pop('sameSite'))
        except:
            pass
        browser.add_cookie(cook)
    browser.refresh()
else:
    g.ccbox("请在弹出chrome中开打页面并登录", choices=("开始"))

is_frame = g.ccbox("是否需要frame",choices=("是","否"))
if is_frame:
    str3 = g.enterbox(msg="输入定位frame元素，如：id='mainFrame'",title="frame")


# xf = self.driver.find_element_by_xpath('//iframe[@allowtransparency="true"]')
#
# self.driver.switch_to.frame(xf)
#
# # 跳出当前iframe
#
# self.driver.switch_to.parent_frame()
#
# # 返回最外层iframe
#
# self.driver.switch_to.default_content()

# < iframe
# src = "myframetest.html" / >
#
# 用xpath定位，传入WebElement对象：
#
#
#
# driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@src,'myframe')]"))

str1 = g.enterbox(msg="输入Xpath",title="Xpath")
str2 = g.enterbox(msg="原来值,直接copy element即可",title="原来值")
try:
    str2 = str2.split(r'<')[-2].split(r'>')[1]
except:
    print("cut element error!")
print(str1)
str2 = str2.strip()
print(str2)

# str2 = str.strip()
# str3 = re.sub(' ','',str)
t = g.integerbox(msg="刷新时间",title="刷新时间",lowerbound=0,upperbound=100)
count_http_error = 0
while True:
    try:
        browser.refresh()
    except TimeoutException as e:
        print('time out in search page', e)
    else:
        try:
            if(is_frame):
                browser.switch_to.default_content()
            if("无法访问此网站" == browser.find_element_by_css_selector('[jsvalues=".innerHTML:msg"]').text):
                count_http_error += 1
                if(count_http_error > 100):
                    sendmail.send_mail("count_http_error", "count_http_error", "count_http_error")
                    count_http_error = 0
                print("网页打开错误！")
                time.sleep(5)
                continue
        except Exception as e:
            try:
                if(is_frame):
                    browser.switch_to.frame(browser.find_element_by_css_selector('[' + str3 + ']'))
                elem = browser.find_element_by_xpath(str1)
            except NoSuchElementException as e:
                print("NoSuchElementException:", e)
                print("no elem!")
                sendmail.send_mail("no elem!", "no elem!", "no elem!")
                time.sleep(600)
            else:
                if(elem.text != str2):
                    print(elem.text)
                    print("ok")
                    sendmail.send_mail("Ok!", "ok", elem.text)
                    time.sleep(600)
            time.sleep(t)
