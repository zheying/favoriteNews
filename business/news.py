# -*- coding: UTF-8 -*-
__author__ = 'zengzheying'
from server.const import *
from server.models import *
from django.core.exceptions import ObjectDoesNotExist
from business.comment import CommentHelper


class NewsOperator:

    @classmethod
    def get_news(cls, uid, cat, page):
        news = []
        if cat == NEWS_CATALOG_RECOMMEND:  #推荐新闻
            news = SinaNews.objects.order_by('-date')
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

        result = []
        for v in news[start:end]:
            item = {}
            item['cat'] = v.cat
            item['id'] = v.id
            item['title'] = v.title
            item['source'] = v.source
            item['pageurl'] = v.pageurl
            item['date'] = v.date
            item['picurl'] = v.picurl
            item['comment_count'] = CommentHelper.get_comment_count_by_news_id(v.id)
            result.append(item)

        return result

    @classmethod
    def find_news_by_id(cls, news_id):
        try:
            news = SinaNews.objects.get(id=news_id)
            return news
        except ObjectDoesNotExist:
            return None