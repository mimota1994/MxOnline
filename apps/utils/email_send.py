#_*_coding:utf-8_*_
__author__ = 'bobby'
__date__ = '2018-03-17 15:10'
from random import Random
from django.core.mail import send_mail,EmailMessage

from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM,EMAIL_HOST_PASSWORD

#原始邮箱发送
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_register_email(email,send_type="register"):
    email_record=EmailVerifyRecord()
    code=random_str(16)
    email_record.code=code
    email_record.email=email
    email_record.send_type=send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type=="register":
        email_title="慕学在线网注册激活链接"
        email_body="请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}".format(code)
        #message=MIMEText(email_boby,'plain','utf-8')
        #message['From']=Header(EMAIL_FROM,'utf-8')
        #message['To']=Header(email,'utf-8')
        #message['Subject']=Header(email_title,'utf-8')
        #msg=smtplib.SMTP()
        #msg.connect('smtp.qq.com',25)
        #msg.login(EMAIL_FROM,EMAIL_HOST_PASSWORD)
        #msg.sendmail(EMAIL_FROM,[email],message.as_string())
        #msg.quit()
        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
        else:
            pass
    else:
        email_title="慕学在线网注册密码重置链接"
        email_body="请点击下面的链接重置密码：http://127.0.0.1:8000/reset/{0}".format(code)
        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
        else:
            pass



def random_str(randomlength=8):
    str=''
    chars='qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    length=len(chars)-1
    random=Random()
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    return str