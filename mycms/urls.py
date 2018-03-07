# coding: UTF-8
from django.urls import re_path, path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

from .views import IndexView
from .views import ArticleView, CreateArticleView, UpdateArticleView, DeleteArticleView
from .views import MyPageView


urlpatterns = [
  path('article/<pk>/', ArticleView.as_view(), name='article'),
  re_path(r'^new_article$', CreateArticleView.as_view(), name='new_article'),
  path('edit_article/<pk>/', login_required(UpdateArticleView.as_view()), name='edit_article'),
  path('delete_article/<pk>/', login_required(DeleteArticleView.as_view()), name='delete_article'),

  re_path(r'^$', IndexView.as_view(), name='index'),
  re_path(r'^mypage$', login_required(MyPageView.as_view()) , name='mypage'),
  re_path(r'^login$', auth_views.login, {'template_name': 'mycms/login.html'}, name='login'),
  re_path(r'^logout$', auth_views.logout, name='logout')
]