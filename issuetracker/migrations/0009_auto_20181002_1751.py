# Generated by Django 2.1 on 2018-10-02 16:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issuetracker', '0008_progresslog'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fund',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='progresslog',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='progresslog',
            name='bug_tended',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(3)]),
        ),
    ]