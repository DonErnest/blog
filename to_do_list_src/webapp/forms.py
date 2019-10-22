from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import Comment, Article, Tag

CHOICE_DEFAULT = 'title'
CHOICE_TAG = 'tags'
CHOICE_TEXT = 'text'
CHOICE_COMMENTS = 'comments'

SEARCH_CHOICES= [(CHOICE_DEFAULT, 'по названию'),(CHOICE_TAG, 'по тегам'),
                  (CHOICE_TEXT,'по содержанию'), (CHOICE_COMMENTS,'по комментариям')]
AUTHOR_CHOICE_DEFAULT = 'articles'
AUTHOR_COMMENT = 'comments'
AUTHOR_CHOICES = [(AUTHOR_CHOICE_DEFAULT, 'по автору статьи'),(AUTHOR_COMMENT, 'по автору комментария')]

class ArticleForm(forms.ModelForm):
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
    class Meta:
        model = Comment
        fields=['author', 'text']
        labels={'text': 'Комментарий', 'author': 'Автор'}

class SearchForm(forms.Form):
    search_text = forms.CharField(max_length=100, required=False, label='Текст')
    search_text_choices = forms.MultipleChoiceField(choices=SEARCH_CHOICES, initial=[c[0] for c in SEARCH_CHOICES[:-1]],
                                            required=False,
                                            widget=forms.CheckboxSelectMultiple(choices=SEARCH_CHOICES))
    search_author = forms.CharField(max_length=40, required=False, label='Автор')
    search_author_choices = forms.MultipleChoiceField(choices=AUTHOR_CHOICES, initial=AUTHOR_CHOICE_DEFAULT,
                                              required=False,
                                              widget=forms.CheckboxSelectMultiple(choices=(AUTHOR_CHOICES)))

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        if cleaned_data['search_text']=='' and cleaned_data['search_author']=='':
            raise ValidationError('Хотя бы одно из полей поиска должно быть заполнено!')
        return cleaned_data

    def clean_search_text_choices(self):
        search_text = self.cleaned_data['search_text']
        search_text_choices = self.cleaned_data['search_text_choices']
        if search_text and not search_text_choices:
            raise ValidationError('Нужно поставить хотя бы одну галочку при поиске по тексту!')
        return search_text_choices

    def clean_search_author_choices(self):
        search_author = self.cleaned_data['search_author']
        search_author_choices = self.cleaned_data['search_author_choices']
        if search_author and not search_author_choices:
            raise ValidationError('Нужно поставить хотя бы одну галочку при поиске по автору!')
        return search_author_choices