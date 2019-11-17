# coding=utf-8
import datetime
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data,\
    get_today_hot_data, get_yesterday_hot_data
from django.contrib.auth import login, authenticate
from articles.models import Article
from django.db.models import Sum
from django.utils import timezone
from django.urls import reverse

def get_7_days_hot_articles():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    articles = Article.objects\
        .filter(read_details__date__lt=today,read_details__date__gte=date)\
        .values('id','title')\
        .annotate(read_num_sum = Sum('read_details__read_num'))\
        .order_by('-read_num_sum')

    return articles[:7]


def index(request):
    article_content_type = ContentType.objects.get_for_model(Article)  # 获取模型类
    dates, read_nums = get_seven_days_read_data(article_content_type)
    today_hot_data = get_today_hot_data(article_content_type)
    yesterday_hot_data = get_yesterday_hot_data(article_content_type)

    # 获取7天热门文章的缓存数据
    hot_articles_for_7_days = cache.get('hot_articles_for_7_days')
    if hot_articles_for_7_days is None:
        hot_articles_for_7_days = get_7_days_hot_articles()
        cache.set('hot_articles_for_7_days', hot_articles_for_7_days, 3600)

    context = {
        'read_nums': read_nums,
        'dates': dates,
        'today_hot_data': today_hot_data,
        'yesterday_hot_data': yesterday_hot_data,
        'hot_articles_for_7_days': hot_articles_for_7_days,
    }
    return render(request, 'index.html', context)


def landing_page(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(request, username=username, password=password)
    referer = request.META.get('HTTP_REFERER', reverse('index'))  # 根据请求头获取信息
    if user is not None:
        login(request, user)
        return redirect(referer)
    else:
        return render(request, 'error.html', {
            'message':'用户名或密码不正确'
        })