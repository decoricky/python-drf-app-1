import os.path
import uuid
from typing import List

from django.db import models

from account.models import User
from bmonster.services.scraping import ScrapingItem, get_schedule_by_studio, parse_schedule_to_performer_and_program


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


def upload_image_path(instance, filename):
    return os.path.join(str(instance.user.id), str(uuid.uuid4()), filename)


class AttendanceHistory(models.Model):
    class Meta:
        db_table = 'attendance_history'
        constraints = [
            models.UniqueConstraint(fields=['user', 'program', 'attendance_datetime'], name='attendance_history_uidx_1'),
        ]

    user = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.CASCADE, db_index=True)
    program = models.ForeignKey(Program, verbose_name='プログラム', on_delete=models.CASCADE)
    attendance_datetime = models.DateTimeField(verbose_name='受講日時')
    image = models.FileField(verbose_name='写真', null=True, upload_to=upload_image_path)
    created_datetime = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    modified_datetime = models.DateTimeField(verbose_name='変更日時', auto_now=True)


def update_data():
    query_set = Studio.objects.all()
    item_list: List[ScrapingItem] = []
    for studio in query_set:
        studio_code = studio.code
        studio_name = studio.name
        item_list += get_schedule_by_studio(studio_code, studio_name)

    performer_name_set, program_name_set = parse_schedule_to_performer_and_program(item_list)

    for name in performer_name_set:
        try:
            performer = Performer.objects.get(name=name)
        except Performer.DoesNotExist:
            performer = Performer(name=name)
        performer.save()

    for performer_name, program_name in program_name_set:
        performer = Performer.objects.get(name=performer_name)
        try:
            program = Program.objects.get(performer=performer, name=program_name)
        except Program.DoesNotExist:
            program = Program(performer=performer, name=program_name)
        program.save()

    for item in item_list:
        studio_name = item.studio_name
        start_time = item.start_time
        performer_name = item.performer_name
        program_name = item.program_name

        studio = Studio.objects.get(name=studio_name)
        performer = Performer.objects.get(name=performer_name)
        program = Program.objects.get(performer=performer, name=program_name)

        try:
            schedule = Schedule.objects.get(studio=studio, start_time=start_time)
        except Schedule.DoesNotExist:
            schedule = Schedule(studio=studio, start_time=start_time, performer=performer, program=program)
        schedule.save()
