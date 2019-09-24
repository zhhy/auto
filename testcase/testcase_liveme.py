# -*- coding:utf-8 -*-
import sys
sys.path.append('..')

from time import sleep
import unittest
import lib.public_functions as pubfuc
from appium import webdriver

class Liveme(unittest.TestCase):

    def setUp(self):
        self.info = pubfuc.get_android_app_info()
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.info)
        self.id = f"{self.info['appPackage']}:id/{functionid}"


    def test_001_开播(self):
        #开播
        self.driver.find_element_by_id(f"{self.info['appPackage']}:id/uplive").click()
        sleep(1)
        #选择多人直播
        self.driver.find_element_by_id(f"{self.info['appPackage']}:id/live_multi_layout").click()
        #点击开播
        self.driver.find_element_by_id(f"{self.info['appPackage']}:id/txt_video_start_live").click()
        sleep(5)
        self.driver.find_element_by_id(f"{self.info['appPackage']}:id/shortid_iv").get_attribute('text')