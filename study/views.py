from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count, Q
from datetime import timedelta
import json
import pandas as pd

from .models import MainTask, SubTask, StudyRecord


# ========== 首页视图 ==========
def index(request):
    """首页视图
    展示系统简介、核心数据看板（今日学习时长、已完成任务数、待完成任务数）
    """
    # 获取所有主任务
    all_tasks = MainTask.objects.all()

    # 计算今日学习时长（分钟）
    today = timezone.now().date()
    today_study_records = StudyRecord.objects.filter(study_start__date=today)
    today_study_duration = today_study_records.aggregate(total=Sum('study_duration'))['total'] or 0

    # 计算已完成任务数
    completed_tasks = all_tasks.filter(progress=100.0).count()

    # 计算待完成任务数
    pending_tasks = all_tasks.filter(progress__lt=100.0).count()

    # 获取即将过期的任务（24小时内）
    now = timezone.now()
    nearly_due_tasks = all_tasks.filter(deadline__lte=now + timedelta(hours=24), deadline__gt=now)

    context = {
        'today_study_duration': today_study_duration,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'nearly_due_tasks': nearly_due_tasks,
        'all_tasks_count': all_tasks.count(),
    }

    return render(request, 'study/index.html', context)


# ========== 学习任务管理视图 ==========
def task_list(request):
    """学习任务列表页面
    展示所有主任务及其子任务、完成进度
    """
    tasks = MainTask.objects.all()

    # 获取即将过期的任务
    now = timezone.now()
    nearly_due_tasks = [task for task in tasks if task.is_nearly_due()]
    overdue_tasks = [task for task in tasks if task.is_overdue()]

    context = {
        'tasks': tasks,
        'nearly_due_tasks': nearly_due_tasks,
        'overdue_tasks': overdue_tasks,
    }

    return render(request, 'study/task_list.html', context)


def task_create(request):
    """创建新的学习任务"""
    if request.method == 'POST':
        task_name = request.POST.get('task_name', '').strip()
        task_desc = request.POST.get('task_desc', '').strip()
        deadline = request.POST.get('deadline')

        if not task_name or not deadline:
            messages.error(request, '任务名称和截止时间不能为空')
            return redirect('study:task_create')

        try:
            MainTask.objects.create(
                task_name=task_name,
                task_desc=task_desc,
                deadline=deadline
            )
            messages.success(request, f'任务"{task_name}"创建成功！')
            return redirect('study:task_list')
        except Exception as e:
            messages.error(request, f'创建任务失败：{str(e)}')

    return render(request, 'study/task_form.html', {'action': 'create'})


def task_edit(request, task_id):
    """编辑学习任务"""
    task = get_object_or_404(MainTask, id=task_id)

    if request.method == 'POST':
        task.task_name = request.POST.get('task_name', '').strip() or task.task_name
        task.task_desc = request.POST.get('task_desc', '').strip()
        deadline = request.POST.get('deadline')

        if deadline:
            task.deadline = deadline

        try:
            task.save()
            messages.success(request, f'任务"{task.task_name}"更新成功！')
            return redirect('study:task_list')
        except Exception as e:
            messages.error(request, f'更新任务失败：{str(e)}')

    context = {
        'task': task,
        'action': 'edit',
    }

    return render(request, 'study/task_form.html', context)


def task_delete(request, task_id):
    """删除学习任务（级联删除子任务和学习记录）"""
    task = get_object_or_404(MainTask, id=task_id)
    task_name = task.task_name

    try:
        task.delete()
        messages.success(request, f'任务"{task_name}"已删除！')
    except Exception as e:
        messages.error(request, f'删除任务失败：{str(e)}')

    return redirect('study:task_list')


# ========== 子任务管理AJAX视图 ==========
@require_http_methods(["POST"])
def subtask_create(request):
    """创建子任务（AJAX）"""
    try:
        task_id = request.POST.get('task_id')
        sub_name = request.POST.get('sub_name', '').strip()

        if not task_id or not sub_name:
            return JsonResponse({'success': False, 'error': '参数不完整'})

        main_task = get_object_or_404(MainTask, id=task_id)

        subtask = SubTask.objects.create(
            main_task=main_task,
            sub_name=sub_name
        )

        return JsonResponse({
            'success': True,
            'message': '子任务添加成功',
            'subtask_id': subtask.id,
            'sub_name': subtask.sub_name,
            'is_finish': subtask.is_finish,
            'progress': main_task.progress,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_http_methods(["POST"])
def subtask_toggle(request):
    """切换子任务完成状态（AJAX）"""
    try:
        subtask_id = request.POST.get('subtask_id')
        subtask = get_object_or_404(SubTask, id=subtask_id)

        # 切换完成状态
        subtask.is_finish = not subtask.is_finish
        subtask.save()  # 自动触发主任务进度更新

        # 获取更新后的进度
        main_task = subtask.main_task
        progress = main_task.progress

        return JsonResponse({
            'success': True,
            'is_finish': subtask.is_finish,
            'progress': progress,
            'message': '状态已更新',
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_http_methods(["POST"])
def subtask_delete(request):
    """删除子任务（AJAX）"""
    try:
        subtask_id = request.POST.get('subtask_id')
        subtask = get_object_or_404(SubTask, id=subtask_id)
        main_task = subtask.main_task

        subtask.delete()
        progress = main_task.progress

        return JsonResponse({
            'success': True,
            'progress': progress,
            'message': '子任务已删除',
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ========== 番茄钟计时视图 ==========
def pomodoro(request):
    """番茄钟页面
    前端实现25分钟学习+5分钟休息的经典番茄模式
    """
    tasks = MainTask.objects.all()

    context = {
        'tasks': tasks,
    }

    return render(request, 'study/pomodoro.html', context)


@require_http_methods(["POST"])
def pomodoro_finish(request):
    """番茄钟完成后保存学习记录（AJAX）
    支持两种模式：
    1. 关联到具体任务：传入 task_id
    2. 自由学习模式：不传 task_id 或传空值，记录为无任务关联的学习时长
    """
    try:
        data = json.loads(request.body)
        task_id = data.get('task_id')
        study_duration = data.get('study_duration', 25)  # 默认25分钟

        main_task = None
        if task_id:
            main_task = get_object_or_404(MainTask, id=task_id)

        # 创建学习记录
        study_end = timezone.now()
        study_start = study_end - timedelta(minutes=int(study_duration))

        StudyRecord.objects.create(
            task=main_task,
            study_start=study_start,
            study_end=study_end,
            study_duration=int(study_duration)
        )

        return JsonResponse({
            'success': True,
            'message': '学习记录已保存',
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ========== 数据统计和可视化视图 ==========
def statistics(request):
    """数据统计页面
    展示日/周学习数据、任务完成率等
    """
    # 获取所有学习记录
    study_records = StudyRecord.objects.all().order_by('study_start')

    # 计算今日数据
    today = timezone.now().date()
    today_records = study_records.filter(study_start__date=today)
    today_duration = today_records.aggregate(total=Sum('study_duration'))['total'] or 0
    today_tasks_count = today_records.values('task').distinct().count()

    # 计算周数据（最近7天）
    seven_days_ago = timezone.now() - timedelta(days=7)
    week_records = study_records.filter(study_start__gte=seven_days_ago)
    week_duration = week_records.aggregate(total=Sum('study_duration'))['total'] or 0

    # 生成日学习时长数据（最近14天）
    daily_data = []
    for i in range(14, -1, -1):
        date = (timezone.now() - timedelta(days=i)).date()
        day_records = study_records.filter(study_start__date=date)
        day_duration = day_records.aggregate(total=Sum('study_duration'))['total'] or 0
        daily_data.append({
            'date': date.strftime('%m-%d'),
            'duration': day_duration,
        })

    # 计算任务完成率数据
    all_tasks = MainTask.objects.all()
    completed_count = all_tasks.filter(progress=100.0).count()
    pending_count = all_tasks.filter(progress__lt=100.0).count()

    # 任务状态分布
    task_status_data = [
        {'name': '已完成', 'value': completed_count},
        {'name': '进行中', 'value': pending_count},
    ]

    # 各任务学习时长排名
    task_study_data = []
    for task in all_tasks:
        task_duration = task.study_records.aggregate(total=Sum('study_duration'))['total'] or 0
        if task_duration > 0:
            task_study_data.append({
                'task_name': task.task_name,
                'duration': task_duration,
            })

    # 按时长排序
    task_study_data.sort(key=lambda x: x['duration'], reverse=True)

    # 统计无任务关联的自由学习记录
    untracked_duration = StudyRecord.objects.filter(task__isnull=True).aggregate(
        total=Sum('study_duration')
    )['total'] or 0

    context = {
        'today_duration': today_duration,
        'today_tasks_count': today_tasks_count,
        'week_duration': week_duration,
        'daily_data': json.dumps(daily_data),
        'task_status_data': json.dumps(task_status_data),
        'task_study_data': json.dumps(task_study_data[:10]),  # 前10个任务
        'total_study_duration': study_records.aggregate(total=Sum('study_duration'))['total'] or 0,
        'total_study_records': study_records.count(),
        'untracked_duration': untracked_duration,
    }

    return render(request, 'study/statistics.html', context)


# ========== API接口 ==========
def api_task_detail(request, task_id):
    """获取任务详情API"""
    task = get_object_or_404(MainTask, id=task_id)

    subtasks = task.subtask_set.all()

    data = {
        'id': task.id,
        'task_name': task.task_name,
        'task_desc': task.task_desc,
        'progress': task.progress,
        'deadline': task.deadline.isoformat(),
        'subtasks': [
            {
                'id': st.id,
                'sub_name': st.sub_name,
                'is_finish': st.is_finish,
            }
            for st in subtasks
        ]
    }

    return JsonResponse(data)
