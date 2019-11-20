# coding=utf-8
import datetime

from django.contrib import auth
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data,\
    get_today_hot_data, get_yesterday_hot_data
from django.contrib.auth import authenticate
from articles.models import Article
from django.db.models import Sum
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import LoginForm, RegForm
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


def login(request):
    if request.method == 'POST':  # 如果是提交数据
        login_form = LoginForm(request.POST)  # 提交数据是否有效
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('index')))

    else:  # 其他是加载页面的行为
        login_form = LoginForm()

    context = {
        'login_form': login_form
    }
    return render(request, 'login.html', context)


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            email = reg_form.cleaned_data['email']
            # 创建用户
            user = User.objects.create_user(username,password,email)
            user.save()
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('form', reverse('index')))  # 跳转到注册之前的页面
    else:
        reg_form = RegForm()

    context = {
        'reg_form': reg_form
    }
    return render(request, 'register.html', context)
