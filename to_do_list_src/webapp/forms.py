from django import forms
from django.forms import widgets

from webapp.models import Comment, Article, Tag

SEARCH_CHOICE_DEFAULT = 'title_author'
SEARCH_CHOICE_TAG = 'tags'
SEARCH_CHOICES= [(SEARCH_CHOICE_DEFAULT, 'по названию или автору'),(SEARCH_CHOICE_TAG, 'по тегам')]


class ArticleForm(forms.ModelForm):
    tags = forms.CharField(max_length=500, label='Теги', required=False)

    class Meta:
        model=Article
        exclude=['created_at', 'updated_at']

    # def clean_tags(self):
    #     tag_queryset = []
    #     print("These are tags", self.cleaned_data['tags'])
    #     tags = self.cleaned_data['tags']
    #     for tag in tags:
    #         if tag.strip() == "":
    #             tags.remove(tag)
    #         Tag.objects.get_or_create(name=tag)
    #         tag_queryset.append(Tag.objects.get(name=tag))
    #     return tag_queryset


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=['article', 'text', 'author']
        labels={'article': 'Статья', 'text': 'Комментарий', 'author': 'Автор'}


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=['author', 'text']
        labels={'text': 'Комментарий', 'author': 'Автор'}

class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Поиск')
    search_field = forms.ChoiceField(choices=SEARCH_CHOICES)
    