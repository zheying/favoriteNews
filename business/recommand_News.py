#!usr/bin/python
#encoding=utf-8
import sys 
import MySQLdb
import copy
import datetime
#from datetime import *

reload(sys)
sys.setdefaultencoding('utf-8') 
conn=MySQLdb.connect(host="120.25.217.247",user="root",passwd="zengzheying@icloud.com",db="favorite_news",charset='utf8')
cursor =conn.cursor()


longHobby_weight = {}
shortHobby_weight = {}
synA_syns = {}
longHobbies_rec = []
#shortHobbies_rec = []
cat_num = {}

#打开文件
def openFile(filename):
    file = open(filename)
    lines = file.readlines()
    return lines

#从uid_longHobby_time数据表获取用户的长期兴趣标签，如果四天没看并且有三天没有给用户推荐则继续推荐，如果四天没看并且中止给用户推荐的天数小于3天，则不推荐，interval+1；如果四天内有看，则加入推荐标签以及interval置0；
def getLongHobbies(uid):
    cursor.execute("select * from uid_longHobby_time where uid=" + uid)
    longHobbies = cursor.fetchall()
    todayTime = datetime.date.today()
    for longHobby in longHobbies:
        interval = longHobby[4]
        lastVisit = longHobby[3]
        #print todayTime
        lastTime = (todayTime - lastVisit).days
        #print lastTime
        #print longHobby[2]
        if lastTime >4:
            if interval < 3:
                cursor.execute('update `uid_longHobby_time` set `interval`=' + str(interval+1) + ' where `uid`=' + uid + ' and `longHobby`="' + longHobby[2] + '"')
                conn.commit()
            else:
                longHobbies_rec.append(longHobby[2])
                cursor.execute("update `uid_longHobby_time` set `interval`=0 where `uid`=" + uid + " and `longHobby`=" + "\"" + longHobby[2] + "\"")
                conn.commit()
        else:
            longHobbies_rec.append(longHobby[2])
            cursor.execute("update `uid_longHobby_time` set `interval`=0 where `uid`=" + uid + " and `longHobby`=" + "\"" + longHobby[2] + "\"")
            conn.commit()
    return longHobbies_rec

#从uid_shortHobby_time数据表获取用户的短期兴趣标签，如果用户七天没有访问该兴趣标签，则跳过，否则加入短期推荐兴趣标签。    
def getShortHobbies(uid):
    shortHobbies_rec = []
    cursor.execute("select * from uid_shortHobby_time where uid=" + uid)
    shortHobbies = cursor.fetchall()
    today = datetime.date.today()
    #print today
    for shortHobby in shortHobbies:
        #print shortHobby[2]
        lastVisit = shortHobby[3]
        lastTime = (today - lastVisit).days
        if lastTime >7:
            continue
        else:
            shortHobbies_rec.append(shortHobby[2])
            #print shortHobby[2]
    return shortHobbies_rec

#根据用户的uid_newsCat_num数据表，得到其兴趣阅读类别以做随机推荐类别
def gen_randomNews(uid):
    cursor.execute("select * from uid_newsCat_num where uid=" + uid)
    cats = cursor.fetchall()
    #for cat in cats:
    #print cat[2] + "\t" + cat[3]
    for cat in cats:
        cat_num[cat[2]] = cat[3]
    
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
            synA_syns.setdefault(synoym,[]).append(synoyms_duplicate)
    return synA_syns

#根据同义词字典添加长期兴趣标签的同义词到推荐标签中,目前不用，而用word2vec计算两个词的相似度
def add_syn_to_longHobbies(uid):
    longHobbies_rec = getLongHobbies(uid)
    for longHobby in longHobbies_rec:
        if synA_syns.has_key(longHobby):
            for syn in synA_syns[longHobby]:
                longHobbies_rec.append(syn)
                #synA = cursor.execute("select time,internal from uid_longHobby_time where uid=" + uid + "and longHobby=" + longHobby)
                #cursor.execute("insert into uid_longHobby_time(uid,longHobby,time,internal values(" + uid + "," + synA[0] + "," + synA[1] + ")")
        else:
            continue
    return longHobbies_rec
        
#根据同义词字典添加短期兴趣标签的同义词到推荐标签中    ,目前不用，而用word2vec计算两个词的相似度    
def add_syn_to_shortHobbies(uid):
    shortSyn_rec = []
    shortSource_rec = getShortHobbies(uid)
    for shortHobby in shortSource_rec:
        #print shortHobby
        if synA_syns.has_key(shortHobby):
            print "\\\\\\\\"
            for a in synA_syns[shortHobby]:
                for syn in a:
                    shortSyn_rec.append(syn)
                    print syn
                #synA = cursor.execute("select time,internal from uid_longHobby_time where uid=" + uid + "and longHobby=" + longHobby)
                #cursor.execute("insert into uid_longHobby_time(uid,longHobby,time,internal values(" + uid + "," + synA[0] + "," + synA[1] + ")")
        else:
            continue
    return shortSyn_rec
    
if __name__ == "__main__": 
    gen_syn()
    for a in synA_syns.keys():
        if synA_syns.has_key("火影"):
            #print "''''''''"
            d = "d"
        #print a
        for aa in synA_syns[a]:
            #print aa
            aa = "aa"
    uid = "2202887130"
    getLongHobbies(uid)
    #add_syn_to_longHobbies(uid)
    shortHobbies_rec = getShortHobbies(uid)
    for shortHobby in shortHobbies_rec:
        #print shortHobby
        if synA_syns.has_key(shortHobby):
            #print "[[[[[]]]]]]"
            c = "c"
        else:
            print "[[[[[]]]]]]"
    shortSyn_rec = add_syn_to_shortHobbies(uid)
    gen_randomNews(uid)
    randomHobbies_rec = []
    for cat in cat_num.keys():
        randomHobbies_rec.append(cat)
    recommend_News = longHobbies_rec + shortHobbies_rec + randomHobbies_rec #输出长期兴趣标签、短期兴趣标签和随机推荐的新闻类别；
    for news in recommend_News:
        #print news
        a = "a"
    
cursor.close()
conn.close()