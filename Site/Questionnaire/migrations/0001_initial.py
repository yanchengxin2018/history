# Generated by Django 2.1 on 2018-12-29 07:00

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.IntegerField(help_text='此动作用一个数字表示')),
                ('help', models.TextField(help_text='动作的描述')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now=True)),
                ('city_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CityCityHead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CitySchool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.City')),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(help_text='班级名称', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='ClassQuestionnaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Class')),
            ],
        ),
        migrations.CreateModel(
            name='ClassStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Class')),
            ],
        ),
        migrations.CreateModel(
            name='ClassTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.ForeignKey(help_text='选择班级', on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Class')),
            ],
        ),
        migrations.CreateModel(
            name='Codes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('mobile', models.CharField(max_length=15)),
                ('type', models.IntegerField(choices=[(1, '注册'), (2, '改密')], help_text='1为注册,2为修改密码')),
            ],
        ),
        migrations.CreateModel(
            name='ErrorCommit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now=True)),
                ('original_name', models.CharField(max_length=100)),
                ('original_school', models.CharField(max_length=100)),
                ('original_grade', models.CharField(max_length=100)),
                ('original_class', models.CharField(max_length=100)),
                ('original_code', models.CharField(max_length=100)),
                ('error_type', models.CharField(choices=[(1, '问卷里提供的信息不足以查询到这个学生'), (2, '提交者信息被匹配为学校的学生但是未被邀请填写问卷'), (3, '所属任务因为[已提交/已过期等原因]已经关闭'), (4, '匹配到多个学生,并且多个学生都拥有这份问卷,系统不知道具体是哪一个问卷任务'), (5, '此问卷没有在服务器注册,请及时注册,以免耽误正常业务.'), (6, '通过提交的信息匹配到多个学生,但是所有的学生都没有被邀请.')], max_length=100)),
                ('error_help', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_name', models.CharField(help_text='输入年级名称', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='GradeClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Class')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Grade')),
            ],
        ),
        migrations.CreateModel(
            name='GradeGradeHead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='MatchButError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matcherrorcommit_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.ErrorCommit')),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now=True)),
                ('province_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ProvinceProvinceHead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateField(auto_now=True)),
                ('questionnaire_url', models.CharField(help_text='问卷的链接', max_length=100, unique=True)),
                ('questionnaire_code', models.CharField(help_text='问卷的唯一编码', max_length=100, unique=True)),
                ('questionnaire_name', models.CharField(help_text='问卷的名字', max_length=100)),
                ('school_name_field', models.IntegerField(help_text='告诉服务器问卷里学生的学校填在了哪个字段[例如field_13就填13即可]')),
                ('grade_name_field', models.IntegerField(help_text='告诉服务器问卷里学生的年级填在了哪个字段[例如field_14就填14即可]')),
                ('class_name_field', models.IntegerField(help_text='告诉服务器问卷里学生的班级填在了哪个字段[例如field_15就填15即可]')),
                ('student_name_field', models.IntegerField(help_text='告诉服务器问卷里学生的姓名填在了哪个字段[例如field_16就填16即可]')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionnaireType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(help_text='添加问卷类型[例如学生问卷家长问卷]', max_length=50)),
                ('help', models.TextField(help_text='备注信息', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResourceRoleAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.ForeignKey(help_text='选择动作', on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Action')),
            ],
        ),
        migrations.CreateModel(
            name='Resources',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource', models.CharField(help_text='接口的完整类名在此注册', max_length=50)),
                ('help', models.TextField(help_text='输入接口的帮助信息', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(help_text='为角色命名', max_length=10, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(help_text='输入学校的名称', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Grade')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.School')),
            ],
        ),
        migrations.CreateModel(
            name='SchoolMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.School')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='StudentQuestionnaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('questionnaire_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Questionnaire')),
                ('student_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valied', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherQuestionnaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('questionnaire', models.ForeignKey(help_text='绑定问卷', on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Questionnaire')),
                ('teacher', models.ForeignKey(help_text='绑定老师', on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='UsersRoles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Roles')),
            ],
        ),
        migrations.CreateModel(
            name='WaitSend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(help_text='在这里输入需要发送的内容')),
                ('content_type', models.CharField(choices=[(1, '批量注册老师'), (2, '家长问卷通知'), (3, '其他类型的通知')], max_length=10)),
                ('remark', models.TextField(help_text='在这里输入帮助信息')),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(help_text='账户名', max_length=20, unique=True)),
                ('mobile', models.CharField(help_text='手机号', max_length=15, unique=True)),
                ('age', models.IntegerField(default=0, help_text='年龄')),
                ('sex', models.CharField(choices=[('男', '男'), ('女', '女'), ('未知', '未知')], default='未知', help_text='性别', max_length=5)),
                ('e_maile', models.EmailField(max_length=254, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('password', models.CharField(help_text='密码', max_length=50)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='waitsend',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usersroles',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userrole', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(help_text='绑定用户', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(help_text='绑定用户', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='schoolmaster',
            name='user_obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='resourceroleaction',
            name='resource',
            field=models.ForeignKey(help_text='在此处选择接口', on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Resources'),
        ),
        migrations.AddField(
            model_name='resourceroleaction',
            name='role',
            field=models.ForeignKey(help_text='选择角色', on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Roles'),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='questionnaire_type',
            field=models.ForeignKey(help_text='问卷的类型', on_delete=False, to='Questionnaire.QuestionnaireType'),
        ),
        migrations.AddField(
            model_name='provinceprovincehead',
            name='province_head_obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='provinceprovincehead',
            name='province_obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Province'),
        ),
        migrations.AddField(
            model_name='matchbuterror',
            name='matchstudent_obj',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Student'),
        ),
        migrations.AddField(
            model_name='matchbuterror',
            name='matchstudentquestionnaire_obj',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.StudentQuestionnaire'),
        ),
        migrations.AddField(
            model_name='gradegradehead',
            name='grade_head_obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='gradegradehead',
            name='grade_obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Grade'),
        ),
        migrations.AddField(
            model_name='classteacher',
            name='teacher',
            field=models.ForeignKey(help_text='选择老师', on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Teacher'),
        ),
        migrations.AddField(
            model_name='classstudent',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Student'),
        ),
        migrations.AddField(
            model_name='classquestionnaire',
            name='questionnaire_obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Questionnaire'),
        ),
        migrations.AddField(
            model_name='cityschool',
            name='school_obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.School'),
        ),
        migrations.AddField(
            model_name='citycityhead',
            name='city_head_obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='citycityhead',
            name='city_obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.City'),
        ),
        migrations.AddField(
            model_name='city',
            name='province_obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.Province'),
        ),
        migrations.AlterUniqueTogether(
            name='usersroles',
            unique_together={('user', 'role')},
        ),
        migrations.AlterUniqueTogether(
            name='studentquestionnaire',
            unique_together={('student_obj', 'questionnaire_obj')},
        ),
        migrations.AlterUniqueTogether(
            name='schoolgrade',
            unique_together={('school', 'grade')},
        ),
        migrations.AlterUniqueTogether(
            name='provinceprovincehead',
            unique_together={('province_obj', 'province_head_obj')},
        ),
        migrations.AlterUniqueTogether(
            name='gradeclass',
            unique_together={('class_name', 'grade')},
        ),
        migrations.AlterUniqueTogether(
            name='classstudent',
            unique_together={('s_class', 'student')},
        ),
        migrations.AlterUniqueTogether(
            name='classquestionnaire',
            unique_together={('class_obj', 'questionnaire_obj')},
        ),
        migrations.AlterUniqueTogether(
            name='citycityhead',
            unique_together={('city_obj', 'city_head_obj')},
        ),
    ]
