# -*- coding: UTF-8 -*- 
__author__ = 'zengzheying'

import sys
import MySQLdb
import copy
import datetime
from models import *
# from jpype import *
#from datetime import *
reload(sys)
sys.setdefaultencoding('utf-8')


longHobby_weight = {}
shortHobby_weight = {}
synA_syns = {}
longHobbies_rec = []
shortHobbies_rec = []
cat_num = {}

#打开文件
def openFile(filename):
    file = open(filename)
    lines = file.readlines()
    return lines

#从uid_longHobby_time数据表获取用户的长期兴趣标签，如果四天没看并且有三天没有给用户推荐则继续推荐，如果四天没看并且中止给用户推荐的天数小于3天，则不推荐，interval+1；如果四天内有看，则加入推荐标签以及interval置0；
def getLongHobbies(uid):
    # cursor.execute("select * from uid_longHobby_time where uid=" + uid)
    # longHobbies = cursor.fetchall()
    longHobbies = UidLonghobbyTime.objects.filter(uid=uid)
    todayTime = datetime.date.today()
    for longHobby in longHobbies:
        interval = longHobby.interval
        lastVisit = longHobby.time
        #print todayTime
        lastTime = (todayTime - lastVisit).days
        #print lastTime
        #print longHobby[2]
        if lastTime >4:
            if interval < 3:
                # cursor.execute('update `uid_longHobby_time` set `interval`=' + str(interval+1) + ' where `uid`=' + uid + ' and `longHobby`="' + longHobby[2] + '"')
                # conn.commit()
                longHobby.interval = interval + 1
                longHobby.save()
            else:
                longHobbies_rec.append(longHobby.longhobby)
                # cursor.execute("update `uid_longHobby_time` set `interval`=0 where `uid`=" + uid + " and `longHobby`=" + "\"" + longHobby[2] + "\"")
                # conn.commit()
                longHobby.interval = 0
                longHobby.save()
        else:
            longHobbies_rec.append(longHobby.longhobby)
            # cursor.execute("update `uid_longHobby_time` set `interval`=0 where `uid`=" + uid + " and `longHobby`=" + "\"" + longHobby[2] + "\"")
            # conn.commit()
            longHobby.interval = 0
            longHobby.save()
    return longHobbies_rec

#从uid_shortHobby_time数据表获取用户的短期兴趣标签，如果用户七天没有访问该兴趣标签，则跳过，否则加入短期推荐兴趣标签。
def getShortHobbies(uid):
    shortHobbies_rec = []
    # cursor.execute("select * from uid_shortHobby_time where uid=" + uid)
    # shortHobbies = cursor.fetchall()
    shortHobbies = UidShorthobbyTime.objects.filter(uid=uid)
    today = datetime.date.today()
    #print today
    for shortHobby in shortHobbies:
        #print shortHobby[2]
        short = shortHobby.shorthobby.split("|")
        lastVisit = shortHobby.time
        lastTime = (today - lastVisit).days
        if lastTime > 7:
            continue
        else:
            for shortone in short:
                #shortHobbies_rec.append(shortHobby[2])
                shortHobbies_rec.append(shortone)
            #print shortHobby[2]
    return shortHobbies_rec

#根据用户的uid_newsCat_num数据表，得到其兴趣阅读类别以做随机推荐类别
def gen_randomNews(uid):
    # cursor.execute("select * from uid_newsCat_num where uid=" + uid)
    # cats = cursor.fetchall()
    cats = UidNewscatNum.objects.filter(uid=uid)
    #for cat in cats:
    #print cat[2] + "\t" + cat[3]
    for cat in cats:
        cat_num[cat.newscat] = cat.num

#计算用户标签和新闻标签的相似度
def simarlarity(tag, cat):
    # jvmpath = getDefaultJVMPath()
    # startJVM(jvmpath, "-ea", "-Djava.class.path=/home/zengzheying/project/favoriteNews/server/WORD2VEC.jar")
    # TA = JPackage('com.ansj.vec').WORD2VEC
    # jd = TA()
    # print jd is None
    # jd.loadModel("/home/zengzheying/project/favoriteNews/server/vectors1.bin")
    return 0

#根据用户uid产生的用户长期兴趣标签、短期兴趣标签和随机推荐标签
def get_recommend_news(user_id):
    uid = user_id
    longHobbies_rec = getLongHobbies(uid)
    shortHobbies_rec = getShortHobbies(uid)
    gen_randomNews(uid)
    randomHobbies_rec = []
    recommend_ID = []
    for cat in cat_num.keys():
        #print cat
        randomHobbies_rec.append(cat)
    recommend_News = longHobbies_rec + shortHobbies_rec + randomHobbies_rec #输出长期兴趣标签、短期兴趣标签和随机推荐的新闻类别；
    # cursor.execute("select id,tags from sina_news")
    # ID_cats = cursor.fetchall()
    ID_cats = SinaNews.objects.filter(date__gte=datetime.datetime.now() - datetime.timedelta(4)).order_by('-date')
    ID_cats = list(ID_cats)
    #print ID_cats
    for tag in recommend_News:
        for ID_cat in ID_cats:
            if tag in ID_cat.cat:
                recommend_ID.append(ID_cat)
                ID_cats.remove(ID_cat)
            else:
                for cat in ID_cat.cat.split("|"):
                    if simarlarity(tag, cat) > 0.8:
                        recommend_ID.append(ID_cat)
                        ID_cats.remove(ID_cat)
                        break
                    else:
                        continue
    return recommend_ID
    #return recommend_News

#根据synonyms.txt产生同义词字典    ,目前不用，而用word2vec计算两个词的相似度
def gen_syn():
    synonymsLines = openFile("synonyms.txt")
    for synonymsLine in synonymsLines:
        synoyms = synonymsLine.split("\t")
        #print synonymsLine
        for synoym in synoyms:
            #print synoym
            synoyms_duplicate = copy.deepcopy(synoyms)
            #print synoyms_duplicate
            synoyms_duplicate.remove(synoym)
            for aa in synoyms_duplicate:
                #print aa
                a = "aa"
            #synA_syns[synoym] = []
            synA_syns.setdefault(synoym, []).append(synoyms_duplicate)
    return synA_syns

#根据同义词字典添加长期兴趣标签的同义词到推荐标签中,目前不用，而用word2vec计算两个词的相似度
def add_syn_to_longHobbies(uid):
    longHobbies_rec = getLongHobbies(uid)
    for longHobby in longHobbies_rec:
        if synA_syns.has_key(longHobby):
            for syn in synA_syns[longHobby]:
                longHobbies_rec.append(syn)
        else:
            continue
    return longHobbies_rec

#根据同义词字典添加短期兴趣标签的同义词到推荐标签中    ,目前不用，而用word2vec计算两个词的相似度
def add_syn_to_shortHobbies(uid):
    shortSyn_rec = []
    shortSource_rec = getShortHobbies(uid)
    for shortHobby in shortSource_rec:
        if synA_syns.has_key(shortHobby):
            print "\\\\\\\\"
            for a in synA_syns[shortHobby]:
                for syn in a:
                    shortSyn_rec.append(syn)
                    print syn
        else:
            continue
    return shortSyn_rec

# if __name__ == "__main__":
def test_method():
    recommand_News = get_recommend_news("2202887130")
    # recommand_News = SinaNews.objects.filter(date__gte=datetime.datetime.now() - datetime.timedelta(7))
    for news in recommand_News:
        print news.id