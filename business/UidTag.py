# -*- coding: UTF-8 -*-
__author__ = 'zengzheying'

from server.models import TagsViewHistory
from django.core.exceptions import ObjectDoesNotExist

class UidTagHistory:

    @classmethod
    def upateUserViewNewsTags(cls, uid, tags):
        if uid is not None:
            if tags.strip() != '' and tags.strip() != 'null tag':
                tags = tags.split('|')
                for tag in tags:
                    if tag != '':
                        try:
                            tvh = TagsViewHistory.objects.get(uid=uid, tag=tag)
                            count = tvh.count + 1
                            tvh.count = count
                            tvh.save()
                        except ObjectDoesNotExist:
                            tvh = TagsViewHistory()
                            tvh.uid = uid
                            tvh.tag = tag
                            tvh.count = 1
                            tvh.save()