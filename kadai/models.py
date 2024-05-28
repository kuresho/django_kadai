from accounts.models import CustomUser
from django.db import models

class Kadai(models.Model):
    user = models.ForeignKey(CustomUser,verbose_name='ユーザー',on_delete=models.PROTECT)
    year = models.PositiveSmallIntegerField	(
        verbose_name='年',
        blank=True,
        null=False
    )
    month = models.PositiveSmallIntegerField	(
        verbose_name='月',
        blank=True,
        null=False
    )
    words = models.TextField(verbose_name='検索ワード',blank=True,null=True)
    search_at = models.DateTimeField(verbose_name='検索日時',auto_now=True)

    class Meta:
        verbose_name_plural = 'Kadai'