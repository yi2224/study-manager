# 数据库初始迁移文件
# 自动生成的Django迁移文件

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(help_text='主任务的名称', max_length=200, verbose_name='任务名称')),
                ('task_desc', models.TextField(blank=True, help_text='任务的详细描述', null=True, verbose_name='任务描述')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('deadline', models.DateTimeField(help_text='任务的截止日期和时间', verbose_name='截止时间')),
                ('progress', models.FloatField(default=0.0, help_text='任务完成进度百分比0-100', verbose_name='完成进度')),
            ],
            options={
                'verbose_name': '主任务',
                'verbose_name_plural': '主任务列表',
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_name', models.CharField(help_text='子任务的名称', max_length=200, verbose_name='子任务名称')),
                ('is_finish', models.BooleanField(default=False, help_text='子任务完成状态', verbose_name='是否完成')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('main_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.maintask', verbose_name='关联主任务')),
            ],
            options={
                'verbose_name': '子任务',
                'verbose_name_plural': '子任务列表',
                'ordering': ['create_time'],
            },
        ),
        migrations.CreateModel(
            name='StudyRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('study_start', models.DateTimeField(auto_now_add=True, verbose_name='学习开始时间')),
                ('study_end', models.DateTimeField(verbose_name='学习结束时间')),
                ('study_duration', models.IntegerField(help_text='本次学习的时长', verbose_name='学习时长（分钟）')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='study_records', to='study.maintask', verbose_name='关联任务')),
            ],
            options={
                'verbose_name': '学习记录',
                'verbose_name_plural': '学习记录列表',
                'ordering': ['-study_start'],
            },
        ),
    ]
