from accounts.models import CustomUser
from django.db import models

class Kadai(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    year = models.CharField(verbose_name='年', max_length=4)
    month = models.CharField(verbose_name='月', max_length=2)
    words = models.CharField(verbose_name='検索ワード', blank=True, null=True)
    search_at = models.DateTimeField(verbose_name='検索日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Kadai'