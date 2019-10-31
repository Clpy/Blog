from django.shortcuts import render, get_object_or_404
from .models import Article, Category
from django.core.paginator import Paginator

# Create your views here.
def article_list(request):
    article_all_list = Article.objects.all()
    paginator = Paginator(article_all_list,7)  # 每10篇 进行分页
    page_num = request.GET.get('page', 1)  # 获取url的页面参数(请求的页码)
    current_page_articles = paginator.get_page(page_num)  # 当前页的文章
    current_page_num = current_page_articles.number # 获取当前页码

    # 获取当前页码前后各两页的范围
    # page_range = list(range(max(current_page_num - 2, 1), current_page_num)) \
                 # + list(range(current_page_num, min(current_page_num + 2,
                                                    # paginator.num_pages) + 1))
    page_range = [x for x in range(current_page_num - 2, current_page_num + 3) if
       (x > 0 and x < paginator.num_pages + 1)]  # paginator.num_pages 获得总页数

    # 加入省略号标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加入首页和尾页页码
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    categorys = Category.objects.all()  #获取分类的类中所有数据
    article_dates = Article.objects.dates('created_time', 'month', order="DESC")
    articles_list = current_page_articles.object_list
    context = {
        'current_page_articles': current_page_articles,
        'categorys': categorys,
        'articles_list': articles_list,
        'page_range': page_range,
        'article_dates': article_dates,
    }
    return render(request,'article_list.html', context)


def article_detail(request, article_pk):
    """
    :param request:
    :param article_pk: 文章主键
    :return:
    """
    article = get_object_or_404(Article, pk=article_pk)
    previous_article = Article.objects.filter(
        created_time__lt=article.created_time).first()  # 上一篇文章
    next_article = Article.objects.filter(
        created_time__gt=article.created_time).last() # 下一篇文章
    context = {
        'article': article,
        'previous_article': previous_article,
        'next_article': next_article
    }
    return render(request, 'article_detail.html', context)


def article_category(request, category_pk):
    # 查询pk=category_pk参数的分类
    category = get_object_or_404(Category, pk=category_pk)
    con_category = Article.objects.filter(category=category)  # 查找属于同一分类的文章
    categorys_all = Category.objects.all()  # 返回分类的类的全部数据
    context = {
        'articles_list': con_category,
        'category': category,
        'categorys_all': categorys_all
    }
    return render(request, 'category_article.html', context)

# 按月归档
def date_archive(request, year, month):
    """

    :param request:
    :param year: 年
    :param month: 月
    :return:
    """
    article_all_list = Article.objects.filter(created_time__year=year,
                                            created_time__month=month)
    paginator = Paginator(article_all_list, 7)  # 每7篇 进行分页
    page_num = request.GET.get('page', 1)  # 获取url的页面参数(请求的页码)
    current_page_articles = paginator.get_page(page_num)  # 当前页的文章
    current_page_num = current_page_articles.number  # 获取当前页码

    # 获取当前页码前后各两页的范围
    # page_range = list(range(max(current_page_num - 2, 1), current_page_num)) \
    # + list(range(current_page_num, min(current_page_num + 2,
    # paginator.num_pages) + 1))
    page_range = [x for x in range(current_page_num - 2, current_page_num + 3)
                  if
                  (
                              x > 0 and x < paginator.num_pages + 1)]  # paginator.num_pages 获得总页数

    # 加入省略号标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加入首页和尾页页码
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    categorys = Category.objects.all()  # 获取分类的类中所有数据
    articles = current_page_articles.object_list  # 文章显示列表
    article_dates = Article.objects.dates(
        'created_time',
        'month',
        order="DESC"
    )
    article_of_date = '{}年{}月'.format(year, month)  # 文章日期
    context = {
        'current_page_articles': current_page_articles,
        'categorys': categorys,
        'articles_list': articles,  # 文章显示列表
        'page_range': page_range,
        'article_of_date': article_of_date,
        'article_dates': article_dates
    }
    return render(request, 'date_archive.html', context)