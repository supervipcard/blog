from django.contrib import admin
from blog.models import *


@admin.register(Myself)
class MyselfAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '/static/js/kindeditor/kindeditor-all-min.js',
            '/static/js/kindeditor/lang/zh-CN.js',
            '/static/js/kindeditor/config.js',
        )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('comment_content',)

    class Media:
        js = (
            '/static/js/kindeditor/kindeditor-all-min.js',
            '/static/js/kindeditor/lang/zh-CN.js',
            '/static/js/kindeditor/config.js',
        )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'website', 'content', 'time', 'reply', 'reply_time')
    list_per_page = 50
    ordering = ('-time', )


admin.site.register(Tag)
admin.site.register(Link)
