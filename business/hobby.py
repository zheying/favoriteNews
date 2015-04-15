# -*- coding: UTF-8 -*-
__author__ = 'zengzheying'

from server.models import *
from datetime import date, timedelta
from django.core.exceptions import ObjectDoesNotExist

class ShortTimeHobby:

    @classmethod
    def addHobby(cls, uid, tag):
        try:
            hobby = UidShorthobbyTime.objects.get(uid=uid, shorthobby=tag, time=date.today())
        except ObjectDoesNotExist:
            hobby = UidShorthobbyTime()
            hobby.uid = uid
            hobby.shorthobby = tag
            hobby.time = date.today()
            hobby.save()

    @classmethod
    def updateHobby(cls, uid, tags):
        if tags is not None and tags.strip() != '':
            listOfTags = tags.split('|')
            for v in listOfTags:
                if v.strip() != '':
                    count = len(UidShorthobbyTime.objects.filter(uid=uid, shorthobby=v,
                                                                 time__gt=date.today() - timedelta(15)))
                    if count > 0:
                        ShortTimeHobby.addHobby(uid, v)
