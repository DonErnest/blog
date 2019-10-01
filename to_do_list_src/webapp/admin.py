from django.contrib import admin

from webapp.models import Article, Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'author', 'article', 'created_at', 'updated_at']
    list_filter = ['author']
    search_fields = ['text', 'author']
    fields = ['author', 'text', 'article', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id','title','author','created_at']
    list_filter = ['author']
    search_fields = ['title','text']
    fields = ['title', 'author', 'text', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
