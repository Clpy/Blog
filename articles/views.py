from django.shortcuts import render, get_object_or_404
from .models import Article, Category
from django.core.paginator import Paginator

# Create your views here.
def article_list(request):
    # 通过获取get请求来获取url的页面参数
    article_all_list = Article.objects.all()
    paginator = Paginator(article_all_list,10)  # 每10篇 进行分页
    page_num = request.GET.get('page', 1)
    # 分页展示的文章
    page_of_articles = paginator.get_page(page_num)

    # page_of_articles
    categorys = Category.objects.all()
    articles_list = page_of_articles.object_list
    context = {
        'articles': page_of_articles,
        'categorys': categorys,
        'articles_list': articles_list
    }
    return render(request,'article_list.html', context)


def article_detail(request, article_pk):
    """
    :param request:
    :param article_pk: 文章主键
    :return:
    """
    article = get_object_or_404(Article, pk=article_pk)
    context = {
        'article': article
    }
    return render(request, 'article_detail.html', context)


def category_article(request, category_pk):
    # 查询pk=category_pk参数的分类
    category = get_object_or_404(Category, pk=category_pk)
    # 查找同一分类的文章
    articles = Article.objects.filter(category=category)
    # 查找分类
    categorys = Category.objects.all()
    context = {
        'articles': articles,
        'category': category,
        'categorys': categorys
    }
    return render(request, 'category_article.html', context)