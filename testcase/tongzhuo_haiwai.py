# -*- coding:utf-8 -*-
# import re
# sys.path.append('..')

from time import sleep
import unittest
import lib.public_functions as pubfuc
import multiprocessing
from appium import webdriver
import testcase.app_behavior as app_behavior
import logging

logger = logging.getLogger('autolog')


class TongZhuoHaiWaiTest(unittest.TestCase):

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
            desire_caps['appPackage'] = 'com.tongzhuo.tongzhuogame.international'
            desire_caps['appActivity'] = 'com.tongzhuo.tongzhuogame.international.theme.default'
            driver = webdriver.Remote(f"http://localhost:{self.sd.aport[i]}/wd/hub", desire_caps)
            self.driverlist.append(driver)

        logger.info(self.driverlist)

    def test_001同桌多次加入离开房间(self):
        logger.info('test_001同桌多次加入离开房间')
        driver_zhubo = self.driverlist[0]
        if '更新' in driver_zhubo.page_source:
            # driver_zhubo.find_element_by_xpath("//android.widget.Button[@text='确定']").click()
            driver_zhubo.back()
        app_behavior.createnewparty(driver_zhubo)

    def test_002同桌多次加入离开房间(self):
        logger.info('test_001同桌多次加入离开房间')
        driver_zhubo = self.driverlist[0]
        driver_zhubo.find_element_by_xpath("//android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout[3]").click()
        sleep(2)
        driver_zhubo.find_element_by_id("com.tongzhuo.tongzhuogame.international:id/mRightBt").click()
        sleep(3)
        driver_zhubo.tap([[700, 270]])
        sleep(2)
        driver_zhubo.find_element_by_id("com.tongzhuo.tongzhuogame.international:id/mChangeBtn").click()
        sleep(3)
        driver_zhubo.find_element_by_xpath("//android.widget.TextView[@text='Create']").click()
        sleep(20)
        print(driver_zhubo.page_source)
        # logger.info(driver_zhubo.page_source)
        driver_zhubo.find_element_by_id("com.tongzhuo.tongzhuogame.international:id/mIvExit").click()
        sleep(1)
        driver_zhubo.find_element_by_xpath("//android.widget.Button[@text='Yes']").click()
        sleep(4)


    def tearDown(self):
        logger.info('test运行完成')
        # quite the device driver
        # pass
        # for driver in self.driverlist:
        #     driver.quit()
        # for proc in self.proc_list:
            # print(proc.is_alive())
            # proc.terminate()
