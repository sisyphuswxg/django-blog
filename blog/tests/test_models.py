# -*- coding: utf-8 -*-

# Author: wangxuguang11
# Date: 2021/11/10 11:43 AM 
# Desc: 存放和模型有关的单元测试


from django.apps import apps
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from ..models import Post, Category, Tag


class PostModelTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_superuser(username='admin',
                                             email='admin@hellogithub.com',
                                             password='admin')

        cate = Category.objects.create(name='测试')
        self.post = Post.objects.create(title='测试标题',
                                        body='测试内容',
                                        category=cate,
                                        author=user,
                                        )

    def test_str_representation(self):
        self.assertEqual(self.post.__str__(), self.post.title)

    def test_auto_populate_modified_time(self):
        self.assertIsNotNone(self.post.modified_time)

        old_post_modified_time = self.post.modified_time
        self.post.body = '新的测试内容'
        self.post.save()
        self.post.refresh_from_db()
        self.assertTrue(self.post.modified_time > old_post_modified_time)

    def test_auto_populate_excerpt(self):
        self.assertIsNotNone(self.post.excerpt)
        self.assertTrue(0 < len(self.post.excerpt) <= 54)

    def test_get_absolute_url(self):
        expected_url = reverse('blog:detail', kwargs={'pk': self.post.pk})
        self.assertEqual(self.post.get_absolute_url(), expected_url)

    def test_increase_views(self):
        self.post.increase_views()
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 1)

        self.post.increase_views()
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 2)


class CategoryModelTestCase(TestCase):
    def setUp(self):
        self.cate = Category.objects.create(name="测试")

    def test_str_representation(self):
        self.assertEqual(self.cate.__str__(), self.cate.name)


class TagModelTestCase(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="测试")

    def test_str_representation(self):
        self.assertEqual(self.tag.__str__(), self.tag.name)
