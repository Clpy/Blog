from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions

# Create your models here.
class ReadNum(models.Model):
    read_num = models.IntegerField('阅读计数',default=0)  # 定义文章的阅读次数

    # 获取内容类型也就是==分类
    content_type = models.ForeignKey(
        ContentType,
        verbose_name='内容类型',
        on_delete=models.DO_NOTHING
    )  # 连接于ContentType
    object_id = models.PositiveIntegerField('对象id') # 记录所对应的模型的实例的id号
    content_object = GenericForeignKey()  # 默认传入content_type, object_id

    def __str__(self):
        return self.read_num

    class Meta:
        verbose_name = '计数'
        verbose_name_plural = verbose_name


class ReadNumExpandMethod():
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0