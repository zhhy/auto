# -*- coding:utf-8 -*-

from time import sleep
import lib.public_functions as pubfuc
from pathlib import Path
import re
import subprocess
import logging

logger = logging.getLogger('autolog')


def joinandpk(driver):
    print(1)
    driver.find_element_by_id("net.imusic.android.dokidoki:id/btn_live").click()
    sleep(2)
    driver.find_element_by_id("net.imusic.android.dokidoki:id/live_icon").click()
    sleep(2)
    driver.find_element_by_id("net.imusic.android.dokidoki:id/btn_live").click()
    sleep(5)
    driver.find_element_by_id("net.imusic.android.dokidoki:id/btn_live").click()
    sleep(2)
    driver.find_element_by_id("net.imusic.android.dokidoki:id/ll_pk").click()
    sleep(2)
    driver.find_element_by_id("net.imusic.android.dokidoki:id/ll_pk").click()
    sleep(2)
    driver.find_element_by_id("net.imusic.android.dokidoki:id/rl_friends").click()
    sleep(2)
    driver.find_element_by_id("net.imusic.android.dokidoki:id/tv_invite").click()
    sleep(5)
    driver.find_element_by_id("net.imusic.android.dokidoki:id/tv_accept").click()
    sleep(10)
    #driver.find_element_by_id(  ).click()  #结束PK
    sleep(2)
    driver.find_element_by_id("net.imusic.android.dokidoki:id/tv_right").click()
    sleep(5)
    driver.find_element_by_id("net.imusic.android.dokidoki:id/btn_close").click()
    sleep(2)
    driver.find_element_by_id("android:id/button1").click()
    sleep(2)
    driver.find_element_by_id("net.imusic.android.dokidoki:id/btn_close").click()
    sleep(5)


def create_doki_room(driver):
    driver.find_element_by_id("net.imusic.android.dokidoki:id/img_me").click()  # me界面
    sleep(2)
    driver.find_element_by_id("net.imusic.android.dokidoki:id/btn_live").click()
    sleep(4)
    driver.find_element_by_id("net.imusic.android.dokidoki:id/live_icon").click()
    sleep(4)
    driver.find_element_by_id("net.imusic.android.dokidoki:id/btn_live").click()
    sleep(10)