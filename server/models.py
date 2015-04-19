# -*- coding: UTF-8 -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models




class SinaNews(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    cat = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    source = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.TextField()
    picurl = models.CharField(db_column='picUrl', max_length=800)  # Field name made lowercase.
    pageurl = models.CharField(db_column='pageUrl', max_length=200)  # Field name made lowercase.
    mobile_html = models.TextField()

    class Meta:
        managed = False
        db_table = 'sina_news'


class TagsViewHistory(models.Model):
    uid = models.CharField(primary_key=True, max_length=200)
    tag = models.CharField(primary_key=True, max_length=200)
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tags_view_history'
        unique_together=('uid','tag')


class UidLonghobbyTime(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    uid = models.CharField(max_length=2000)
    longhobby = models.CharField(db_column='longHobby', max_length=2000)  # Field name made lowercase.
    time = models.DateField()
    interval = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'uid_longHobby_time'


class UidNewscatNum(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    uid = models.CharField(max_length=2000)
    newscat = models.CharField(db_column='newsCat', max_length=2000)  # Field name made lowercase.
    num = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'uid_newsCat_num'


class UidShorthobbyTime(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=2000)
    shorthobby = models.CharField(db_column='shortHobby', max_length=2000)  # Field name made lowercase.
    time = models.DateField()

    class Meta:
        managed = False
        db_table = 'uid_shortHobby_time'

class User(models.Model):
    uid = models.CharField(primary_key=True, max_length=80)
    name = models.CharField(max_length=100)
    token = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'user'


class UidTags(models.Model):
    uid = models.ForeignKey('User', db_column='uid', primary_key=True)
    tag = models.TextField()

    class Meta:
        managed = False
        db_table = 'uid_tags'


class NewsComment(models.Model):
    uid = models.CharField(max_length=80)
    news_id = models.IntegerField()
    content = models.TextField()
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'news_comment'