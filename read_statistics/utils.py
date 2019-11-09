# coding=utf-8
import datetime
from django.utils import timezone
from .models import ReadNum, ReadDetail
from django.db.models import Sum
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
        # 总阅读数加1
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        # 计数加1
        readnum.read_num += 1
        readnum.save()

        date = timezone.now().date()
        readdetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readdetail.read_num += 1
        readdetail.save()

    return key

def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)  # 获取相隔i天的日期
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)  # 获取阅读明细
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result.get('read_num_sum') or 0)

    return dates, read_nums