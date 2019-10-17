from django import forms
from django.forms import widgets

from webapp.models import Comment, Article


class ArticleForm(forms.ModelForm):
    # title = forms.CharField(max_length=200, label = 'Title', required= True)
    # author = forms.CharField(max_length=40, label='Author', required=True)
    # text= forms.CharField(max_length=3000, label='Text', required=True, widget=widgets.Textarea)
    tags = forms.CharField(max_length=500, label='Теги', required=False)

    class Meta:
        model=Article
        exclude=['created_at', 'updated_at']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=['article', 'text', 'author']
        labels={'article': 'Статья', 'text': 'Комментарий', 'author': 'Автор'}


class ArticleCommentForm(forms.ModelForm):
    # author = forms.CharField(max_length=40, required=False, label='Author', initial='Аноним')
    # text = forms.CharField(max_length=400, required=True, label='Text',
    #                        widget=widgets.Textarea)

    class Meta:
        model = Comment
        fields=['author', 'text']
        labels={'text': 'Комментарий', 'author': 'Автор'}

class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Поиск')
    