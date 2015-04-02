# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from tools import Response
from business import UserInfo
from const import *
# Create your views here.

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