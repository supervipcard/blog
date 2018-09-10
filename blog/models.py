import pytz
from django.db import models


class ArticleManager(models.Manager):
    def distinct_date(self, year, month, day=None):
        data_list = []
        for cell in self.all().order_by('-time'):
            trans_time = cell.time.astimezone(pytz.timezone('Asia/Shanghai'))
            if not day:
                if year == str(trans_time.year) and month == str(trans_time.month):
                    data_list.append(cell)
            else:
                if year == str(trans_time.year) and month == str(trans_time.month) and day == str(trans_time.day):
                    data_list.append(cell)
        return data_list

    def get_date_list(self):
        articles_date_list = []
        for i in self.values('time'):
            trans_time = i['time'].astimezone(pytz.timezone('Asia/Shanghai'))
            group = [trans_time.year, trans_time.month]
            if group not in articles_date_list:
                articles_date_list.append(group)
        return articles_date_list

    def get_same_tag_article(self, tags, title):
        related_articles = []
        for related_tag in tags:
            for related_article in related_tag.article_set.all().order_by('-praise_count', '-time'):
                if related_article.title != title and related_article not in related_articles:
                    related_articles.append(related_article)
                    if len(related_articles) >= 5:
                        return related_articles
        return related_articles


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='标签名称')

    def __str__(self):
        return self.name


class Myself(models.Model):
    period = models.CharField(max_length=10, verbose_name='阶段')
    article = models.TextField(verbose_name='个人简介')

    def __str__(self):
        return self.period


class Comment(models.Model):
    username = models.CharField(max_length=20, verbose_name='用户昵称')
    email = models.CharField(max_length=50, verbose_name='用户邮箱')
    website = models.CharField(max_length=50, verbose_name='用户网站', null=True, blank=True)
    content = models.TextField(verbose_name='评论内容')
    time = models.DateTimeField(verbose_name='发布时间')
    reply = models.TextField(verbose_name='站长回复', null=True, blank=True)
    reply_time = models.DateTimeField(verbose_name='发布时间', null=True, blank=True)

    def __str__(self):
        return self.username + '：' + self.content


class Article(models.Model):
    title = models.CharField(max_length=30, verbose_name='文章标题')
    image = models.ImageField(upload_to='cover', verbose_name='封面图', null=True, blank=True)
    article = models.TextField(verbose_name='文章内容')
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    time = models.DateTimeField(verbose_name='发布时间')
    read_count = models.IntegerField(default=0, verbose_name='查看次数')
    comment_count = models.IntegerField(default=0, verbose_name='评论次数')
    praise_count = models.IntegerField(default=0, verbose_name='喜欢次数')
    comment_content = models.ManyToManyField(Comment, verbose_name='评论信息', blank=True)

    # comment_content = models.ForeignKey(Comment, null=True, blank=True, default=None, verbose_name='评论信息', on_delete=models.CASCADE)

    objects = ArticleManager()  # 如果有自定义manage记得写上

    def __str__(self):
        return self.title


class Link(models.Model):
    name = models.CharField(max_length=20, verbose_name='链接名')
    url = models.URLField(verbose_name='友情链接')

    def __str__(self):
        return self.name
