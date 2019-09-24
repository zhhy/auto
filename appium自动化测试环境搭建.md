# appium自动化测试环境搭建

## mac环境

- mac一台
- 翻墙vpn一个

## 1、配置java环境

### 1.1 下载jdk

1、在jdk官网上下载mac相应的版本https://www.oracle.com/technetwork/java/javase/downloads/index.html 2、下载好相应mac的版本后，安装即可

### 1.2 配置环境变量

1、 打开终端输入`echo $SHELL`来确认本机使用的shell是哪个：zsh或bash 如果输出`/bin/bash`则为bash, 如果输出结果为`/bin/zsh`则为zsh。

2、根据上面不同的结果修改不同的shell配置文件 若为bash，则用`vi ~/.bash_profile`，若为zsh则用`vi ~/.zshrc`

输入`ls /Library/Java/JavaVirtualMachines`得到jdk的安装目录`/Library/Java/JavaVirtualMachines/jdk-10.0.2.jdk/Contents/Home/`

在相应文件末尾中添加以下内容，并`:wq`保存退出

```
JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-10.0.2.jdk/Contents/Home
  
PATH=$JAVA_HOME/bin:$PATH:.
CLASSPATH=$JAVA_HOME/lib/tools.jar:$JAVA_HOME/lib/dt.jar:.
export JAVA_HOME
export PATH
export CLASSPATH
```

3、在`~/`目录，执行`source`命令使配置文件生效,`source .bash_profile`或`source .zshrc` 4、执行`java -version`和`echo JAVA_HOME`出现相关信息即配置成功

## 2、安装homebrew

使用以下命令安装： `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

## 3、安装python3

执行`brew install python3` 安装后可输入`python3 --version`查看python版本信息

执行`pip3 install Appium-Python-Client`安装python的appium客户端库

## 4、配置Android Studio

- 安装Android Studio，除Android sdk tools外还需要Android Studio中的分析工具分析app性能

### 4.1 下载Android Studio

在官方网站下载最新版本Android Studio： <https://developer.android.com/studio/>

### 4.2 安装Android Studio

打开dmg文件，将Android Studio 拖到 Applications中

### 4.3 启动Android Studio

启动Android Studio，一路next，安装sdk相关tools即可

### 4.2 配置ANDROID_HOME变量

安装好Android Studio后android sdk的路径在`~/Libaray/Android/sdk`下， 在`.bash_profile`中添加:

```
export ANDROID_HOME=/Users/liminglei/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
```

保存退出后，执行`source .bash_profile`，使用`adb devices`查看是否生效

## 5、安装appium doctor检查appium环境配置

1、执行`brew install node`安装node 2、执行 `npm install appium-doctor -g`,安装完成后可使用相关命令查看appium的环境是否可行 3、执行`appium-doctor --android`查看安卓相关配置是否可行

```
info AppiumDoctor Appium Doctor v.1.4.3
info AppiumDoctor ### Diagnostic starting ###
info AppiumDoctor  ✔ The Node.js binary was found at: /usr/local/bin/node
info AppiumDoctor  ✔ Node version is 10.10.0
info AppiumDoctor  ✔ ANDROID_HOME is set to: /Users/liminglei/Library/Android/sdk
info AppiumDoctor  ✔ JAVA_HOME is set to: /Library/Java/JavaVirtualMachines/jdk-10.0.2.jdk/Contents/Home
info AppiumDoctor  ✔ adb exists at: /Users/liminglei/Library/Android/sdk/platform-tools/adb
info AppiumDoctor  ✔ android exists at: /Users/liminglei/Library/Android/sdk/tools/android
info AppiumDoctor  ✔ emulator exists at: /Users/liminglei/Library/Android/sdk/tools/emulator
info AppiumDoctor  ✔ Bin directory of $JAVA_HOME is set
info AppiumDoctor ### Diagnostic completed, no fix needed. ###
info AppiumDoctor 
info AppiumDoctor Everything looks good, bye!
info AppiumDoctor 
```

4、执行`appium-doctor --ios`检查ios的环境配置

## 6、安装appium-desktop

在官网下载: <https://github.com/appium/appium-desktop/releases> 下载后安装即可 在`.bash_profile`中添加以下，保存退出后`source .bash_profile`使其生效，这样就可以命令行启动appium了

```
export APPIUM=/Applications/Appium.app/Contents
export PATH=$PATH:$APPIUM
```

## 7、安装Xcode

在 App Store中下载安装即可,

## 8、安装IOS XCUITest驱动的依赖项

### 8.1 安装libimobiledevice

和iOS手机通讯使用: `brew install -- HEAD libimobiledevice`

### 8.2 安装ideviceinstaller

用于给IOS设备安装卸载app或者备份app：`brew install --HEAD ideviceinstaller`

### 8.3 安装ios-deploy

可以用命令行安装ios app到连接的设备：`brew install ios-deploy`

### 8.4 安装Carthage

类似CocoaPods的包管理工具：`brew install carthage`

### 8.5 安装xcpretty[可选]

用于对xcodebuild的输出进行格式化的 ：`sudo gem install -n /usr/local/bin xcpretty`

### 8.6 遇到问题

#### 8.6.1 libimobiledevice命令执行报错`Could not connect to lockdownd`

- 查看libimobiledevice和ideviceinstaller发现缺少相关依赖,brew安装相关依赖后，重新安装即可

## 9、配置WebDriverAgent

- 参考网站 : <https://github.com/appium/appium/blob/master/docs/en/drivers/ios-xcuitest-real-devices.md#basic-manual-configuration>

按照全手动配置中

```
cd /Applications/Appium.app/Contents/Resources/app/node_modules/appium/node_modules/appium-xcuitest-driver/WebDriverAgent/``mkdir -p Resources/WebDriiverAgetn.bundle``./Scripts/bootstrap.sh -d
```

用xcode打开`WebDriverAgent.xcodeproj`在分别选择

`WebDriverAgentLib`和`WebDriverAgentRunner`，选择“自动管理签约”，在“常规”选项卡，然后选择你的`Development Team`。这也应该自动选择`Signing Ceritificate`。

```
WebDriverAgentRunner`需要通过进入“Build Settings”选项卡手动更改目标的bundle id，并将“Product Bundle Identifier”更改为`com.powerinfo(原位facekbook).WebDriverAgentRunner.xxx
```

需要注意的是，如果按照全手动配置的WebDriverAgent，在脚本中，启动参数中不应包含:

```
"xcodeOrgId": "H6E8P88Q4E",#teamid
"xcodeSigningId": "iPhone Develaoper",
```

## 10、启动appium建立session

- 启动appium，start appium-server

### 10.1、安卓手机连接电脑

建立类似以下的相关参数，start session，如果启动成功则证明Android-appium环境搭建成功

```
{
  "platformName": "Android",
  "platformVersion": "8.0",
  "deviceName": "VGT7N17818000730",
  "appPackage": "com.powerinfo.pi_iroom.demo",
  "appActivity": "com.powerinfo.pi_iroom.demo.setting.LoginSettingActivity",
  "autoAcceptAlerts": "true",
  "noRest": "true"
}
```

### 10.2、ios手机连接电脑

建立类似以下的相关参数，start session，如果启动成功则证明Android-appium环境搭建成功

```
{
  "platformName": "IOS",
  "platformVersion": "10.3.3",
  "deviceName": "IPhone",
  "automationName": "XCUITest",
  "bundleId": "com.powerinfo.iRoom",
  "udid": "2e739c10ce9ce8f75c18ae7b0621231ebbbf23b1",
  "noReset": "true"
}
```

## 11、配置环境过程中遇到的问题

### 11.1、ios启动session时 Could not determine Xcode version

运行`xcode-select --install`检查 command line tools 是否安装,以下结果说明已经安装 `xcode-select: error: command line tools are already installed, use "Software Update" to install updates` 执行`sudo xcode-select --reset`重置，然后执行`sudo xcode-select --switch /Applications/Xcode.app` 重新打开appium，启动session成功

### 11.2、ios启动session 报错info XCUITest xcodebuild exited with code '65' and signal 'null'

原因是手动配置了`WebDriverAgent`后，启动session的参数中有`xcodeOrgId`和`xcodeSigningId`，去掉这2个参数即可启动成功

## windows测试环境搭建

- 1、配置Java 环境
- 2、安装python3
- 3、安装appium-desktop
- 4、下载自动化脚本：[http://192.168.11.8/Shared/AutoTester，根据脚本中readme配置相关变量和安卓python第三方库](http://192.168.11.8/Shared/AutoTester%EF%BC%8C%E6%A0%B9%E6%8D%AE%E8%84%9A%E6%9C%AC%E4%B8%ADreadme%E9%85%8D%E7%BD%AE%E7%9B%B8%E5%85%B3%E5%8F%98%E9%87%8F%E5%92%8C%E5%AE%89%E5%8D%93python%E7%AC%AC%E4%B8%89%E6%96%B9%E5%BA%93)

## 12、问题

### 12.1、运行一段时间后，重新运行会提示'65'的报错，

解决方法：

```
1、[可选]用findler 打开下面目录 /Users/liminglei/Library/Developer/Xcode/DerivedData 删除 WebDriverAgent 
3、重新执行以下命令,id注意更换，可通过idevice_id --list获取udid
xcodebuild -project /Applications/Appium.app/Contents/Resources/app/node_modules/appium-xcuitest-driver/WebDriverAgent/WebDriverAgent.xcodeproj -scheme WebDriverAgentRunner -destination 'id=aa94d167fa1165e50027056d1f4697b728d8b583' test
```

### 12.2、运行一段时间后，签名失效，xcodebuild会失败

解决方法：需要重新签下名

```
1、像12.1中的删除xcode目录下的webdriveragent项目
2、打开xcode，perfermences下account 下删除原来的账号
3、在钥匙串中，选择我的证书，删除开发者账号的证书
4、打开xcode 重新添加开发者账号，下载证书
5、新建一个项目，选择自动签名，选择刚才登录的开发者账号，如果自动签名不生效，修改bundleid
6、执行xcodebuild 命令，可参考12.1,成功后可按ctrl+c停止
```

### 13、查找apppackage和activity

- 1、手机连接电脑，杀掉app，收集logcat日志,`adb logcat -v threadtime -b all > log.txt`
- 2、在logcat日志中搜索`am_create_activity`，查看结果，第一个com.的为packa，后面的是activity

```
03-25 17:44:36.339  1643  2347 I am_create_activity: [0,8569133,195,com.bitstartlight.xvideo/com.btxg.xvideo.features.general.SplashActivity,android.intent.action.MAIN,NULL,NULL,270532608]
```

