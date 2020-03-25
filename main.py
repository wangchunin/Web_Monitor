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
from time import strftime, localtime

# 打印当前时间
def printTime():
    print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
    return
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
    browser.get(url)
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

if(is_frame): # 关于frame调试可以参考banwagon
    browser.switch_to.frame(browser.find_element_by_css_selector('[' + str3 + ']'))
elem_init = browser.find_element_by_xpath(str1)
str2 = elem_init.text

print("Xpath:",str1)
print("element:", str2)


t = g.integerbox(msg="刷新时间",title="刷新时间",lowerbound=0,upperbound=100)
out_str = g.enterbox(msg="输入mail发送信息",title="字符")
count_http_error = 0
while True:
    try:
        browser.refresh()
    except TimeoutException as e:
        printTime()
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
                printTime()
                print("网页打开错误！")
                time.sleep(5)
                continue
        except Exception as e:
            try:
                if(is_frame):
                    browser.switch_to.frame(browser.find_element_by_css_selector('[' + str3 + ']'))
                elem = browser.find_element_by_xpath(str1)
            except NoSuchElementException as e:
                printTime()
                print("NoSuchElementException:", e)
                print("no elem!")
                #sendmail.send_mail("no elem!", "no elem!", "no elem!")
                sendmail.send_mail("Ok!" + out_str, "ok", elem.text)
                time.sleep(600)
            else:
                if(elem.text != str2):
                    printTime()
                    print(elem.text)
                    print("ok")
                    sendmail.send_mail("Ok!"+out_str, "ok", elem.text)
                    time.sleep(600)
                else:
                    printTime()
                    print("内容没变！")

            time.sleep(t)
