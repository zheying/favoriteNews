# -*- coding: UTF-8 -*-
__author__ = 'zengzheying'
from server.const import *
from server.models import *
from django.core.exceptions import ObjectDoesNotExist
from business.comment import CommentHelper
from server.recommend_News import *
from datetime import datetime
import pytz


class NewsOperator:

    @classmethod
    def get_news(cls, uid, cat, page):
        user = None
        if uid is not None:
            try:
                user = User.objects.get(uid=uid)
            except ObjectDoesNotExist:
                user = None
        news = []
        if cat == NEWS_CATALOG_RECOMMEND:  #推荐新闻
            if uid is None:
                news = SinaNews.objects.order_by('-date')
            else:
                news = get_recommend_news(uid)
        elif cat == NEWS_CATALOG_CIVIL:  #国内新闻
            news = SinaNews.objects.filter(cat=STRING_NEWS_CATALOG_CIVIL).order_by('-date')
        elif cat == NEWS_CATALOG_INTERNATIONAL:  #国际新闻
            news = SinaNews.objects.filter(cat=STRING_NEWS_CATALOG_INTERNATIONAL).order_by('-date')
        elif cat == NEWS_CATALOG_SPORT:  #体育新闻
            news = SinaNews.objects.filter(cat=STRING_NEWS_CATALOG_SPORT).order_by('-date')
        elif cat == NEWS_CATALOG_ENTERTAINMENT:  #娱乐新闻
            news = SinaNews.objects.filter(cat=STRING_NEWS_CATALOG_ENTERTAINMENT).order_by('-date')
        elif cat == NEWS_CATALOG_ENVIRONMENTAL:  #环保新闻
            news = SinaNews.objects.filter(cat=STRING_NEWS_CATALOG_ENVIRONMENTAL).order_by('-date')
        elif cat == NEWS_CATALOG_SOCIETY:  #社会新闻
            news = SinaNews.objects.filter(cat=STRING_NEWS_CATALOG_SOCIETY).order_by('-date')
        elif cat == NEWS_CATALOG_SCIENTIST:  #科技新闻
            news = SinaNews.objects.filter(cat=STRING_NEWS_CATALOG_SCIENTIST).order_by('-date')
        elif cat == NEWS_CATALOG_FINANCE:  #财经新闻
            news = SinaNews.objects.filter(cat=STRING_NEWS_CATALOG_FINANCE).order_by('-date')

        start = page * PAGE_SIZE
        end = (page + 1) * PAGE_SIZE

        news = list(news[start:100])

        if user is not None:
            dislike_news_list = NewsOperator.get_dislike_news_list(user)
            # if len(news) > 0:
            for v in dislike_news_list:
                # news = news.exclude(id=v.news.id)
                for v1 in news:
                    if v.news.id == v1.id:
                        news.remove(v1)


        result = []
        for v in news[:PAGE_SIZE]:
            item = {}
            item['cat'] = v.cat
            item['id'] = v.id
            item['title'] = v.title
            item['source'] = v.source
            item['pageurl'] = v.pageurl
            item['date'] = v.date.replace(tzinfo=pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M')
            item['picurl'] = v.picurl
            item['comment_count'] = CommentHelper.get_comment_count_by_news_id(v.id)
            item['tags'] = v.tags
            if user is not None:
                item['collect_status'] = NewsOperator.is_collected_news(user, v)
                if cat == NEWS_CATALOG_RECOMMEND:
                    item['recommend'] = True
                    try:
                        recommend_news = RecommendNewsHistory.objects.get(uid=user.uid, news_id=v.id)
                    except ObjectDoesNotExist:
                        recommend_news = RecommendNewsHistory(uid=user.uid, news_id=v.id, visited=0)
                        recommend_news.save()
            else:
                item['collect_status'] = False
            result.append(item)

        return result

    @classmethod
    def find_news_by_id(cls, news_id):
        try:
            news = SinaNews.objects.get(id=news_id)
            return news
        except ObjectDoesNotExist:
            return None

    @classmethod
    def collect_news(cls, user, news):
        try:
            news_collect = NewsCollect.objects.get(user=user, news=news);
            news_collect.delete()
        except ObjectDoesNotExist:
            news_collect = NewsCollect()
            news_collect.user = user
            news_collect.news = news
            news_collect.collect_time = datetime.now()
            news_collect.save()

    @classmethod
    def get_collected_news(cls, user, page):
        news_list = NewsCollect.objects.filter(user=user).order_by('-collect_time')
        start = page * PAGE_SIZE
        end = (page + 1) * PAGE_SIZE
        result = []
        for v in news_list[start:end]:
            item = {}
            item['cat'] = v.news.cat
            item['id'] = v.news.id
            item['title'] = v.news.title
            item['source'] = v.news.source
            item['pageurl'] = v.news.pageurl
            item['date'] = v.collect_time.replace(tzinfo=pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M')
            item['picurl'] = v.news.picurl
            item['comment_count'] = CommentHelper.get_comment_count_by_news_id(v.news.id)
            item['tags'] = v.news.tags
            item['collect_status'] = True
            result.append(item)
        return result

    @classmethod
    def is_collected_news(cls, user, news):
        try:
            collected_news = NewsCollect.objects.get(user=user, news=news)
            if collected_news is not None:
                return True
            else:
                return False
        except ObjectDoesNotExist:
            return False

    @classmethod
    def dislike_news(cls, user, news):
        try:
            UserDislikeNews.objects.get(user=user, news=news)
        except ObjectDoesNotExist:
            user_dislike_news = UserDislikeNews(user=user, news=news,
                                                time=datetime.now(tz=pytz.timezone('Asia/Shanghai')))
            user_dislike_news.save()

    @classmethod
    def get_dislike_news_list(cls, user):
        return UserDislikeNews.objects.filter(user=user)

    @classmethod
    def add_share_news(cls, user, news):
        try:
            UserShare.objects.get(user=user, news=news)
        except ObjectDoesNotExist:
            user_share = UserShare(user=user, news=news,
                                   time=datetime.now(tz=pytz.timezone('Asia/Shanghai')))
            user_share.save()