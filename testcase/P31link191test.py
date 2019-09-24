# -*- coding:utf-8 -*-

from time import sleep
import unittest
import lib.public_functions as pubfuc
import multiprocessing
from appium import webdriver
import testcase.app_behavior as app_behavior
import logging

logger = logging.getLogger('autolog')


class P31linkTest(unittest.TestCase):

    def setUp(self):
        with open('mail.txt', 'r') as f:
            info = f.readlines()
        devicelist = info[0].rstrip().split(',')
        logger.info(f'devicelist: {devicelist}')
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

            # desire_caps['bundleId'] = 'com.powerinfo.P31-Link'
            desire_caps['bundleId'] = 'com.powerinfo.P31-LinkSVC'

            driver = webdriver.Remote(f"http://localhost:{self.sd.aport[i]}/wd/hub", self.sd.realdevice[i])
            driver.implicitly_wait(20)
            self.driverlist.append(driver)

        print(self.driverlist)

    def test_001_p31link参与者多次加入离开房间(self):
        logger.info('test_001参与者多次加入离开房间')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            proc = pool.apply_async(app_behavior.startpushp31link191, (driver, ))
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
