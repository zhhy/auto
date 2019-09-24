import uiautomator2 as u2
from time import  sleep

d = u2.connect('172.16.11.102')
# d = u2.connect_usb('CSX0217629006119')

print(d.info)

d.app_start("com.powerinfo.pi_iroom.demo")

sleep(2)

d()

d(text="多人群聊").click()

sleep(2)

print(d(resourceId="com.powerinfo.pi_iroom.demo:id/iv_create_room").exists)

d(resourceId="com.powerinfo.pi_iroom.demo:id/iv_create_room").click()

sleep(2)

d.press()

d(resourceId="com.powerinfo.pi_iroom.demo:id/bt_start").click()

d(resourceId="com.powerinfo.pi_iroom.demo:id/tv_roomId").click()

d(resourceId="com.powerinfo.pi_iroom.demo:id/mBtnWhoops").click()#进行打点

s = d(resourceId="com.powerinfo.pi_iroom.demo:id/tv_info").info

print(s["text"]) #获取推流相关信息

d(resourceId="com.powerinfo.pi_iroom.demo:id/iv_camera").click() #切换摄像头

d(resourceId="com.powerinfo.pi_iroom.demo:id/iv_torch").click() #打开闪光灯

d(resourceId="com.powerinfo.pi_iroom.demo:id/iv_torch").click() #关闭闪光灯

d(resourceId="com.powerinfo.pi_iroom.demo:id/iv_back").click()  #退出房间

d.app_stop("com.powerinfo.pi_iroom.demo")
