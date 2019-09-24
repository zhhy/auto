# -*- coding:utf-8 -*-
# import re
# sys.path.append('..')

from time import sleep
import unittest
import lib.public_functions as pubfuc
import multiprocessing
from appium import webdriver
import testcase.QSStarlight_behavior as QSStarlight_behavior
import logging

logger = logging.getLogger('autolog')


class QSStarlightTest(unittest.TestCase):

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
                desire_caps['bundleId'] = 'com.powerinfo.iLiveQSStarLight'  # bootstrapA50
                # desire_caps['waitForQuiescence'] = 'false'
            else:
                desire_caps['appPackage'] = 'com.powerinfo.iLiveQSStarLight'
                desire_caps['appActivity'] = 'com.powerinfo.iLiveQSStarLight.StarLightLoginSettingActivity'
            driver = webdriver.Remote(f"http://localhost:{self.sd.aport[i]}/wd/hub", self.sd.realdevice[i])
            self.driverlist.append(driver)

        logger.info(self.driverlist)

    def test_001参与者多次加入离开房间(self):
        logger.info('test_001参与者多次加入离开房间')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(QSStarlight_behavior.joinandleaveroom, (driver, self.roomid, self.device_name[index], ))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()

    def test_002参与者多次切后台(self):
        logger.info('test_003参与者多次切后台')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(QSStarlight_behavior.backapp, (driver, self.roomid, self.device_name[index], ))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()

    def test_004多次切换摄像头(self):
        logger.info('test_007多次切换摄像头')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(QSStarlight_behavior.switchcamera, (driver, self.roomid, self.device_name[index],))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()

    def test_005参与者多次锁屏(self):
        logger.info('test_004参与者多次创建房间')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(QSStarlight_behavior.lockscreen, (driver, self.roomid, self.device_name[index], ))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()

    def test_006参与者切后台(self):
        logger.info('test_006参与者切后台')
        driver_zhubo, driver_fubo = self.driverlist[0], self.driverlist[1]
        devicedriverinfo = driver_zhubo.desired_capabilities  # 获取正在运行的设备的参数设置
        elementinfo, deviceid = pubfuc.getiteminfo(devicedriverinfo, 'bootstrap')
        QSStarlight_behavior.startnewroom(driver_zhubo, elementinfo)
        size = driver_fubo.get_window_size()
        print(size)
        if 'desired' not in driver_fubo.desired_capabilities:
            driver_fubo.execute_script("mobile: dragFromToForDuration",
                                  {'fromX': 100, 'fromY': size['height'] / 2, 'toX': 100,
                                   'toY': size['height'] - 100, 'duration': 2})
            print(2)
        else:
            driver_fubo.swipe(30, size['height'] / 2, 30, size['height'] - 100, 200)
        page_info = driver_fubo.page_source
        print(page_info)
        import re
        room_id = re.findall('RoomI.+name=', page_info)
        print(room_id)
        # room_id = '1'
        # a50_behavior.backapp(driver_fubo, self.roomid, self.device_name[1])

    def tearDown(self):
        logger.info('test运行完成')
        # quite the device driver
        # pass
        for driver in self.driverlist:
            driver.quit()
        # for proc in self.proc_list:
            # print(proc.is_alive())
            # proc.terminate()
