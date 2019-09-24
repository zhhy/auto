# -*- coding:utf-8 -*-

from time import sleep
import lib.public_functions as pubfuc
from pathlib import Path
import re
import subprocess
import logging
import os
from appium.webdriver.common.touch_action import TouchAction


logger = logging.getLogger('autolog')

'''
直面
'''

def startpushf2f(driver, device_name):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    success_flag = True
    num = 1
    caps = driver.desired_capabilities
    appid = caps['bundleId']
    elementinfo, deviceid = pubfuc.getiteminfo(caps, '直面')
    try:
        if "稍后提醒我" in driver.page_source:
            driver.find_element_by_xpath("//XCUIElementTypeButton[@name='稍后提醒我']").click()
        elif "稍后" in driver.page_source:
            driver.find_element_by_xpath("//XCUIElementTypeButton[@name='稍后']").click()
        sleep(5)
        # if num ==1:
            # uploadlog(driver, elementinfo)
            # cleanlog(driver, elementinfo)
            # logger.info(f'第{runcount}次启动截图')
            # logger.info(driver.page_source)
            # img_file = Path(__file__).cwd().parent / 'testresult' / f'{pubfuc.getlocaltime()}-{device_name}.png'
            # driver.save_screenshot(str(img_file))
            # sleep(5)
        # size = driver.get_window_size()
        while success_flag:
            logger.info(f"第{num}次{device_name}召开会议")
            print(f"第{num}次{device_name}召开会议")
            driver.find_element_by_xpath(elementinfo['召开会议']['xpath']).click()
            sleep(3)
            driver.find_element_by_xpath(elementinfo['召开会议2']['xpath']).click()
            sleep(5)
            # y = driver.page_source
            # x=re.findall('临时会议.+\d+', y)[0]
            # z=re.findall('\d+', x)[0];
            # print(z)
            # driver.find_element_by_xpath(f'(//XCUIElementTypeOther[@name="临时会议-{z}"])[1]/XCUIElementTypeOther[1]').click()
            driver.find_element_by_xpath(elementinfo['退出会议']['xpath']).click()
            sleep(3)
            driver.find_element_by_xpath(elementinfo['结束会议']['xpath']).click()
            sleep(3)
            driver.find_element_by_xpath(elementinfo['召开会议-返回']['xpath']).click()
            # uploadlog(driver, elementinfo)
            # cleanlog(driver, elementinfo)
            # pubfuc.download_file_from_server('A50')
            #if num % 50 == 0:
                #logger.info(f"第{num}次{device_name}开始上传日志")
                #uploadlog(driver, elementinfo)
                #cleanlog(driver, elementinfo)
                #downloadfiles = pubfuc.download_file_from_server('A50')
            num += 1
            if num > 100 or runcount > failcount:
                success_flag = False
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
        driver.close_app()
        driver.launch_app()

# def savebutton(self):
#     ip6机型
#     TouchAction(driver).tap(x=180, y=121).perform()  #输入会议ID
#     TouchAction(driver).tap(x=66, y=473).perform()   #1
#     TouchAction(driver).tap(x=187, y=472).perform()  #2
#     TouchAction(driver).tap(x=309, y=476).perform()  #3
#     TouchAction(driver).tap(x=66, y=528).perform()   #4
#     TouchAction(driver).tap(x=185, y=526).perform()  #5
#     TouchAction(driver).tap(x=310, y=527).perform()  #6
#     TouchAction(driver).tap(x=63, y=581).perform()   #7
#     TouchAction(driver).tap(x=185, y=581).perform()  #8
#     TouchAction(driver).tap(x=312, y=585).perform()  #9
#     TouchAction(driver).tap(x=185, y=637).perform()  #0
#     TouchAction(driver).tap(x=183, y=276).perform()  #加入会议
#     ip5机型
#     TouchAction(driver).tap(x=54, y=377).perform()   #1
#     TouchAction(driver).tap(x=162, y=375).perform()  #2
#     TouchAction(driver).tap(x=264, y=376).perform()  #3
#     TouchAction(driver).tap(x=54, y=430).perform()   #4
#     TouchAction(driver).tap(x=158, y=430).perform()  #5
#     TouchAction(driver).tap(x=265, y=431).perform()  #6
#     TouchAction(driver).tap(x=55, y=483).perform()   #7
#     TouchAction(driver).tap(x=157, y=485).perform()  #8
#     TouchAction(driver).tap(x=265, y=483).perform()  #9
#     TouchAction(driver).tap(x=158, y=541).perform()  #0


# cmd_exec = f'adb shell dumpsys window w |{find_exec} \/|{find_exec} name='
#     getappinfo = subprocess.getoutput(cmd_exec)


# size = driver.get_window_size()                下拉
#             x = size['width'] / 2
#             y = size['height'] * 0.7
#             end_y = size['height'] * 0.3
#             while not roomisfind:
#                 print(re.findall('ext="Room.+\d+"', driver.page_source))
#                 driver.swipe(x, y, x, end_y)
#                 roomisfind = re.findall('Room.+\d+


# driver.back()  Android返回
# driver.lock()  锁屏 括号里写锁多久


def joinroomf2f(driver, device_name):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    success_flag = True
    num = 1
    caps = driver.desired_capabilities
    appid = caps['bundleId']
    elementinfo, deviceid = pubfuc.getiteminfo(caps, '直面')
    try:
        if "稍后提醒我" in driver.page_source:
            driver.find_element_by_xpath("//XCUIElementTypeButton[@name='稍后提醒我']").click()
        elif "稍后" in driver.page_source:
            driver.find_element_by_xpath("//XCUIElementTypeButton[@name='稍后']").click()
        sleep(5)
        # if num ==1:
            # uploadlog(driver, elementinfo)
            # cleanlog(driver, elementinfo)
            # logger.info(f'第{runcount}次启动截图')
            # logger.info(driver.page_source)
            # img_file = Path(__file__).cwd().parent / 'testresult' / f'{pubfuc.getlocaltime()}-{device_name}.png'
            # driver.save_screenshot(str(img_file))
            # sleep(5)
        # size = driver.get_window_size()
        while success_flag:
            logger.info(f"第{num}次{device_name}加入会议")
            print(f"第{num}次{device_name}加入会议")
            driver.find_element_by_xpath(elementinfo['加入会议']['xpath']).click()
            sleep(1)
            TouchAction(driver).tap(x=180, y=121).perform()  #输入会议ID
            sleep(3)
            TouchAction(driver).tap(x=54, y=377).perform()  # 1
            TouchAction(driver).tap(x=265, y=431).perform()  # 6
            TouchAction(driver).tap(x=55, y=483).perform()  # 7
            TouchAction(driver).tap(x=162, y=375).perform()  # 2
            TouchAction(driver).tap(x=265, y=431).perform()  # 6
            sleep(1)
            TouchAction(driver).tap(x=158, y=298).perform()  #加入会议
            sleep(2000)
            # y = driver.page_source
            # x = re.findall('临时会议.+\d+', y)[0]
            # z = re.findall('\d+', x)[0];
            # print(z)
            # driver.find_element_by_xpath(
            #     f'(//XCUIElementTypeOther[@name="临时会议-{z}"])[1]/XCUIElementTypeOther[1]').click()
            driver.find_element_by_xpath(elementinfo['退出会议']['xpath']).click()
            sleep(3)
            driver.find_element_by_xpath(elementinfo['确认离开']['xpath']).click()
            sleep(3)
            driver.find_element_by_xpath(elementinfo['加入会议-返回']['xpath']).click()
            sleep(10)


            # uploadlog(driver, elementinfo)
            # cleanlog(driver, elementinfo)
            # pubfuc.download_file_from_server('A50')
            #if num % 50 == 0:
                #logger.info(f"第{num}次{device_name}开始上传日志")
                #uploadlog(driver, elementinfo)
                #cleanlog(driver, elementinfo)
                #downloadfiles = pubfuc.download_file_from_server('A50')
            num += 1
            if num > 100 or runcount > failcount:
                success_flag = False
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
        driver.close_app()
        driver.launch_app()





def f2fbackapp(driver, device_name):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    success_flag = True
    num = 1
    caps = driver.desired_capabilities
    appid = caps['bundleId']
    elementinfo, deviceid = pubfuc.getiteminfo(caps, '直面')
    try:
        if "稍后提醒我" in driver.page_source:
            driver.find_element_by_xpath("//XCUIElementTypeButton[@name='稍后提醒我']").click()
        elif "稍后" in driver.page_source:
            driver.find_element_by_xpath("//XCUIElementTypeButton[@name='稍后']").click()
        sleep(5)
        # if num ==1:
            # uploadlog(driver, elementinfo)
            # cleanlog(driver, elementinfo)
            # logger.info(f'第{runcount}次启动截图')
            # logger.info(driver.page_source)
            # img_file = Path(__file__).cwd().parent / 'testresult' / f'{pubfuc.getlocaltime()}-{device_name}.png'
            # driver.save_screenshot(str(img_file))
            # sleep(5)
        # size = driver.get_window_size()
        bundleid = driver.capabilities['bundleId']
        size = driver.get_window_size()
        driver.find_element_by_xpath(elementinfo['加入会议']['xpath']).click()
        sleep(1)
        TouchAction(driver).tap(x=180, y=121).perform()  # 输入会议ID
        sleep(3)
        TouchAction(driver).tap(x=67, y=473).perform()  # 1
        TouchAction(driver).tap(x=312, y=585).perform()  # 9
        TouchAction(driver).tap(x=185, y=581).perform()  # 8
        sleep(1)
        TouchAction(driver).tap(x=183, y=276).perform()  # 加入会议
        sleep(3)
        while success_flag:
            logger.info(f"第{num}次{device_name}切后台")
            print(f"第{num}次{device_name}切后台")


            TouchAction(driver).tap(x=341, y=634).perform()
            sleep(2)
            TouchAction(driver).tap(x=185, y=526).perform() # iphone辅助功能按键放置在右下角
            sleep(5)

            driver.activate_app(bundleid)
            sleep(5)
            # 切后台回来后，查看离开房间按钮是否可用，确定正确切回了前台
            # y = driver.page_source
            # x = re.findall('临时会议.+\d+', y)[0]
            # z = re.findall('\d+', x)[0];
            # print(z)
            # back_is_enable = driver.find_element_by_xpath(
            #     f'(//XCUIElementTypeOther[@name="临时会议-{z}"])[1]/XCUIElementTypeOther[1]').get_attribute('enabled')
            back_is_enable = driver.find_element_by_id(elementinfo['退出会议']['id']).get_attribute('enabled')
            logger.info(f"离开房间按钮是否可用：{back_is_enable}")


            # uploadlog(driver, elementinfo)
            # cleanlog(driver, elementinfo)
            # pubfuc.download_file_from_server('A50')
            #if num % 50 == 0:
                #logger.info(f"第{num}次{device_name}开始上传日志")
                #uploadlog(driver, elementinfo)
                #cleanlog(driver, elementinfo)
                #downloadfiles = pubfuc.download_file_from_server('A50')
            num += 1
            if num > 100 or runcount > failcount:
                success_flag = False
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
        driver.close_app()
        driver.launch_app()




def f2flockscreen(driver, device_name):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    success_flag = True
    num = 1
    caps = driver.desired_capabilities
    appid = caps['bundleId']
    elementinfo, deviceid = pubfuc.getiteminfo(caps, '直面')
    try:
        if "稍后提醒我" in driver.page_source:
            driver.find_element_by_xpath("//XCUIElementTypeButton[@name='稍后提醒我']").click()
        elif "稍后" in driver.page_source:
            driver.find_element_by_xpath("//XCUIElementTypeButton[@name='稍后']").click()
        sleep(5)
        # if num ==1:
            # uploadlog(driver, elementinfo)
            # cleanlog(driver, elementinfo)
            # logger.info(f'第{runcount}次启动截图')
            # logger.info(driver.page_source)
            # img_file = Path(__file__).cwd().parent / 'testresult' / f'{pubfuc.getlocaltime()}-{device_name}.png'
            # driver.save_screenshot(str(img_file))
            # sleep(5)
        # size = driver.get_window_size()
        driver.find_element_by_xpath(elementinfo['加入会议']['xpath']).click()
        sleep(1)
        TouchAction(driver).tap(x=180, y=121).perform()  # 输入会议ID
        sleep(3)
        TouchAction(driver).tap(x=187, y=472).perform()  # 2
        TouchAction(driver).tap(x=310, y=527).perform()  # 6
        TouchAction(driver).tap(x=185, y=581).perform()  # 8
        sleep(1)
        TouchAction(driver).tap(x=183, y=276).perform()  # 加入会议
        sleep(5)
        while success_flag:
            logger.info(f"第{num}次{device_name}锁屏")
            print(f"第{num}次{device_name}锁屏")

            driver.lock(5)

            sleep(5)

            # 锁屏回来后，查看离开房间按钮是否可用，确定正确切回了前台
            # y = driver.page_source
            # x = re.findall('临时会议.+\d+', y)[0]
            # z = re.findall('\d+', x)[0];
            # print(z)
            # back_is_enable = driver.find_element_by_xpath(
            #             #     f'(//XCUIElementTypeOther[@name="临时会议-{z}"])[1]/XCUIElementTypeOther[1]').get_attribute('enabled')
            back_is_enable = driver.find_element_by_id(elementinfo['退出会议']['id']).get_attribute('enabled')
            logger.info(f"离开房间按钮是否可用：{back_is_enable}")


            # uploadlog(driver, elementinfo)
            # cleanlog(driver, elementinfo)
            # pubfuc.download_file_from_server('A50')
            #if num % 50 == 0:
                #logger.info(f"第{num}次{device_name}开始上传日志")
                #uploadlog(driver, elementinfo)
                #cleanlog(driver, elementinfo)
                #downloadfiles = pubfuc.download_file_from_server('A50')
            num += 1
            if num > 100 or runcount > failcount:
                success_flag = False
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
        driver.close_app()
        driver.launch_app()


def f2fchangeview(driver, device_name):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    success_flag = True
    num = 1
    caps = driver.desired_capabilities
    appid = caps['bundleId']
    elementinfo, deviceid = pubfuc.getiteminfo(caps, '直面')
    try:
        if "稍后提醒我" in driver.page_source:
            driver.find_element_by_xpath("//XCUIElementTypeButton[@name='稍后提醒我']").click()
        elif "稍后" in driver.page_source:
            driver.find_element_by_xpath("//XCUIElementTypeButton[@name='稍后']").click()
        sleep(5)
        # if num ==1:
        # uploadlog(driver, elementinfo)
        # cleanlog(driver, elementinfo)
        # logger.info(f'第{runcount}次启动截图')
        # logger.info(driver.page_source)
        # img_file = Path(__file__).cwd().parent / 'testresult' / f'{pubfuc.getlocaltime()}-{device_name}.png'
        # driver.save_screenshot(str(img_file))
        # sleep(5)
        # size = driver.get_window_size()
        driver.find_element_by_xpath(elementinfo['加入会议']['xpath']).click()
        sleep(1)
        TouchAction(driver).tap(x=180, y=121).perform()  # 输入会议ID
        sleep(3)
        TouchAction(driver).tap(x=187, y=472).perform()  # 2
        TouchAction(driver).tap(x=310, y=527).perform()  # 6
        TouchAction(driver).tap(x=185, y=581).perform()  # 8
        sleep(1)
        TouchAction(driver).tap(x=183, y=276).perform()  # 加入会议
        sleep(5)
        while success_flag:
            logger.info(f"第{num}次{device_name}切换视角")
            print(f"第{num}次{device_name}切换视角")





            # 锁屏回来后，查看离开房间按钮是否可用，确定正确切回了前台
            # y = driver.page_source
            # x = re.findall('临时会议.+\d+', y)[0]
            # z = re.findall('\d+', x)[0];
            # print(z)
            # back_is_enable = driver.find_element_by_xpath(
            #             #     f'(//XCUIElementTypeOther[@name="临时会议-{z}"])[1]/XCUIElementTypeOther[1]').get_attribute('enabled')
            back_is_enable = driver.find_element_by_id(elementinfo['退出会议']['id']).get_attribute('enabled')
            logger.info(f"离开房间按钮是否可用：{back_is_enable}")

            # uploadlog(driver, elementinfo)
            # cleanlog(driver, elementinfo)
            # pubfuc.download_file_from_server('A50')
            # if num % 50 == 0:
            # logger.info(f"第{num}次{device_name}开始上传日志")
            # uploadlog(driver, elementinfo)
            # cleanlog(driver, elementinfo)
            # downloadfiles = pubfuc.download_file_from_server('A50')
            num += 1
            if num > 100 or runcount > failcount:
                success_flag = False
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
        driver.close_app()
        driver.launch_app()






def f2fPushSiri(driver, device_name):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    success_flag = True
    num = 1
    caps = driver.desired_capabilities
    appid = caps['bundleId']
    elementinfo, deviceid = pubfuc.getiteminfo(caps, '直面')
    try:
        if "稍后提醒我" in driver.page_source:
            driver.find_element_by_xpath("//XCUIElementTypeButton[@name='稍后提醒我']").click()
        elif "稍后" in driver.page_source:
            driver.find_element_by_xpath("//XCUIElementTypeButton[@name='稍后']").click()
        sleep(5)
        # if num ==1:
            # uploadlog(driver, elementinfo)
            # cleanlog(driver, elementinfo)
            # logger.info(f'第{runcount}次启动截图')
            # logger.info(driver.page_source)
            # img_file = Path(__file__).cwd().parent / 'testresult' / f'{pubfuc.getlocaltime()}-{device_name}.png'
            # driver.save_screenshot(str(img_file))
            # sleep(5)
        # size = driver.get_window_size()
        bundleid = driver.capabilities['bundleId']
        size = driver.get_window_size()
        driver.find_element_by_xpath(elementinfo['加入会议']['xpath']).click()
        sleep(1)
        TouchAction(driver).tap(x=180, y=121).perform()  # 输入会议ID
        sleep(3)
        TouchAction(driver).tap(x=66, y=528).perform()  # 4
        TouchAction(driver).tap(x=185, y=526).perform()  # 5
        TouchAction(driver).tap(x=310, y=527).perform()  # 6
        sleep(1)
        TouchAction(driver).tap(x=183, y=276).perform()  # 加入会议
        sleep(5)
        while success_flag:
            logger.info(f"第{num}次{device_name}开siri")
            print(f"第{num}次{device_name}开siri")


            TouchAction(driver).tap(x=341, y=634).perform()
            sleep(2)
            TouchAction(driver).tap(x=101, y=488).perform() # iphone辅助功能按键放置在右下角
            sleep(6)

            driver.activate_app(bundleid)
            sleep(15)
            # 切后台回来后，查看离开房间按钮是否可用，确定正确切回了前台
            # y = driver.page_source
            # x = re.findall('临时会议.+\d+', y)[0]
            # z = re.findall('\d+', x)[0];
            # print(z)
            # back_is_enable = driver.find_element_by_xpath(
            #     f'(//XCUIElementTypeOther[@name="临时会议-{z}"])[1]/XCUIElementTypeOther[1]').get_attribute('enabled')
            back_is_enable = driver.find_element_by_xpath(elementinfo['会议界面返回按钮']['xpath']).get_attribute('enabled')
            logger.info(f"离开房间按钮是否可用：{back_is_enable}")


            # uploadlog(driver, elementinfo)
            # cleanlog(driver, elementinfo)
            # pubfuc.download_file_from_server('A50')
            #if num % 50 == 0:
                #logger.info(f"第{num}次{device_name}开始上传日志")
                #uploadlog(driver, elementinfo)
                #cleanlog(driver, elementinfo)
                #downloadfiles = pubfuc.download_file_from_server('A50')
            num += 1
            if num > 500 or runcount > failcount:
                success_flag = False
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
        driver.close_app()
        driver.launch_app()
