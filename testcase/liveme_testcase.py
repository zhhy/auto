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


class LivemeTest(unittest.TestCase):

    def setUp(self):
        # 在当前目录，新建mail.txt，文件第一行存放设备列表，第二行存放roomid
        with open('mail.txt', 'r') as f:
            info = f.readlines()
        devicelist = info[0].rstrip().split(',')
        logger.info(f'devidelist: {devicelist}')
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
                desire_caps['bundleId'] = 'com.cmcm.live'
            else:
                desire_caps['appPackage'] = 'com.cmcm.live'
                desire_caps['appActivity'] = 'com.cmcm.cmlive.activity.SplashActivity'
            driver = webdriver.Remote(f"http://localhost:{self.sd.aport[i]}/wd/hub", self.sd.realdevice[i])
            driver.implicitly_wait(20)
            self.driverlist.append(driver)

        print(self.driverlist)

    def test_001参与者多次加入离开房间(self):
        # procs = []
        # pool = multiprocessing.Pool(processes=len(self.driverlist))
        app_behavior.startlivemeroom(self.driverlist[0], self.device_name[0])
        for driver in self.driverlist[1::]:
            index = self.driverlist.index(driver)
            print(self.device_name[index])
            app_behavior.joinlivemeroom(driver, self.device_name[index])


            # app_behavior.startlivemeroom(driver, self.device_name[index])
            # logger.info(driver.page_source)
        #     proc = pool.apply_async(app_behavior.startlivemeroom, (driver,))
        #     procs.append(proc)
        # for i in procs:
        #     i.get()
        # for i in procs:
        #     i.wait()

    def tearDown(self):
        logger.info('test运行完成')
        for driver in self.driverlist:
            driver.quit()
        for proc in self.proc_list:
            proc.terminate()
