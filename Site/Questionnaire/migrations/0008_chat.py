# Generated by Django 2.1 on 2019-01-03 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Questionnaire', '0007_auto_20190102_1915'),
    ]

    operations = [
        migrations.CreateModel(
            name='chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('centext', models.CharField(max_length=100)),
            ],
        ),
    ]
