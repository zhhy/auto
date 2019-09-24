# -*- coding:utf-8 -*-

from time import sleep
import unittest
import lib.public_functions as pubfuc
import multiprocessing
from appium import webdriver
import testcase.f2f_behavior as f2f_behavior
import logging

logger = logging.getLogger('autolog')


class ZhiMianHaoYouTest(unittest.TestCase):

    def setUp(self):
        with open('mail.txt', 'r') as f:
            info = f.readlines()
        self.device_name = info[0].rstrip().split(',')
        logger.info(f'devicelist: {self.device_name}')
        self.roomid = info[1].split('#')[0].rstrip()
        self.sd = pubfuc.StartDriver(self.device_name)
        self.proc_list = []

        pubfuc.cleannodeproc()
        for i in range(len(self.sd.devicelist)):
            self.proc_list.append(multiprocessing.Process(target=self.sd.startappiumserver, args=(i,)))

        for pro in self.proc_list:
            pro.start()

        for pro in self.proc_list:
            pro.join()

        while len(self.sd.getnodeprocpid()) < len(self.device_name):
            sleep(1)

        logger.info(self.sd.getnodeprocpid())

        self.driverlist = []

        for i in range(len(self.sd.devicelist)):
            logger.info(i)
            desire_caps = self.sd.realdevice[i]
            if 'bundleId' in desire_caps:
                desire_caps['bundleId'] = 'net.powerinfo.face2face'
                desire_caps['waitForQuiescence'] = 'false'
            else:
                desire_caps['appPackage'] = 'net.powerinfo.face2face'
                desire_caps['appActivity'] = 'net.powerinfo.face2face.MainActivity'
            driver = webdriver.Remote(f"http://localhost:{self.sd.aport[i]}/wd/hub", desire_caps)
            sleep(3)
            self.driverlist.append(driver)

        print(self.driverlist)

    def tearDown(self):
        # quite the device driver
        # pass
        logger.info('用例运行完毕')
        # for driver in self.driverlist:
        #     driver.close_app()
            # driver.quit()
        # for proc in self.proc_list:
        #     proc.terminate()

    def test_001_直面正确添加好友(self):
        logger.info('test_001_直面添加好友')
        driver = self.driverlist[0]
        # driver.find_element_by_xpath("//android.widget.TextView[@text='好友']").click()
        print(driver.page_source)

