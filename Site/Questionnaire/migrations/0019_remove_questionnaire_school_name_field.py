# Generated by Django 2.1.4 on 2019-03-04 03:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Questionnaire', '0018_auto_20190114_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionnaire',
            name='school_name_field',
        ),
    ]
