from django.shortcuts import render, get_object_or_404
from .models import Article, Category
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
import markdown
from read_statistics.utils import read_statistics_once_read
from comments.models import Comment
from comments.forms import CommentForm

# Create your views here.
def article_list(request):
    '''
    :param request:
    :return:
    '''
    article_all_list = Article.objects.all()
    paginator = Paginator(article_all_list,6)  # 每10篇 进行分页
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

    # 获取文章分类的对应文章数量
    '''
    categorys = Category.objects.all()  #获取所有分类
    article_categorys_list = []
    for category in categorys:
        category.article_count = Article.objects.filter(
            category=category).count()
        article_categorys_list.append(category)
    '''
    # annotate 拓展查询字段
    categorys = Category.objects.annotate(article_count=Count('article_relate'))

    # 获取日期归档的对应文章数量
    article_dates = Article.objects.dates('created_time', 'month', order="DESC")
    article_date_dict = {}
    for article_date in article_dates:
        article_count = Article.objects.filter(
            created_time__year=article_date.year,
            created_time__month=article_date.month
        ).count()
        article_date_dict[article_date] = article_count


    articles_list = current_page_articles.object_list
    context = {
        'current_page_articles': current_page_articles,
        'categorys': categorys,
        'articles_list': articles_list,
        'page_range': page_range,
        'article_dates': article_date_dict,
    }
    return render(request,'article_list.html', context)


def article_detail(request, article_pk):
    """
    :param request:
    :param article_pk: 文章主键,从http://127.0.0.1:8000/articles/36/传递
    :return:
    """
    article = get_object_or_404(Article, pk=article_pk)  # Article.objects.get(pk=article_pk)
    read_cookie_key = read_statistics_once_read(request, article)  # 取出article实例之后传递

    previous_article = Article.objects.filter(created_time__lt=article.created_time).first()  # 上一篇文章
    next_article = Article.objects.filter(created_time__gt=article.created_time).last() # 下一篇文章

    article_content_type = ContentType.objects.get_for_model(article)  # 通过modle或model的实例来寻找ContentType类型
    comments = Comment.objects.filter(content_type=article_content_type, object_id=article.pk)

    # 渲染markdown文档
    article.content = markdown.markdown(
        article.content, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    comment_form = CommentForm(initial={
        'content_type': article_content_type.model,
        'object_id': article_pk,
    })  # 实例化一个form

    context = {
        'article': article,
        'previous_article': previous_article,
        'next_article': next_article,
        'comments': comments,
        'comment_form': comment_form,
    }

    response = render(request, 'article_detail.html', context)  # 响应
    response.set_cookie(read_cookie_key, 'true', max_age=60*60*12)  # 阅读cookie标记
    return response


def article_category(request, category_pk):
    # 查询pk=category_pk参数的分类
    category = get_object_or_404(Category, pk=category_pk)
    con_category = Article.objects.filter(category=category)  # 查找属于同一分类的文章
    categorys_all = Category.objects.all()  # 返回分类的类的全部数据
    context = {
        'articles_list': con_category,
        'category': category,
        'categorys_all': categorys_all,
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
                                              created_time__month=month)  #
    # 查询本年月所有文章列表
    paginator = Paginator(article_all_list, 2)  # 每7篇 进行分页
    page_num = request.GET.get('page', 1)  # 获取url的页面参数(请求的页码)
    current_page_articles = paginator.get_page(page_num)  # 当前页的文章
    current_page_num = current_page_articles.number  # 获取当前页码
    page_range = [x for x in range(current_page_num - 2, current_page_num + 3)
                  if(x > 0 and x < paginator.num_pages + 1)]  # paginator.num_pages 获得总页数

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