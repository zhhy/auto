# -*- coding:utf-8 -*-

from time import sleep
import lib.public_functions as pubfuc
from pathlib import Path
import re
import subprocess
import logging
import os

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


def backiosapp(driver, size, appid, time=5):
    x = size['width'] - 30
    y = size['height'] - 30
    driver.tap([[x, y]])  # iphone辅助功能按键放置在右下角
    sleep(2)
    x = size['width'] / 2
    y = size['height'] - 138
    driver.tap([[x, y]])
    sleep(time)
    driver.activate_app(appid)


def switch_wifi(driver, t=5):
    size = driver.get_window_size()
    driver.swipe(size['width'] - 50, 5, size['width'] - 50, size['height'] / 2)
    sleep(0.5)
    driver.tap([[108, 248]])
    # driver.swipe(size['width'] - 50, size['height'] / 2, size['width'] - 50, 5)
    sleep(t)
    # driver.swipe(size['width'] - 50, 5, size['width'] - 50, size['height'] / 2)
    # sleep(0.5)
    driver.tap([[105, 245]])
    sleep(0.5)
    driver.swipe(size['width'] - 50, size['height'] / 2, size['width'] - 50, 5)
    sleep(20)


def chooseroomtype(driver, elementinfo, roomtype='多人群聊'):
    el = elementinfo['多人群聊']['xpath']
    if roomtype != '多人群聊':
        el = re.sub('多人群聊', roomtype, el)
    driver.find_element_by_xpath(el).click()
    sleep(5)
    if 'desired' not in driver.desired_capabilities:
        return
    success_flag = 'RoomI' not in driver.page_source
    while success_flag:
        sleep(3)
        success_flag = 'RoomI' not in driver.page_source


def joinroom(driver, elementinfo, roomid, isprint=True):
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
    sleep(10)
    if not driver.find_element_by_id(elementinfo['JOIN']['id']).get_attribute('enabled'):
        driver.back()
        sleep(1)
        joinroom(driver, elementinfo, roomid)
    driver.find_element_by_id(elementinfo['JOIN']['id']).click()
    sleep(5)
    issuccess = elementinfo['离开房间']['id'] in driver.page_source
    if isprint:
        logger.info(f'加入房间成功:{issuccess}')


def autopuloadlog(driver, devicedriverinfo, devicename, elementinfo):
    print(devicedriverinfo)
    if 'desired' not in devicedriverinfo:
        chooseroomtype(driver, elementinfo)
        driver.find_element_by_id(elementinfo['创建房间']['id']).click()
        sleep(2)
        driver.find_element_by_id(elementinfo['设置']['id']).click()
        sleep(1)
        driver.find_element_by_id(elementinfo['开发者选项']['id']).click()
        sleep(1)
        size = driver.get_window_size()
        driver.execute_script("mobile: dragFromToForDuration",
                              {'fromX': 15, 'fromY': size['height'] / 2 - 50, 'toX': 15,
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
    else:
        local_log_path = f"/Users/liminglei/Desktop/log/{pubfuc.getlocaltime()}-{devicename}"
        subprocess.call(f"adb -s {devicedriverinfo['desired']['deviceName']} pull /sdcard/powerinfo {local_log_path}",
                        shell=True)
        sleep(20)
    driver.close_app()
    driver.launch_app()
    chooseroomtype(driver, elementinfo)


def joinandleaveroom(driver, roomid, devicename):
    fail_count = 5  # 用例中出错后重新执行的次数
    run_count = 1
    success_flag = True
    num = 1
    device_driver_info = driver.desired_capabilities  # 获取正在运行的设备的参数设置
    elementinfo, deviceid = pubfuc.getiteminfo(device_driver_info)
    while success_flag:
        try:
            if run_count > fail_count:
                break
            while num < 501:
                if 'RoomI' not in driver.page_source:
                    chooseroomtype(driver, elementinfo)
                if num % 10 == 0:
                    logger.info(f"第{num}次{devicename}加入房间")
                joinroom(driver, elementinfo, roomid, False)
                sleep(5)
                driver.find_element_by_id(elementinfo['离开房间']['id']).click()
                sleep(6)
                num += 1

        except Exception as e:
            logger.error(f'第{num}次运行出错，设备是:{devicename}')
            # print(driver.page_source)
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{pubfuc.getlocaltime()}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            if not success_flag:
                return
            logger.info(f'第{run_count}次重跑')
            run_count += 1
            driver.close_app()
            driver.launch_app()
            autopuloadlog(driver, device_driver_info, devicename, elementinfo)

def audiojoinroom(driver,devicename,roomid):
    fail_count = 5  # 用例中出错后重新执行的次数
    run_count = 1
    success_flag = True
    num = 1
    device_driver_info = driver.desired_capabilities  # 获取正在运行的设备的参数设置
    elementinfo, deviceid = pubfuc.getiteminfo(device_driver_info)
    print(roomid)
    while success_flag:
        try:
            if run_count > fail_count:
                break
            while num < 501:
                if 'RoomI' not in driver.page_source:
                    driver.find_element_by_xpath("//android.widget.TextView[@text='游戏连麦']").click()
                    sleep(10)
                    #print(driver.page_source)
                    driver.find_element_by_xpath("//android.widget.TextView[@text='纯音频群聊']").click()
                    sleep(5)
                if num % 10 == 0:
                    logger.info(f"第{num}次{devicename}加入房间")
                joinroom(driver, elementinfo, roomid, False)
                sleep(5)
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
            if not success_flag:
                return
            logger.info(f'第{run_count}次重跑')
            run_count += 1
            driver.close_app()
            driver.launch_app()
            autopuloadlog(driver, device_driver_info, devicename, elementinfo)

def changerole(driver, roomid, devicename):
    failcount = 5 # 用例中出错后重新执行的次数
    runcount = 1
    success_flag = True
    num = 1
    devicedriverinfo = driver.desired_capabilities  # 获取正在运行的设备的参数设置
    elementinfo, deviceid = pubfuc.getiteminfo(devicedriverinfo)
    while True:
        try:
            if runcount > failcount:
                break
            if 'RoomI' not in driver.page_source:
                chooseroomtype(driver, elementinfo)  # 选择多人群聊
            joinroom(driver, elementinfo, roomid)  # 加入房间
            sleep(10)
            if elementinfo['离开房间']['id'] not in driver.page_source:
                raise RuntimeError('加入房间失败')
            while num < 1001:
                if num % 10 == 0:
                    logger.info(f"第{num}次{devicename}切换角色")
                driver.find_element_by_id(elementinfo['切换角色']['id']).click()
                sleep(6)
                num += 1
            driver.find_element_by_id(elementinfo['离开房间']['id']).click()
            break
        except Exception as e:
            logger.info(f'第{num}次运行出错，设备是:{devicename}')
            err_time = pubfuc.getlocaltime()
            # xml_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{err_time}-{devicename}.xml')
            # with open(xml_file, 'a') as f:
            #     f.write(driver.page_source)
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{err_time}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            if not success_flag:
                return
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            driver.close_app()
            driver.launch_app()
            autopuloadlog(driver, devicedriverinfo, devicename, elementinfo)


def backapp(driver, roomid, devicename):
    failcount = 5  # 用例中出错后重新执行的次数
    runcount = 1
    success_flag = True
    num = 1
    device_driver_info = driver.desired_capabilities  # 获取正在运行的设备的参数设置
    elementinfo, deviceid = pubfuc.getiteminfo(device_driver_info)
    while success_flag:
        try:
            if runcount > failcount:
                break
            isios = 'desired' not in device_driver_info
            if 'RoomI' not in driver.page_source:
                chooseroomtype(driver, elementinfo)  # 选择多人群聊
            # startnewroom(driver, elementinfo)  # 加入房间
            joinroom(driver, elementinfo, roomid)
            sleep(10)
            bundleid = size = None
            if isios:
                bundleid = driver.capabilities['bundleId']
                size = driver.get_window_size()
            while num < 1001:
                if num % 10 == 0:
                    logger.info(f"第{num}次{devicename}切后台")
                if isios:
                    backiosapp(driver, size, bundleid, time=5)
                else:
                    driver.background_app(5)
                sleep(5)
                # 切后台回来后，查看离开房间按钮是否可用，确定正确切回了前台
                driver.find_element_by_id(elementinfo['离开房间']['id']).get_attribute('enabled')
                # logger.info(f"离开房间按钮是否可用：{back_is_enable}")
                num += 1
            driver.find_element_by_id(elementinfo['离开房间']['id']).click()
            break
        except Exception as e:
            logger.info(f'第{num}次运行出错，设备是:{devicename}')
            # print(driver.page_source)
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{pubfuc.getlocaltime()}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            if not success_flag:
                return
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
    elementinfo, deviceid = pubfuc.getiteminfo(device_driver_info)
    while True:
        try:
            if runcount > failcount:
                break
            if 'RoomI' not in driver.page_source:
                chooseroomtype(driver, elementinfo)  # 选择多人群聊
            # startnewroom(driver, elementinfo)  # 加入房间
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
            driver.find_element_by_id(elementinfo['离开房间']['id']).click()
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
    success_flag = True
    num = 1
    devicedriverinfo = driver.desired_capabilities  # 获取正在运行的设备的参数设置
    elementinfo, deviceid = pubfuc.getiteminfo(devicedriverinfo)
    while True:
        try:
            if runcount > failcount:
                break
            if 'RoomI' not in driver.page_source:
                chooseroomtype(driver, elementinfo)  # 选择多人群聊
            joinroom(driver, elementinfo, roomid)  # 加入房间
            sleep(10)
            if elementinfo['离开房间']['id'] not in driver.page_source:
                raise RuntimeError('加入房间失败')
            while num < 1001:
                if num % 10 == 0:
                    logger.info(f"第{num}次{devicename}切换摄像头")
                driver.find_element_by_id(elementinfo['摄像头']['id']).click()
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
            if not success_flag:
                return
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            driver.close_app()
            driver.launch_app()
            autopuloadlog(driver, devicedriverinfo, devicename, elementinfo)


def switchwifi(driver, roomid, devicename):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    devicedriverinfo = driver.desired_capabilities  # 获取正在运行的设备的参数设置
    elementinfo, deviceid = pubfuc.getiteminfo(devicedriverinfo)
    while True:
        try:
            if runcount > failcount:
                break
            if 'RoomI' not in driver.page_source:
                chooseroomtype(driver, elementinfo)  # 选择多人群聊
            joinroom(driver, elementinfo, roomid)  # 加入房间
            sleep(10)
            if elementinfo['离开房间']['id'] not in driver.page_source:
                raise RuntimeError('加入房间失败')
            while num < 1001:
                if num % 10 == 0:
                    logger.info(f"第{num}次{devicename}断网10s左右恢复")
                switch_wifi(driver, 6)
                driver.find_element_by_id(elementinfo['离开房间']['id']).get_attribute('enabled')
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


def startnewroom(driver, elementinfo, istestversion=False):
    driver.find_element_by_id(elementinfo['创建房间']['id']).click()
    sleep(2)
    if not driver.find_element_by_xpath(elementinfo['START']['xpath']).get_attribute('enabled'):
        sleep(1)
        driver.back()
        startnewroom(driver, elementinfo)
    driver.find_element_by_xpath(elementinfo['START']['xpath']).click()
    sleep(2)
    if '录屏与麦克风' in driver.page_source:
        driver.find_element_by_id(elementinfo['录屏与麦克风']['id']).click()
        sleep(2)
    if istestversion:
        driver.find_element_by_xpath("//android.widget.Button[@text='OK']").click()
        sleep(3)
        driver.find_element_by_id("com.powerinfo.pi_iroom.demo:id/tv_roomId").click()
        sleep(4)
    sleep(3)
    while driver.find_element_by_id(elementinfo['离开房间']['id']) is None:
        sleep(2)


def getroominfo(driver, elementinfo):
    # roomid = re.findall('roomId: \d+', driver.page_source)[0]
    driver.find_element_by_id(elementinfo['RoomID']['id']).click()
    sleep(2)
    info = driver.find_element_by_id(elementinfo['推流信息']['id']).get_attribute('text')
    sleep(5)
    # print(info)
    roomid = re.findall('roomId.+', info)[0].split(' ')[1]
    # roomid = re.findall('\d+', roomid)[0]
    uid = re.findall('uid:.+', info)[0].split(' ')[1]
    driver.find_element_by_id(elementinfo['RoomID']['id']).click()
    return roomid, uid


def startroom(driver, devicename):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    success_flag = True
    num = 1
    while success_flag:
        try:
            if runcount > failcount:
                success_flag = False
            devicedriverinfo = driver.desired_capabilities  # 获取正在运行的设备的参数设置
            elementinfo, deviceid = pubfuc.getiteminfo(devicedriverinfo)
            chooseroomtype(driver, elementinfo)
            while num < 1001:
                logger.info(f'{num}次{devicename}创建房间')
                startnewroom(driver, elementinfo)
                sleep(5)
                driver.find_element_by_id(elementinfo['离开房间']['id']).click()
                sleep(2)
                while driver.find_element_by_id(elementinfo['创建房间']['id']) is None:
                    sleep(2)
                num += 1
        except Exception as e:
            runcount += 1
            logger.info(f'第{num}次运行出错，设备是:{devicename}')
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{pubfuc.getlocaltime()}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            if not success_flag:
                return
            driver.close_app()
            driver.launch_app()


def startpkroomios(driver, devicename):
    failcount = 1  # 用例中出错后重新执行的次数
    runcount = 1
    success_flag = True
    num = 1
    devicedriverinfo = driver.desired_capabilities  # 获取正在运行的设备的参数设置
    elementinfo, deviceid = pubfuc.getiteminfo(devicedriverinfo)
    appid = devicedriverinfo['bundleId']
    while success_flag:
        try:
            if runcount > failcount:
                break
            if 'RoomI' not in driver.page_source:
                print(driver.page_source)
                chooseroomtype(driver, elementinfo, '主播PK')  # 选择PK
                startnewroom(driver, elementinfo)  # 创建
            while num < 100:
                logger.info(f'设备{devicename}第{num}次选择房间PK')
                #startnewroom(driver, elementinfo)  # 创建
                #print(driver.page_source)

                driver.find_element_by_xpath("//XCUIElementTypeButton[@name='combineRoom']").click()
                sleep(3)

                driver.find_element_by_xpath("//XCUIElementTypeStaticText[@name='RoomId : 3165']").click()
                sleep(3)
                driver.find_element_by_xpath("//XCUIElementTypeButton[@name='combineRoom']").click()

                sleep(3)
                num += 1
            driver.find_element_by_id(elementinfo['离开房间']['id']).click()
            break
        except Exception as e:
            logger.info(f'第{num}次运行出错，设备是:{devicename}')
            logger.info(driver.page_source)
            img_file = Path(__file__).cwd().parent / 'testresult' / f'{pubfuc.getlocaltime()}-{devicename}.png'
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            driver.activate_app(appid)


def chooseroompk(driver, elementinfo, roomid):
    driver.find_element_by_id(elementinfo['合并房间']['id']).click()
    sleep(3)
    driver.find_element_by_xpath(f'//android.widget.TextView[@text="{roomid}"]').click()
    sleep(10)
    driver.find_element_by_id(elementinfo['合并房间']['id']).click()


def analysis_pk_success(roomid, uid, deviceid, devicename):
    local_log_path = f"/Users/liminglei/Desktop/log/{pubfuc.getlocaltime()}-{devicename}"
    subprocess.call(
        f"adb -s {deviceid} pull /sdcard/powerinfo {local_log_path}",
        shell=True)
    sleep(20)
    print(local_log_path)
    with open(f'{local_log_path}/pslstreaming_log.txt', 'r') as f:
        lines = f.readlines()
    res_video = []
    res_audeo = []
    for line in lines:
        if f'onReceivePeerVideoSuccess {roomid} {uid}' in line:
            res_video.append(line)
            logger.info(line)
        if f'onReceivePeerAudioSuccess {roomid} {uid}' in line:
            res_audeo.append(line)
            logger.info(line)
    logger.warning(f'此次统计共计{len(res_video)}次收流成功视频回调')
    logger.warning(f'此次统计共计{len(res_audeo)}次收流成功音频回调')
    subprocess.call(f"adb -s {deviceid} "
                    f"shell rm /sdcard/powerinfo/*.txt", shell=True)


def startpkroomandroid(driver, devicename, roomid):
    failcount = 1  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    devicedriverinfo = driver.desired_capabilities  # 获取正在运行的设备的参数设置
    elementinfo, deviceid = pubfuc.getiteminfo(devicedriverinfo)
    while True:
        try:
            if runcount > failcount:
                break
            if 'RoomI' not in driver.page_source:
                print(driver.page_source)
                chooseroomtype(driver, elementinfo, '主播 PK')  # 选择PK
                startnewroom(driver, elementinfo)  # 创建
            while num < 11:
                logger.info(f'设备{devicename}第{num}次选择房间PK')
                chooseroompk(driver, elementinfo, roomid)
            driver.find_element_by_id(elementinfo['离开房间']['id']).click()
            break
        except Exception as e:
            logger.info(f'第{num}次运行出错，设备是:{devicename}')
            logger.info(driver.page_source)
            img_file = Path(__file__).cwd().parent / 'testresult' / f'{pubfuc.getlocaltime()}-{devicename}.png'
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            # driver.activate_app(appid)


def startpkroomandroid_analysis(driver, driver_A, devicename, roomid, uid):
    failcount = 1  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    devicedriverinfo = driver.desired_capabilities  # 获取正在运行的设备的参数设置
    elementinfo, deviceid = pubfuc.getiteminfo(devicedriverinfo)
    subprocess.call(f"adb -s {deviceid} shell rm /sdcard/powerinfo/*", shell=True)  # 测试前清理日志
    while True:
        try:
            if runcount > failcount:
                break
            if 'RoomI' not in driver.page_source:
                chooseroomtype(driver, elementinfo, '主播 PK')  # 选择PK
                startnewroom(driver, elementinfo)  # 创建
            while num < 201:
                if num % 10 == 0:
                    logger.info(f'设备{devicename}第{num}次选择房间PK')
                chooseroompk(driver, elementinfo, roomid)
                driver_A.find_element_by_id(elementinfo['离开房间']['id'])  # 查找一下离开按钮，防止另一台手机超时退出房间
                if num % 20 == 0:  # 20次分析一次日志，否则日志太多，文件会更新
                    driver.find_element_by_id(elementinfo['离开房间']['id']).click()
                    analysis_pk_success(roomid, uid, deviceid, devicename)
                    startnewroom(driver, elementinfo)
                num += 1
            driver.find_element_by_id(elementinfo['离开房间']['id']).click()
            break
        except Exception as e:
            logger.info(f'第{num}次运行出错，设备是:{devicename}')
            # logger.info(driver.page_source)
            img_file = Path(__file__).cwd().parent / 'testresult' / f'{pubfuc.getlocaltime()}-{devicename}.png'
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{runcount}次重跑')
            analysis_pk_success(roomid, uid, deviceid, devicename)
            runcount += 1
            # driver.activate_app(appid)


def startgameroom(driver, devicename):
    failcount = 1  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    devicedriverinfo = driver.desired_capabilities  # 获取正在运行的设备的参数设置
    elementinfo, deviceid = pubfuc.getiteminfo(devicedriverinfo)
    subprocess.call(f"adb -s {deviceid} shell rm /sdcard/powerinfo/*", shell=True)  # 测试前清理日志
    while True:
        try:
            if runcount > failcount:
                break
            if 'RoomI' not in driver.page_source:
                el = elementinfo['多人群聊']['xpath']
                el = re.sub('多人群聊', '游戏连麦', el)
                driver.find_element_by_xpath(el).click()
                sleep(3)
                driver.find_element_by_xpath("//android.widget.TextView[@text='录屏直播']").click()
                sleep(1)
                startnewroom(driver, elementinfo, True)  # 创建
            while num < 301:
                print(f'设备{devicename}第{num}次选择房间PK')
                if num % 10 == 0:
                    logger.info(f'设备{devicename}第{num}次选择房间PK')
                driver.background_app(5)
                sleep(10)
                driver.find_element_by_id(elementinfo['离开房间']['id'])
                # sleep(30)
                num += 1
            driver.find_element_by_id(elementinfo['离开房间']['id']).click()
            break
        except Exception as e:
            logger.info(f'第{num}次运行出错，设备是:{devicename}')
            # logger.info(driver.page_source)
            img_file = Path(__file__).cwd().parent / 'testresult' / f'{pubfuc.getlocaltime()}-{devicename}.png'
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            # driver.activate_app(appid)


def change_config(driver, elementinfo):
    driver.find_element_by_id(elementinfo['changeconfig']['id']).click()
    sleep(0.5)
    driver.find_element_by_xpath("//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[1]").click()
    sleep(5)


def startgameroom_changgeresolution(driver, devicename):
    failcount = 1  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    devicedriverinfo = driver.desired_capabilities  # 获取正在运行的设备的参数设置
    elementinfo, deviceid = pubfuc.getiteminfo(devicedriverinfo)
    isios = 'desired'not in devicedriverinfo
    while True:
        try:
            if runcount > failcount:
                break
            if 'RoomI' not in driver.page_source:
                el = elementinfo['多人群聊']['xpath']
                gamechat_name = '游戏录屏' if isios else '游戏连麦'
                el = re.sub('多人群聊', gamechat_name, el)
                driver.find_element_by_xpath(el).click()
                sleep(3)
                if not isios:
                    driver.find_element_by_xpath("//android.widget.TextView[@text='录屏直播']").click()
                    sleep(1)
                # 创建房间
                startnewroom(driver, elementinfo, False)
                # 开始游戏
                driver.find_element_by_xpath(elementinfo['game']['xpath']).click()
                sleep(20)
            while num < 5:
                print(f'设备{devicename}第{num}次选调整分辨率')
                if num % 10 == 0:
                    logger.info(f'设备{devicename}第{num}次选调整分辨率')
                # 调整分辨率
                driver.find_element_by_id(elementinfo['changeconfig']['id']).click()
                sleep(0.5)
                driver.find_element_by_xpath("//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[1]").click()
                sleep(1)
                # 查看离开房间按钮，验证调整分辨率后还在房间中
                driver.find_element_by_id(elementinfo['离开房间']['id'])
                sleep(180)
                num += 1
            driver.find_element_by_id(elementinfo['离开房间']['id']).click()
            break
        except Exception as e:
            logger.info(f'第{num}次运行出错，设备是:{devicename}')
            # logger.info(driver.page_source)
            img_file = Path(__file__).cwd().parent / 'testresult' / f'{pubfuc.getlocaltime()}-{devicename}.png'
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            # driver.activate_app(appid)
"""
以下为liveme app 相关用例
"""


def startlivemeroom(driver, devicename):
    devicedriverinfo = driver.desired_capabilities  # 获取正在运行的设备的参数设置
    elementinfo, deviceid = pubfuc.getiteminfo(devicedriverinfo, 'liveme')

    driver.find_element_by_xpath(elementinfo['开启直播']['xpath']).click()
    sleep(3)
    driver.find_element_by_xpath(elementinfo['多人直播']['xpath']).click()
    sleep(2)

    driver.find_element_by_xpath(elementinfo['开始直播']['xpath']).click()
    sleep(5)
    xml_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{pubfuc.getlocaltime()}-{devicename}.xml')
    with open(xml_file, 'a') as f:
        f.write(driver.page_source)


def joinlivemeroom(driver, room, device):
    devicedriverinfo = driver.desired_capabilities  # 获取正在运行的设备的参数设置
    elementinfo, deviceid = pubfuc.getiteminfo(devicedriverinfo, 'liveme')

    driver.find_element_by_xpath(elementinfo['搜索房间列表']['xpath']).click()
    sleep(3)
    driver.find_element_by_xpath(elementinfo['搜索框']['xpath']).click()
    sleep(2)
    driver.find_element_by_xpath(elementinfo['搜索框']['xpath']).send_keys(room)

    driver.find_element_by_xpath(f'//XCUIElementTypeStaticText[@name="{room}"]').click()

    sleep(2)
    driver.find_element_by_xpath(elementinfo['加入按钮']['xpath']).click()
    sleep(10)
    print(elementinfo['辅播编号']['xpath'])
    fubo_location = driver.find_element_by_xpath(elementinfo['辅播编号']['xpath']).location
    print(fubo_location)
    driver.tap([[46, 127]])
    sleep(5)
    driver.tap([[46, 127]])
    driver.find_element_by_xpath(elementinfo['辅播下麦']['xpath']).click()
    sleep(1)
    print(2)
    sleep(7)
    driver.find_element_by_xpath(elementinfo['退出房间']['xpath']).click()
    sleep(3)
    print(device)


'''
以下为内存泄漏demo的控件和用例
roomid输入框 com.sjdd.testleakdemo:id/mEtRoomID
uid输入框 com.sjdd.testleakdemo:id/mEtUid
start按钮 com.sjdd.testleakdemo:id/mBtnStart
是否勾选pushstream com.sjdd.testleakdemo:id/mCbPush
离开房间 com.sjdd.testleakdemo:id/iv_back
切换角色com.sjdd.testleakdemo:id/iv_changeRole
'''


def startpushstream(driver, roomid, ispushstream=True):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    success_flag = True
    num = 1
    while success_flag:
        try:
            if runcount > failcount:
                success_flag = False
            elementinfo, deviceid = pubfuc.getiteminfo(driver.desired_capabilities)
            driver.find_element_by_id('com.sjdd.testleakdemo:id/mEtRoomID').send_keys('101010'+str(roomid))
            if ispushstream:
                driver.find_element_by_id('com.sjdd.testleakdemo:id/mCbPush').click()
                sleep(1)
                logger.info('勾选推流')
            while num < 1001:
                logger.info(f'{num}次{deviceid}创建房间')
                driver.find_element_by_id('com.sjdd.testleakdemo:id/mBtnStart').click()
                sleep(10)
                driver.find_element_by_id('com.sjdd.testleakdemo:id/iv_back').click()
                sleep(4)
                num += 1
            if num > 1000:
                success_flag = False
        except Exception as e:
            runcount += 1
            logger.error(f'第{num}次运行出错，设备是:{deviceid}')
            img_file = Path(__file__).cwd().parent / 'testresult' / f'{pubfuc.getlocaltime()}-{deviceid}.png'
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            if not success_flag:
                return
            # driver.close_app()
            # driver.launch_app()


def onechangerole(driver_zhubo, driver_fubo):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    success_flag = True
    num = 1
    while success_flag:
        try:
            if runcount > failcount:
                success_flag = False
            elementinfo_zhubo, deviceid_zhubo = pubfuc.getiteminfo(driver_zhubo.desired_capabilities)
            elementinfo_zhubo, deviceid_fubo = pubfuc.getiteminfo(driver_fubo.desired_capabilities)
            for driver in [driver_zhubo, driver_fubo]:
                driver.find_element_by_id('com.sjdd.testleakdemo:id/mCbPush').click()
                sleep(1)
                logger.info('勾选推流')
                driver.find_element_by_id('com.sjdd.testleakdemo:id/mBtnStart').click()
            sleep(4)
            while num < 1001:
                logger.info(f'{num}次{deviceid_zhubo}切换角色')
                driver_zhubo.find_element_by_id('com.sjdd.testleakdemo:id/iv_changeRole').click()
                sleep(6)
                logger.info(f"主播切换角色后，辅播按钮: {driver_fubo.find_element_by_id('com.sjdd.testleakdemo:id/iv_back')}")
                num += 1
            driver.find_element_by_id('com.sjdd.testleakdemo:id/iv_back').click()
            sleep(2)
            if num > 1000:
                success_flag = False
        except Exception as e:
            runcount += 1
            logger.info(f'第{num}次运行出错')
            img_file = Path(__file__).cwd().parent / 'testresult' / f'{pubfuc.getlocaltime()}-{deviceid_zhubo}.png'
            driver_zhubo.save_screenshot(str(img_file))
            img_file = Path(__file__).cwd().parent / 'testresult' / f'{pubfuc.getlocaltime()}-{deviceid_fubo}.png'
            driver_fubo.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            if not success_flag:
                return
            for driver in [driver_zhubo, driver_fubo]:
                if driver.find_element_by_xpath("//android.widget.Button[@text='确定'") is not None:
                    driver.find_element_by_xpath("//android.widget.Button[@text='确定'") .click()
                # driver.close_app()
                # driver.launch_app()


def onlyreceive(driver):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    success_flag = True
    num = 1
    caps = driver.desired_capabilities
    while success_flag:
        try:
            elementinfo, deviceid = pubfuc.getiteminfo(caps)
            sleep(4)
            driver.find_element_by_id('com.sjdd.testleakdemo:id/mCbViewerMode').click()  # 勾选观众模式
            sleep(1)
            while num < 1001:
                logger.info(f'{num}次{deviceid}只收流')
                driver.find_element_by_id('com.sjdd.testleakdemo:id/mBtnStart').click()
                sleep(10)
                driver.find_element_by_id('com.sjdd.testleakdemo:id/iv_back').click()
                sleep(5)
                num += 1
            sleep(2)
            if num > 1000 or runcount > failcount:
                success_flag = False
        except Exception as e:
            runcount += 1
            logger.info(f'第{num}次{deviceid}运行出错')
            logger.info(f'第{runcount}次重跑')
            img_file = Path(__file__).cwd().parent / 'testresult' / f'{pubfuc.getlocaltime()}-{deviceid}.png'
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            if not success_flag:
                return
            if "确定" in driver.page_source:
                driver.find_element_by_xpath("//android.widget.Button[@text='确定'").click()


'''
A50执行方法 
'''


def uploadlog(driver, elementinfo):
    if not driver.find_element_by_xpath(elementinfo['uploadlog']['xpath']).is_displayed():
        driver.execute_script("mobile: dragFromToForDuration",
                              {'fromX': 100, 'fromY': 350, 'toX': 100, 'toY': 50, 'duration': 1})
    driver.find_element_by_xpath(elementinfo['uploadlog']['id']).click()
    sleep(10)
    # driver.find_element_by_xpath(elementinfo['CN']['xpath']).click()
    uoloadtime = pubfuc.getlocaltime()
    sleep(1)
    iswaite = driver.find_element_by_xpath(elementinfo['OK']['xpath']) is None
    while iswaite:
        sleep(3)
        iswaite = driver.find_element_by_xpath(elementinfo['OK']['xpath']) is None
    if 'Upload Success' not in driver.page_source:
        driver.find_element_by_xpath(elementinfo['OK']['xpath']).click()
        uploadlog(driver, elementinfo)
    logger.info(f"上传是否成功: {not iswaite}")
    driver.find_element_by_xpath(elementinfo['OK']['xpath']).click()
    logger.info(f"upload log time is : {uoloadtime}")
    return uoloadtime


def cleanlog(driver, elementinfo):
    driver.find_element_by_xpath(elementinfo['cleanlog']['xpath']).click()
    sleep(3)
    logger.info(f"清理日志成功")
    driver.find_element_by_xpath(elementinfo['OK']['xpath']).click()


def startpusha50(driver, device_name):
    failcount = 5  # 用例中出错后重新执行的次数
    runcount = 1
    success_flag = True
    num = 1
    caps = driver.desired_capabilities
    appid = caps['bundleId']
    elementinfo, deviceid = pubfuc.getiteminfo(caps, 'A50')
    try:
        print(driver.get_window_size())
        isdown = driver.find_element_by_xpath(elementinfo['uploadlog']['xpath']).is_displayed()
        print(isdown)
        if "稍后提醒我" in driver.page_source:
            driver.find_element_by_xpath("//XCUIElementTypeButton[@name='稍后提醒我']").click()
        elif "稍后" in driver.page_source:
            driver.find_element_by_xpath("//XCUIElementTypeButton[@name='稍后']").click()
        while not isdown:
            driver.execute_script("mobile: dragFromToForDuration",
                                  {'fromX': 10, 'fromY': 300, 'toX': 10, 'toY': 50, 'duration': 1})
            isdown = driver.find_element_by_xpath(elementinfo['uploadlog']['xpath']).is_displayed()
        sleep(5)
        # logger.info(f"第{num}次{device_name}开始上传日志")
        # size = driver.get_window_size()
        while True:
            logger.info(f"第{num}次{device_name}加入房间")
            driver.find_element_by_id('START').click()
            sleep(60)
            # driver.find_element_by_id('Music').click()
            # backiosapp(driver, size, appid)
            # sleep(300)
            driver.find_element_by_id('Back').click()
            sleep(5)
            # if num % 50 == 0:
            #     logger.info(f"第{num}次{device_name}开始上传日志")
            #     uploadlog(driver, elementinfo)
            #     cleanlog(driver, elementinfo)
            #     downloadfiles = pubfuc.download_file_from_server('A50')
            #     for file in downloadfiles:
            #         extra_dir = pubfuc.extrafile(file)
            #         for f in os.listdir(extra_dir):
            #             filepath = os.path.join(extra_dir, f)
            #             print(filepath)
            #             if 'pslstreaming' in f:
            #                 logger.info('\n推流失败connect为1的结果:')
            #                 pubfuc.parselog(filepath, 'connect=-1')
            num += 1
            if num > 501 or runcount > failcount:
                break
    except Exception as e:
        runcount += 1
        logger.info(f'第{num}次{device_name}运行出错')
        logger.info(f'第{runcount}次重跑')
        # logger.info(driver.page_source)
        img_file = Path(__file__).cwd().parent / 'testresult' / f'{pubfuc.getlocaltime()}-{device_name}.png'
        driver.save_screenshot(str(img_file))
        sleep(5)
        logger.error(e.args[0], exc_info=True)
        driver.activate_app(appid)
        if not success_flag:
            return
        # driver.terminate_app(appid)
        # driver.launch_app()
    finally:
        # return
        if num % 50 != 0:
            logger.info(f"第{num}次{device_name}开始上传日志")
            uploadlog(driver, elementinfo)
            cleanlog(driver, elementinfo)
            downloadfiles = pubfuc.download_file_from_server('A50')
            for file in downloadfiles:
                extra_dir = pubfuc.extrafile(file)

                for f in os.listdir(extra_dir):
                    filepath = os.path.join(extra_dir, f)
                    if 'pslstreaming' in f:
                        logger.info('\n推流失败connect为1的结果:')
                        pubfuc.parselog(filepath, 'connect=-1')


'''
P31link执行方法 
'''


def startpushp31link191(driver):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    success_flag = True
    num = 1
    caps = driver.desired_capabilities
    elementinfo, deviceid = pubfuc.getiteminfo(caps, 'A50')
    size = driver.get_window_size()
    print(size)
    try:
        if "稍后提醒我" in driver.page_source:
            driver.find_element_by_xpath("//XCUIElementTypeButton[@name='稍后提醒我']").click()
        while True:
            uploadisvisiable = driver.find_element_by_xpath(elementinfo['uploadlog']['xpath']).is_displayed()
            if not uploadisvisiable:
                driver.execute_script("mobile: dragFromToForDuration",
                                      {'fromX': size['width']-10, 'fromY': size['height']-50, 'toX': size['width']-10,
                                       'toY': 50, 'duration': 1})
            elif uploadisvisiable:
                break
        sleep(5)
        while True:
            logger.info(f"第{num}次{deviceid}加入房间")
            driver.find_element_by_id('Save Config').click()
            sleep(2)
            driver.find_element_by_id('START').click()
            sleep(15)
            # backiosapp(driver, size, appid)
            driver.find_element_by_id('STOP').click()
            sleep(5)
            if num % 3000 == 0:
                uploadlog(driver, elementinfo)
                cleanlog(driver, elementinfo)
                downloadfiles = pubfuc.download_file_from_server('P31Link')
                print(downloadfiles)
                for file in downloadfiles:
                    print(file)
                    extra_dir = pubfuc.extrafile(file)
                    print(extra_dir)
                    for f in os.listdir(extra_dir):
                        if 'pslstreaming' in f:
                            logger.info('\n推流失败connect为1的结果:\n')
                            pubfuc.parselog(f, 'connect=-1')
                        elif 'psdemux'in f:
                            logger.info('\npsmoe为\n')
                            pubfuc.parselog(f, 'psmode')
                            logger.info('\nbps为0的结果\n')
                            pubfuc.parselog(f, 'bps 0')
            num += 1
            if num > 300 or runcount > failcount:
                break
    except Exception as e:
        runcount += 1
        logger.info(f'第{num}次{deviceid}运行出错')
        logger.info(f'第{runcount}次重跑')
        # logger.info(driver.page_source)
        img_file = Path(__file__).cwd().parent / 'testresult' / f'{pubfuc.getlocaltime()}-{deviceid}.png'
        driver.save_screenshot(str(img_file))
        sleep(5)
        logger.error(e.args[0], exc_info=True)
        if not success_flag:
            return
        # driver.terminate_app(appid)
        # driver.launch_app()
    finally:
        if num % 30 != 0:
            uploadlog(driver, elementinfo)
            cleanlog(driver, elementinfo)


'''
MPdemo

'''


def startmpdemo(driver, device_name):
    failcount = 1  # 用例中出错后重新执行的次数
    runcount = 1
    success_flag = True
    num = 1
    size = driver.get_window_size()
    try:
        if 'Clean log' not in driver.page_source:
            x = size['width'] - 50
            y = size['height'] * 0.7
            end_y = size['height'] * 0.3
            driver.swipe(x, y, x, end_y)
        sleep(5)
        while success_flag:
            logger.info(f"第{num}次{device_name}加入房间")
            driver.find_element_by_xpath("//android.widget.Button[@text='Start']").click()
            sleep(6)
            driver.find_element_by_xpath("//android.widget.Button[@text='STOP']").click()
            sleep(5)
            if num % 30 == 0:
                logger.info(f"第{num}次{device_name}开始上传日志")
                driver.find_element_by_xpath("//android.widget.Button[@text='  Upload log']").click()
                sleep(10)
                driver.find_element_by_xpath("//android.widget.Button[@text='Clean log  ']").click()
                sleep(10)
                pubfuc.download_file_from_server('MPDemo')
            num += 1
            if num > 1000 or runcount > failcount:
                success_flag = False
    except Exception as e:
        runcount += 1
        logger.info(f'第{num}次{device_name}运行出错')
        logger.info(f'第{runcount}次重跑')
        print(driver.page_source)
        img_file = Path(__file__).cwd().parent / 'testresult' / f'{pubfuc.getlocaltime()}-{device_name}.png'
        driver.save_screenshot(str(img_file))
        sleep(5)
        logger.error(e.args[0], exc_info=True)
        driver.close_app()
        driver.launch_app()
        if not success_flag:
            return
    finally:
        if num % 30 != 0:
            logger.info(f"第{num}次{device_name}开始上传日志")
            driver.find_element_by_xpath("//android.widget.Button[@text='  Upload log']").click()
            sleep(10)
            driver.find_element_by_xpath("//android.widget.Button[@text='Clean log  ']").click()
            sleep(10)
            pubfuc.download_file_from_server('MPDemo')


'''
同桌游戏-海外版本
'''


def createnewparty(driver):
    caps = driver.desired_capabilities
    elementinfo, deviceid = pubfuc.getiteminfo(caps, 'TongZhuoHaiWai')
    size = driver.get_window_size()
    driver.find_element_by_xpath(elementinfo['chat']['xpath']).click()
    sleep(2)
    driver.find_element_by_id(elementinfo['加号']['id']).click()
    sleep(3)
    driver.tap([[size['width']/2 + 200, 270]])
    sleep(2)
    driver.find_element_by_id(elementinfo['random_roomtitile']['id']).click()
    sleep(3)
    driver.find_element_by_xpath(elementinfo['create']['xpath']).click()
    sleep(3)
    driver.find_element_by_xpath(elementinfo['invite']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['invite_friends']['xpath']).click()
    sleep(1)
    driver.find_element_by_id(elementinfo['invite_search']['id']).send_keys('loy')
    sleep(1)
    driver.find_element_by_id(elementinfo['invite_select']['id']).click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.Button[@text='Done(1)']").click()
    sleep(1)
