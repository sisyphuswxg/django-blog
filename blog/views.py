from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def index(request):
    context = {
        'title': '我的博客首页',
        'welcome': '欢迎访问我的博客首页',
    }
    # return HttpResponse("欢迎访问我的博客首页！")
    return render(request, 'blog/index.html', context=context)