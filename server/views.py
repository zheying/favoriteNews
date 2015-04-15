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

@csrf_exempt
def login(req):
    uid = req.POST.get('uid')
    token = req.POST.get('token')
    name = req.POST.get('name')
    if uid is not None and token is not None and name is not None:
        u = UserInfo.login(uid, name, token)
        UserInfo.getTags(u)
        return HttpResponse(Response.response({}))
    else:
        return HttpResponse(Response.responseError(NOT_AVAILABLE_REQUEST_PARAMETERS, "无效的请求参数"))

def getNews(req):
    news = SinaNews.objects.all()[:10]
    return HttpResponse(Response.response({"list": list(news)}))


def viewNews(req, news_id):
    news = SinaNews.objects.get(id=news_id)
    uid = req.GET.get('uid', None)
    UidTagHistory.upateUserViewNewsTags(uid, news.tags)
    return HttpResponseRedirect(news.pageurl)