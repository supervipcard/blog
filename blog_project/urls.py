"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include
from django.conf import settings
from django.views import static

from blog import views
from blog.upload import upload_image

urlpatterns = [
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^uploads/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),   # 封面图和文章内的图片显示
    url(r'^admin/load/(?P<dir_name>[^/]+)$', upload_image),   # 富文本编辑器内的图片上传接口
    url(r'^admin/', admin.site.urls),
    url(r'^search/', include('haystack.urls')),
    url(r'^praise-ajax/$', views.praise_ajax, name='praise-ajax'),
    url(r'^comment-ajax/$', views.comment_ajax, name='comment-ajax'),
    url(r'^details/(?P<id>.*?)/$', views.details, name='details'),
    url(r'^technique/$', views.technique, name='technique'),
    url(r'^journal/$', views.journal, name='journal'),
    url(r'^tag/(?P<tag_name>.*?)/$', views.tag, name='tag'),
    url(r'^date/(?P<year>.*?)/(?P<month>.*?)/$', views.date, name='date'),
    url(r'^about/$', views.about, name='about'),
    url(r'^$', views.home, name='home'),
]
