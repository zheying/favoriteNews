# -*- coding: UTF-8 -*-
from django.shortcuts import render, render_to_response
from django.http.response import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from tools import Response
from business import UserInfo
from const import *
# Create your views here.
from models import *
from business.UidTag import *
from business.news import *
from business.hobby import *
from business.comment import *
from business.ParseNews import *

#用户登录
@csrf_exempt
def login(req):
    uid = req.POST.get('uid')
    token = req.POST.get('token')
    name = req.POST.get('name')
    avatar = req.POST.get('avatar')
    if uid is not None and token is not None and name is not None and avatar is not None:
        u = UserInfo.login(uid, name, token, avatar)
        UserInfo.get_tags(u)
        return HttpResponse(Response.response(None))
    else:
        return HttpResponse(Response.responseError(NOT_AVAILABLE_REQUEST_PARAMETERS,
                                                   STRING_NOT_AVAILABLE_REQUEST_PARAMETERS))
#用户获取新闻
def get_news(req):
    try:
        uid = req.GET.get('uid', None)
        page = int(req.GET.get('page'))
        cat = int(req.GET.get('cat'))
        news = NewsOperator.get_news(uid, cat, page)
        return HttpResponse(Response.response({'list': news}))
    except ValueError, e:
        return HttpResponse(Response.responseError(NOT_AVAILABLE_REQUEST_PARAMETERS,
                                                   STRING_NOT_AVAILABLE_REQUEST_PARAMETERS))

'''用户阅读新闻'''
def view_news(req, news_id):
    news = SinaNews.objects.get(id=news_id)
    uid = req.GET.get('uid', None)
    UidTagHistory.upateUserViewNewsTags(uid, news.tags)
    ShortTimeHobby.updateHobby(uid, news.tags)
    model = {}
    model['title'] = news.title
    model['source_url'] = news.pageurl
    model['source'] = news.source
    model['date'] = news.date.strftime('%Y-%m-%d %H:%M')
    model['content'] = news.mobile_html
    content = NewsParser.get_news(news.pageurl, model)
    # return HttpResponse(Response.response({"content": content}))
    if content is None:
        return HttpResponseRedirect(news.pageurl)
    else:
        return HttpResponse(content)

'''用户设置短期兴趣'''
@csrf_exempt
def add_short_hobby(req):
    try:
        uid = req.POST.get('uid')
        tag = req.POST.get('tag')
        ShortTimeHobby.addHobby(uid, tag)
        return HttpResponse(Response.response(None))
    except Exception, e:
        return HttpResponse(Response.responseError(NOT_AVAILABLE_REQUEST_PARAMETERS,
                                                   STRING_NOT_AVAILABLE_REQUEST_PARAMETERS))


#对新闻进行评论
@csrf_exempt
def comment(req):
    try:
        uid = req.POST.get('uid')
        news_id = req.POST.get('news_id')
        content = req.POST.get('content')
        token = req.POST.get('token')
        if not UserInfo.verify_user(uid, token):
            return HttpResponse(Response.responseError(UID_NOT_MATCH_TOKEN, STRING_UID_NOT_MATCH_TOKEN))
        if NewsOperator.find_news_by_id(news_id) is None:
            return HttpResponse(Response.responseError(NO_SUCH_NEWS, STRING_NO_SUCH_NEWS))
        CommentHelper.add_comment(uid, news_id, content)
        return HttpResponse(Response.response(None))
    except Exception, e:
        return HttpResponse(Response.responseError(NOT_AVAILABLE_REQUEST_PARAMETERS,
                                                   STRING_NOT_AVAILABLE_REQUEST_PARAMETERS))


#删除新闻评论
@csrf_exempt
def delete_comment(req):
    try:
        uid = req.POST.get('uid')
        cid = req.POST.get('cid')
        token = req.POST.get('token')
        if not UserInfo.verify_user(uid, token):
            return HttpResponse(Response.responseError(UID_NOT_MATCH_TOKEN, STRING_UID_NOT_MATCH_TOKEN))
        try:
            CommentHelper.delete_comment(uid, cid)
            return HttpResponse(Response.response(None))
        except ValueError, e:
            return HttpResponse(Response.responseError(UID_NOT_MATCH, STRING_UID_NOT_MATCH))
        except ObjectDoesNotExist:
            return HttpResponse(Response.responseError(NO_SUCH_COMMENT, STRING_NO_SUCH_COMMENT))
    except Exception, e:
        return HttpResponse(Response.responseError(NOT_AVAILABLE_REQUEST_PARAMETERS,
                                                   STRING_NOT_AVAILABLE_REQUEST_PARAMETERS))


#拉取新闻的评论列表
@csrf_exempt
def pull_comment_list(req):
    try:
        news_id = req.POST.get('news_id')
        uid = req.POST.get('uid')
        token = req.POST.get('token')
        if not UserInfo.verify_user(uid, token):
            return HttpResponse(Response.responseError(UID_NOT_MATCH_TOKEN, STRING_UID_NOT_MATCH_TOKEN))
        if NewsOperator.find_news_by_id(news_id) is None:
            return HttpResponse(Response.responseError(NO_SUCH_NEWS, STRING_NO_SUCH_NEWS))
        comment_list = CommentHelper.get_comment_list_by_news_id(uid, token, news_id)
        return HttpResponse(Response.response({'list': comment_list}))
    except ValueError, e:
        return HttpResponse(Response.responseError(NOT_AVAILABLE_REQUEST_PARAMETERS,
                                                   STRING_NOT_AVAILABLE_REQUEST_PARAMETERS))


#对用户的分享新闻进行记录
@csrf_exempt
def share(req):
    try:
        uid = req.POST.get('uid')
        token = req.POST.get('token')
        news_id = req.POST.get('news_id')
        user = UserInfo.find_user_by_id(uid, token)
        if user is None:
            return HttpResponse(Response.responseError(UID_NOT_MATCH_TOKEN, STRING_UID_NOT_MATCH_TOKEN))
        news = NewsOperator.find_news_by_id(news_id)
        if news is None:
            return HttpResponse(Response.responseError(NO_SUCH_NEWS, STRING_NO_SUCH_NEWS))
        NewsOperator.add_share_news(user, news)
        return HttpResponse(Response.response(None))
    except ValueError, e:
        return HttpResponse(Response.responseError(NOT_AVAILABLE_REQUEST_PARAMETERS,
                                                   STRING_NOT_AVAILABLE_REQUEST_PARAMETERS))


#用户反馈不感兴趣的新闻
@csrf_exempt
def not_like_news(req):
    try:
        uid = req.POST.get('uid')
        token = req.POST.get('token')
        news_id = req.POST.get('news_id')
        user = UserInfo.find_user_by_id(uid, token)
        if user is None:
            return HttpResponse(Response.responseError(UID_NOT_MATCH_TOKEN, STRING_UID_NOT_MATCH_TOKEN))
        news = NewsOperator.find_news_by_id(news_id)
        if news is None:
            return HttpResponse(Response.responseError(NO_SUCH_NEWS, STRING_NO_SUCH_NEWS))
        NewsOperator.dislike_news(user, news)
        return HttpResponse(Response.response(None))
    except ValueError:
        return HttpResponse(Response.responseError(NOT_AVAILABLE_REQUEST_PARAMETERS,
                                                   STRING_NOT_AVAILABLE_REQUEST_PARAMETERS))

#用户收藏某些新闻
@csrf_exempt
def collect(req):
    try:
        uid = req.POST.get('uid')
        token = req.POST.get('token')
        news_id = req.POST.get('news_id')
        user = UserInfo.find_user_by_id(uid, token)
        if user is None:
            return HttpResponse(Response.responseError(UID_NOT_MATCH_TOKEN, STRING_UID_NOT_MATCH_TOKEN))
        news = NewsOperator.find_news_by_id(news_id)
        if news is None:
            return HttpResponse(Response.responseError(NO_SUCH_NEWS, STRING_NO_SUCH_NEWS))
        NewsOperator.collect_news(user, news)
        return HttpResponse(Response.response(None))
    except ValueError:
        return HttpResponse(Response.responseError(NOT_AVAILABLE_REQUEST_PARAMETERS,
                                                   STRING_NOT_AVAILABLE_REQUEST_PARAMETERS))


#用户获取新闻列表
@csrf_exempt
def pull_collect_list(req):
    try:
        uid = req.POST.get('uid')
        token = req.POST.get('token')
        page = int(req.POST.get('page'))
        user = UserInfo.find_user_by_id(uid, token)
        if user is None:
            return HttpResponse(Response.responseError(UID_NOT_MATCH_TOKEN, STRING_UID_NOT_MATCH_TOKEN))
        result = NewsOperator.get_collected_news(user, page)
        return HttpResponse(Response.response({'list': result}))
    except ValueError:
        return HttpResponse(Response.responseError(NOT_AVAILABLE_REQUEST_PARAMETERS,
                                                   STRING_NOT_AVAILABLE_REQUEST_PARAMETERS))

