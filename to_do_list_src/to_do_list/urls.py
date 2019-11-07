
from django.contrib import admin
from django.urls import path, include

from to_do_list import settings
from webapp.views import IndexView, ArticleView, ArticleCreateView, \
    IndexRedirectView, ArtUpdateView, ArtDeleteView, CommentAddView, CommentListView, CommentEditView, \
    CommentDeleteView, CommentToArticleView, SearchView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name = 'index'),
    path('index/', IndexRedirectView.as_view(), name='article_index_redirect'),
    path('article/<int:pk>/', ArticleView.as_view(), name="article_view"),
    path('articles/add', ArticleCreateView.as_view(), name = 'article_add'),
    path('article/<int:pk>/update', ArtUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete', ArtDeleteView.as_view(), name="article_delete"),
    path('comments/add/', CommentAddView.as_view(), name='add comment'),
    path('comments/', CommentListView.as_view(), name='comments list'),
    path('comment/<int:pk>/edit/', CommentEditView.as_view(), name='edit comment'),
    path('comment/<int:pk>/', CommentDeleteView.as_view(), name='delete comment'),
    path('article/<int:pk>/comment/add/', CommentToArticleView.as_view(), name='add comment to article'),

    path('search/', SearchView.as_view(), name='advanced search'),
    # path('search/results', SearchResultsView.as_view(), name='advanced search results'),

    path('accounts/', include('accounts.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
