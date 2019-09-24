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
    控件文件 = pubfuc.getymlfileinfo()
    print(driver.desired_capabilities)
    devicedriverinfo = driver.desired_capabilities
    isIOS = 'desired' not in devicedriverinfo
    num = 1
    while num < 301:
        if num == 1:
            driver.find_element_by_id('com.zego.videotalk:id/sessionid_edittext').send_keys(roomid)
            sleep(2)
        print(f"第{num}次{driver}joinandleaveroom")
        # pubfuc.waittimeout(driver.find_element_by_id(控件信息['JOIN']['id']))
        if not driver.find_element_by_id('com.zego.videotalk:id/start_button').get_attribute('enabled'):
            sleep(3)
        driver.find_element_by_id('com.zego.videotalk:id/start_button').click()
        sleep(10)
        driver.find_element_by_id('com.zego.videotalk:id/vt_btn_close').click()
        sleep(3)
        driver.find_element_by_xpath("//android.widget.Button[@text='离开']").click()
        sleep(2)
        num += 1

def 切换角色(driver,roomid):
    控件文件 = pubfuc.getymlfileinfo()
    print(driver.desired_capabilities)
    devicedriverinfo = driver.desired_capabilities
    isIOS = 'desired' not in devicedriverinfo
    if isIOS:
        控件信息 = 控件文件['iRoom_{}'.format(devicedriverinfo['platformName'])]
    else:
        控件信息 = 控件文件['iRoom_{}'.format(devicedriverinfo['desired']['platformName'])]
    #click 多人群聊
    driver.find_element_by_xpath(控件信息['多人群聊']['xpath']).click()
    sleep(3)
    roomid = f' {roomid}' if isIOS else roomid
    roomxpath = re.sub("xxxx", roomid, 控件信息['房间列表']['xpath'])
    pubfuc.waittimeout(driver.find_element_by_xpath(roomxpath))
    # click 房间
    driver.find_element_by_xpath(roomxpath).click()
    # pubfuc.waittimeout(driver.find_element_by_id(控件信息['JOIN']['id']))
    sleep(5)
    if not driver.find_element_by_id(控件信息['JOIN']['id']).get_attribute('enabled'):
        sleep(3)
    driver.find_element_by_id(控件信息['JOIN']['id']).click()
    sleep(10)
    num = 1
    while num < 301:
        print(f"第{num}次{driver}changerole")
        print(driver.find_element_by_id(控件信息['changerole']['id']).get_attribute('enabled'))
        driver.find_element_by_id(控件信息['changerole']['id']).click()
        sleep(6)
        num += 1

def 切后台(driver,roomid):
    控件文件 = pubfuc.getymlfileinfo()
    print(driver.desired_capabilities)
    print(driver.capabilities)
    devicedriverinfo = driver.desired_capabilities
    isIOS = 'desired' not in devicedriverinfo
    if isIOS:
        控件信息 = 控件文件['iRoom_{}'.format(devicedriverinfo['platformName'])]
        return
    else:
        控件信息 = 控件文件['iRoom_{}'.format(devicedriverinfo['desired']['platformName'])]
    #click 多人群聊
    driver.find_element_by_xpath(控件信息['多人群聊']['xpath']).click()
    sleep(3)
    roomid = f' {roomid}' if isIOS else roomid
    roomxpath = re.sub("xxxx", roomid, 控件信息['房间列表']['xpath'])
    pubfuc.waittimeout(driver.find_element_by_xpath(roomxpath))
    # click 房间
    driver.find_element_by_xpath(roomxpath).click()
    # pubfuc.waittimeout(driver.find_element_by_id(控件信息['JOIN']['id']))
    sleep(5)
    if not driver.find_element_by_id(控件信息['JOIN']['id']).get_attribute('enabled'):
        sleep(3)
    driver.find_element_by_id(控件信息['JOIN']['id']).click()
    sleep(10)
    num = 1
    while num < 301:
        print(f"第{num}次{driver}backapp")
        driver.background_app(5)
        sleep(5)
        #切后台回来后，查看离开房间按钮是否可用，确定正确切回了前台
        print(driver.find_element_by_id(控件信息['离开房间']['id']).get_attribute('enabled'))
        num += 1


class zegoTest(unittest.TestCase):

    def setUp(self):
        self.控件信息 = pubfuc.getymlfileinfo()['zego_Android']
        #第一个为主播
        devicelist = ['p6']


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
            desire_caps['appPackage'] = 'com.zego.videotalk'
            desire_caps['appActivity'] = 'com.zego.videotalk.MainActivity'
            driver = webdriver.Remote(f"http://localhost:{self.sd.aport[i]}/wd/hub", desire_caps)
            self.driverlist.append(driver)
            driver.page_source
        print(self.driverlist)

    def test_001参与者多次加入离开房间(self):
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            proc = pool.apply_async(加入离开房间,(driver,'234',))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()



    def test_002参与者多次切回角色(self):
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            proc = pool.apply_async(切换角色, (driver, '4678',))
            procs.append(proc)
        for i in procs:
            i.get()
        for i in procs:
            i.wait()


    def test_003参与者多次切后台(self):
        procs = []
        pool = multiprocessing.Pool(processes=len(self.driverlist))
        for driver in self.driverlist:
            proc = pool.apply_async(切后台, (driver, '4625',))
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





