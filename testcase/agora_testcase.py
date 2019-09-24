# -*- coding:utf-8 -*-
import sys,re,subprocess
sys.path.append('..')

from time import sleep
import unittest
import lib.public_functions as pubfuc
import multiprocessing
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction


def 加入离开房间(driver,roomid):
    print(driver.desired_capabilities)
    devicedriverinfo = driver.desired_capabilities
    sleep(5)
    num = 1
    print(driver.page_source)
    while num < 301:
        if num == 1:
            driver.find_element_by_xpath('//android.widget.EditText[@text="会议室名称"]').send_keys(roomid)
            sleep(2)
        print(f"第{num}次{driver}加入离开房间")
        # io.agora.vcall:id/encryption_key
        # pubfuc.waittimeout(driver.find_element_by_id(控件信息['JOIN']['id']))
        if not driver.find_element_by_xpath('//android.widget.Button[@text="加入"]').get_attribute('enabled'):
            sleep(3)
        driver.find_element_by_xpath('//android.widget.Button[@text="加入"]').click()
        sleep(10)
        if driver.find_element_by_xpath("//android.widget.ImageView[@content-desc='END_CALL']") is None:
            driver.tap([100,100])
            sleep(2)
        driver.find_element_by_xpath("//android.widget.ImageView[@content-desc='END_CALL']").click()
        sleep(2)
        num += 1


class AgoraTest(unittest.TestCase):

    def setUp(self):
        # self.控件信息 = pubfuc.getymlfileinfo()['zego_Android']
        #第一个为主播
        devicelist = ['RedMI']


        self.sd = pubfuc.StartDriver(devicelist)

        self.proc_list = []
        是否mac = 'mac' in pubfuc.getcurretsystem()

        pubfuc.cleannodeproc()
        for i in range(len(self.sd.devicelist)):
            self.proc_list.append(multiprocessing.Process(target=self.sd.startappiumserver, args=(i,)))

        # print(self.proc_list)

        for pro in self.proc_list:
            pro.start()

        for pro in self.proc_list:
            pro.join()

        while len(self.sd.getnodeprocpid()) < len(devicelist):
            sleep(1)


        print(self.sd.getnodeprocpid())

        self.driverlist = []
        for i in range(len(self.sd.devicelist)):
            desire_caps = self.sd.realdevice[i]
            desire_caps['appPackage'] = 'io.agora.vcall'
            desire_caps['appActivity'] = 'io.agora.vcall.ui.SplashActivity'
            driver = webdriver.Remote(f"http://localhost:{self.sd.aport[i]}/wd/hub", desire_caps)
            self.driverlist.append(driver)
            driver.page_source
        print(self.driverlist)

    def test_001参与者多次加入离开房间(self):
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            proc = pool.apply_async(加入离开房间,(driver,'qq',))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()

    def tearDown(self):
        # quite the device driver
        for driver in self.driverlist:
            driver.quit()
        for proc in self.proc_list:
            print(proc.is_alive())
            proc.terminate()
            # proc.kill()
        #clean the node process,appium server is started by node
        pubfuc.cleannodeproc()





