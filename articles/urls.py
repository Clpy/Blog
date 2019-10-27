from django.urls import path
from . import views
urlpatterns = [
    path('', views.article_list, name="article_list"),
    path('<int:article_pk>/', views.article_detail, name="article_detail"),
    path('category/<int:category_pk>', views.category_article,
         name="category_article")
]
