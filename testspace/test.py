# -*- coding:utf-8 -*-

from appium import webdriver
from time import sleep
import cv2
import matplotlib.pyplot as plt

desired_caps = {
    "platformName": "Android",
    "platformVersion": "8.0",
    "deviceName": "PBV0216801001067",
    "appPackage": "com.bitstartlight.xvideo",  # com.powerinfo.pi_iroom.demo
    # com.powerinfo.pi_iroom.demo.setting.LoginSettingActivity /
    "appActivity": "com.btxg.xvideo.features.general.SplashActivity",
    "autoAcceptAlerts": "true",
    "newCommandTimeout": "3600",
    "noReset": "true"
}



# driver = webdriver.Remote(f"http://localhost:4731/wd/hub", desired_caps)

def get_screen_file(desired_caps):
    driver = webdriver.Remote(f"http://localhost:4731/wd/hub", desired_caps)

    driver.find_element_by_id("com.bitstartlight.xvideo:id/iv_create_room").click()
    sleep(1)
    driver.find_element_by_xpath("//android.widget.Button[@text='START']").click()
    sleep(5)

    driver.get_screenshot_as_file('tmp.png')
    # get the position and size of the preview  [0,72][1080,1920]
    view_xpath = "//android.widget.FrameLayout[1]/android.widget.FrameLayout" \
                 "/android.widget.FrameLayout/android.view.View"
    element_loction = driver.find_element_by_xpath(view_xpath).location
    element_size = driver.find_element_by_xpath(view_xpath).size
    print(element_loction)
    print(element_size)
    driver.quit()

# get_screen_file(desired_caps)


image_a = cv2.imread('/Users/liminglei/Documents/A.png')
image_b = cv2.imread('/Users/liminglei/Documents/c.png')

# gray_a = cv2.cvtColor(image_a, cv2.COLOR_BAYER_BG2GRAY)
# gray_b = cv2.cvtColor(image_b, cv2.COLOR_BAYER_BG2GRAY)

H1 = cv2.calcHist([image_a], [1], None, [256], [0, 256])
H1 = cv2.normalize(H1, H1, 0, 1, cv2.NORM_MINMAX, -1)

H2 = cv2.calcHist([image_b], [1], None, [256], [0, 256])
H2 = cv2.normalize(H2, H2, 0, 1, cv2.NORM_MINMAX, -1)

similatry = cv2.compareHist(H1, H2, 0)
print(similatry)

plt.subplot(2, 1, 1)
plt.plot(H1)
plt.subplot(2, 1, 2)
plt.plot(H2)
plt.show()