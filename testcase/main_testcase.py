# -*- coding:utf-8 -*-
# import re
# sys.path.append('..')

from time import sleep
import unittest
import lib.public_functions as pubfuc
import multiprocessing
from appium import webdriver
import testcase.QSA50_behavior as a50_behavior
import testcase.app_behavior as app_behavior
import testcase.classification as classification
import logging

logger = logging.getLogger('autolog')


class MainTest(unittest.TestCase):

    def setUp(self):
        # 在当前目录，新建mail.txt，文件第一行存放设备列表，第二行存放roomid
        with open('mail.txt', 'r') as f:
            info = f.readlines()
        devicelist = info[0].rstrip().split(',')
        logger.info(f'devicelist: {devicelist}')
        self.device_name = devicelist
        self.roomid = info[1].split('#')[0].rstrip()
        self.package = info[2].rstrip()
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
            packageinfo = pubfuc.getpackageinfo(desire_caps,self.package)
            if 'bundleId' in desire_caps:
                desire_caps['bundleId'] = packageinfo['bundleId']
                # desire_caps['waitForQuiescence'] = 'false'
            else:
                desire_caps['appPackage'] = packageinfo['appPackage']
                desire_caps['appActivity'] = packageinfo['appActivity']
            driver = webdriver.Remote(f"http://localhost:{self.sd.aport[i]}/wd/hub", self.sd.realdevice[i])
            self.driverlist.append(driver)

        logger.info(self.driverlist)

    def tearDown(self):
        logger.info('test运行完成')
        # quite the device driver
        # pass
        for driver in self.driverlist:
            driver.quit()
        # for proc in self.proc_list:
        # print(proc.is_alive())
        # proc.terminate()

    def test_001参与者多次加入离开房间(self):
        logger.info('test_001参与者多次加入离开房间')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(classification.joinandleaveroom, (driver, self.roomid, self.device_name[index],self.package))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()

    def test_002参与者多次切后台(self):
        logger.info('test_002参与者多次切换角色')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(classification.backapp, (driver, self.roomid, self.device_name[index],self.package))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()


    def test_003参与者多次锁屏(self):
        logger.info('test_004参与者多次创建房间')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(classification.lockscreen, (driver, self.roomid, self.device_name[index],self.package))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()


    def test_004参与者多次切换角色(self):
        logger.info('test_004参与者多次切换角色')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(classification.changerole, (driver, self.roomid, self.device_name[index],self.package))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()


    def test_005录屏直播多次进入退出(self):
        logger.info('test_005录屏直播多次进入退出')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(classification.recordhoinandleave, (driver, self.roomid, self.device_name[index],self.package))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()
    def test_006不断创建新房间(self):
        logger.info('test_005录屏直播多次进入退出')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(classification.creatroom,
                                    (driver, self.device_name[index], self.package))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()




'''       
    def test_005录屏直播多次进入退出(self):
        logger.info('test_004参与者多次切换角色')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(classification.recordhoinandleave(driver, self.roomid, self.device_name[index], self.package))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()
'''
'''
    def test_004参与者多次创建房间(self):
        logger.info('test_004参与者多次创建房间')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(app_behavior.startroom, (driver, self.device_name[index],))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()

    def test_006多次断网恢复(self):
        logger.info('test_006_pusicPK秒开')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(app_behavior.switchwifi, (driver, self.roomid, self.device_name[index],))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()

    def test_007多次切换摄像头(self):
        logger.info('test_007多次切换摄像头')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(app_behavior.switchcamera, (driver, self.roomid, self.device_name[index],))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()

    def test_008参与者多次锁屏(self):
        logger.info('test_004参与者多次创建房间')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(app_behavior.lockscreen, (driver, self.roomid, self.device_name[index],))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()

    def test_009多次pk(self):
        logger.info('test_004参与者多次创建房间')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(app_behavior.startpkroomandroid, (driver, self.device_name[index], self.roomid,))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()

    def test_010pk判断收流成功(self):
        logger.info('test_004参与者多次创建房间')
        driver_A = self.driverlist[0]
        driver_B = self.driverlist[1]
        elementinfo, deviceid = pubfuc.getiteminfo(driver_A.desired_capabilities)
        if 'RoomI' not in driver_A.page_source:
            app_behavior.chooseroomtype(driver_A, elementinfo, '主播 PK')  # 选择PK
            app_behavior.startnewroom(driver_A, elementinfo)
        roomid, uid = app_behavior.getroominfo(driver_A, elementinfo)
        print(roomid, uid)
        app_behavior.startpkroomandroid_analysis(driver_B, driver_A, self.device_name[1], roomid, uid)
        driver_A.find_element_by_id(elementinfo['离开房间']['id']).click()

    def test_011游戏录屏多次切后台(self):
        logger.info('test_004参与者多次创建房间')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(app_behavior.startgameroom, (driver, self.device_name[index],))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()

    def test_012游戏录屏多次切换分辨率(self):
        logger.info('test_004参与者多次创建房间')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(app_behavior.startgameroom_changgeresolution, (driver, self.device_name[index],))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()

    def test_013纯音频连麦进出房间(self):
        logger.info('test_013纯音频连麦进出房间')
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        print(self.roomid)
        for driver in self.driverlist:
            index = self.driverlist.index(driver)
            proc = pool.apply_async(app_behavior.audiojoinroom, (driver, self.device_name[index], self.roomid))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()
'''