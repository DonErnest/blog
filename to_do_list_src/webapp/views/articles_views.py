from django.shortcuts import render, get_object_or_404, redirect

from webapp.forms import ArticleForm, CommentForm
from webapp.models import Article

from django.views.generic import View, RedirectView, ListView
from django.views.generic import TemplateView


class IndexView(ListView):
    template_name = 'index.html'
    model = Article
    context_object_name = 'articles'
    ordering = ['-created_at']
    paginate_by = 6
    paginate_orphans = 1
    page_kwarg = 'page' # - по умолчанию имеет это значение, означает , что страницы бдут передаваться под данным названием
# model, queryset и метод get queryset - взимоисключащие параметры. Можно использовать любой из них , вместо остальных
# allow_empty - параметр, определяющий, будет ли выводиться страница с пустым списком. По умолчанию True , т.е. будет.
# Если переопределить False, то вместо вывода пустой страницы будет выходить ошибка 404

class IndexRedirectView(RedirectView):
    pattern_name = 'index'



class ArticleView(TemplateView):
    template_name = 'article/article_view.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['article'] = get_object_or_404(Article, pk=pk)
        article = Article.objects.get(pk=pk)
        context['object_list'] = article.comments.filter(article_id=article.pk).order_by('-created_at')
        context['form'] = CommentForm()
        return context


class ArticleCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        return render(request, 'article/article_create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = Article.objects.create(title=form.cleaned_data['title'],
                                             text=form.cleaned_data['text'],
                                             author=form.cleaned_data['author'])
            return redirect('article_view', pk=article.pk)
        return render(request, 'article/article_create.html', context={'form': form})


class ArtUpdateView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(data={'title': article.title, 'text': article.text, 'author': article.author})
        return render(request, 'article/article_update_view.html', context={'form': form, 'article': article})

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
            return render(request, 'article/article_update_view.html', context={
                'form': form, 'article': article
            })


class ArtDeleteView(View):
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