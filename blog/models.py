from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    '''
    分类
    '''
    name = models.CharField(max_length=100)


class Tag(models.Model):
    '''
    标签
    '''
    name = models.CharField(max_length=100)


class Post(models.Model):
    '''
    文章
    '''
    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200, blank=True)  # 摘要
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

