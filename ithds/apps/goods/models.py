from django.db import models
from db.base_model import BaseModel
from tinymce.models import HTMLField

# Create your models here.

class Article(BaseModel):
    '''文章模型类'''
    status_choices = (
        (0, '上线'),
        (1, '下线'),
    )

    title = models.CharField(max_length=200, verbose_name='文章标题')
    slug = models.CharField(max_length=200, verbose_name='文章概括')
    text = HTMLField(verbose_name='文章内容')
    status = models.SmallIntegerField(default=0, choices=status_choices, verbose_name='文章状态')
    image = models.ImageField(upload_to='image')

    def __str__(self):

        return  self.title

    class Meta:
        db_table = 'it_article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name
