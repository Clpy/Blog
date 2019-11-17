from django.db import models
from articles.models import Article
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()  # 评论对象

    comment_content = models.TextField('评论内容', max_length=140)
    comment_time = models.DateTimeField('评论时间', auto_now_add=True)
    commenter = models.ForeignKey(User, verbose_name='评论人', on_delete=models.DO_NOTHING)

    class Meta():
        ordering = ['-comment_time']
        verbose_name = '评论'
        verbose_name_plural = verbose_name
