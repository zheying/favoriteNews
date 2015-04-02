import json
__author__ = 'zengzheying'


def response(rep):
    result = dict(c=0)
    result['d'] = rep
    return json.dumps(result)

def responseError(errorCode, errorMessage):
    return json.dumps(dict(c=errorCode, msg=errorMessage)).encode("utf8")

