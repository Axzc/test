from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
import time

# django 环境的初始化 添加到任务的处理者一端
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ithds.settings")
django.setup()



app = Celery('celery_tasks.tasks', broker='redis://192.168.1.52:6379/8')



@app.task
def send_signup_active_email(to_email, username, token):
    '''发送激活邮件'''
    subject = '欢迎信息'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]  # 收件人
    htmlmessage = '<h1>%s 恭喜你成为本店会员,请点击下面链接激活:</h1><br /><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
    username, token, token)

    send_mail(subject, message, sender, receiver, html_message=htmlmessage)
    time.sleep(5)

