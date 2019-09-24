# -*- coding:utf-8 -*-

from time import sleep
import lib.public_functions as pubfuc
import testcase.behavior as behavior
from pathlib import Path
import re
import logging

def joinandleaveroom(driver,roomid,devicename,packagename):
    suceess_flag = True
    num = 1
    elementinfo,deviceid = pubfuc.getiteminfo(driver.desired_capabilities,packagename)

    while suceess_flag:
        try:
            while num<1000:
                behavior.findroomid(driver, elementinfo, roomid)
                behavior.joinroom(driver,elementinfo)
                behavior.leaveroom(driver,elementinfo)
                num+1

        except Exception as e:
            print('error')
            #logger.error(f'第{num}次运行出错，设备是:{devicename}')
            sleep(3)
            driver.close_app()
            driver.launch_app()

def backapp(driver,roomid,devicename,packagename):
    suceess_flag = True
    num = 1
    elementinfo, deviceid = pubfuc.getiteminfo(driver.desired_capabilities, packagename)
    while suceess_flag:
        try:
            behavior.findroomid(driver, elementinfo, roomid)
            behavior.joinroom(driver, elementinfo)
            while num<1000:
                behavior.backapp(driver,elementinfo)
                num+1
            behavior.leaveroom(driver,elementinfo)

        except Exception as e:
            print('error')
            #logger.error(f'第{num}次运行出错，设备是:{devicename}')
            sleep(3)
            driver.close_app()
            driver.launch_app()

def lockscreen(driver,roomid,devicename,packagename):
    suceess_flag = True
    num = 1
    elementinfo, deviceid = pubfuc.getiteminfo(driver.desired_capabilities, packagename)
    while suceess_flag:
        try:
            behavior.findroomid(driver, elementinfo, roomid)
            behavior.joinroom(driver, elementinfo)
            while num < 1000:
                behavior.lockapp(driver)
                num + 1
            behavior.leaveroom(driver, elementinfo)

        except Exception as e:
            print('error')
            # logger.error(f'第{num}次运行出错，设备是:{devicename}')
            sleep(3)
            driver.close_app()
            driver.launch_app()