from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel

# Create your models here.

class User(AbstractUser, BaseModel):
    '''用户模型类'''

    class Meta:
        db_table = 'it_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class UserCenter(BaseModel):
    '''用户中心'''
    user = models.ForeignKey('User', verbose_name='所属账户')
    user_exp = models.IntegerField(default=0, verbose_name='用户经验值')
    user_lv = models.SmallIntegerField(default=0, verbose_name='用户等级')
    user_ach = models.CharField(max_length=20, verbose_name='用户成就')


    class Meta:
        db_table = 'it_usercenter'
        verbose_name = '用户中心'
        verbose_name_plural = verbose_name
