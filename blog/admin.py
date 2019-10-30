from django.contrib import admin
from blog.models import *


@admin.register(Myself)
class MyselfAdmin(admin.ModelAdmin):

    # 配置富文本编辑器
    class Media:
        js = (
            '/static/js/kindeditor/kindeditor-all-min.js',
            '/static/js/kindeditor/lang/zh-CN.js',
            '/static/js/kindeditor/config.js',
        )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('comment_content',)    # ManyToManyField 的一种后台操作样式

    # 配置富文本编辑器
    class Media:
        js = (
            '/static/js/kindeditor/kindeditor-all-min.js',
            '/static/js/kindeditor/lang/zh-CN.js',
            '/static/js/kindeditor/config.js',
        )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'website', 'content', 'time', 'reply_username')    # 显示字段
    list_per_page = 50    # 每页条数
    ordering = ('-time', )    # 按时间顺序显示


admin.site.register(Tag)
admin.site.register(Link)
