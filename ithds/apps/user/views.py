from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from celery_tasks.tasks import send_signup_active_email
from django.contrib.auth import authenticate, login, logout
from django_redis import get_redis_connection
from apps.goods.models import Article

from django.contrib.auth.decorators import login_required


from django.conf import settings
from django.views.generic import View
from apps.user.models import User
import re


# Create your views here.

class SignupView(View):

    def get(self, request):
        print('get')

        return render(request, 'signup.html')

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('pwd')
        repassword = request.POST.get('repwd')
        email = request.POST.get('email')

        # 检验信息是否填写完整
        if not all([username, password, email]):

            return render(request, 'signup.html', {'errmsg': '数据填写不完整'})

        # 判断 两次密码是否输入 相同
        if not password == repassword:

            return render(request, 'signup.html', {'errmsg': '两次密码输入不相同'})

        # 检验邮箱格式是否合法
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):

            return render(request, 'signup.html', {'errmsg': '邮箱格式不合法'})

        # 检验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            # 用户名已存在
            return render(request, 'signup.html', {'errmsg': '用户名已存在'})

        # 进行业务处理 : 进行用户注册
        # 把校验完的数据 添加到 表里面
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # 加密用户身份信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)  # bytes
        token = token.decode()

        # 发送用户激活邮件
        send_signup_active_email.delay(email, username, token)

        return redirect(reverse('goods:index'))


class ActiveView(View):
    '''用户激活'''
    def get(self, request, token):
        '''进行用户激活'''

        # 进行解密 获取加密的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            userid = info['confirm']
            # 根据 id获取用户信息
            user = User.objects.get(id=userid)
            user.is_active = 1  # 修改用户激活状态
            user.save()

            # 跳转到登录页面
            return redirect (reverse('user:login'))

        except SignatureExpired as e:
            # 激活链接  已经过期
            return HttpResponse('激活链接已经过期')


class LoginView(View):
    '''登录'''

    def get(self, request):

        return render(request, 'login.html')

    def post(self, request):
        '''登录检验'''

        # 接受数据

        username = request.POST.get('username')
        password = request.POST.get('pwd')

        # 校验数据完整性
        if not all([username, password]):
            print(username, password)
            return render(request, 'login.html', {'errmsg':'数据填写不完整'})

        # 判断用户名密码
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名密码正确
            if user.is_active:
                # 用户已激活
                # 记录用户登录状态
                login(request, user)

                # 获取登录后要跳转的页面
                next_rul = request.GET.get('next', reverse('goods:index'))

                # 跳转到首页
                return redirect(next_rul)

            else:
                return render(request, 'login.html', {'errmsg':'用户未激活'})

        else:
            return render(request, 'login.html', {'errmsg':'用户名或密码错误'})


# user/logout
class LogoutView(View):
    '''退出登录'''

    def get(self, request):
        # 清除 session 信息
        logout(request)
        # 跳转到首页
        return redirect(reverse('goods:index'))


class UserCenterView(View):
    '''用户中心'''

    def get(self, request):
        '''显示'''


        user = request.user

        user = User.objects.get(id=user.id)

        # 获取用户的浏览记录
        conn = get_redis_connection('default')

        history_key = 'history_%d'%user.id

        # 获取用户最新浏览的文章id
        aricle_ids = conn.lrange(history_key, 0, 4)

        # aricle_list = Article.objects.filter(id__in=aricle_ids)
        #
        # print(len(aricle_list))

        aricle_list = []

        for aricle_id in aricle_ids:
            aricle = Article.objects.get(id=aricle_id)
            aricle_list.append(aricle)




        return render(request, 'homepage.html', {'user':user, 'aricle_list':aricle_list})













