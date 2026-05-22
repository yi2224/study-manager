from django.urls import path
from . import views

app_name = 'study'

urlpatterns = [
    # 首页
    path('', views.index, name='index'),

    # 任务管理
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),

    # 子任务管理（AJAX接口）
    path('api/subtask/create/', views.subtask_create, name='subtask_create'),
    path('api/subtask/toggle/', views.subtask_toggle, name='subtask_toggle'),
    path('api/subtask/delete/', views.subtask_delete, name='subtask_delete'),

    # 番茄钟
    path('pomodoro/', views.pomodoro, name='pomodoro'),
    path('api/pomodoro/finish/', views.pomodoro_finish, name='pomodoro_finish'),

    # 数据统计
    path('statistics/', views.statistics, name='statistics'),

    # API接口
    path('api/task/<int:task_id>/', views.api_task_detail, name='api_task_detail'),
]
