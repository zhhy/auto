from time import sleep

from appium import webdriver
desired_caps = {}

desired_caps["platformName"] = "Android"
desired_caps["platformVersion"] = "6.0.1"
#desired_caps["platformVersion"] = "9"
desired_caps["deviceName"] = "172.16.11.101:5555"
#desired_caps["deviceName"] = "VGT7N17818000695"
desired_caps["noReset"] = "true"

desired_caps["appPackage"] = "com.powerinfo.demo.a50_stb"
desired_caps["appActivity"] = "com.powerinfo.demo.a50.SettingActivity"

driver = webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)

i=0
while i<10000:
    i+=1
    driver.find_element_by_id("com.powerinfo.demo.a50_stb:id/start_btn").click()
    sleep(30)
    driver.find_element_by_id("com.powerinfo.demo.a50_stb:id/img_close").click()
    sleep(30)

driver.quit()