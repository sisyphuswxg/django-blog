# -*- coding: utf-8 -*-

# Author: wangxuguang11
# Date: 2021/11/3 8:05 PM 
# Desc: XXXX


from django import template
from django.db.models import Count

from ..models import Post, Category, Tag

register = template.Library()


# 最新文章模板标签
@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
    }


# 归档模板标签
@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    date_list = Post.objects.dates('created_time', 'month', order='DESC')
    return {
        'date_list': date_list
    }


# 分类模板标签
@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    return {
        'category_list': Category.objects.all(),
    }


# 标签云模板标签
@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tag_list': Tag.objects.all(),
    }


@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
    }


@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }