# -*- coding: utf-8 -*-

# Author: wangxuguang11
# Date: 2021/11/1 4:33 PM 
# Desc: XXXX


from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
]