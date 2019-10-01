
from django.contrib import admin
from django.urls import path

from webapp.views import IndexView, ArticleView, ArticleCreateView, \
    IndexRedirectView, ArtUpdateView, ArtDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name = 'index'),
    path('index/', IndexRedirectView.as_view(), name='article_index_redirect'),
    path('article/<int:pk>/', ArticleView.as_view(), name="article_view"),
    path('articles/add', ArticleCreateView.as_view(), name = 'article_add'),
    path('article/<int:pk>/update', ArtUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete', ArtDeleteView.as_view(), name="article_delete"),
]
