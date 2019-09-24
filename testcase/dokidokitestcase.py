# -*- coding:utf-8 -*-
# import re
# sys.path.append('..')

from time import sleep
import unittest
import lib.public_functions as pubfuc
import multiprocessing
from appium import webdriver
import testcase.dokidokibehavior as dokidokibehavior
import logging

logger = logging.getLogger('autolog')


class dokidokiTest(unittest.TestCase):

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
                desire_caps['bundleId'] = 'net.imusic.android.dokidoki'
                # desire_caps['waitForQuiescence'] = 'false'
            else:
                desire_caps['appPackage'] = 'net.imusic.android.dokidoki'
                desire_caps['appActivity'] = 'net.imusic.android.dokidoki.page.main.MainActivity'
            driver = webdriver.Remote(f"http://localhost:{self.sd.aport[i]}/wd/hub", self.sd.realdevice[i])

            self.driverlist.append(driver)

        logger.info(self.driverlist)

    def test_001参与者多次加入离开房间(self):
        logger.info('test_001参与者多次加入离开房间')
        fail_count = 5  # 用例中出错后重新执行的次数
        run_count = 1
        success_flag = True
        num = 1
        procs = []
        driver = self.driverlist[0]
        driver.find_element_by_id("net.imusic.android.dokidoki:id/img_me").click()   #me界面
        sleep(2)
        driver.find_element_by_id("net.imusic.android.dokidoki:id/ll_follow_container").click()   #关注界面
        sleep(10)
        driver.tap([[600, 150]])
        sleep(10)
        while success_flag:
            try:
                if run_count > fail_count:
                    break
                while num < 1001:
                    if num % 10 == 0:
                        logger.info(f"第{num}次{self.device_name}加入房间")
                    driver.find_element_by_id("net.imusic.android.dokidoki:id/btn_live").click()
                    sleep(15)
                    driver.tap([[1000, 150]])
                    sleep(5)
                    num += 1
                break
            except Exception as e:
                logger.error(f'第{num}次运行出错，设备是:{self.device_name}')
                # print(driver.page_source)
                img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{pubfuc.getlocaltime()}-{self.device_name}.png')
                driver.save_screenshot(str(img_file))
                sleep(3)
                logger.error(e.args[0], exc_info=True)
                if not success_flag:
                    return
                logger.info(f'第{run_count}次重跑')
                run_count += 1
                driver.close_app()
                driver.launch_app()
                driver.find_element_by_id("net.imusic.android.dokidoki:id/img_me").click()   #me界面
                sleep(2)
                driver.find_element_by_id("net.imusic.android.dokidoki:id/ll_follow_container").click()   #关注界面
                sleep(10)
                driver.tap([[600, 150]])
                sleep(10)

    def test_002参与者多次PK(self):
        logger.info('test_002参与者多次PK')
        fail_count = 10  # 用例中出错后重新执行的次数
        run_count = 1
        success_flag = True
        num = 1
        driverA = self.driverlist[0]
        driverB = self.driverlist[1]
        sleep(10)
        driverA.implicitly_wait(4)
        while success_flag:
            try:
                if run_count > fail_count:
                    break
                dokidokibehavior.create_doki_room(driverA)
                dokidokibehavior.create_doki_room(driverB)
                sleep(10)
                while num < 1001:
                    logger.info(f"第{num}次进行pk")
                    driverA.find_element_by_id("net.imusic.android.dokidoki:id/btn_interaction").click()
                    sleep(4)
                    driverA.find_element_by_id("net.imusic.android.dokidoki:id/ll_pk").click()
                    sleep(4)
                    driverA.find_element_by_id("net.imusic.android.dokidoki:id/rl_friends").click()
                    sleep(4)
                    driverA.find_element_by_id("net.imusic.android.dokidoki:id/tv_invite").click()
                    sleep(5)
                    driverB.find_element_by_id("net.imusic.android.dokidoki:id/tv_accept").click()
                    sleep(10)
                    driverA.tap([[550, 1050]], duration=100)
                    driverB.tap([[550, 1050]])
                    sleep(4)
                    driverA.tap([[940, 940]])
                    driverB.tap([[940, 940]])
                    sleep(10)
                    driverB.find_element_by_id("net.imusic.android.dokidoki:id/tv_end_pk").click()  #结束PK
                    sleep(2)
                    driverB.find_element_by_id("net.imusic.android.dokidoki:id/tv_right").click()
                    sleep(10)
                    driverA.tap([[550, 1050]], duration=100)
                    driverB.tap([[550, 1050]])
                    sleep(4)
                    driverA.tap([[940, 940]])
                    driverB.tap([[940, 940]])
                    sleep(10)
                    num += 1
                break
            except Exception as e:
                logger.error(f'第{num}次运行出错，设备是:{self.device_name}')
                img_file_A = pubfuc.get_real_dir_path(__file__,
                                                      f'../testresult/{pubfuc.getlocaltime()}-{self.device_name[0]}.png')
                driverA.save_screenshot(str(img_file_A))
                img_file_B = pubfuc.get_real_dir_path(__file__,
                                                      f'../testresult/{pubfuc.getlocaltime()}-{self.device_name[1]}.png')
                driverB.save_screenshot(str(img_file_B))
                sleep(3)
                logger.error(e.args[0], exc_info=True)
                if not success_flag:
                    return
                logger.info(f'第{run_count}次重跑')
                run_count += 1
                driverA.close_app()
                driverA.launch_app()
                driverB.close_app()
                driverB.launch_app()




    def tearDown(self):
        logger.info('test运行完成')
        # quite the device driver
        # pass
        for driver in self.driverlist:
            driver.quit()
        # for proc in self.proc_list:
            # print(proc.is_alive())
            # proc.terminate()


