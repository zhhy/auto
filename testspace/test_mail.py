# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.headerregistry import Address

mail_host = "mail.sjdd.com.cn"
mail_user = 'liml@sjdd.com.cn'

mail_pass = 'sjdd1234'

sender = 'liml@sjdd.com.cn'

receivers = ['liml@sjdd.com.cn']

# with open(f'F:/1/Test_TestStringMethods_2018-08-23_16-53-14.html','rb') as f:
#     mail_body = f.read()

message = MIMEMultipart()
message['Subject'] = '自动化测试结果'
message['From'] = sender
message['To'] = ','.join(receivers)
mail_body = '123'

message.attach(MIMEText(mail_body,'html','utf-8'))

# puretext = MIMEText(mail_host)

try:
    # smtpObj = smtplib.SMTP()s
    # smtpObj.connect(mail_host,25)
    smtpObj = smtplib.SMTP_SSL(mail_host,465)
    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(sender,receivers,message.as_string())
    smtpObj.quit()
    print('success')
except smtplib.SMTPException as e:
    print('error:',e.args)
    
