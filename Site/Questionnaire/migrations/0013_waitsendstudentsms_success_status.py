# Generated by Django 2.1 on 2019-01-03 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Questionnaire', '0012_waitsendstudentsms_questionnaire_obj'),
    ]

    operations = [
        migrations.AddField(
            model_name='waitsendstudentsms',
            name='success_status',
            field=models.BooleanField(default=True),
        ),
    ]
