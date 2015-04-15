# -*- coding: UTF-8 -*-
__author__ = 'zengzheying'
from server.const import *
class NewsOperator:

    @classmethod
    def getNews(cls, uid, cat, page):
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

        start = (page - 1) * PAGE_SIZE
        end = page * PAGE_SIZE
        return news[start:end]