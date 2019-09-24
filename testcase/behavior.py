from time import sleep
import lib.public_functions as pubfuc
from pathlib import Path
import re
import subprocess
import logging
import os


def findroomid(driver,elementinfo,roomid):
    #print(driver.desired_capabilities)
    print('findroomid')
    isios = 'desired' not in driver.desired_capabilities
    roomid = f' {roomid}' if isios else roomid
    roomxpath = re.sub("xxxx", roomid, elementinfo['房间列表']['xpath'])
    if not isios:
        roomisfind = re.findall('Room.+\d+', roomxpath)[0] in driver.page_source
        if not roomisfind:
            size = driver.get_window_size()
            x = size['width'] / 2
            y = size['height'] * 0.7
            end_y = size['height'] * 0.3
            while not roomisfind:
                # print(re.findall('ext="Room.+\d+"', driver.page_source))
                driver.swipe(x, y, x, end_y)
                roomisfind = re.findall('Room.+\d+', roomxpath)[0] in driver.page_source
                # print(re.findall('Room.+\d+', driver.page_source))
            sleep(1)
    #print(roomxpath)
    driver.find_element_by_xpath(roomxpath).click()
    sleep(5)





def choosetype(driver,elementinfo,roomtype='多人群聊'):
    print('choostype')
    el = elementinfo['多人群聊']['xpath']
    if roomtype != '多人群聊':
        el = re.sub('多人群聊', roomtype, el)
    driver.find_element_by_xpath(el).click()
    sleep(5)

def joinroom(driver,elementinfo):
    driver.find_element_by_id(elementinfo['JOIN']['id']).click()
    sleep(5)

def leaveroom(driver,elementinfo):
    driver.find_element_by_id(elementinfo['离开房间']['id']).click()
    sleep(5)

def set(driver,elementinfo):
    driver.find_element_by_id(elementinfo['设置']['id'])
    sleep(5)


def backapp(driver,elmentinfo):

    if 'desired' not in driver.desired_capabilities:
        appid = driver.capabilities['bundleId']
        x = size['width'] - 30
        y = size['height'] - 30
        driver.tap([[x, y]])  # iphone辅助功能按键放置在右下角
        sleep(3)
        x = size['width'] / 2
        y = size['height'] - 138
        driver.tap([[x, y]])
        # print(pubfuc.getlocaltime())
        sleep(waittime)
        # print(pubfuc.getlocaltime())
        driver.activate_app(appid)
    else:
        driver.background_app(5)
        sleep(5)

def lockapp(driver):
    driver.lock(5)
    sleep(5)


def changerole(driver,element):
    driver.find_element_by_id(element['切换角色']['id']).click()
    sleep(5)

def switchcamera(driver,element):
    driver.find_element_by_id(element['摄像头']['id']).click()
    sleep(6)

def creatroom(driver,element):
    driver.find_element_by_id(element['创建房间']['id']).click()
    sleep(5)
    driver.find_element_by_id(element['JOIN']['id']).click()
    sleep(5)
'''
def PK(driver,element):
    driver.find_elment_by_id()
'''