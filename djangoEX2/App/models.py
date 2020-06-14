import datetime

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    user_type = models.IntegerField(choices=((1, '普通用户'), (2, 'VIP'), (3, 'VVIP')), default=1)


class UserToken(models.Model):
    user = models.OneToOneField(to='User', on_delete=models.CASCADE)
    token = models.CharField(max_length=128)


class Order(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(to='User', on_delete=models.CASCADE)
    createDate = models.DateTimeField(default=datetime.datetime.now())
