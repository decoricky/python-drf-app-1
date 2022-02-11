from django.db import models

from account.models import User


class Studio(models.Model):
    class Meta:
        db_table = 'studio'

    code = models.CharField(verbose_name='コード', max_length=4, unique=True, db_index=True)
    name = models.CharField(verbose_name='スタジオ', max_length=16, unique=True, db_index=True)
    created_datetime = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    modified_datetime = models.DateTimeField(verbose_name='変更日時', auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Performer(models.Model):
    class Meta:
        db_table = 'performer'

    name = models.CharField(verbose_name='パフォーマー', max_length=16, unique=True, db_index=True)
    created_datetime = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    modified_datetime = models.DateTimeField(verbose_name='変更日時', auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Program(models.Model):
    class Meta:
        db_table = 'program'
        constraints = [
            models.UniqueConstraint(fields=['performer', 'name'], name='program_uidx_1'),
        ]

    performer = models.ForeignKey(Performer, verbose_name='パフォーマー', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='プログラム名', max_length=16)
    created_datetime = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    modified_datetime = models.DateTimeField(verbose_name='変更日時', auto_now=True)

    def __str__(self):
        return f'{self.performer}:{self.name}'


class Schedule(models.Model):
    class Meta:
        db_table = 'schedule'
        constraints = [
            models.UniqueConstraint(fields=['studio', 'start_time'], name='schedule_uidx_1'),
        ]

    studio = models.ForeignKey(Studio, verbose_name='スタジオ', on_delete=models.CASCADE)
    start_time = models.DateTimeField(verbose_name='開始日時')
    performer = models.ForeignKey(Performer, verbose_name='パフォーマー', on_delete=models.CASCADE)
    program = models.ForeignKey(Program, verbose_name='プログラム', on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    modified_datetime = models.DateTimeField(verbose_name='変更日時', auto_now=True)


class AttendanceHistory(models.Model):
    class Meta:
        db_table = 'attendance_history'
        constraints = [
            models.UniqueConstraint(fields=['user', 'program', 'attendance_datetime'], name='attendance_history_uidx_1'),
        ]

    user = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.CASCADE, db_index=True)
    program = models.ForeignKey(Program, verbose_name='プログラム', on_delete=models.CASCADE)
    attendance_datetime = models.DateTimeField(verbose_name='受講日時')
    created_datetime = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    modified_datetime = models.DateTimeField(verbose_name='変更日時', auto_now=True)
