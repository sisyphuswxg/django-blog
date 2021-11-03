import markdown
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags


class Category(models.Model):
    '''
    分类
    '''
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    '''
    标签
    '''
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    '''
    文章
    '''
    # title = models.CharField(max_length=70)
    # body = models.TextField()
    # created_time = models.DateTimeField()
    # modified_time = models.DateTimeField()
    # excerpt = models.CharField(max_length=200, blank=True)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # tags = models.ManyToManyField(Tag, blank=True)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 中文展示 ↓↓↓
    title = models.CharField('标题', max_length=70)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', default=timezone.now)   # 给一个默认时间，取当前时间
    modified_time = models.DateTimeField('修改时间')
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '文章'  # verbose_name 指定对应的model在admin后台的显示名称
        verbose_name_plural = verbose_name  # 复数展示形式，中文无复数表现形式，这里和verbose_name一样展示

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        '''
        修改时间：
        注意：修改时间不能和创建时间一样使用默认值，因为当模型数据第二次修改时，
             modified_time以为有第一次的默认值，第二次就不会生效。
             -> 每一个Model都有一个save()方法，包含了将model数据保存到数据库的逻辑。
        '''
        self.modified_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body)[:54])
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        '''
        reverse() 函数会解析视图函数对应的url,如若Post的id是12，则函数返回的就是/posts/12
        '''
        return reverse('blog:detail', kwargs={'pk': self.pk})
