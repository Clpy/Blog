from django.contrib import admin
from articles.models import Article, Category, Tags, ReadNum

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'author',
        'get_read_num',
        'created_time',
        'update_time'
    )

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = (
        'article',
        'read_num',
    )