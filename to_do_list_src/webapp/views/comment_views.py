from django.shortcuts import render, redirect
from django.urls import reverse

from webapp.forms import CommentForm, ArticleCommentForm
from webapp.models import Article, Comment

from django.views.generic import UpdateView, DeleteView, ListView

from django.views.generic import CreateView
# from webapp.views.base_classes import CreateView


class CommentAddView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment/comment_add.html'

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.article.pk})


    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CommentToArticleView(CreateView):
    model = Comment
    template_name = 'comment/comment_add.html'
    form_class = ArticleCommentForm

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.article.pk})

    def post(self, request, *args, **kwargs):
        article_pk = kwargs.get('pk')
        article = Article.objects.get(pk=article_pk)
        form = ArticleCommentForm(data={'text': request.POST['text'],
                                 'author': request.POST['author']})
        if form.is_valid():
            comment = Comment.objects.create(article=article,
                                             text=form.cleaned_data['text'],
                                             author=form.cleaned_data['author'])
            comment.save()
            return redirect('article_view', pk=article_pk)
        return render(request, 'article/article_view.html', context={'form': form, 'article': article})


class CommentListView(ListView):
    model = Comment
    paginate_by = 10
    template_name = 'comment/comment_list.html'
    context_object_name = 'comments'
    ordering = ['-created_at']


class CommentEditView(UpdateView):
    model = Comment
    fields = ['author', 'text', 'article']
    template_name = 'comment/comment_edit.html'
    success_url = '/comments/'

    def form_valid(self, form):
        return super().form_valid(form)

class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'comment/comment_delete.html'
    success_url = '/comments/'