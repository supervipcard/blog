import pytz
import json
import datetime
import markdown

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from blog.models import *

# pip install pygments    # 实现代码高亮，只需安装，并引入 css 样式即可


def global_setting(request):
    links = Link.objects.all()
    tags = Tag.objects.all()

    today = datetime.datetime.now()
    initial_date = datetime.datetime.strptime('2018-08-02', '%Y-%m-%d')
    day = (today - initial_date).days

    article_num = len(Article.objects.all())

    article_date_list = Article.objects.get_date_list()
    recommend_articles = Article.objects.get_recommend_articles()[0: 5]

    return {
            'links': links,
            'tags': tags,
            'day': day,
            'article_num': article_num,
            'article_date_list': article_date_list,
            'recommend_articles': recommend_articles
            }


def pagination(request, articles, number):
    paginator = Paginator(articles, number)
    try:
        page = request.GET.get('page')
        articles = paginator.page(page)
    except (InvalidPage, EmptyPage, PageNotAnInteger):
        articles = paginator.page(1)
    return articles


def home(request):
    articles = Article.objects.all().order_by('-time')
    articles = pagination(request, articles, 10)

    today = datetime.datetime.now()
    today_article_num = len(Article.objects.get_articles_through_date(year=str(today.year), month=str(today.month), day=str(today.day)))
    return render(request, 'home.html', locals())


def about(request):
    myself = Myself.objects.all()
    if myself:
        myself = myself[0]
        return render(request, 'me.html', locals())
    else:
        return HttpResponseRedirect('/')    # 重定向到首页


def details(request, id):
    if request.method == 'GET':
        try:
            article = Article.objects.get(Q(id=id), Q(hide=False))
            article.read_count = article.read_count + 1
            article.save()
            related_articles = Article.objects.get_related_articles(article.tag.all(), article.title)[0: 5]

            comments = dict()
            for cell in article.comment_content.filter(reply_to=0).order_by('-time'):
                comments[cell] = list()

            for cell in article.comment_content.filter(~Q(reply_to=0)).order_by('time'):
                comments[Comment.objects.get(id=cell.root_id)].append((cell, Comment.objects.get(id=cell.reply_to)))

            praise_class = 'article-praise active' if request.COOKIES.get('praise_' + id) else 'article-praise'

            username = request.session.get('username', '')
            email = request.session.get('email', '')
            website = request.session.get('website', '')
            login_status = True if any([username, email, website]) else False

            return render(request, 'details.html', locals())

        except Article.DoesNotExist:
            return render(request, '404.html')
    else:
        return render(request, '404.html')


def technique(request):
    articles = Article.objects.filter(~Q(tag__name__exact='随记')).order_by('-time')
    articles = pagination(request, articles, 10)
    return render(request, 'technique.html', locals())


def journal(request):
    tag_name = '随记'
    articles = Article.objects.filter(tag__name__exact=tag_name).order_by('-time')
    articles = pagination(request, articles, 10)
    return render(request, 'journal.html', locals())


def tag(request, tag_name):
    articles = Article.objects.filter(tag__name__exact=tag_name).order_by('-time')
    articles = pagination(request, articles, 10)
    if articles:
        return render(request, 'tag.html', locals())
    else:
        return render(request, '404.html')


def date(request, year, month):
    articles = Article.objects.get_articles_through_date(year=year, month=month)
    articles = pagination(request, articles, 10)
    if articles:
        return render(request, 'date.html', locals())
    else:
        return render(request, '404.html')


@csrf_exempt
def praise_ajax(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        article = Article.objects.get(id=id)

        add_praise_count = article.praise_count + 1
        article.praise_count = add_praise_count
        article.save()
        return JsonResponse({'isSuccess': True})

    else:
        return render(request, '404.html')


@csrf_exempt
def comment_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        article = Article.objects.get(id=data['id'])
        data['content'] = markdown.markdown(data['content'],
                                            extensions=[
                                                'markdown.extensions.extra',
                                                'markdown.extensions.codehilite',
                                            ])
        data.pop('id')

        request.session['username'] = data['username']
        request.session['email'] = data['email']
        request.session['website'] = data['website']

        reply_to = data['reply_to']
        if bool(reply_to):
            data['reply_username'] = Comment.objects.get(id=reply_to).username
            article.comment_content.create(**data)
        else:
            article.comment_content.create(**data)

        if data['email'] != '805071841@qq.com':
            message = '访客 "{username}" 在文章 "{title}" 中发表评论：{content}'.format(username=data['username'],
                                                                           title=article.title, content=data['content'])
            send_mail('博客有新评论了', message, '805071841@qq.com', ['805071841@qq.com'], fail_silently=True)
        else:
            reply_email = Comment.objects.get(id=reply_to).email
            message = '您好，您在文章 "{title}" 中发表的评论已经收到了博主的回复，请点击下面的链接查看：\n{url}'.format(
                title=article.title, url=request.META.get('HTTP_REFERER'))
            send_mail('博主回复', message, '805071841@qq.com', [reply_email], fail_silently=True)

        return JsonResponse({'isSuccess': True})

    else:
        return render(request, '404.html')
