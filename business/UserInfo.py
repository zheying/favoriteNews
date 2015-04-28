# -*- coding: UTF-8 -*-
from server.models import *
from django.core.exceptions import ObjectDoesNotExist
__author__ = 'zengzheying'


def login(uid, name, token, avatar):
    try:
        u = User.objects.all().get(uid=uid)
        if u.name != name:
            u.name = name
        if u.token != token:
            u.token = token
        if u.avatar != avatar:
            u.avatar = avatar
        u.save()
        return u
    except ObjectDoesNotExist:
        u = User(uid=uid, name=name, token=token, avatar=avatar)
        u.save()
        return u


def get_tags(u):
    import urllib2
    url = "https://api.weibo.com/2/tags.json?uid=" + u.uid + "&access_token=" + u.token + "&source=942411083"
    req = urllib2.Request(url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    import json
    tags = json.loads(res)
    user_tags = ""
    for tag in tags:
        for k in tag.iterkeys():
            if k != 'weight' and k != 'flag':
               user_tags = user_tags + tag[k] + "\n"
    t = UidTags(uid=u, tag=user_tags)
    t.save()


def verify_user(uid, token):
    try:
        u = User.objects.get(uid=uid)
        return u.token == token
    except ObjectDoesNotExist:
        return False


def get_user(uid, token):
    try:
        u = User.objects.get(uid=uid)
        if u.token == token:
            return u
        else:
            return None
    except ObjectDoesNotExist:
        return None


def find_user_by_id(uid, token):
    try:
        return User.objects.get(uid=uid, token=token)
    except ObjectDoesNotExist:
        return None