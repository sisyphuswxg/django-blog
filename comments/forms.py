from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """
    存放表单代码
        model = Comment -> 表示这个表单对应的数据库模型是Comment类；
        fields 指定了表单需要显示的字段；
    """
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']

