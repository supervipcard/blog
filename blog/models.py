import pytz
from django.db import models


class ArticleManager(models.Manager):
    """
    自定义模型管理器，按照特定的方式返回数据库中的对象
    """
    def get_articles_through_date(self, year, month, day=None):
        articles = []
        for cell in self.all().order_by('-time'):
            trans_time = cell.time.astimezone(pytz.timezone('Asia/Shanghai'))
            if not day:
                if year == str(trans_time.year) and month == str(trans_time.month):
                    articles.append(cell)
            else:
                if year == str(trans_time.year) and month == str(trans_time.month) and day == str(trans_time.day):
                    articles.append(cell)
        return articles

    def get_date_list(self):
        article_date_list = []
        for cell in self.all().order_by('-time'):
            trans_time = cell.time.astimezone(pytz.timezone('Asia/Shanghai'))
            group = (trans_time.year, trans_time.month)
            if group not in article_date_list:
                article_date_list.append(group)
        return article_date_list

    @staticmethod
    def get_related_articles(tags, title):
        related_articles = []
        for related_tag in tags:
            for related_article in related_tag.article_set.get_recommend_articles():
                if related_article.title != title and related_article not in related_articles:
                    related_articles.append(related_article)
        return related_articles

    def get_recommend_articles(self):
        recommend_articles = self.filter(recommend=True).order_by('-praise_count', '-read_count', '-comment_count', '-time')
        return recommend_articles


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='标签名称')
    major = models.BooleanField(default=False, verbose_name='是否是主标签')

    def __str__(self):
        return self.name + '（{}）'.format('主' if self.major else '副')


class Myself(models.Model):
    period = models.CharField(max_length=10, verbose_name='阶段')
    article = models.TextField(verbose_name='个人简介')

    def __str__(self):
        return self.period


class Comment(models.Model):
    username = models.CharField(max_length=20, verbose_name='访客昵称')
    email = models.CharField(max_length=50, verbose_name='访客邮箱')
    website = models.CharField(max_length=50, verbose_name='访客网站', null=True, blank=True)
    content = models.TextField(verbose_name='评论/回复内容')
    time = models.DateTimeField(verbose_name='评论/回复时间', auto_now_add=True)

    # 如果是回复
    root_id = models.IntegerField(default=0, verbose_name='外层被回复人ID')
    reply_to = models.IntegerField(default=0, verbose_name='内层被回复人ID')
    reply_username = models.CharField(max_length=20, verbose_name='被回复人昵称', null=True, blank=True)

    def __str__(self):
        return self.username + '：' + self.content


class Article(models.Model):
    title = models.CharField(max_length=30, verbose_name='文章标题')
    image = models.ImageField(upload_to='cover', verbose_name='封面图', default='python.jpg', null=True, blank=True)    # null=True表示数据库中该字段可以是null，如果为空就存为null；null=False，如果为空存为字符串；blank=True表示后台该字段非必填
    article = models.TextField(verbose_name='文章内容')
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    hide = models.BooleanField(default=False, verbose_name='是否隐藏')
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
