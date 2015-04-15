# -*- coding: UTF-8 -*-
__author__ = 'zengzheying'
from datetime import datetime
from server.models import *
from django.core.exceptions import ObjectDoesNotExist

class CommentHelper:

    @classmethod
    def addComment(cls, uid, news_id, content):
        comment = NewsComment()
        comment.uid = uid
        comment.news_id = news_id
        comment.content = content
        comment.time = datetime.now()
        comment.save()

    @classmethod
    def deleteComment(cls, uid, cid):
        try:
            comment = NewsComment.objects.get(id=cid)
            if comment.uid != uid:
                raise ValueError('uid does not match')
            comment.delete()
        except ObjectDoesNotExist, e:
            raise e

