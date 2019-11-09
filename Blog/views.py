# coding=utf-8
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data
from articles.models import Article

def index(request):
    article_content_type = ContentType.objects.get_for_model(Article)  # 获取模型类
    dates, read_nums = get_seven_days_read_data(article_content_type)
    context = {
        'read_nums': read_nums,
        'dates': dates
    }
    return render(request, 'index.html',context)