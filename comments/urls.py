from django.urls import path
from comments import views


urlpatterns = [
    path('submit_comment', views.submit_comment, name='submit_comment')
]
