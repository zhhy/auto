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

class IRoomLeakTest(unittest.TestCase):

    def setUp(self):
        # 在当前目录，新建mail.txt，文件第一行存放设备列表，第二行存放roomid
        with open('mail.txt', 'r') as f:
            info = f.readlines()
        devicelist = info[0].rstrip().split(',')
        logger.info(devicelist)
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
            desire_caps['appPackage'] = 'com.sjdd.testleakdemo'
            desire_caps['appActivity'] = 'com.sjdd.testleakdemo.MainActivity'
            driver = webdriver.Remote(f"http://localhost:{self.sd.aport[i]}/wd/hub", self.sd.realdevice[i])
            self.driverlist.append(driver)

        logger.info(self.driverlist)

    def test_001参与者多次加入只推流(self):
        logger.info('test_001参与者多次加入只推流 正在运行')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            i = self.driverlist.index(driver)
            proc = pool.apply_async(app_behavior.startpushstream, (driver, i,))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()

    def test_002参与者多次只开预览(self):
        logger.info('test_002参与者多次只开预览 正在运行')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            i = self.driverlist.index(driver)
            proc = pool.apply_async(app_behavior.startpushstream, (driver, i, False))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()

    def test_03参与者不断切换角色(self):
        logger.info('test_03参与者不断切换角色')
        app_behavior.onechangerole(self.driverlist[0],self.driverlist[1])

    def test_04只收流(self):
        logger.info('test_04参与者辅播不断切换角色')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            proc = pool.apply_async(app_behavior.onlyreceive, (driver,))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()

    def tearDown(self):
        # quite the device driver
        # pass
        logger.info('用例运行完毕')
        for driver in self.driverlist:
            driver.close_app()
            driver.quit()
        for proc in self.proc_list:
            # print(proc.is_alive())
            proc.terminate()
