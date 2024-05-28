from accounts.models import CustomUser
from django.db import models

class kadai(models.Model):
    """課題モデル"""

    user = models.ForeignKey(CustomUser,verbose_name='ユーザー',on_delete=models.PROTECT)
    year = models.SmallAutoField(verbose_name='年',null=False)
    month = models.SmallAutoField(verbose_name='月',null=False)
    word = models.TextField(verbose_name='検索ワード',blank=True,null=True)
