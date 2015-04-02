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


# class DjangoMigrations(models.Model):
#     id = models.IntegerField(primary_key=True)  # AutoField?
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'django_migrations'

class User(models.Model):
    uid = models.CharField(primary_key=True, max_length=80)
    name = models.CharField(max_length=100)
    token = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'user'

class Tags(models.Model):
    uid = models.ForeignKey('User', db_column='uid', primary_key=True)
    tag = models.TextField()

    class Meta:
        managed = False
        db_table = 'tags'



