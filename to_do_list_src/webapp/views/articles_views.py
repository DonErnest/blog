from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.http import urlencode

from webapp.forms import ArticleForm, CommentForm, ArticleCommentForm, SearchForm, CHOICE_DEFAULT, \
    CHOICE_TAG
from webapp.models import Article, Tag

from django.views.generic import View, RedirectView, ListView, DetailView, CreateView, UpdateView


class IndexView(ListView):
    template_name = 'index.html'
    model = Article
    context_object_name = 'articles'
    ordering = ['-created_at']
    paginate_by = 6
    paginate_orphans = 1
    form = SearchForm
# - по умолчанию имеет это значение, означает , что страницы бдут передаваться под данным названием
# model, queryset и метод get queryset - взимоисключащие параметры. Можно использовать любой из них , вместо остальных
# allow_empty - параметр, определяющий, будет ли выводиться страница с пустым списком. По умолчанию True , т.е. будет.
# Если переопределить False, то вместо вывода пустой страницы будет выходить ошибка 404

    # def get(self, request, *args, **kwargs):
    #     self.form = self.get_search_form()
    #     self.search_value = self.get_search_value()
    #     return super().get(request, *args, **kwargs)
    #
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     if self.search_value:
    #         if self.search_value['search_field'] == SEARCH_CHOICE_DEFAULT:
    #             queryset = queryset.filter(
    #                 Q(title__icontains=self.search_value['search'])
    #                 | Q(author__icontains=self.search_value['search'])
    #             ).distinct()
    #         elif self.search_value['search_field'] == SEARCH_CHOICE_TAG:
    #             queryset = queryset.filter(
    #                 Q(tags__name__iexact=self.search_value['search'])
    #             )
    #     return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        # if self.search_value:
        #     context['query'] = urlencode({'search': self.search_value})
        return context

    # def get_search_form(self):
    #     return SearchForm(data=self.request.GET)
    #
    # def get_search_value(self):
    #     if self.form.is_valid():
    #         search = {'search': self.form.cleaned_data['search'], 'search_field': self.form.cleaned_data['search_field'] }
    #         return search
    #     return None


class IndexRedirectView(RedirectView):
    pattern_name = 'index'



class ArticleView(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'article/article_view.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object
        comments = article.comments.filter(article_id=article.pk).order_by('-created_at')
        tags = article.tags.all()
        context['form'] = ArticleCommentForm()
        paginator = Paginator(comments, 3, 0)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        context['paginator'] = paginator
        context['page_obj'] = page
        context['comments'] = page.object_list
        context['is_paginated'] = page.has_other_pages()
        context['tags'] = tags
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    form_class = ArticleForm
    model = Article
    template_name = 'article/article_create.html'


    def get_success_url(self):
        return reverse('article_view', kwargs= {'pk': self.object.pk})

    def get_tags(self, form):
        tags = form.cleaned_data['tags'].split(',')
        tag_queryset = []
        for tag in tags:
            if tag.strip() == "":
                tags.remove(tag)
            Tag.objects.get_or_create(name=tag)
            tag_queryset.append(Tag.objects.get(name=tag))
        return tag_queryset

    def form_valid(self, form):
        tags = self.get_tags(form)
        form.cleaned_data.pop('tags')
        self.object = form.save()
        self.object.tags.add(*tags)
        self.object.save()
        return super().form_valid(form)


class ArtUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ArticleForm
    model = Article
    template_name = 'article/article_update_view.html'

    def get_success_url(self):
        return reverse('article_view', kwargs= {'pk': self.object.pk})

    def get_tags(self, form):
        tags = form.cleaned_data['tags'].split(',')
        tag_queryset = []
        for tag in tags:
            if tag.strip() == "":
                tags.remove(tag)
            Tag.objects.get_or_create(name=tag)
            tag_queryset.append(Tag.objects.get(name=tag))
        return tag_queryset

    def get_tag_list(self):
        name_list=[]
        tag_list = Tag.objects.filter(articles__title=self.object.title).values('name')
        for name in tag_list:
            name_list.append(name.get('name'))
        tags = ','.join(name_list)
        return tags

    def form_valid(self, form):
        tags = self.get_tags(form)
        form.cleaned_data.pop('tags')
        self.object = form.save()
        self.object.tags.clear()
        self.object.tags.add(*tags)
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
            tags=self.get_tag_list()
            if tags:
                kwargs['form'] = self.form_class(data={'title': self.object.title, 'text': self.object.text,
                                                   'author': self.object.author, 'tags': tags})
            else:
                kwargs['form'] = self.form_class(data={'title': self.object.title, 'text': self.object.text,
                                                       'author': self.object.author, 'tags': None })
        return super().get_context_data(**kwargs)


class ArtDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(data={'title': article.title, 'text': article.text, 'author': article.author})
        return render(request, 'article/delete_view.html', context={'form': form, 'article': article})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return redirect('index')