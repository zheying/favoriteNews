# -*- coding: UTF-8 -*-
from django.shortcuts import render
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

#用户登录
@csrf_exempt
def login(req):
    uid = req.POST.get('uid')
    token = req.POST.get('token')
    name = req.POST.get('name')
    if uid is not None and token is not None and name is not None:
        u = UserInfo.login(uid, name, token)
        UserInfo.getTags(u)
        return HttpResponse(Response.response(None))
    else:
        return HttpResponse(Response.responseError(NOT_AVAILABLE_REQUEST_PARAMETERS,
                                                   STRING_NOT_AVAILABLE_REQUEST_PARAMETERS))
#用户获取新闻
def getNews(req):
    # try:
        uid = req.GET.get('uid', None)
        page = int(req.GET.get('page'))
        cat = int(req.GET.get('cat'))
        news = NewsOperator.getNews(uid, cat, page)
        return HttpResponse(Response.response({'list': list(news)}))
    # except Exception, e:
    #     return HttpResponse(Response.responseError(NOT_AVAILABLE_REQUEST_PARAMETERS,
    #                                                STRING_NOT_AVAILABLE_REQUEST_PARAMETERS))

#用户阅读新闻
def viewNews(req, news_id):
    news = SinaNews.objects.get(id=news_id)
    uid = req.GET.get('uid', None)
    UidTagHistory.upateUserViewNewsTags(uid, news.tags)
    ShortTimeHobby.updateHobby(uid, news.tags)
    return HttpResponseRedirect(news.pageurl)

#用户设置短期兴趣
def addShortHobby(req):
    try:
        uid = req.GET.get('uid')
        tag = req.GET.get('tag')
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
        CommentHelper.addComment(uid, news_id, content)
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
    except Exception, e:
        return HttpResponse(Response.responseError(NOT_AVAILABLE_REQUEST_PARAMETERS,
                                                   STRING_NOT_AVAILABLE_REQUEST_PARAMETERS))
    try:
        CommentHelper.deleteComment(uid, cid)
        return HttpResponse(Response.response(None))
    except ObjectDoesNotExist, e:
        pass
    except ValueError, e:
        return HttpResponse(Response.responseError(UID_NOT_MATCH, STRING_UID_NOT_MATCH))


#拉取新闻的评论列表
def pull_comment_list(req):
    pass


#对用户的分享新闻进行记录
def share(req):
    pass


#用户反馈不感兴趣的新闻
def not_like_news(req):
    pass


#用户收藏某些新闻
def collect(req):
    pass


#用户获取新闻列表
def pull_collect_list(req):
    pass

