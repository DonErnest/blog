from django.contrib import admin

from webapp.models import Article, Comment, Tag

AUTHOR=['author']
USERAUTHOR = ['user_author']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'author', 'article', 'created_at', 'updated_at']
    list_filter = ['author']
    search_fields = ['text', 'author']
    fields = ['author', 'text', 'article', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id','title','created_at']
    list_filter = []
    search_fields = ['title','text']
    fields = ['title', 'text', 'created_at', 'updated_at', 'tags']
    filter_horizontal = ['tags']
    readonly_fields = ['created_at', 'updated_at']

    list_display += USERAUTHOR
    fields += USERAUTHOR

    list_display +=AUTHOR
    fields += AUTHOR

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag)
