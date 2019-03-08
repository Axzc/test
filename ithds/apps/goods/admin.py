from django.contrib import admin
from apps.goods.models import Article

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    '''文章模型管理类'''

    list_per_page = 10  # 每页显示 10条

admin.site.register(Article, ArticleAdmin)

