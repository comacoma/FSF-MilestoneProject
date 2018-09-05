# Generated by Django 2.1 on 2018-09-05 10:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issuetracker', '0004_auto_20180904_2157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='last_modified',
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='last_modified',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='submission_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
