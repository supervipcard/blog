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
from blog.views import index, details, technique, note, tags, date, praise_ajax, comment_ajax, about
from django.conf import settings
from django.views import static
from blog.upload import upload_image
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^uploads/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),   # 封面图和文章内的图片显示
    url(r'^admin/load/(?P<dir_name>[^/]+)$', upload_image),   # 富文本编辑器内的图片上传接口
    url(r'^admin/', admin.site.urls),
    url(r'^search/', include('haystack.urls')),
    url(r'^praise-ajax/$', praise_ajax, name='praise-ajax'),
    url(r'^comment-ajax/$', comment_ajax, name='comment-ajax'),
    url(r'^details/$', details, name='details'),
    url(r'^technique/$', technique, name='technique'),
    url(r'^note/$', note, name='note'),
    url(r'^tags/(?P<tag>.*?)/$', tags, name='tags'),
    url(r'^date/(?P<year>.*?)/(?P<month>.*?)/$', date, name='date'),
    url(r'^about/$', about, name='about'),
    url(r'^$', index),
]
