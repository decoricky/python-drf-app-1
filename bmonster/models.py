from django.db import models


class Studio(models.Model):
    class Meta:
        db_table = 'studio'

    code = models.CharField(verbose_name='コード', max_length=4, unique=True, db_index=True)
    name = models.CharField(verbose_name='スタジオ', max_length=16, unique=True, db_index=True)
    created_datetime = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    modified_datetime = models.DateTimeField(verbose_name='変更日時', auto_now=True)

    def __str__(self):
        return f'{self.code}:{self.name}'
