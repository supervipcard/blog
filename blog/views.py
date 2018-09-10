import pytz
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from blog.models import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q
import datetime


def global_setting(request):
    links = Link.objects.all()
    tags = Tag.objects.all()

    today = datetime.datetime.now()
    initial_date = datetime.datetime.strptime('2018-08-02', '%Y-%m-%d')
    day = (today - initial_date).days

    articles = Article.objects.all().order_by('-time')
    article_num = len(articles)

    articles_date_list = Article.objects.get_date_list()
    recommend_articles = Article.objects.filter(recommend=True).order_by('-praise_count', '-time')[0: 5]

    return {
            'links': links,
            'tags': tags,
            'day': day,
            'article_num': article_num,
            'articles_date_list': articles_date_list,
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


def index(request):
    today = datetime.datetime.now()

    articles = Article.objects.all().order_by('-time')
    articles = pagination(request, articles, 10)

    today_article_num = len(Article.objects.distinct_date(year=str(today.year), month=str(today.month), day=str(today.day)))
    return render(request, 'index.html', locals())


def about(request):
    myself = Myself.objects.all()[0]
    return render(request, 'me.html', locals())


def details(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            article = Article.objects.get(id=id)
            article.read_count = article.read_count + 1
            article.save()
            related_articles = Article.objects.get_same_tag_article(article.tag.all(), article.title)
            return render(request, 'details.html', locals())

        except Article.DoesNotExist:
            return render(request, '404.html', locals())
    else:
        return render(request, '404.html', locals())


def technique(request):
    articles = Article.objects.filter(~Q(tag__name__exact='随记')).order_by('-time')
    articles = pagination(request, articles, 10)
    return render(request, 'technique.html', locals())


def note(request):
    tag = '随记'
    articles = Article.objects.filter(tag__name__exact=tag).order_by('-time')
    articles = pagination(request, articles, 10)
    return render(request, 'note.html', locals())


def tags(request, tag):
    articles = Article.objects.filter(tag__name__exact=tag).order_by('-time')
    articles = pagination(request, articles, 10)
    if articles:
        return render(request, 'tags.html', locals())
    else:
        return render(request, '404.html', locals())


def date(request, year, month):
    articles = Article.objects.distinct_date(year=year, month=month)
    articles = pagination(request, articles, 10)
    if articles:
        return render(request, 'date.html', locals())
    else:
        return render(request, '404.html', locals())


def praise_ajax(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        article = Article.objects.get(id=id)
        praise_sign = request.COOKIES.get('praise_{id}'.format(id=id))

        if not praise_sign:
            add_praise_count = article.praise_count + 1
            article.praise_count = add_praise_count
            article.save()
            response = JsonResponse({'success': True, 'count': str(add_praise_count)})
            response.set_cookie('praise_{id}'.format(id=id), str(id))
            return response
        else:
            add_praise_count = article.praise_count
            return JsonResponse({'success': False, 'count': str(add_praise_count)})

    else:
        return render(request, '404.html', locals())


def comment_ajax(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        article = Article.objects.get(id=id)

        username = request.POST.get('username')
        email = request.POST.get('email')
        website = request.POST.get('website')
        content = request.POST.get('content')
        if website:
            if 'http://' not in website and 'https://' not in website:
                website = 'http://' + website
        article.comment_content.create(username=username, email=email, website=website, content=content, time=datetime.datetime.now().astimezone(pytz.timezone('Asia/Shanghai')))
        article.comment_count = article.comment_count + 1
        article.save()
        return HttpResponse('true')

    else:
        return render(request, '404.html', locals())
