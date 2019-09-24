# -*- coding:utf-8 -*-

import subprocess
import lib.public_functions as pub_func

device_name = 'p9'
device_id = pub_func.getymlfileinfo('devices')[device_name]['deviceName']
# cmd = f'adb -s {device_id} logcat -v threadtime -b all > {device_name}.txt'
# subprocess.check_call(cmd, shell=True)
test_package = 'com.powerinfo.bootstrapA50'

cmd_monkey = f"adb -s {device_id} shell monkey -v -v -v --throttle 300 --pct-touch 30 --pct-motion 20 --pct-nav 20 " \
             f"--pct-majornav 15 --pct-appswitch 5 --pct-anyevent 5 --pct-trackball 0 --pct-syskeys 0 " \
             f"-p {test_package} 30000 > monkey3.txt"

print(cmd_monkey)
# 测试之前执行logcat
subprocess.call(cmd_monkey, shell=True)

