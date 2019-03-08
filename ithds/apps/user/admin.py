from django.contrib import admin
from apps.user.models import User, UserCenter
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    '''文章模型管理类'''

    list_per_page = 10  # 每页显示 10条

admin.site.register(User, UserAdmin)
admin.site.register(UserCenter)
