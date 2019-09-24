# -*- coding:utf-8 -*-

from time import sleep
import unittest
import lib.public_functions as pubfuc
import multiprocessing
from appium import webdriver
import testcase.app_behavior as app_behavior
import logging

logger = logging.getLogger('autolog')


class A50Test(unittest.TestCase):

    def setUp(self):
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

            desire_caps['bundleId'] = 'com.powerinfo.iLiveA50'

            driver = webdriver.Remote(f"http://localhost:{self.sd.aport[i]}/wd/hub", self.sd.realdevice[i])
            driver.implicitly_wait(20)
            self.driverlist.append(driver)

        print(self.driverlist)

    def tearDown(self):
        # quite the device driver
        # pass
        logger.info('用例运行完毕')
        for driver in self.driverlist:
            driver.close_app()
            driver.quit()

    def test_001_A50参与者多次加入离开房间(self):
        logger.info('test_001_A50参与者多次加入离开房间')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(app_behavior.startpusha50, (driver, self.device_name[index], ))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()

    def test_002_A50启推流杀进程(self):
        logger.info('test_002_A50启推流杀进程')
        driver = self.driverlist[0]
        caps = driver.desired_capabilities
        appid = caps['bundleId']
        elementinfo, deviceid = pubfuc.getiteminfo(caps, 'A50')
        num = 1
        while True:
            isdown = driver.find_element_by_xpath(elementinfo['uploadlog']['xpath']).is_displayed()
            if "稍后提醒我" in driver.page_source:
                driver.find_element_by_xpath("//XCUIElementTypeButton[@name='稍后提醒我']").click()
            elif "稍后" in driver.page_source:
                driver.find_element_by_xpath("//XCUIElementTypeButton[@name='稍后']").click()
            while not isdown:
                driver.execute_script("mobile: dragFromToForDuration",
                                      {'fromX': 10, 'fromY': 300, 'toX': 10, 'toY': 50, 'duration': 1})
                isdown = driver.find_element_by_xpath(elementinfo['uploadlog']['xpath']).is_displayed()

            logger.info(f"第{num}次开始推流")
            print(f"第{num}次开始推流")
            driver.find_element_by_id('START').click()
            sleep(10)

            driver.find_element_by_xpath("//XCUIElementTypeButton[@name='稍后']").click()

            driver.terminate_app(appid)
            sleep(5)
            driver.activate_app(appid)
            sleep(5)
            num += 1
            if num > 301:
                break