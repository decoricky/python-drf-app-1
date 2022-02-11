# Generated by Django 4.0.2 on 2022-02-11 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmonster', '0003_alter_attendancehistory_attendance_date'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='attendancehistory',
            name='attendance_history_uidx_1',
        ),
        migrations.RenameField(
            model_name='attendancehistory',
            old_name='attendance_date',
            new_name='attendance_datetime',
        ),
        migrations.AddConstraint(
            model_name='attendancehistory',
            constraint=models.UniqueConstraint(fields=('user', 'program', 'attendance_datetime'), name='attendance_history_uidx_1'),
        ),
    ]