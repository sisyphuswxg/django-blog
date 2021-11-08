import re

import markdown
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from markdown.extensions.toc import TocExtension

from .models import Post, Category, Tag


# def index(request):
#     post_list = Post.objects.all().order_by('-created_time')
#     context = {'post_list': post_list}
#     return render(request, 'blog/index.html', context=context)
# use ListView ↓↓↓
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'


# def archive(request, year, month):
#     """
#     归档： 年-月
#     """
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month
#                                     ).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})
# use ListView/IndexView ↓↓↓
class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        return super(ArchiveView, self).get_queryset().filter(created_time__year=year,
                                                              created_time__month=month)


# def category(request, pk):
#     '''
#     分类: category过滤获取
#     '''
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})
# use ListView ↓↓↓
# class CategoryView(ListView):
#     model = Post
#     template_name = 'blog/index.html'
#     context_object_name = 'post_list'
#
#     def get_queryset(self):
#         cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
#         return super(CategoryView, self).get_queryset().filter(category=cate)
# -> 可以直接让CategoryView继承IndexView（属性都是一样的）
class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


# def tag(request, pk):
#     '''
#     标签: tag过滤获取
#     '''
#     tag = get_object_or_404(Tag, pk=pk)
#     post_list = Post.objects.filter(tags=tag).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})
# use ListView/IndexView ↓↓↓
class TagView(IndexView):
    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get("pk"))
        return super(TagView, self).get_queryset().filter(tags=t)


# def detail(request, pk):
#     '''
#     get_object_or_404():
#         - 当传入的 pk 对应的 Post 在数据库存在时，就返回对应的 post
#         - 如果不存在，就给用户返回一个 404 错误，表明用户请求的文章不存在
#     markdown:
#         - extra：基础扩展
#         - codehilite：语法高亮扩展
#         - toc：自动生成目录
#     '''
#     post = get_object_or_404(Post, pk=pk)
#
#     # 阅读量+1
#     post.increase_views()
#
#
#     md = markdown.Markdown(extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.fenced_code',
#         'markdown.extensions.toc',
#     ])
#     post.body = md.convert(post.body)
#     m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
#     post.toc = m.group(1) if m is not None else ''
#     return render(request, 'blog/detail.html', context={'post': post})
# -> DetailView
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)

        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''

        return post