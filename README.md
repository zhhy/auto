# AutomationTestFramework_appium

基于appium的移动端自动化测试平台，执行测试任务，测试结果截图，生成测试报告并发送邮件

## 环境配置说明

- 1、安装appium-desktop版本，安装后查看安装目录，增加【APPIUM】的环境变量，值为resources所在的目录
    mac:`/Applications/Appium.app/Contents`;
    windows下appium安装目录有空格后需复制到其他目录下，并且必须在系统变量中添加:`C:\appium\`
- 2、安装jdk，配置JAVA_HOME变量
- 3、安装node，安装完成后自动添加到环境变量
- 4、在命令行终端中，可以使用`shell liminglei$ node /Applications/Appium.app/Contents/Resources/app/node_modules/appium/build/lib/main.js -a 127.0.0.1 -p4723 `启动appium server说明appium server相关配置正确



## 使用说明

**iPhone手机的自动化必须使用mac电脑**

- 1、在devices.yml文件中查看要进行自动化的手机相关配置，如果此文件中没有相关配置，复制模板后修改系统版本、uid即可
- 2、在iRoomtestcase.py文件中有2个class，分别为安卓和ios，更改setUp中的devicelist参数，
    将进行自动化手机添加到devicelist参数中，填入的名字为devices.yml中的配置名称 `devicelist = ['sony','meizu-pro7']`
- 3、在iRoomtestcase文件中有3个case，需要另外一台手机先创建好房间，然后把房间号修改用例中相关
    `proc = pool.apply_async(joinandleaveroom,(driver,'4531',))`
- 4、在suite_singletest.py文件中输入要运行的test,可填入1个或多个
- 5、运行suite_singletest.py文件即可


## 需第三方库

- 1、appium的python客户端库，`pip install Appium-Python-Client`
- 2、读取yaml文件的库,`pip install pyyaml`
- 3、paramiko库，`pip install paramiko`
- 4、安装matplotlib, `pip install matplotlib`

## 失败重跑机制说明

- 1、测试用例在运行过程中，如果setup或者用例执行过程中有失败或者错误的时候，就会重新执行用例，现在设置的重跑次数为1次，
- 2、测试用例自身具有失败重跑的机制，用例出错后会重启APP
- 3、失败重跑机制需修改unittest，修改方法见下方。

### 修改unittest

- 1、找到unittest的目录，复制一份为myunittest,MAC系统下的目录位置在`/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7
`下
- 2、修改`suite.py`文件中`TestSuite`类的`run`函数:
    - 2.1、首先复制一份修改为runbak函数
    - 2.2、在原来的run函数中作出以下修改:
    ```
        def run(self, result, debug=False):
        failcount = 1 #用例出错或失败后自动重试的次数
        class_num = 1
        topLevel = False

        if getattr(result, '_testRunEntered', False) is False:
            result._testRunEntered = topLevel = True

        for test in self:
            case_num = 1

            if result.shouldStop:
                break

            success_flag = True
            while success_flag:
                if _isnotsuite(test):
                    self._tearDownPreviousClass(test, result)
                    self._handleModuleFixture(test, result)
                    self._handleClassSetUp(test, result)
                    result._previousTestClass = test.__class__
                    if (getattr(test.__class__, '_classSetupFailed', False) or
                            getattr(result, '_moduleSetUpFailed', False)):
                        if class_num > case_num:
                            success_flag = False
                        else:
                            time.sleep(5)
                            result._previousTestClass = True
                            print('类{}第{}次重新初始化执行'.format(test.__class__,class_num))
                            class_num += 1
                        continue

                    if not debug:
                        test(result)
                    else:
                        test.debug()
                    print(result)
                    if len(result.errors) > 0 or len(result.failures) > 0 : #结果为fail或者err用例判断
                        if case_num > failcount:
                            success_flag = False
                        else:
                            print('用例{}第{}次重新执行'.format(test,case_num))
                            case_num += 1
                    else:
                        success_flag = False
        if topLevel:
            self._tearDownPreviousClass(None, result)
            self._handleModuleTearDown(result)
            result._testRunEntered = False

        return result
    ```
- 3、在运行用例时，需导入 myunittest,以myunittest的一些方法启动


### 特殊机型设置

- 1、对于小米8手机来说，额外需要在开发者选项中勾选【usb调试（安全设置）】
- 2、对于vivo x9手机来说，额外需要在开发者选项中勾选【usb模拟点击】