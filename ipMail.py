# -*- coding: UTF-8 -*-

# 获取主机公网地址，并用邮件发送到指定邮箱

import smtplib
import requests
import time, os, sched
import re
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import schedule
 
# 这里使用qq邮箱服务器
mail_host="smtp.qq.com"  
mail_user="****@qq.com"
mail_pass="**********"   # 注意这里不是你的邮箱登录密码，而是邮箱服务器授权码
                         # 需要到邮箱的<设置> -- <账户> -- <POP3/SMTP服务> 开启该服务并生成授权码
 

sender = mail_user
receivers = '*****@***.com'

 
#获取IP地址
def get_out_ip():
    print("读取IP地址=>=>=>=>=>=>")
    url = r'http://www.net.cn/static/customercare/yourip.asp'
    readT = requests.get(url)
    Readtxt = readT.text   
    pattern = re.compile('<h2>[0-9]+.[0-9]+.[0-9]+.[0-9]+</h2>') # 正则表达式，得到的格式是<h2>ip</h2>
    showv=pattern.search(Readtxt)
    #print(Readtxt)
    ip = showv.group(0)
    ip = re.sub('<\/?h2>','',ip,0,0)  # 去掉标签  
    print('获取ip成功')
    print(ip)
    return ip
 
#发送邮件代码
def mail():
    print("----正在获取IP------")
    ipSent = get_out_ip()
    try:
        ipmsg="当前IP地址是："+ ipSent
        message = MIMEText(ipmsg,'plain','utf-8')
        message['From']=formataddr(["FromRobots",sender])     # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        message['To']=formataddr(["XGmail",receivers])        # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        message['Subject']="家庭服务器IP报告信息"               # 邮件的主题

        smtpObj = smtplib.SMTP() 
        # server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # SMTP服务器（端口465或587）
        print("--------正在发送--------")
        smtpObj.connect(mail_host, 25)                  # 25端口也可以
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("successful")

    except smtplib.SMTPException:
        print ("Error")


 

# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).days.do(job)
#schedule.every().monday.do(job) 
# schedule.every().wednesday.at("13:15").do(job)
 

#主代码发送并循环
#schedule.every(10).seconds.do(mail) # 每十秒发送一次
schedule.every().wednesday.at("13:15").do(job) 

while True:
    schedule.run_pending()






