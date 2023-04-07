import smtplib
import re
from os import environ
from os.path import exists
from platform import system, node
from time import strftime
from email.mime.text import MIMEText
from email.utils import formataddr
from random import randint
from easygui import msgbox, enterbox
from threading import Timer

print('库加载完成')

title = '验证码'
my_sender = '1848481499@qq.com'  # 发件者邮箱（请自行更改）
my_pass = 'mdzvtyqcosopbijd'  # 授权码（请自行更改）
dt = strftime('%Y-%m-%d %H:%M:%S')
print('已经获取时间')
my_user = '2582435774@qq.com'
# username = environ['USERNAME']
system = system()
computer = node()
# number = randint(100000, 999999)  # 验证码
err = Exception
print('设备信息获取完成\n变量定义完成')

ver_code = 0


def claerVercode():
    global ver_code
    ver_code = 0


def creatVercode():
    global ver_code
    ver_code = randint(100000, 999999)
    cle = Timer(180, claerVercode)
    cle.start()
    print(ver_code)


def get_ver():
    global ver_code
    return ver_code


def mail(address_mail):
    global err
    global ver_code
    ret = True
    print('嵌套入检查语句')
    try:
        msg = MIMEText(str(ver_code), 'plain', 'utf-8')
        msg['From'] = formataddr(["文件共享系统", my_sender])
        msg['To'] = formataddr(["FK", address_mail])
        msg['Subject'] = "文件共享系统的验证码"
        print('已经设置好邮件信息')

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, [address_mail, ], msg.as_string())
        server.quit()
        print('邮件发送已完成')
    except Exception as e:
        ret = False
        err = str(e)
        print('进入错误语句\n错误是%s' % err)
    print('返回信息')
    return ret


def checkmail(ver):
    if ver == ver_code:
        return True
    return False


if __name__ == '__main__':
    print('进入主程序')
    creatVercode()
    mail('2582435774@qq.com')
    print('yes')
