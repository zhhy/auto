# -*- coding:utf-8 -*-

import os
from pathlib import Path
import re
import subprocess
import platform

# print(platform.platform())

# 获取当前目录
# print(os.getcwd())
# print(os.path.abspath(os.path.dirname(__file__)))
# print(Path.cwd())

# 获取上级目录
# print(os.name)

# print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
# print(os.path.abspath(os.path.dirname(os.getcwd())))
# print(os.path.abspath(os.path.join(os.getcwd(),'..')))

# fn = Path(__file__)
# print(fn.name)
# print(fn.suffix)
# print(fn.stem)
#
# print(Path(__file__).cwd().parent)

# p = subprocess.getoutput('adb devices')
# print(p)
# print(p.split('\n')[1].split("\t")[0])
# print(re.findall(r'^\w*\b', p.split('\n')[1])[0])

# import sys

# sys.path.append("..")

# from lib.public_functions import get_android_app_info
# import lib.public_functions as f

# info = get_android_app_info('liveme')

# print(info)

# filepath = Path(__file__).cwd().parent / 'app控件.yml'

# print(filepath)

# import yaml
#
# with open(filepath, 'r', encoding='gbk') as fs:
#     info = yaml.load(fs)
#
# print(info)
# print(info['liveme']['开播'])

# from multiprocessing import Process,Pool
# import subprocess
# import time
#
# def startAppiumServer(aport,bport,udid):
#     print()
#     cmd_base = "node /Applications/Appium.app/Contents/Resources/app/node_modules/appium/build/lib/main.js -a 127.0.0.1 --local-timezone"
#     cmd = cmd_base + f" -p {aport}"+ f" -bp {bport}"+ f" -U {udid} > /Users/liminglei/Desktop/appium/appiumlog.txt"
#     subprocess.Popen(cmd,shell=True)
#
#
# proc = Process(target=startAppiumServer,args=(4723,4724,"VGT7N17811000107",))
#
# proc.start()
# proc.join()
# # time.sleep(15)
# proc.terminate()




def add(a, b):
    return a+b

def minus(a, b):
    return a-b

def multi(a, b):
    return a*b

def divide(a, b):
    return a/b

import unittest
import logging
logging.basicConfig(level=logging.DEBUG,
                    filename= '1.txt',
                    filemode= 'w'
                    )

def t1(cls):
    cls.assertTrue(False,'this is failed')


class TestMathFunc(unittest.TestCase):
    """Test mathfuc.py"""


    def test_add(self):
        """Test method add(a, b)"""
        t1(self)
        self.assertEqual(3, add(1, 2))
        self.assertNotEqual(3, add(2, 2))

    def test_minus(self):
        """Test method minus(a, b)"""
        self.assertEqual(1, minus(3, 2))

    def test_multi(self):
        """Test method multi(a, b)"""
        self.assertEqual(6, multi(2, 3))

    def test_divide(self):
        """Test method divide(a, b)"""
        self.assertEqual(2, divide(6, 3))
        self.assertEqual(2.5, divide(5, 2))


a = "//android.widget.TextView[@text='RoomID :5582']"
print(re.findall('Room\w+',a)[0])


