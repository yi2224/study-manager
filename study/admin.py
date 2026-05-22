from django.contrib import admin
from .models import MainTask, SubTask, StudyRecord


# 主任务管理
@admin.register(MainTask)
class MainTaskAdmin(admin.ModelAdmin):
    """主任务管理界面"""
    list_display = ['task_name', 'deadline', 'progress', 'create_time']
    list_filter = ['create_time', 'deadline']
    search_fields = ['task_name', 'task_desc']
    readonly_fields = ['create_time', 'progress']
    fieldsets = (
        ('基本信息', {
            'fields': ('task_name', 'task_desc')
        }),
        ('时间信息', {
            'fields': ('create_time', 'deadline')
        }),
        ('进度', {
            'fields': ('progress',)
        }),
    )


# 子任务管理
@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    """子任务管理界面"""
    list_display = ['sub_name', 'main_task', 'is_finish', 'create_time']
    list_filter = ['is_finish', 'create_time', 'main_task']
    search_fields = ['sub_name', 'main_task__task_name']
    readonly_fields = ['create_time']


# 学习记录管理
@admin.register(StudyRecord)
class StudyRecordAdmin(admin.ModelAdmin):
    """学习记录管理界面"""
    list_display = ['task', 'study_duration', 'study_start', 'study_end']
    list_filter = ['study_start', 'task']
    search_fields = ['task__task_name']
    readonly_fields = ['study_start', 'study_end']
    date_hierarchy = 'study_start'
