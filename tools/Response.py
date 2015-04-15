import json
from tools.JsonTools import MyEncoder
__author__ = 'zengzheying'
from server.const import *

def response(rep):
    result = dict(c=RESULT_OK)
    result['msg'] = STRING_RESULT_OK
    if rep is not None:
        result['d'] = rep
    return json.dumps(result, cls=MyEncoder)

def responseError(errorCode, errorMessage):
    result = dict(c=errorCode)
    result['msg'] = errorMessage
    return json.dumps(result)
