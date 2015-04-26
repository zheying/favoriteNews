# -*- coding: UTF-8 -*- 
__author__ = 'zengzheying'
import urllib
import re
import chardet
from bs4 import BeautifulSoup
import urllib2
import datetime
from server.models import *


class NewsParser:

    @classmethod
    def get_news(cls, url, model):
        # html = NewsParser.get_news_html(url)
        # content = NewsParser.parse_html(url, html)
        # if content is None:
        #     return None
        if model['content'] == '':
            return None;
        result = '''
        <!DOCTYPE html>
        <html>
	        <head>
		        <meta http-equiv="Cache-Control" content="no-cache" />
                <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
                <meta name="MobileOptimized" content="320" />
                <meta name="robots" content="all" />
                <meta name="viewport" content="initial-scale=1.0, user-scalable=0, minimum-scale=1.0, maximum-scale=1.0">
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                <link type="text/css" rel="stylesheet" href="../../static/news_detail_sytle.css"/>
		    </head>
            <body>
                <header>
                    <h1> ''' + model['title'] + ''' </h1>
                    <div class="subtitle">
                        <a id="source" href="''' + model['source_url'] + '''">''' + model['source'] + '''</a>
                        <time> ''' + model['date'] + ''' </time>
                    </div>
                </header>
                <article>''' + model['content'] + '''
                </article>
            </body>

        </html>
		'''
        return result

    @classmethod
    def get_news_html(cls, url):
        web_page = urllib.urlopen(url)
        result = web_page.read()
        charset = chardet.detect(result)
        code = charset['encoding']
        result_str = str(result).decode(code, 'ignore').encode('utf-8')
        string = result_str.lower()
        pattern = re.compile(r'<meta[\s]*http-equiv="refresh"[\s]*content="\d*;[\s]*url=(http.*?)"\s*>')
        if re.search(pattern, string):
            new_url = pattern.findall(string)[0]
            web_page = urllib.urlopen(new_url)
            result = web_page.read()

        text = result
        charset = chardet.detect(text)
        code = charset['encoding']
        text = str(text).decode(code, 'ignore').encode('utf-8')
        return text

    @classmethod
    def parse_html(cls, url, html):
        soup = BeautifulSoup(html)

        '''新浪微博新闻'''
        if url.find('.sina.com.cn') != -1:
            '''artibody 为新闻内容的页面'''
            article_div = soup.find('div', attrs={'id': 'artibody'})
            if article_div is not None:
                return unicode(article_div)

            '''video 页面'''
            video_div = soup.find('div', attrs={'id': 'video'})
            if video_div is not None:
                return unicode(video_div)

        return None


    @classmethod
    def get_mobile_news(cls, url):
        if url.find('.sina.') != -1:
            html = NewsParser.get_sina_mobile_web_html(url)
            time1 = datetime.datetime.now()
            print '解析新闻内容'
            content = NewsParser.parse_sina_mobile_html(html)
            time2 = datetime.datetime.now()
            print '解析内容花费时间：', time2 - time1
            return content


    @classmethod
    def get_sina_mobile_web_html(cls, url):
        header = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0.1; Nexus 4 Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.0.0 Mobile Safari/537.36'}
        req_url = 'http://data.api.sina.cn/api/redirect/pc_to_wap.php?ref=' + url.replace('/', '%2F').replace(':', '%3A')
        print '正在获取重定向页面'
        time1 = datetime.datetime.now()

        req = urllib2.Request(req_url, headers=header)
        res_data = urllib2.urlopen(req)
        res = res_data.read()

        print '获取重定向页成功'

        time2 = datetime.datetime.now()
        print '请求重定向页面时间：', time2 - time1

        print '正在分析目标链接'

        soup = BeautifulSoup(res)
        phone_link = soup.find('a', attrs={'class': 'phone'})

        print '分析目标链接成功'

        time1 = datetime.datetime.now()
        print '获取重定向链接时间：', time1 - time2
        if phone_link is None:
            return res

        print '正在获取新闻内容'

        req = urllib2.Request(phone_link['href'], headers=header)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        time2 = datetime.datetime.now()

        print '获取新闻内容成功'
        print '获取新闻内容时间：', time2 - time1
        return res


    @classmethod
    def parse_sina_mobile_html(cls, html):
        if html is not None or html.strip() != '':
            soup = BeautifulSoup(html)

            '''art_content 内容'''
            art_content = soup.find('div', attrs={'class': 'art_content'})
            if art_content is not None:
                return unicode(art_content)

            '''articleContent 内容'''
            article_content = soup.find('div', attrs={'class': 'articleContent'})
            if article_content is not None:
                return unicode(article_content)

            '''video_cnt 内容'''
            video_cnt = soup.find('div', attrs={'class': 'video_cnt'})
            if video_cnt is not None:
                result = unicode(video_cnt)
                j_video_intro = soup.find('div', attrs={'id': 'j_video_intro'})
                if j_video_intro is not None:
                    temp = result + unicode(j_video_intro)
                    result = temp
                return result

            return None
        else:
            return None


    @classmethod
    def parse_data_in_database(cls):
        news_list = SinaNews.objects.filter(mobile_html='')
        print '还有', len(news_list), '条需要处理'
        for news in news_list:
            if news.mobile_html is None or news.mobile_html.strip() == '':
                try:
                    html = NewsParser.get_mobile_news(news.pageurl)
                    if html is not None:
                        news.mobile_html = html
                    else:
                        news.mobile_html = ''
                    news.save()
                except Exception, e:
                    news.mobile_html = ''
                    news.save()
        # news_list = SinaNews.objects.filter(tags='n|u|l|l| |t|a|g')
        # print '还有', len(news_list), '条需要处理'
        # for news in news_list:
        #     news.tags = 'null tag'
        #     news.save()

if __name__ == '__main__':
    print NewsParser.get_mobile_news("http://news.sina.com.cn/w/2015-04-09/165331698951.shtml")
