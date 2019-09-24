# -*- coding:utf-8 -*-

from time import sleep
import lib.public_functions as pubfuc
from pathlib import Path
import re
import subprocess
import logging

logger = logging.getLogger('autolog')


def getlog(driver):
    elementinfo, deviceid = pubfuc.getiteminfo(driver.desired_capabilities)
    if 'desired' in driver.desired_capabilities:
        filepath = pubfuc.get_real_dir_path(__file__, '../testresult') + f'/{deviceid}_powerinfo/'
        print(filepath)
        # filepath = f'/Users/liminglei/Desktop/log/{deviceid}/'
        if Path(filepath).exists():
            subprocess.Popen(f'rm {filepath}', shell=True)
        subprocess.Popen(f'mkdir {filepath}', shell=True)
        subprocess.Popen(f'adb -s {deviceid} pull /sdcard/powerinfo {filepath}', shell=True)


def switch_wifi(driver, t=5):
    size = driver.get_window_size()
    driver.swipe(size['width'] - 50, 5, size['width'] - 50, size['height'] / 2)
    sleep(1)
    driver.tap([[108, 248]])
    sleep(t)
    driver.tap([[105, 245]])
    sleep(1)
    driver.swipe(size['width'] - 50, size['height'] / 2, size['width'] - 50, 5)
    sleep(10)


def backiosapp(driver, size, appid, waittime=5):
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


def joinroom(driver, elementinfo, roomid):
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
    # logger.info(roomxpath)
    driver.find_element_by_xpath(roomxpath).click()
    sleep(5)
    if not driver.find_element_by_id(elementinfo['JOIN']['id']).get_attribute('enabled'):
        driver.back()
        sleep(1)
        joinroom(driver, elementinfo, roomid)
    driver.find_element_by_id(elementinfo['JOIN']['id']).click()
    sleep(10)
    issuccess = elementinfo['离开房间']['id'] in driver.page_source
    logger.info(f'加入房间成功:{issuccess}')


def autopuloadlog(driver, devicedriverinfo, devicename, elementinfo):
    print(devicedriverinfo)
    if 'desired' not in devicedriverinfo:
        driver.find_element_by_id(elementinfo['设置']['id']).click()
        sleep(1)
        driver.find_element_by_id(elementinfo['开发者选项']['id']).click()
        sleep(1)
        size = driver.get_window_size()
        driver.execute_script("mobile: dragFromToForDuration",
                              {'fromX': 15, 'fromY': size['height']/2 - 50, 'toX': 15,
                               'toY': 50, 'duration': 1})
        while True:
            uploadisvisiable = driver.find_element_by_xpath(elementinfo['上传日志']['xpath']).is_displayed()
            if not uploadisvisiable:
                print(size)
                driver.execute_script("mobile: dragFromToForDuration",
                                      {'fromX': size['width']-15, 'fromY': size['height']-100, 'toX': size['width']-15,
                                       'toY': size['height']/2+50, 'duration': 1})
            elif uploadisvisiable:
                break
        driver.find_element_by_xpath(elementinfo['上传日志']['xpath']).click()
        sleep(20)
        logger.info(f"upload log time is : {pubfuc.getlocaltime()}")
        driver.close_app()
        driver.launch_app()
    else:
        local_log_path = f"/Users/liminglei/Desktop/log/{pubfuc.getlocaltime()}-{devicename}"
        cmd = f"adb -s {devicedriverinfo['desired']['deviceName']} pull /sdcard/powerinfo {local_log_path}"
        subprocess.call(cmd, shell=True)
        sleep(20)


def joinandleaveroom(driver, roomid, devicename):
    fail_count = 1  # 用例中出错后重新执行的次数
    run_count = 1
    num = 1
    device_driver_info = driver.desired_capabilities  # 获取正在运行的设备的参数设置
    elementinfo, deviceid = pubfuc.getiteminfo(device_driver_info, 'bootstrap')
    size = driver.get_window_size()
    while True:
        try:
            if run_count > fail_count:
                break
            while num < 101:
                if num % 10 == 0:
                    logger.info(f"第{num}次{devicename}加入房间")
                joinroom(driver, elementinfo, roomid)
                driver.tap([[size['width']/2, size['height']/2]])
                sleep(10)
                driver.find_element_by_id(elementinfo['离开房间']['id']).click()
                sleep(6)
                num += 1
            break
        except Exception as e:
            logger.error(f'第{num}次运行出错，设备是:{devicename}')
            # print(driver.page_source)
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{pubfuc.getlocaltime()}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{run_count}次重跑')
            run_count += 1
            # driver.close_app()
            # driver.launch_app()
            autopuloadlog(driver, device_driver_info, devicename, elementinfo)


def backapp(driver, roomid, devicename):
    failcount = 5  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    device_driver_info = driver.desired_capabilities  # 获取正在运行的设备的参数设置
    elementinfo, deviceid = pubfuc.getiteminfo(device_driver_info, 'bootstrap')
    while True:
        try:
            if runcount > failcount:
                break
            isios = 'desired' not in device_driver_info
            joinroom(driver, elementinfo, roomid)
            sleep(10)
            bundleid, size = None, None
            if isios:
                bundleid = driver.capabilities['bundleId']
                size = driver.get_window_size()
            while num < 1001:
                if num % 10 == 0:
                    logger.info(f"第{num}次{devicename}切后台")
                if isios:
                    backiosapp(driver, size, bundleid)  # 切后台5s后切回前台
                else:
                    driver.background_app(5)
                sleep(5)
                # 切后台回来后，查看离开房间按钮是否可用，确定正确切回了前台
                driver.find_element_by_id(elementinfo['离开房间']['id']).get_attribute('enabled')
                # logger.info(f"离开房间按钮是否可用：{back_is_enable}")
                num += 1
            break
        except Exception as e:
            logger.info(f'第{num}次运行出错，设备是:{devicename}')
            # print(driver.page_source)
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{pubfuc.getlocaltime()}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            driver.close_app()
            driver.launch_app()
            autopuloadlog(driver, device_driver_info, devicename, elementinfo)


def lockscreen(driver, roomid, devicename):
    failcount = 5  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    device_driver_info = driver.desired_capabilities  # 获取正在运行的设备的参数设置
    elementinfo, deviceid = pubfuc.getiteminfo(device_driver_info, 'bootstrap')
    while True:
        try:
            if runcount > failcount:
                break
            joinroom(driver, elementinfo, roomid)
            sleep(10)
            while num < 1001:
                if num % 10 == 0:
                    logger.info(f"第{num}次{devicename}锁屏")
                driver.lock(5)
                sleep(3)
                # 锁屏回来后，查看离开房间按钮是否可用，确定正确切回了前台
                driver.find_element_by_id(elementinfo['离开房间']['id']).get_attribute('enabled')
                # logger.info(f"离开房间按钮是否可用：{back_is_enable}")
                num += 1
            break
        except Exception as e:
            logger.info(f'第{num}次运行出错，设备是:{devicename}')
            # print(driver.page_source)
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{pubfuc.getlocaltime()}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            driver.close_app()
            driver.launch_app()
            autopuloadlog(driver, device_driver_info, devicename, elementinfo)


def switchcamera(driver, roomid, devicename):
    failcount = 5  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    devicedriverinfo = driver.desired_capabilities  # 获取正在运行的设备的参数设置
    elementinfo, deviceid = pubfuc.getiteminfo(devicedriverinfo, 'bootstrap')
    while True:
        try:
            if runcount > failcount:
                break
            joinroom(driver, elementinfo, roomid)  # 加入房间
            sleep(10)
            if elementinfo['离开房间']['id'] not in driver.page_source:
                raise RuntimeError('加入房间失败')
            while num < 11:
                if num % 10 == 0:
                    logger.info(f"第{num}次{devicename}切换摄像头")
                switch_wifi(driver, 5)
                # driver.find_element_by_id(elementinfo['摄像头']['id']).click()
                sleep(6)
                num += 1
            driver.find_element_by_id(elementinfo['离开房间']['id']).click()
            break
        except Exception as e:
            logger.info(f'第{num}次运行出错，设备是:{devicename}')
            err_time = pubfuc.getlocaltime()
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{err_time}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            driver.close_app()
            driver.launch_app()
            autopuloadlog(driver, devicedriverinfo, devicename, elementinfo)


def startnewroom(driver, elementinfo):
    driver.find_element_by_id(elementinfo['创建房间']['id']).click()
    sleep(2)
    if not driver.find_element_by_xpath(elementinfo['START']['xpath']).get_attribute('enabled'):
        sleep(1)
        driver.back()
        startnewroom(driver, elementinfo)
    driver.find_element_by_xpath(elementinfo['START']['xpath']).click()
    sleep(5)
    while driver.find_element_by_id(elementinfo['离开房间']['id']) is None:
        sleep(2)


def startroom(driver, devicename):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    while True:
        try:
            if runcount > failcount:
                break
            devicedriverinfo = driver.desired_capabilities  # 获取正在运行的设备的参数设置
            elementinfo, deviceid = pubfuc.getiteminfo(devicedriverinfo, 'bootstrap')
            while num < 1001:
                logger.info(f'{num}次{devicename}创建房间')
                startnewroom(driver, elementinfo)
                sleep(5)
                driver.find_element_by_id(elementinfo['离开房间']['id']).click()
                sleep(2)
                if driver.find_element_by_id(elementinfo['创建房间']['id']) is None:
                    sleep(5)
                num += 1
            break
        except Exception as e:
            runcount += 1
            logger.info(f'第{num}次运行出错，设备是:{devicename}')
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{pubfuc.getlocaltime()}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            driver.close_app()
            driver.launch_app()


def startback(driver, devicename):
    failcount = 1  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    while True:
        try:
            if runcount > failcount:
                break
            devicedriverinfo = driver.desired_capabilities  # 获取正在运行的设备的参数设置
            elementinfo, deviceid = pubfuc.getiteminfo(devicedriverinfo, 'bootstrap')
            while num < 101:
                logger.info(f'{num}次{devicename}创建房间')
                print(num)
                driver.find_element_by_id(elementinfo['设置']['id']).click()
                sleep(2)
                driver.find_element_by_id('iLive QS Huajiao').click()
                sleep(3)
                driver.find_element_by_id(elementinfo['创建房间']['id']).click()
                sleep(2)
                driver.find_element_by_id(elementinfo['离开房间']['id']).click()
                sleep(3)
                num += 1
            break
        except Exception as e:
            runcount += 1
            logger.info(f'第{num}次运行出错，设备是:{devicename}')
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{pubfuc.getlocaltime()}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
