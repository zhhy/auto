# -*- coding:utf-8 -*-

from time import sleep
import lib.public_functions as pubfuc
from pathlib import Path
import re
import subprocess
import logging

logger = logging.getLogger('autolog')


def joinandleaveroom(driver, roomid, devicename):
    fail_count = 1  # 用例中出错后重新执行的次数
    run_count = 1
    num = 1
    device_driver_info = driver.desired_capabilities  # 获取正在运行的设备的参数设置
    elementinfo, deviceid = pubfuc.getiteminfo(device_driver_info)
    #size = driver.get_window_size()
    while True:
        try:
            driver.find_element_by_id("com.powerinfo.demo.a50_stb:id/start_btn").click()
            sleep(20)
            driver.find_element_by_id("com.powerinfo.demo.a50_stb:id/img_close").click()
            sleep(20)

        except Exception as e:
            logger.error(f'第{num}次运行出错，设备是:{devicename}')
            # print(driver.page_source)
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{pubfuc.getlocaltime()}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            if not True:
                return
            logger.info(f'第{run_count}次重跑')
            run_count += 1
            driver.close_app()
            driver.launch_app()
            #autopuloadlog(driver, device_driver_info, devicename, elementinfo)

