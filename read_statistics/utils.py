# coding=utf-8
from .models import ReadNum
from django.contrib.contenttypes.models import ContentType


def read_statistics_once_read(request, obj):
    '''
    :param request:
    :param obj: 接收传递过来的模型
    :return:
    '''
    ct = ContentType.objects.get_for_model(obj)  # 告诉ContentType,要和obj这个模型创建连接
    key = "{}_{}_read".format(ct.model, obj.pk)

    # 提取浏览器中的cookie,如果不存在cookie
    if not request.COOKIES.get(key):
        if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
            # 存在记录
            readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        else:
            # 不存在对应的记录
            readnum = ReadNum(content_type=ct, object_id=obj.pk)
        # 计数加1
        readnum.read_num += 1
        readnum.save()
    return key
