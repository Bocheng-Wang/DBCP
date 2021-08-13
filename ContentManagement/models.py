from django.db import models

# Create your models here.
from django.utils import timezone


class Userip(models.Model):
    ip = models.CharField(verbose_name='IP', max_length=30)
    count = models.IntegerField(verbose_name='visit', default=0)
    visitTime = models.DateTimeField(auto_now_add=True)
    memo = models.CharField(verbose_name='memo', max_length=300)
    class Meta:
        verbose_name = 'visitor'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip


class VisitNumber(models.Model):
    count = models.IntegerField(verbose_name='total visits', default=0)

    class Meta:
        verbose_name = 'total visits'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.count)
