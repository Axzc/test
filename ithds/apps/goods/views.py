from django.shortcuts import render
from apps.user.models import User
from django.views.generic import View
from apps.goods.models import Article
from django_redis import get_redis_connection



# Create your views here.


class IndexView(View):
    '''首页'''

    def get(self, request):

        aricle = Article.objects.all()
        new_aricle = Article.objects.all().order_by('-create_time')

        return render(request, 'index.html', {'aricle':aricle, 'new_aricle':new_aricle})



class ArticleDetailsView(View):
    '''文章详情页'''

    def get(self, request, aricle_id):

        user = request.user

        print(user.username)

        # 最新发布
        new_aricle = Article.objects.all().order_by('-create_time')

        # 相关推荐
        recommend_aricle = Article.objects.all()

        # 文章主体
        aricle = Article.objects.get(id=aricle_id)

        if user.is_authenticated():
            # 判断用户是否登录
            # 添加历史浏览记录
            conn = get_redis_connection('default')
            history_key = 'history_%d' %user.id
            # 移除 aricle.id
            conn.lrem(history_key, 0, aricle.id)
            # 从左侧插入
            conn.lpush(history_key, aricle.id)
            # 显示 最新 的 5条 ltrim 进行裁切
            conn.ltrim(history_key, 0, 4)


        # 整理上下文
        context = {'aricle':aricle, 'new_aricle':new_aricle, 'recommend':recommend_aricle}



        return render(request, 'detail.html', context)





