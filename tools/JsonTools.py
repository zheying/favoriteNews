# -*- coding: UTF-8 -*- 
__author__ = 'zengzheying'

from django.db import models

import json
import time
from datetime import datetime
from server.models import *

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, models.Model):
            d = obj.__dict__
            if '_state' in d:
                d.pop('_state')
            if 'content' in d and isinstance(d, SinaNews):
                d.pop('content')
            # if d.has_key('date') and isinstance(d['date'], datetime):
            #     d['date'] = int(time.mktime(d['date'].timetuple())) - 8 * 60 * 60
            for k, v in d.iteritems():
                if isinstance(v, datetime):
                    d[k] = int(time.mktime(v.timetuple())) - 8 * 60 * 60
                # d['date'] = int(time.mktime(datetime.now().timetuple()))
            # if d.has_key('date') and d['date'] is None:
            #     d['date'] = int(time.mktime(d['date'].timetuple()))
                # d['date'] = int(time.mktime(datetime.now().timetuple()))
            return d
        if isinstance(obj, datetime):
            return int(time.mktime(obj.timetuple())) - 8 * 60 * 60
        return json.JSONEncoder.default(self, obj)


