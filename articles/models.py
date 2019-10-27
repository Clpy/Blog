from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    category_name = models.CharField('类名', max_length=15)

    def __str__(self):
        return self.category_name

class Article(models.Model):
    title = models.CharField('标题', max_length=50)
    content = models.TextField('内容')
    category = models.ForeignKey(Category,verbose_name='分类',
                                 on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='作者',
                               on_delete=models.CASCADE)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']

class Tags:
    pass