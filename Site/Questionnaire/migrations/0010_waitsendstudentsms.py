# Generated by Django 2.1 on 2019-01-03 04:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Questionnaire', '0009_chat_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaitSendStudentSmS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('context', models.TextField()),
                ('student_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Student')),
            ],
        ),
    ]
