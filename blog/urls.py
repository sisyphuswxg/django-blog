# -*- coding: utf-8 -*-

# Author: wangxuguang11
# Date: 2021/11/1 4:33 PM 
# Desc: XXXX


from django.urls import path

from . import views


app_name = 'blog'
urlpatterns = [
    # path('posts/', views.index, name='index'),
    path('posts/', views.IndexView.as_view(), name='index'),

    # path('posts/<int:pk>', views.detail, name='detail'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='detail'),

    # path('posts/archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('posts/archives/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive'),

    # path('categories/<int:pk>/', views.category, name='category'),
    path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),

    # path('tags/<int:pk>/', views.tag, name='tag'),
    path('tags/<int:pk>/', views.TagView.as_view(), name='tag'),
]