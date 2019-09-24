# -*- coding:utf-8 -*-
# import re
# sys.path.append('..')

from time import sleep
import unittest
import lib.public_functions as pubfuc
import multiprocessing
from appium import webdriver
import testcase.huajiao_behavior as huajiao_behavior
import logging

logger = logging.getLogger('autolog')


class HuaJiaoTest(unittest.TestCase):

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
                desire_caps['bundleId'] = 'com.huajiao.seeding'  # bootstrapA50
                # desire_caps['waitForQuiescence'] = 'false'
            else:
                desire_caps['appPackage'] = 'com.huajiao.seeding'
                desire_caps['appActivity'] = 'com.huajiao.seeding'
            driver = webdriver.Remote(f"http://localhost:{self.sd.aport[i]}/wd/hub", self.sd.realdevice[i])
            sleep(10)
            self.driverlist.append(driver)

        logger.info(self.driverlist)

    def test_001开始直播(self):
        logger.info('test_001开始直播')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            driver.find_element_by_xpath('//XCUIElementTypeButton[@name="tab logo"]').click()
            sleep(3)
            # logger.info(driver.page_source)
            # driver.find_element_by_xpath('//XCUIElementTypeImage[@name="tab_live"]').click()
            driver.find_element_by_xpath('//XCUIElementTypeStaticText[@name="立即 直播"]').click()
            sleep(5)
            driver.find_element_by_xpath('//XCUIElementTypeButton[@name="开始直播"]').click()
            sleep(10)
            driver.find_element_by_xpath('//XCUIElementTypeButton[@name="live button close"]').click()
            sleep(1)
            driver.find_element_by_xpath('//XCUIElementTypeButton[@name="确定"]').click()
            sleep(2)
            driver.find_element_by_xpath('//XCUIElementTypeButton[@name="video close"]').click()
            sleep(10)
            # //XCUIElementTypeImage[@name="tab_live"] #81 151
            # //XCUIElementTypeButton[@name="icon gd zbj"]
            # //XCUIElementTypeImage[@name="icon_lm_gd"] 连麦
            # //XCUIElementTypeStaticText[ @ name = "立即 直播"]
            # //XCUIElementTypeButton[@name="开始直播"]
            # //XCUIElementTypeButton[@name="live button close"] # location
            # //XCUIElementTypeButton[@name="确定"]
            # //XCUIElementTypeButton[@name="video close"]
            # //XCUIElementTypeButton[@name="live button music"]
            # //XCUIElementTypeButton[@name="live icon line normal"] # location
            # driver.find_element_by_xpath('//XCUIElementTypeButton[@name="tab me normal"]').click()
            # driver.find_element_by_xpath('//XCUIElementTypeButton[@name="geren shezhi"]').click()
            # //XCUIElementTypeStaticText[@name="关于花椒"]
            # //XCUIElementTypeStaticText[@name="上传日志"]
            # //XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeOther[2]
            # //XCUIElementTypeStaticText[@name="上传完成"]
            # //XCUIElementTypeButton[@name="好的"]
            # //XCUIElementTypeButton[@name="titlebar back normal"] # 返回按钮
            # driver.find_element_by_id('tab logo').click()
            # proc = pool.apply_async(huajiao_behavior.login, (driver, self.device_name[index], ))
            # procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()

    def tearDown(self):
        logger.info('test运行完成')
        # quite the device driver
        pass
        # for driver in self.driverlist:
        #     driver.quit()



