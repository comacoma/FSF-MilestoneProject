# Generated by Django 2.1 on 2018-09-25 16:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issuetracker', '0007_auto_20180923_1300'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgressLog',
            fields=[
                ('date', models.DateField(primary_key=True, serialize=False)),
                ('bug_tended', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(1)])),
                ('feature_tended', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)])),
            ],
        ),
    ]
