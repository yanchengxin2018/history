# Generated by Django 2.0 on 2019-02-24 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_familiarmodel_recordmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='models',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
