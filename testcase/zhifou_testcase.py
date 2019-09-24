# -*- coding:utf-8 -*-
# import re
# sys.path.append('..')

from time import sleep
import unittest
import lib.public_functions as pubfuc
import multiprocessing
from appium import webdriver
import testcase.zhifou_behavior as zhifou_behavior
import logging

logger = logging.getLogger('autolog')


class ZhifouTest(unittest.TestCase):

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
                desire_caps['bundleId'] = 'com.btxg.xvideo'  # bootstrapA50
                # desire_caps['waitForQuiescence'] = 'false'
            else:
                desire_caps['appPackage'] = 'com.bitstartlight.xvideo'
                desire_caps['appActivity'] = 'com.btxg.xvideo.features.general.SplashActivity'
            driver = webdriver.Remote(f"http://localhost:{self.sd.aport[i]}/wd/hub", self.sd.realdevice[i])
            self.driverlist.append(driver)

        logger.info(self.driverlist)

    def test_001知否加入离开房间(self):
        logger.info('test_001参与者多次加入离开房间')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(zhifou_behavior.start_match, (driver, self.device_name[index], ))
            procs.append(proc)
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



