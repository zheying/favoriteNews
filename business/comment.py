# -*- coding: UTF-8 -*-
__author__ = 'zengzheying'
from datetime import datetime
from server.models import *
from django.core.exceptions import ObjectDoesNotExist
import UserInfo
import pytz

class CommentHelper:

    @classmethod
    def add_comment(cls, uid, news_id, content):
        comment = NewsComment()
        comment.uid = uid
        comment.news_id = news_id
        comment.content = content
        comment.time = datetime.now(pytz.timezone('Asia/Shanghai'))
        comment.save()

    @classmethod
    def delete_comment(cls, uid, cid):
        try:
            comment = NewsComment.objects.get(id=cid)
            if comment.uid != uid:
                raise ValueError('uid does not match')
            comment.delete()
        except ObjectDoesNotExist, e:
            raise e

    @classmethod
    def get_comment_list_by_news_id(cls, uid, news_id):
        comment_list = []
        comments = NewsComment.objects.filter(news_id=news_id)
        if comments is not None:
            for comment in comments:
                comment_dict = {}
                comment_dict['cid'] = comment.id
                if comment.uid == uid:
                    comment_dict['uid'] = comment.uid
                else:
                    comment_dict['uid'] = ''
                comment_dict['news_id'] = comment.news_id
                comment_dict['content'] = comment.content
                u = UserInfo.find_user_by_id(comment.uid)
                comment_dict['avatar'] = u.avatar
                comment_dict['time'] = comment.time
                comment_dict['user_name'] = u.name
                comment_list.append(comment_dict)
        return comment_list


    @classmethod
    def get_comment_count_by_news_id(cls, news_id):
        comments = NewsComment.objects.filter(news_id=news_id)
        if comments is None:
            return 0
        return comments.count()
