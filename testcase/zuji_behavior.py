# -*- coding:utf-8 -*-

from time import sleep
import lib.public_functions as pubfuc
from appium.webdriver.common.touch_action import TouchAction
import logging

logger = logging.getLogger('autolog')

# ios 控件
# 开始比赛：


def backiosapp(driver, size, appid, time=5):
    x = size['width'] - 30
    y = size['height'] - 30
    driver.tap([[x, y]])  # iphone辅助功能按键放置在右下角
    sleep(2)
    x = size['width'] / 2
    y = size['height'] - 138
    driver.tap([[x, y]])
    sleep(time)
    driver.activate_app(appid)


# 退出登陆
def logout(driver):
    driver.find_element_by_xpath("//android.widget.TextView[@text='我的']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='设置']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='退出登录']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.Button[@text='确定']").click()


# 未登录状态功能测试
def logout_status(driver):
    while True:
        driver.find_element_by_xpath("//android.widget.TextView[@text='比赛']").click()
        sleep(1)
        driver.find_element_by_xpath("//android.widget.TextView[@text='全部']").click()
        sleep(1)
        var = driver.find_element_by_xpath("//android.widget.ScrollView").text
        if var != "没有比赛":
            break
        driver.find_element_by_xpath("//android.widget.TextView[@text='个人']").click()
        sleep(1)
        var = driver.find_element_by_xpath("//android.widget.ScrollView").text
        if var != "没有比赛":
            break


# 手机号登陆
def loginbyphonenumber(driver):
    driver.find_element_by_xpath("//android.widget.EditText[@text='请输入手机号']").send_keys('17612296741')
    driver.find_element_by_xpath("//android.widget.EditText[@text='请输入密码']").send_keys('sjdd1234')
    driver.tap([[200, 200]])  # 点击空白处返回按钮
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='登录']").click()
    # s1 = driver.find_element_by_xpath("//android.widget.TextView[@text='微信']").size
    # s2 = driver.find_element_by_xpath("//android.widget.TextView[@text='微信']").location
    # driver.tap([[s2['x']+50, s2['y']-60]])
    # driver.find_element_by_xpath("//android.widget.ViewGroup/android.widget.ViewGroup").click()
    sleep(3)
    driver.find_element_by_xpath("//android.widget.TextView[@text='登录成功']")
    driver.find_element_by_xpath("//android.widget.Button[@text='OK']").click()


# 登陆退出功能测试
def login_logout_test(driver, devicename):
    failcount = 3  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    elementinfo, deviceid = pubfuc.getiteminfo(driver.desired_capabilities, 'zuji')
    while True:
        try:
            if runcount > failcount:
                break
            sleep(3)
            driver.find_element_by_xpath(elementinfo['我的']['xpath']).click()
            sleep(1)
            if '请登录' in driver.page_source:
                driver.find_element_by_xpath("//android.widget.TextView[@text='请登录']").click()
            else:
                logout(driver)
            while num < 501:
                logger.info(f'第{num}次登录')
                sleep(2)
                loginbyphonenumber(driver)
                sleep(2)
                driver.tap([[200, 200]])
                logout(driver)
                num += 1
            sleep(2)
            # 为保证接下来用例正常运行，测试完登录功能后登录账户
            loginbyphonenumber(driver)
            break
        except Exception as e:
            logger.info(f'第{num}次运行出错，设备是:{devicename}')
            err_time = pubfuc.getlocaltime()
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{err_time}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            driver.close_app()
            driver.launch_app()
            logger.info(pubfuc.getlocaltime())
            sleep(20)


# 创建球队比赛
def create_team_game(driver, elementinfo):
    driver.find_element_by_xpath(elementinfo['加号']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['创建比赛']['xpath']).click()
    sleep(3)
    driver.find_element_by_xpath("//android.widget.TextView[@text='1']").click()
    sleep(0.5)
    driver.find_element_by_xpath("//android.widget.TextView[@text='下一步']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='下一步']").click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['拍摄']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='确定']").click()
    sleep(1)


# 创建个人比赛
def create_personal_game(driver, elementinfo):
    driver.find_element_by_xpath(elementinfo['加号']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['创建比赛']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='下一步']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='下一步']").click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['确定']['xpath']).click()
    sleep(1)


#  安卓点击返回按钮
def back_android(driver):
    driver.press_keycode(4)  # 返回


# 进入球队列表
def browse_team(driver, elementinfo):
    driver.find_element_by_xpath(elementinfo['球队']['xpath']).click()
    sleep(1)


# 选择球队
def select_team(driver, team_name):
    driver.find_element_by_xpath("//android.widget.TextView[@text={"+ team_name +"}]").click()
    sleep(1)


# 创建球队
def create_team(driver, elementinfo):
    name = 10000
    driver.find_element_by_xpath(elementinfo['加号']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.EditText[@text='请填写球队名称(10字符以内)']").send_keys(name)
    name+1
    logger.info(f'球队名{name}')
    sleep(1)
    driver.find_element_by_xpath(elementinfo['选择队徽']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['完成']['xpath']).click()
    sleep(2)
    driver.find_element_by_id("android:id/button1").click()
    sleep(1)


# 修改球队队名
def edit_team_name(driver, elementinfo,team_name,new_team_name):
    driver.find_element_by_xpath(elementinfo['设置']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.EditText[@text="+ team_name +"]").send_keys(new_team_name)
    logger.info(f'新球队名{new_team_name}')
    sleep(1)
    driver.find_element_by_xpath(elementinfo['保存']['xpath']).click()
    sleep(2)


# 退出球队
def out_team(driver, elementinfo):
    team_name = "t1"
    browse_team(driver, elementinfo)
    select_team(driver, team_name)
    driver.find_element_by_xpath(elementinfo['退出球队']['xpath']).click()
    sleep(1)
    driver.find_element_by_id("android:id/button1").click()
    sleep(1)


# 邀请队员
def invite_member(driver, elementinfo):
    driver.find_element_by_xpath(elementinfo['添加球员']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.EditText[@text=' 输入用户昵称']").send_keys('测试员lanzt')
    # 需要修改username
    sleep(1)
    driver.find_element_by_xpath(elementinfo['搜索']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['username']['xpath']).click()  # 需要修改username
    sleep(2)
    driver.find_element_by_xpath(elementinfo['完成']['xpath']).click()
    sleep(5)


# 请出队员
def remove_member(driver, elementinfo):
    size = driver.get_window_size()
    x = size['width'] / 2
    y = size['height'] * 0.7
    end_y = size['height'] * 0.3
    driver.swipe(x, y, x, end_y)
    driver.find_element_by_xpath(elementinfo['请出球员']['xpath']).click()
    sleep(2)
    driver.find_element_by_xpath(elementinfo['username']['xpath']).click()
    # 需要修改username
    sleep(1)
    driver.find_element_by_xpath(elementinfo['确定']['xpath']).click()
    sleep(2)


# 设置管理员
def allot_manager(driver, elementinfo):
    driver.find_element_by_xpath(elementinfo['设置管理员']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['添加管理员']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['username']['xpath']).click()
    # 需要修改username
    sleep(1)
    driver.find_element_by_xpath(elementinfo['确定']['xpath']).click()
    sleep(2)


# 取消管理员
def remove_manager(driver, elementinfo):
    driver.find_element_by_xpath(elementinfo['设置管理员']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['收回权限']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['username']['xpath']).click()
    # 需要修改username
    sleep(1)
    driver.find_element_by_xpath(elementinfo['确定']['xpath']).click()
    sleep(2)


# 进入消息管理
def browse_message(driver, elementinfo):
    driver.find_element_by_xpath(elementinfo['我的']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['消息']['xpath']).click()


# 进入比赛历史
def browse_match(driver, elementinfo):
    driver.find_element_by_xpath(elementinfo['比赛历史']['xpath']).click()
    sleep(1)


# 修改个人信息
def edit_per_info(driver, elementinfo):
    driver.find_element_by_xpath(elementinfo['我的']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['个人信息']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='testname1']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.EditText[@text='testname1']").send_keys('testname2')
    sleep(1)
    driver.find_element_by_xpath(elementinfo['男']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['女']['xpath']).click()
    driver.find_element_by_xpath("//android.widget.TextView[@text='确定']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='test1']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.EditText[@text='test1']").send_keys('test2')
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='确定']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='北京']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.EditText[@text='北京']").send_keys('天津')
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='确定']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='6']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='7']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='确定']").click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['保存']['xpath']).click()
    sleep(1)

    driver.find_element_by_xpath(elementinfo['个人信息']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='testname2']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.EditText[@text='testname2']").send_keys('testname1')
    sleep(1)
    driver.find_element_by_xpath(elementinfo['女']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['男']['xpath']).click()
    driver.find_element_by_xpath("//android.widget.TextView[@text='确定']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='test2']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.EditText[@text='test2']").send_keys('test1')
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='确定']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='天津']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.EditText[@text='天津']").send_keys('北京')
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='确定']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='7']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='6']").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='确定']").click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['保存']['xpath']).click()
    sleep(1)


def get_game_code(driver, elementinfo):
    driver.find_element_by_xpath(elementinfo['添加设备']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['比赛口令码']['xpath']).click()
    sleep(1)
    password = driver.find_element_by_xpath(elementinfo['口令码']['xpath']).text
    sleep(1)
    driver.tap([[300, 300]])
    print(password)
    sleep(1)
    return password


def join_game_by_code(driver, elementinfo, code):
    driver.find_element_by_xpath(elementinfo['加号']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['加入比赛']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['口令']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['输入口令']['xpath']).send_keys(code)
    driver.press_keycode(66)
    driver.find_element_by_xpath(elementinfo['口令确定']['xpath']).click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['拍摄']['xpath']).click()
    sleep(3)
    driver.find_element_by_xpath("//android.widget.TextView[@text='确定']").click()
    sleep(5)


def clean_game_video(driver, elementinfo, cleanway='删除'):
    driver.find_element_by_xpath(elementinfo['比赛视频']['xpath']).click()
    sleep(2)
    driver.find_element_by_xpath("//android.widget.TextView[@text='选择']").click()
    sleep(1)
    driver.find_element_by_xpath(elementinfo['比赛视频']['xpath']).click()
    sleep(2)
    driver.find_element_by_xpath(f"//android.widget.TextView[@text='{cleanway}']").click()
    sleep(1)
    driver.find_element_by_id("android:id/button1").click()
    sleep(1)
    driver.back()
    sleep(2)


def joingame(driver_A, driver_B, devicename):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    elementinfo, deviceid = pubfuc.getiteminfo(driver_A.desired_capabilities, "zuji")
    while True:
        try:
            if runcount > failcount:
                break
            while num < 501:
                logger.info(f'第{num}次开始比赛')
                create_team_game(driver_A, elementinfo)
                game_code = get_game_code(driver_A, elementinfo)
                join_game_by_code(driver_B, elementinfo, game_code)

                driver_A.find_element_by_xpath(elementinfo['开始比赛']['xpath']).click()
                sleep(2)
                driver_A.find_element_by_id("android:id/button1").click()
                sleep(10)

                # 结束比赛
                driver_A.find_element_by_xpath(elementinfo['结束比赛']['xpath']).click()
                sleep(2)
                driver_A.find_element_by_id("android:id/button1").click()
                sleep(1)
                driver_A.find_element_by_id("android:id/button1").click()
                driver_B.find_element_by_id("android:id/button1").click()
                sleep(8)

                # 清理视频
                clean_game_video(driver_A, elementinfo)
                clean_game_video(driver_B, elementinfo)

                num += 1
            break
        except Exception as e:
            logger.info(f'第{num}次运行出错')
            err_time = pubfuc.getlocaltime()
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{err_time}-{devicename}.png')
            driver_A.save_screenshot(str(img_file))
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{err_time}-{devicename}-B.png')
            driver_B.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            driver_A.close_app()
            driver_A.launch_app()
            driver_B.close_app()
            driver_B.launch_app()
            logger.info(pubfuc.getlocaltime())
            sleep(20)


# 创建球队比赛并结束测试
def create_team_game_test(driver, devicename):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    elementinfo, deviceid = pubfuc.getiteminfo(driver.desired_capabilities, "zuji")
    while True:
        try:
            if runcount > failcount:
                break
            while num < 50:
                logger.info(f'第{num}次开始球队比赛')
                sleep(3)
                create_team_game(driver, elementinfo)
                driver.find_element_by_xpath(elementinfo['开始比赛']['xpath']).click()
                sleep(2)
                driver.find_element_by_id("android:id/button1").click()
                sleep(10)

                # 结束比赛
                driver.find_element_by_xpath(elementinfo['结束比赛']['xpath']).click()
                sleep(2)
                driver.find_element_by_id("android:id/button1").click()
                sleep(1)
                driver.find_element_by_id("android:id/button1").click()
                sleep(8)

                # 清理视频
                # clean_game_video(driver, elementinfo)

                num += 1
            break
        except Exception as e:
            logger.info(f'第{num}次运行出错')
            err_time = pubfuc.getlocaltime()
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{err_time}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            driver.close_app()
            driver.launch_app()
            logger.info(pubfuc.getlocaltime())
            sleep(20)


# 创建个人比赛并结束测试
def create_personal_game_test(driver, devicename):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    elementinfo, deviceid = pubfuc.getiteminfo(driver.desired_capabilities, 'zuji')
    while True:
        try:
            if runcount > failcount:
                break
            while num < 50:
                logger.info(f'第{num}次开始个人比赛')
                sleep(3)
                create_personal_game(driver, elementinfo)
                driver.find_element_by_xpath(elementinfo['开始比赛']['xpath']).click()
                sleep(2)
                driver.find_element_by_id("android:id/button1").click()
                sleep(10)

                # 结束比赛
                driver.find_element_by_xpath(elementinfo['结束比赛']['xpath']).click()
                sleep(2)
                driver.find_element_by_id("android:id/button1").click()
                sleep(1)
                driver.find_element_by_id("android:id/button1").click()
                sleep(8)

                # 清理视频
                # clean_game_video(driver, elementinfo)

                num += 1
            break
        except Exception as e:
            logger.info(f'第{num}次运行出错')
            err_time = pubfuc.getlocaltime()
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{err_time}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            driver.close_app()
            driver.launch_app()
            logger.info(pubfuc.getlocaltime())
            sleep(20)


# 创建球队测试
def create_team_test(driver, devicename):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    elementinfo, deviceid = pubfuc.getiteminfo(driver.desired_capabilities, "zuji")
    while True:
        try:
            if runcount > failcount:
                break
            while num < 51:
                logger.info(f'第{num}次创建球队')
                browse_team(driver,elementinfo)
                create_team(driver, elementinfo)
                sleep(2)
                driver.find_element_by_xpath(elementinfo['退出']['xpath']).click()
                sleep(2)

                num += 1
            break
        except Exception as e:
            logger.info(f'第{num}次运行出错')
            err_time = pubfuc.getlocaltime()
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{err_time}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            driver.close_app()
            driver.launch_app()
            logger.info(pubfuc.getlocaltime())
            sleep(20)


# 浏览消息并返回测试
def browse_message_test(driver, devicename):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    elementinfo, deviceid = pubfuc.getiteminfo(driver.desired_capabilities, "zuji")
    while True:
        try:
            if runcount > failcount:
                break
            while num < 100:
                logger.info(f'第{num}次浏览消息')
                sleep(3)
                browse_message(driver, elementinfo)
                sleep(2)
                back_android(driver)
                sleep(2)

                num += 1
            break
        except Exception as e:
            logger.info(f'第{num}次运行出错')
            err_time = pubfuc.getlocaltime()
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{err_time}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            driver.close_app()
            driver.launch_app()
            logger.info(pubfuc.getlocaltime())
            sleep(20)


# 邀请并请出队员测试
def invite_remove_member_test(driver, devicename):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    elementinfo, deviceid = pubfuc.getiteminfo(driver.desired_capabilities, "zuji")
    while True:
        try:
            if runcount > failcount:
                break
            logger.info(f'第{num}次邀请队员')
            sleep(5)
            team_name = "t1"
            browse_team(driver, elementinfo)
            select_team(driver, team_name)
            invite_member(driver, elementinfo)
            sleep(2)
            logger.info(f'第{num}次请出队员')
            remove_member(driver, elementinfo)
            sleep(2)
            back_android(driver)
            sleep(2)
            num + 1
        except Exception as e:
            logger.info(f'第{num}次运行出错')
            err_time = pubfuc.getlocaltime()
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{err_time}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            driver.close_app()
            driver.launch_app()
            logger.info(pubfuc.getlocaltime())
            sleep(20)


# 添加并取消管理员测试
def allot_remove_manager_test(driver, devicename):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    elementinfo, deviceid = pubfuc.getiteminfo(driver.desired_capabilities, "zuji")
    while True:
        try:
            if runcount > failcount:
                break
            logger.info(f'第{num}次添加管理员')
            sleep(3)
            team_name = "t1"
            browse_team(driver, elementinfo)
            select_team(driver, team_name)
            allot_manager(driver, elementinfo)
            sleep(2)
            logger.info(f'第{num}次取消管理员')
            remove_manager(driver, elementinfo)
            sleep(2)
            back_android(driver)
            sleep(2)
            num + 1
        except Exception as e:
            logger.info(f'第{num}次运行出错')
            err_time = pubfuc.getlocaltime()
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{err_time}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            driver.close_app()
            driver.launch_app()
            logger.info(pubfuc.getlocaltime())
            sleep(20)


# 浏览比赛历史并返回测试
def browse_match_test(driver, devicename):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    elementinfo, deviceid = pubfuc.getiteminfo(driver.desired_capabilities, "zuji")
    while True:
        try:
            if runcount > failcount:
                break
            while num < 100:
                logger.info(f'第{num}次浏览比赛历史')
                sleep(3)
                team_name = "t1"
                browse_team(driver, elementinfo)
                select_team(driver, team_name)
                browse_match(driver, elementinfo)
                sleep(2)
                back_android(driver)
                sleep(2)

                num += 1
            break
        except Exception as e:
            logger.info(f'第{num}次运行出错')
            err_time = pubfuc.getlocaltime()
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{err_time}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            driver.close_app()
            driver.launch_app()
            logger.info(pubfuc.getlocaltime())
            sleep(20)


# 修改球队队名测试
def edit_team_name_test(driver, devicename):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    team_name = "t1"
    new_team_name = "t10"
    elementinfo, deviceid = pubfuc.getiteminfo(driver.desired_capabilities, "zuji")
    while True:
        try:
            if runcount > failcount:
                break
            while num < 100:
                logger.info(f'第{num}次修改队名')
                sleep(3)
                browse_team(driver, elementinfo)
                select_team(driver, team_name)
                edit_team_name(driver, elementinfo, team_name, new_team_name)
                sleep(2)
                back_android(driver)
                sleep(2)
                a = new_team_name
                new_team_name = team_name
                team_name = a
                num += 1
            break
        except Exception as e:
            logger.info(f'第{num}次运行出错')
            err_time = pubfuc.getlocaltime()
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{err_time}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            driver.close_app()
            driver.launch_app()
            logger.info(pubfuc.getlocaltime())
            sleep(20)


# 修改个人信息测试
def edit_per_info_test(driver, devicename):
    failcount = 10  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    elementinfo, deviceid = pubfuc.getiteminfo(driver.desired_capabilities, "zuji")
    while True:
        try:
            if runcount > failcount:
                break
            while num < 100:
                logger.info(f'第{num}、{num+1}次修改个人信息')
                sleep(3)
                edit_per_info(driver, elementinfo)
                sleep(2)
                back_android(driver)
                sleep(2)
                num += 2
            break
        except Exception as e:
            logger.info(f'第{num}次运行出错')
            err_time = pubfuc.getlocaltime()
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{err_time}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            driver.close_app()
            driver.launch_app()
            logger.info(pubfuc.getlocaltime())
            sleep(20)


def playgamevideo(driver, devicename):
    failcount = 3  # 用例中出错后重新执行的次数
    runcount = 1
    num = 1
    elementinfo, deviceid = pubfuc.getiteminfo(driver.desired_capabilities, "zuji")

    while True:
        try:
            if runcount > failcount:
                break
            driver.find_element_by_xpath("//android.widget.TextView[@text='lidw的主队']").click()
            sleep(2)
            driver.find_element_by_xpath(elementinfo['视频']['xpath']).click()
            sleep(3)
            phone_size = driver.get_window_size()
            size = driver.find_element_by_xpath(elementinfo['视频播放器']['xpath']).size
            print(phone_size, size)
            while num < 501:
                logger.info(f'第{num}次播放视频')
                driver.tap([[300, 400]])
                driver.swipe(start_x=size['width'] * 0.2, start_y=size['height'] * 0.7, end_x=size['width'] * 0.5,
                             end_y=size['height'] * 0.7,duration=3000)
                sleep(10)
                driver.tap([[300, 400]])
                driver.swipe(start_x=size['width'] * 0.2, start_y=size['height'] * 0.7, end_x=size['width'] * 0.5,
                             end_y=size['height'] * 0.7, duration=3000)
                sleep(10)
                driver.tap([[300, 400]])
                driver.swipe(start_x=size['width'] * 0.2, start_y=size['height'] * 0.7, end_x=size['width'] * 0.5,
                             end_y=size['height'] * 0.7, duration=3000)
                sleep(10)

                driver.tap([[300, 400]])
                sleep(0.5)
                driver.find_element_by_xpath(elementinfo['视频全屏']['xpath']).click()

                sleep(10)
                driver.tap([[300, 400]])
                sleep(0.5)
                driver.find_element_by_xpath(elementinfo['视频切换多视频']['xpath']).click()
                sleep(2)
                driver.back()
                num += 1
            break
        except Exception as e:
            logger.info(f'第{num}次运行出错')
            err_time = pubfuc.getlocaltime()
            img_file = pubfuc.get_real_dir_path(__file__, f'../testresult/{err_time}-{devicename}.png')
            driver.save_screenshot(str(img_file))
            sleep(3)
            logger.error(e.args[0], exc_info=True)
            logger.info(f'第{runcount}次重跑')
            runcount += 1
            driver.close_app()
            driver.launch_app()
            logger.info(pubfuc.getlocaltime())
            sleep(20)


