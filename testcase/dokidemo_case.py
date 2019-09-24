# -*- coding:utf-8 -*-
# import re
# sys.path.append('..')

from time import sleep
import unittest
import lib.public_functions as pubfuc
import multiprocessing
from appium import webdriver
import testcase.dokidemo_behavior as dokidemo_behavior
import logging

logger = logging.getLogger('autolog')


class QSDokiDemoTest(unittest.TestCase):

    def setUp(self):
        # 在当前目录，新建mail.txt，文件第一行存放设备列表，第二行存放roomid
        with open('mail.txt', 'r') as f:
            info = f.readlines()
        devicelist = info[0].rstrip().split(',')
        logger.info(f'devicelist: {devicelist}')
        self.device_name = devicelist
        self.roomid = info[1].split('#')[0].rstrip()
        self.sd = pubfuc.StartDriver(devicelist)
        self.proc_list = []

        pubfuc.cleannodeproc()
        for i in range(len(self.sd.devicelist)):
            self.proc_list.append(multiprocessing.Process(target=self.sd.startappiumserver, args=(i,)))

        for pro in self.proc_list:
            pro.start()

        for pro in self.proc_list:
            pro.join()

        while len(self.sd.getnodeprocpid()) < len(devicelist):
            sleep(1)

        logger.info(self.sd.getnodeprocpid())

        self.driverlist = []

        for i in range(len(self.sd.devicelist)):
            logger.info(i)
            desire_caps = self.sd.realdevice[i]
            if 'bundleId' in desire_caps:
                desire_caps['bundleId'] = 'com.powerinfo.iLiveQSStarLight'  # doki demo
                # desire_caps['waitForQuiescence'] = 'false'
            else:
                desire_caps['appPackage'] = 'com.powerinfo.iLiveQSDoki'
                desire_caps['appActivity'] = 'com.powerinfo.iLiveQSDoki.DokiLoginSettingActivity'
            driver = webdriver.Remote(f"http://localhost:{self.sd.aport[i]}/wd/hub", self.sd.realdevice[i])
            self.driverlist.append(driver)

        logger.info(self.driverlist)

    def tearDown(self):
        logger.info('test运行完成')
        # quite the device driver
        # pass
        for driver in self.driverlist:
            driver.quit()

    def test_001_DokiDemo_两主播多次PK(self):
        logger.info('test_001_DokiDemo_创建加入房间')
        driver_A = self.driverlist[0]   # 主播A
        driver_B = self.driverlist[1]   # 主播B
        failcount = 3  # 用例中出错后重新执行的次数
        runcount = 1
        num = 1
        caps = driver_A.desired_capabilities
        elementinfo, deviceid = pubfuc.getiteminfo(caps, 'QSDoki')
        while True:
            try:
                # 创建房间并返回房间号
                roomid_A = dokidemo_behavior.create_doki_room(driver_A, elementinfo)
                roomid_B = dokidemo_behavior.create_doki_room(driver_B, elementinfo)
                # 进行PK
                while True:
                    dokidemo_behavior.choose_room_pk(driver_A, roomid_B, elementinfo)
                    dokidemo_behavior.choose_room_pk(driver_B, roomid_A, elementinfo)
                    if num > 101 or runcount > failcount:
                        break
            except Exception as e:
                logger.info(f'第{num}次运行出错，设备是:{devicename}')
                # print(driver.page_source)
                img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{pubfuc.getlocaltime()}-{self.devicename[0]}.png')
                driver_A.save_screenshot(str(img_file))
                img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{pubfuc.getlocaltime()}-{self.devicename[1]}.png')
                driver_B.save_screenshot(str(img_file))
                sleep(3)
                logger.error(e.args[0], exc_info=True)
                logger.info(f'第{runcount}次重跑')
                runcount += 1
                driver_A.close_app()
                driver_A.launch_app()
                driver_B.close_app()
                driver_B.launch_app()

    def test_002_DokiDemo_多次加入离开房间(self):
        logger.info('test_002_DokiDemo_多次加入离开房间')
        driver_A = self.driverlist[0]   # 主播A
        failcount = 3  # 用例中出错后重新执行的次数
        runcount = 1
        num = 1
        elementinfo, deviceid = pubfuc.getiteminfo(driver_A.desired_capabilities, 'QSDoki')
        while True:
            try:
                # 进行PK
                print(f'第{num}次加入房间')
                dokidemo_behavior.join_doki_room(driver_A, elementinfo, self.roomid)
                # sleep(5)
                # driver_A.background_app(5)
                # sleep(5)
                driver_A.find_element_by_id(elementinfo['离开房间']['id']).click()
                sleep(3)
                num += 1
                if num > 501 or runcount > failcount:
                    break

            except Exception as e:
                logger.info(f'第{num}次运行出错，设备是:{self.devicename}')
                # print(driver.page_source)
                img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{pubfuc.getlocaltime()}-{self.devicename[0]}.png')
                driver_A.save_screenshot(str(img_file))
                sleep(3)
                logger.error(e.args[0], exc_info=True)
                logger.info(f'第{runcount}次重跑')
                runcount += 1
                driver_A.close_app()
                driver_A.launch_app()

    def test_003_DokiDemo_加入切后台操作(self):
        logger.info('test_003_DokiDemo_创建加入房间')
        driver_A = self.driverlist[0]   # 主播A
        failcount = 3  # 用例中出错后重新执行的次数
        runcount = 1
        num = 1
        elementinfo, deviceid = pubfuc.getiteminfo(driver_A.desired_capabilities, 'QSDoki')
        while True:
            try:
                # 进行PK
                print(f'第{num}次加入房间')
                for i in range(15):
                    dokidemo_behavior.join_doki_room(driver_A, elementinfo, self.roomid)
                    sleep(5)
                    driver_A.find_element_by_id(elementinfo['离开房间']['id']).click()
                    sleep(3)
                dokidemo_behavior.join_doki_room(driver_A, elementinfo, self.roomid)
                sleep(5)
                for i in range(15):
                    driver_A.background_app(5)
                    sleep(10)
                driver_A.find_element_by_id(elementinfo['离开房间']['id']).click()
                sleep(3)
                num += 1
                if num > 21 or runcount > failcount:
                    break

            except Exception as e:
                logger.info(f'第{num}次运行出错，设备是:{self.devicename}')
                # print(driver.page_source)
                img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{pubfuc.getlocaltime()}-{self.devicename[0]}.png')
                driver_A.save_screenshot(str(img_file))
                sleep(3)
                logger.error(e.args[0], exc_info=True)
                logger.info(f'第{runcount}次重跑')
                runcount += 1
                driver_A.close_app()
                driver_A.launch_app()


