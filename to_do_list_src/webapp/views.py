from django.shortcuts import render, get_object_or_404, redirect

from webapp.forms import ArticleForm
from webapp.models import Article

from django.views.generic import View
from django.views.generic import TemplateView, RedirectView


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()
        return context


class IndexRedirectView(RedirectView):
    pattern_name = 'index'


class ArticleView(TemplateView):
    template_name = 'article_view.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['article'] = get_object_or_404(Article, pk=pk)
        return context


class ArticleCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        return render(request, 'article_create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = Article.objects.create(title=form.cleaned_data['title'],
                                             text=form.cleaned_data['text'],
                                             author=form.cleaned_data['author'])
            return redirect('article_view', pk=article.pk)
        return render(request, 'article_create.html', context={'form': form})


class ArtUpdateView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(data={'title': article.title, 'text': article.text, 'author': article.author})
        return render(request, 'article_update_view.html', context={'form': form, 'article': article})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.text = form.cleaned_data['text']
            article.author = form.cleaned_data['author']
            print(article.title, article.text, article.author)
            article.save()
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'article_update_view.html', context={
                'form': form, 'article': article
            })


class ArtDeleteView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(data={'title': article.title, 'text': article.text, 'author': article.author})
        return render(request, 'delete_view.html', context={'form': form, 'article': article})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return redirect('index')
