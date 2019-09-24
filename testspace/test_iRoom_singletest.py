# -*- coding:utf-8 -*-

import sys
sys.path.append('..')

import subprocess
from time import sleep
import unittest
import lib.public_functions as pubfuc
from appium import webdriver


# desired_caps = pubfuc.get_android_app_info()
# desired_caps = pubfuc.get_ios_app_info()

控件信息 = pubfuc.getymlfileinfo()
设备信息 = pubfuc.getymlfileinfo('devices')

print(设备信息['ip5s_test8'])
desired_caps = 设备信息['ip5s_test5']


# pubfuc.启动appium_server(desired_caps['deviceName'])

driver = webdriver.Remote("http://localhost:4723/wd/hub",desired_caps)

# driver.find_element_by_xpath("//android.widget.TextView[@text='多人群聊']").click()
# sleep(1)

# driver.find_element_by_xpath("//android.widget.TextView[@text='RoomID :3050']").click()
# sleep(1)

# print(driver.page_source)

driver.find_element_by_xpath("//XCUIElementTypeStaticText[@name='多人群聊']").click()

num = 1

while num < 51:
    sleep(5)
    # driver.find_element_by_xpath("//android.widget.TextView[@text='RoomID :3484']").click()
    driver.find_element_by_xpath("//XCUIElementTypeStaticText[@name='RoomId : 3050']").click()
    sleep(2)
    # driver.find_element_by_xpath("//android.widget.Button[@text='JOIN']").click()
    if driver.find_element_by_xpath("//XCUIElementTypeButton[@name='JOIN']").is_enabled() == False:
        driver.back()
        continue
    driver.find_element_by_xpath("//XCUIElementTypeButton[@name='JOIN']").click()
    sleep(10)

    # findStopButton = ('Stop' in driver.page_source)
    print('第{}次加入房间成功'.format(num))

    # print(driver.page_source)

    # driver.find_element_by_id("com.powerinfo.pi_iroom.demo:id/iv_back").click()
    # driver.find_element_by_xpath("//android.widget.Button[@name='stop']").click()
    driver.find_element_by_xpath("//XCUIElementTypeButton[@name='Stop']").click()

    num +=1

driver.quit()