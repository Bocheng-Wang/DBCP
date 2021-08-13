import datetime

from django.db import models
from django.utils.translation import gettext as _
# Create your models here.
from UserManagement import Toolbox


class User(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    affiliation = models.CharField(max_length=256, default='')
    email = models.EmailField(unique=True)
    # sex = models.CharField(max_length=32, choices=gender, default="男")
    usage = models.CharField(max_length=1024, default='')
    c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"
