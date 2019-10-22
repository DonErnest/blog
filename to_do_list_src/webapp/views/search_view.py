from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, TemplateView, FormView

from webapp.forms import SearchForm, CHOICE_DEFAULT, CHOICE_TAG, CHOICE_COMMENTS, CHOICE_TEXT, AUTHOR_CHOICE_DEFAULT, \
    AUTHOR_COMMENT
from webapp.models import Article




class SearchView(FormView):
    template_name = 'search_index.html'
    form_class = SearchForm


    def form_valid(self, form):
        text = form.cleaned_data['search_text']
        author = form.cleaned_data['search_author']
        query, query_2 = self.get_text_author_search_query(form, text, author)
        context = self.get_context_data(form=form)
        # context['articles']=Article.objects.filter(query & query_2).distinct()
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