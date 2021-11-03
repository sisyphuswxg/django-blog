import re

import markdown
from django.shortcuts import render, get_object_or_404

from .models import Post


def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context=context)


def detail(request, pk):
    '''
    get_object_or_404():
        - 当传入的 pk 对应的 Post 在数据库存在时，就返回对应的 post
        - 如果不存在，就给用户返回一个 404 错误，表明用户请求的文章不存在
    markdown:
        - extra：基础扩展
        - codehilite：语法高亮扩展
        - toc：自动生成目录
    '''
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.fenced_code',
        'markdown.extensions.toc',
    ])
    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/detail.html', context={'post': post})