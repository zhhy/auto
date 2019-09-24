# -*- coding:utf-8 -*-

from testcase.iRoom_testcase import IRoomTest
from testcase.zego_testcase import zegoTest
from testcase.liveme_testcase import LivemeTest
from testcase.P31link191test import P31linkTest
from testcase.mpdemo import MPdemotest
from testcase.tongzhuo_haiwai import TongZhuoHaiWaiTest
from testcase.QSA50_testcase import QSA50Test
from testcase.QSStarlight_testcase import QSStarlightTest
from testcase.A50_testcase import A50Test
from testcase.f2ftestcase import f2fTest
from testcase.zhifou_testcase import ZhifouTest
from testcase.zuji_testcase import ZujiTest
from testcase.huajiao_testcase import HuaJiaoTest
from zhimian.zhimian_case import ZhiMianHaoYouTest
from testcase.dokidemo_case import QSDokiDemoTest
from testcase.main_testcase   import MainTest
from testcase.STB_testcase   import StbTest

import testcase.leaktest
import unittest
# import myunittest #导入添加出错运行机制的库
import os
import lib.public_functions as pubfunc


mail_recievers = ['liml', 'douxs']


if __name__ == '__main__':
    suite = unittest.TestSuite()
    #tests = [QSStarlightTest("test_001参与者多次加入离开房间")]  # test_001参与者多次加入离开房间 test_004多次切换摄像头 test_002参与者多次切后台
    #tests = [IRoomTest("test_013纯音频连麦进出房间")]
    #tests = [ZhifouTest("test_001知否加入离开房间")]
    # tests = [ZujiTest("test_003足记播放视频")]
    # test_002足记创建加入比赛 test_001足记登录  test_003足记播放视频
    #tests = [IRoomTest("test_001参与者多次加入离开房间"), IRoomTest("test_003参与者多次切后台")]
    # , IRoomTest("test_002参与者多次切换角色"),] test_001参与者多次加入离开房间
    # , IRoomTest("test_003参与者多次切后台"), IRoomTest("test_008参与者多次锁屏")]  #, IRoomTest("test_002参与者多次切换角色"),
    #         IRoomTest("test_003参与者多次切后台"), IRoomTest("test_008参与者多次锁屏"), IRoomTest("test_007多次切换摄像头")]
    # tests =[testcase.f2ftestcase.f2fTest("test_002_f2f多次加入离开会议")]
    # tests =[] test_002参与者多次切换角色 test_001参与者多次加入离开房间 test_004参与者多次创建房间 test_003参与者多次切后台 test_008参与者多次锁屏 test_007多次切换摄像头
<<<<<<< HEAD
    tests = [MainTest("test_001参与者多次加入离开房间")]
=======
    tests = [StbTest("test_001参与者多次加入离开房间")]
>>>>>>> origin/master
    # tests = [testcase.leaktest.IRoomLeakTest('test_04只收流')]
    #tests = [QSDokiDemoTest('test_002_DokiDemo_多次加入离开房间')]  # test_001_A50参与者多次加入离开房间
    # tests = [testcase.P31link191test.P31linkTest('test_001_p31link参与者多次加入离开房间')]
    # tests = [MPdemotest("test_001_mpdemo参与者多次加入离开房间")]
    # tests = [TongZhuoHaiWaiTest('test_001同桌多次加入离开房间')]
    # tests = [ZhifouTest('test_001参与者加入离开房间')]
    # tests = [ZhiMianHaoYouTest('test_001_直面正确添加好友')]
    suite.addTests(tests)

    logger = pubfunc.setcustomlogger('autolog')  # 可以添加第二个参数False来控制打印日志到屏幕上test_001参与者多次加入离开房间

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

    result_dir = pubfunc.get_real_dir_path(__file__, '../testresult/')
    result_file = os.path.join(result_dir, 'autolog.log')

    appium_log = []
    img_list = []
    for imgfile in os.listdir(result_dir):
        if os.path.splitext(imgfile)[1] == '.png':
            img_list.append(os.path.join(result_dir, imgfile))
        elif 'appiumlog' in imgfile:
            appium_log.append(os.path.join(result_dir, imgfile))

    # pubfunc.send_mail(mail_recievers, result_file, img_list, appium_log)
