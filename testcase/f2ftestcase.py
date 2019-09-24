# -*- coding:utf-8 -*-

from time import sleep
import unittest
import lib.public_functions as pubfuc
import multiprocessing
from appium import webdriver
import testcase.f2f_behavior as f2f_behavior
import logging
from appium.webdriver.common.touch_action import TouchAction

logger = logging.getLogger('autolog')


class f2fTest(unittest.TestCase):

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
            if 'bundleId' in desire_caps:
                desire_caps['bundleId'] = 'net.powerinfo.face2face'
                desire_caps['waitForQuiescence'] = 'false'
            else:
                desire_caps['appPackage'] = 'net.powerinfo.face2face'
                desire_caps['appActivity'] = 'net.powerinfo.face2face.MainActivity'
            print(desire_caps)
            driver = webdriver.Remote(f"http://localhost:{self.sd.aport[i]}/wd/hub", desire_caps)
            print(driver)
            # driver.implicitly_wait(20)
            self.driverlist.append(driver)

        print(self.driverlist)

    def test_001_f2f多次召开会议(self):
        logger.info('test_001参与者多次加入离开房间')
        print('111')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(f2f_behavior.startpushf2f, (driver, self.device_name[index], ))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()

    def test_002_f2f多次加入离开会议(self):
        logger.info('test_001参与者多次加入离开房间')
        print('111')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(f2f_behavior.joinroomf2f, (driver, self.device_name[index],))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()


    def test_003_f2f多次切后台(self):
        logger.info('test_001参与者多次加入离开房间')
        print('111')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(f2f_behavior.f2fbackapp, (driver, self.device_name[index],))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()


    def test_004_f2f多次锁屏(self):
        logger.info('test_001参与者多次加入离开房间')
        print('111')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(f2f_behavior.f2flockscreen, (driver, self.device_name[index],))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()




    def test_005_f2f多次开Siri(self):
        logger.info('test_001参与者多次加入离开房间')
        print('111')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(f2f_behavior.f2fPushSiri, (driver, self.device_name[index],))
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