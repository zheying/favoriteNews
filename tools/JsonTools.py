# -*- coding: UTF-8 -*- 
__author__ = 'zengzheying'

from django.db import models

import json
import time
from datetime import datetime

class MyEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj, models.Model):
            d = obj.__dict__
            if d.has_key('_state'):
                d.pop('_state')
            if d.has_key('content'):
                d.pop('content')
            if d.has_key('date') and isinstance(d['date'], datetime):
                # d['time'] = int(time.mktime(d['time'].timetuple()))
                d['date'] = int(time.mktime(datetime.now().timetuple()))
            if d.has_key('date') and d['date'] is None:
                # d['time'] = int(time.mktime(d['time'].timetuple()))
                d['date'] = int(time.mktime(datetime.now().timetuple()))
            return d
        return json.JSONEncoder.default(self, obj)

