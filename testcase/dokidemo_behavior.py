# -*- coding:utf-8 -*-

from time import sleep
import lib.public_functions as pubfuc
from pathlib import Path
import re
# import subprocess
import logging

logger = logging.getLogger('autolog')


def create_doki_room(driver, elementinfo):
    print(driver)
    driver.find_element_by_xpath(elementinfo['']).click()  # 点击+号
    sleep(2)
    driver.find_element_by_id().click()  # 点击start
    sleep(3)
    pageinfo = driver.page_source  # 获取页面资源信息
    roomid_A = pageinfo  # 处理页面资源信息，得到房间号
    return roomid_A


def choose_room_pk(driver, roomid):
    driver.find_element_by_xpath().click()  # 点击pk按钮
    sleep(2)
    roompath = roomid  # 将roomid处理为控件定位
    driver.find_element_by_xpath(roompath).click()  # 选择房间进行pk
    sleep(30)
    driver.find_element_by_xpath().click()  # 结束PK


def join_doki_room(driver, elementinfo, roomid, isprint=True):
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
    if isprint:
        logger.info(roomxpath)
    driver.find_element_by_xpath(roomxpath).click()
    sleep(7)
    driver.find_element_by_id(elementinfo['JOIN']['id']).click()
    sleep(5)
    issuccess = elementinfo['离开房间']['id'] in driver.page_source
    if isprint:
        logger.info(f'加入房间成功:{issuccess}')