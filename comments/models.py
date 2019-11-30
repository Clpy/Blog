from django.db import models
from articles.models import Article
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()  # 评论对象

    comment_content = models.TextField('评论内容', max_length=140)
    comment_time = models.DateTimeField('评论时间', auto_now_add=True)
    commenter = models.ForeignKey(User, related_name="comments",
                                  verbose_name='评论人', on_delete=models.DO_NOTHING)  # 评论人

    root = models.ForeignKey('self', related_name='root_comment',
                             null=True, on_delete=models.DO_NOTHING)  # 记录评论树的最顶级的评论
    parent = models.ForeignKey('self', related_name='parent_comment',
                               null=True, on_delete=models.DO_NOTHING)  # 外键指向自己
    reply_to = models.ForeignKey(User, related_name="replies",
                                 null=True, on_delete=models.DO_NOTHING)  # 回复谁（哪个评论人）的评论

    def __str__(self):
        return self.comment_content

    class Meta():
        ordering = ['-comment_time']
        verbose_name = '评论'
        verbose_name_plural = verbose_name
