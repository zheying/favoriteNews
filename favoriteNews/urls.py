# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, include, url
# from django.contrib import admin
import settings
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'favoriteNews.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),

    url(r'^login/', 'server.views.login', name='login'),  #登录链接
    url(r'^news/', 'server.views.get_news', name='getNews'),   #获取新闻链接
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATICFILES_DIRS, 'show_indexes': True}),  #静态文件链接
    url(r'^view_news/(?P<news_id>\d+)/$', 'server.views.view_news', name='viewNews'), #用户浏览新闻
    url(r'^hobby/$', 'server.views.add_short_hobby', name='hobby'),  #用户添加短期兴趣
    url(r'^comment/$', 'server.views.comment', name='comment'),  #用户评论新闻
    url(r'^delete_comment/$', 'server.views.delete_comment', name='delete_comment'),
    url(r'^pull_comments/$', 'server.views.pull_comment_list', name='pull_comments'), #拉取评论列表
    url(r'^pull_collects/$', 'server.views.pull_collect_list', name='pull_collects'), #拉取收藏列表
    url(r'^collect/$', 'server.views.collect', name='collect'), #收藏新闻
    url(r'^share/$', 'server.views.share', name='share'), #分享记录
    url(r'^dislike/$', 'server.views.not_like_news', name='not_like'), #用户反馈不感兴趣
)
