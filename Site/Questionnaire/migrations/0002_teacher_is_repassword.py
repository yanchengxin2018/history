# Generated by Django 2.1 on 2019-01-02 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Questionnaire', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='is_repassword',
            field=models.BooleanField(default=False),
        ),
    ]