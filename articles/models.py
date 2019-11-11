from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from mdeditor.fields import MDTextField
from read_statistics.models import ReadNumExpandMethod, ReadDetail

# Create your models here.
class Category(models.Model):
    category_name = models.CharField('类名', max_length=15)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class Article(models.Model, ReadNumExpandMethod):
    title = models.CharField('标题', max_length=50)
    # content = models.TextField('内容')
    content = MDTextField()
    category = models.ForeignKey(Category,verbose_name='分类', on_delete=models.CASCADE, related_name='article_relate')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)


    '''
    # 返回文章阅读计数
    def get_read_num(self):
        try:
            return self.readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0
    '''
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']
        verbose_name = '文章'
        verbose_name_plural = verbose_name
'''
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    article = models.OneToOneField(Article,on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = '阅读计数'
        verbose_name_plural = verbose_name
'''

class Tags:
    pass