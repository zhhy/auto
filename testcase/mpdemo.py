# -*- coding:utf-8 -*-

from time import sleep
import unittest
import lib.public_functions as pubfuc
import multiprocessing
from appium import webdriver
import testcase.app_behavior as app_behavior
import logging

logger = logging.getLogger('autolog')


class MPdemotest(unittest.TestCase):

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

            desire_caps['appPackage'] = 'com.powerinfo.demo.mpdemo'
            desire_caps['appActivity'] = 'com.powerinfo.demo.mpdemo.SettingActivity'

            driver = webdriver.Remote(f"http://localhost:{self.sd.aport[i]}/wd/hub", self.sd.realdevice[i])
            driver.implicitly_wait(20)
            self.driverlist.append(driver)

        print(self.driverlist)

    def test_001_mpdemo参与者多次加入离开房间(self):
        logger.info('test_001_mpdemo参与者多次加入离开房间')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(app_behavior.startmpdemo, (driver, self.device_name[index], ))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()

    def tearDown(self):
        # quite the device driver
        pass
        # logger.info('用例运行完毕')
        # for driver in self.driverlist:
        #     driver.close_app()
        #     driver.quit()
        # for proc in self.proc_list:
        #     print(proc.is_alive())
            # proc.terminate()
