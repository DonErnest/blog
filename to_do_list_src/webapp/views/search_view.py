from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import ListView, TemplateView, FormView

from webapp.forms import SearchForm, CHOICE_DEFAULT, CHOICE_TAG, CHOICE_COMMENTS, CHOICE_TEXT, AUTHOR_CHOICE_DEFAULT, \
    AUTHOR_COMMENT
from webapp.models import Article




class SearchView(FormView):
    template_name = 'search_index.html'
    form_class = SearchForm

    # def form_valid(self, form):
    #     query= urlencode(form.cleaned_data)
    #     url = reverse('advanced search results') + '?'+query
    #     return redirect(url)


# class SearchResultsView(ListView):
#     model = Article
#     template_name = 'search_index.html'
    # context_object_name = 'articles'
    # paginate_by = 5
    # paginate_orphans = 2
    #
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     form = SearchForm(data=self.request.GET)
    #     if form.is_valid():
    #         query = self.get_text_query(form) & self.get_author_query(form)
    #         queryset = queryset.filter(query).distinct()
    #     return queryset
    #
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     form = SearchForm(data=self.request.GET)
    #     query = self.get_query_string()
    #     return super().get_context_data(
    #         form=form, query=query, object_list=object_list, **kwargs
    #     )
    #
    # def get_query_string(self):
    #     data = {}
    #     for key in self.request.GET:
    #         if key != 'page':
    #             data[key] = self.request.GET.get(key)
    #     return urlencode(data)
    #
    # def get_text_query(self, form):
    #     query = Q()
    #     text = form.cleaned_data['search_text']
    #     if text:
    #         if CHOICE_DEFAULT in form.cleaned_data['search_text_choices']:
    #             query = query | Q(title__icontains=text)
    #         if CHOICE_TEXT in form.cleaned_data['search_text_choices']:
    #             query = query | Q(text__icontains=text)
    #         if CHOICE_TAG in form.cleaned_data['search_text_choices']:
    #             query = query | Q(tags__name__iexact=text)
    #         if CHOICE_COMMENTS in form.cleaned_data['search_text_choices']:
    #             query = query | Q(comments__text__icontains=text)
    #     return query
    #
    # def get_author_query(self, form):
    #     query_2 = Q()
    #     author = form.cleaned_data['search_author']
    #     if author:
    #         if AUTHOR_CHOICE_DEFAULT in form.cleaned_data['search_author_choices']:
    #             query_2 = query_2 | Q(author__iexact=author)
    #         if AUTHOR_COMMENT in form.cleaned_data['search_author_choices']:
    #             query_2 = query_2 | Q(comments__author__iexact=author)
    #     return query_2



    def form_valid(self, form):
        text = form.cleaned_data['search_text']
        author = form.cleaned_data['search_author']
        query, query_2 = self.get_text_author_search_query(form, text, author)
        context = self.get_context_data(form=form)
        articles = Article.objects.filter(query & query_2).distinct()
        self.paginate_articles_to_context(articles, context)
        return self.render_to_response(context=context)

    def get_text_author_search_query(self, form, text, author):
        query = Q()
        query_2 = Q()
        if text:
            if CHOICE_DEFAULT in form.cleaned_data['search_text_choices']:
                query = query | Q(title__icontains=text)
            if CHOICE_TEXT in form.cleaned_data['search_text_choices']:
                query = query | Q(text__icontains=text)
            if CHOICE_TAG in form.cleaned_data['search_text_choices']:
                query = query | Q(tags__name__iexact=text)
            if CHOICE_COMMENTS in form.cleaned_data['search_text_choices']:
                query = query | Q(comments__text__icontains=text)

        if author:
            if AUTHOR_CHOICE_DEFAULT in form.cleaned_data['search_author_choices']:
                query_2 = query_2 | Q(author__iexact=author)
            if AUTHOR_COMMENT in form.cleaned_data['search_author_choices']:
                query_2 = query_2 | Q(comments__author__iexact=author)
        return query, query_2

    def paginate_articles_to_context(self, articles, context):
        paginator = Paginator(articles, 3, 0)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        context['paginator'] = paginator
        context['page_obj'] = page
        context['articles'] = page.object_list
        context['is_paginated'] = page.has_other_pages()