# -*- coding:utf-8 -*-

import os
import re
import time
import subprocess
from pathlib import Path
import yaml
import platform
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
#import paramiko
import zipfile

logger = logging.getLogger('autolog')


def setcustomlogger(name, isprintsreen=False):
    # 定义logger对象，设置日志级别
    logger_first = logging.getLogger(name)
    logger_first.setLevel(logging.INFO)

    formatter = logging.Formatter(fmt="[%(levelname)s] %(asctime)s: %(message)s")
    # 把日志输出到控制台
    if isprintsreen:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    # 把日志输出到文件
    filehandler = logging.FileHandler(filename="../testresult/autolog.log")
    filehandler.setFormatter(formatter)
    logger_first.addHandler(filehandler)

    return logger_first


def send_mail(receivers, resfile, img_list, appium_log):
    if not os.path.exists(resfile):
        return
    mail_host = "mail.sjdd.com.cn"
    mail_user = '@sjdd.com.cn'
    mail_pass = ''

    sender = '@sjdd.com.cn'

    parsreceivers = [f'{name}@sjdd.com.cn' for name in receivers]
    with open(resfile, 'rb') as f:
        resbody = f.read()

    message = MIMEMultipart()
    message['Subject'] = '自动化测试结果'
    message['From'] = sender
    message['To'] = ','.join(receivers)
    mail_body = resbody

    message.attach(MIMEText(mail_body, 'plain', 'utf-8'))

    logfile = MIMEText(open(resfile, 'rb').read(), 'base64', 'utf-8')
    logfile['Content-Type'] = 'application/octet-stream'
    logfile['Content-Disposition'] = f'attachment; filename={os.path.basename(resfile)}'
    message.attach(logfile)
    # 将appiumlog发送到邮件中
    for appiumlog in appium_log:
        appiumlogfile = MIMEText(open(appiumlog, 'rb').read(), 'base64', 'utf-8')
        appiumlogfile['Content-Type'] = 'application/octet-stream'
        appiumlogfile['Content-Disposition'] = f'attachment; filename={os.path.basename(appiumlog)}'
        message.attach(appiumlogfile)
    # 将图片发送到邮件中
    for img in img_list:
        part = MIMEApplication(open(img, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(img))
        message.attach(MIMEText(f'\n\n{img}:\n\n', 'text', 'utf-8'))
        message.attach(part)

    try:
        # smtpObj = smtplib.SMTP()
        # smtpObj.connect(mail_host,25)
        smtpobj = smtplib.SMTP_SSL(mail_host, 465)
        smtpobj.login(mail_user, mail_pass)
        smtpobj.sendmail(sender, parsreceivers, message.as_string())
        smtpobj.quit()
        print('success')
        # 发送邮件成功后删除图片和autolog
        for img in img_list:
            os.remove(img)
        for appiumlog in appium_log:
            os.remove(appiumlog)
        logging.shutdown()
        os.remove(resfile)
    except smtplib.SMTPException as e:
        print('error:', e.args)


def get_real_dir_path(path, paths=''):
    curdir = os.path.dirname(path)
    if paths is None:
        return curdir
    else:
        return os.path.abspath(os.path.join(curdir, paths))


def getcurretsystem():
    systeminfo = platform.platform()
    # print(systeminfo)
    if 'Windows' in systeminfo:
        systemname = 'windows'
    elif 'Darwin' in systeminfo:
        systemname = 'mac'
    else:
        systemname = 'linux'
    return systemname


def getymlfileinfo(filename='app控件'):
    filepath = Path(__file__).cwd().parent / f'{filename}.yml'
    with open(filepath, 'r', encoding='gbk') as loadfile:
        info = yaml.load(loadfile)
    return info


def cleannodeproc():
    if 'mac' in getcurretsystem():
        execute_cmd = 'ps -A|grep node'
        cmd_res = subprocess.getoutput(execute_cmd)
        for res in cmd_res.split('\n'):
            # print(res)
            if 'node /' in res:
                pid = re.split('\s+', res.strip())[0]
                # print(pid)
                kill_cmd = f'kill -9 {pid}'
                kill_res = subprocess.getoutput(kill_cmd)
                print(kill_res)
    else:
        execute_cmd = 'tasklist|findstr node'
        cmd_res = subprocess.getoutput(execute_cmd)
        for res in cmd_res.split('\n'):
            if 'node.exe' in res:
                pid = re.split('\s+', res)[1]
                # print(pid)
                kill_cmd = f'taskkill /F /PID {pid}'
                kill_res = subprocess.getoutput(kill_cmd)
                print(kill_res)


def waittimeout(element, timeout=10):
    begintime = time.time()
    while begintime + timeout > time.time():
        isstop = element is not None
        if isstop:
            break
        else:
            time.sleep(1)


def getlocaltime():
    loctime = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
    print(loctime)
    return loctime


def get_android_app_info():
    # get device name
    deviceid = subprocess.getoutput('adb devices').split('\n')[1].split("\t")[0]

    # get Android device systerm version
    deviceversion = subprocess.getoutput('adb shell getprop ro.build.version.release')

    # get app package name and activity
    if 'mac' in getcurretsystem():
        find_exec = 'grep'
    else:
        find_exec = 'findstr'
    cmd_exec = f'adb shell dumpsys window w |{find_exec} \/|{find_exec} name='
    getappinfo = subprocess.getoutput(cmd_exec)
    appinfo = re.findall(r'com.+?tivity', getappinfo)[0].split('/')
    package = appinfo[0]
    activity = appinfo[1]

    desired_caps = {
        'platformName': 'Android',
        'platformVersion': deviceversion.rstrip('\n'),
        'deviceName': deviceid,
        'appPackage': package,
        'appActivity': activity,
        'autoAcceptAlerts': 'true',
        'noReset': 'true'
    }

    print(desired_caps)
    return desired_caps


def get_ios_app_info():
    udid = os.popen('idevice_id --list').readlines()
    bundleid = os.popen("ideviceInstaller -l|grep PowerInfo").readlines()
    device_os_version = os.popen('ideviceinfo -k ProductVersion').readlines()

    desired_caps = {
        'platformName': 'IOS',
        'platformVesion': device_os_version[0].rstrip(),
        'deviceName': 'IPhone',
        'automationName': 'XCUITest',
        'bundleId': bundleid[0].split(',')[0],
        'udid': udid[0].rstrip(),
        'noReset': 'true'
    }

    print(desired_caps)
    return desired_caps


def getiteminfo(devicedriverinfo, classname='iRoom'):
    itemfileinfo = getymlfileinfo()
    isios = 'desired' not in devicedriverinfo  # 判断运行的设备是否为IOS
    if isios:
        iteminfo = itemfileinfo['{}_{}'.format(classname, devicedriverinfo['platformName'])]
        deviceid = devicedriverinfo['udid']
    else:
        iteminfo = itemfileinfo['{}_{}'.format(classname, devicedriverinfo['desired']['platformName'])]
        deviceid = devicedriverinfo['desired']['deviceName']
    return iteminfo, deviceid

def getpackageinfo(devicedriverinfo,packagename='iRoom'):
    itemfileinfo = getymlfileinfo('packagename')
    isios = 'desired' not in devicedriverinfo  # 判断运行的设备是否为IOS
    if isios:
        iteminfo = itemfileinfo['{}_{}'.format(packagename, devicedriverinfo['platformName'])]

    else:
        iteminfo = itemfileinfo['{}_{}'.format(packagename, devicedriverinfo['desired']['platformName'])]

    return iteminfo



class StartDriver:

    def __init__(self, devicelist):
        deviceinfo = getymlfileinfo('devices')
        self.aport = list(range(4723, 4800, 2))
        self.bport = list(range(4724, 4800, 2))
        self.iosport = list(range(8100, 8200, 2))
        self.devicelist = devicelist
        self.realdevice = [deviceinfo[device] for device in devicelist]

    def startappiumserver(self, i):
        appium_env = os.environ['APPIUM']
        print(appium_env)
        excute_cmd_base = f'node "{appium_env}/Resources/app/node_modules/appium/build/lib/main.js" -a 127.0.0.1'
        # print(excute_cmd_base)
        uidkey = 'udid' if 'IOS' in self.realdevice[i]['platformName'] else 'deviceName'

        deviceport = f'--webdriveragent-port {self.iosport[i]}' if 'IOS' in self.realdevice[i][
            'platformName'] else f'-bp {self.bport[i]}'
        # print(uidkey)
        excute_cmd = f"{excute_cmd_base} -p {self.aport[i]} {deviceport} -U {self.realdevice[i][uidkey]} " \
                     f"--local-timezone --log-timestamp --command-timeout 3000"

        appiumlogpath = get_real_dir_path(__file__, '../testresult')

        subprocess.Popen(excute_cmd, shell=True,
                         stdout=open(f"{appiumlogpath}/appiumlog_{self.devicelist[i]}.txt", 'w+'))

    def getnodeprocpid(self):

        pidlist = []

        for i in range(len(self.devicelist)):
            if 'mac' in getcurretsystem():
                cmd = f'lsof -i:{self.aport[i]}'
            else:
                cmd = f'netstat -ano|findstr {self.aport[i]}'
            getportused = subprocess.getoutput(cmd)
            info = getportused.split('\n')
            if f':{self.aport[i]}' in getportused:
                pid = re.split('\s+', info[1])[1] if 'mac' in getcurretsystem() else re.split('\s+', info[0])[-1]
                pidlist.append(pid)

        # print(pidlist)
        return pidlist


def parselog(filepath, findstr):
    with open(filepath) as f:
        loginfo = f.readlines()
        for log in loginfo:
            if findstr in log:
                print(log)
                logger.info(log)


def download_file_from_server(*args):
    # 服务器连接信息
    host_name = 'app.powzamedia.com'
    user_name = 'liml'
    password = 'lei@1210'
    port = 22

    # 连接远程服务器
    t = paramiko.Transport((host_name, port))
    t.connect(username=user_name, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)

    tm = time.strftime('%Y-%m-%d', time.localtime())
    # 远程文件路径（需要绝对路径）
    if 'iRoom' in args:
        remote_dir = f'/storage/new_upload_file/iRoom/{tm}/'
    elif 'P31Link' in args:
        remote_dir = f'/storage/new_upload_file/P31Link/{tm}/'
    else:
        remote_dir = f'/storage/new_upload_file/others/{tm}/'
    print(remote_dir)
    # 本地文件存放路径（绝对路径或者相对路径都可以）
    local_dir = '/Users/liminglei/Desktop/log/'

    downloadfiles = []
    localfiles = []
    # 远程文件开始下载
    files = sftp.listdir(remote_dir)
    for i in files:
        istargetfile = True
        for arg in args:
            istargetfile = istargetfile and (arg in i)
            if not istargetfile:
                break
        if istargetfile:
            downlad_file = os.path.join(remote_dir, i)
            local_file = os.path.join(local_dir, i)
            downloadfiles.append(downlad_file)
            localfiles.append(local_file)
    downloadfiles = sorted(downloadfiles)
    localfiles = sorted(localfiles)
    print(downloadfiles)
    print(localfiles)
    sftp.get(downloadfiles[-1], localfiles[-1])  # 只上传最新上传的日志,适用一台手机自动化上传日志，多台上传时可能会有问题
    while True:
        time.sleep(1)
        if os.path.exists(localfiles[-1]):
            break
    # 关闭连接
    t.close()
    return [localfiles[-1]]

def extrafile(file):
    if not os.path.exists(file):
        logger.info(f"文件{file}不存在，解压失败!")
        return
    file_dir = os.path.dirname(file)
    extra_dir = os.path.join(file_dir, os.path.basename(file).split('.')[0])
    zipfile.ZipFile(file).extractall(extra_dir)
    time.sleep(5)
    return extra_dir
