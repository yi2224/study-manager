#!/usr/bin/env python
"""
示例数据导入脚本
用于快速为系统生成演示数据
使用方法：python manage_data.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# 配置Django设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from study.models import MainTask, SubTask, StudyRecord


def create_sample_data():
    """创建示例任务数据"""
    print("=" * 60)
    print("学习任务管理系统 - 示例数据导入")
    print("=" * 60)

    # 清空现有数据（可选）
    confirm = input("\n是否清空现有所有数据？(y/N): ").strip().lower()
    if confirm == 'y':
        MainTask.objects.all().delete()
        print("✓ 现有数据已清空")

    # 创建示例主任务1
    task1 = MainTask.objects.create(
        task_name="Python Django项目开发",
        task_desc="完成一个完整的Django Web应用，包括前端界面、后端API、数据库等功能模块",
        deadline=timezone.now() + timedelta(days=7)
    )

    # 为任务1添加子任务
    SubTask.objects.bulk_create([
        SubTask(main_task=task1, sub_name="完成模型设计"),
        SubTask(main_task=task1, sub_name="实现视图逻辑"),
        SubTask(main_task=task1, sub_name="编写前端模板"),
        SubTask(main_task=task1, sub_name="数据库迁移"),
        SubTask(main_task=task1, sub_name="API接口测试"),
    ])

    # 标记部分子任务为完成
    for i, subtask in enumerate(task1.subtask_set.all()[:2]):
        subtask.is_finish = True
        subtask.save()

    print(f"✓ 创建任务：{task1.task_name}")

    # 创建示例主任务2
    task2 = MainTask.objects.create(
        task_name="数据结构与算法学习",
        task_desc="学习常见的数据结构（数组、链表、树等）和算法（排序、查找等）",
        deadline=timezone.now() + timedelta(days=14)
    )

    SubTask.objects.bulk_create([
        SubTask(main_task=task2, sub_name="学习链表"),
        SubTask(main_task=task2, sub_name="学习树和二叉树"),
        SubTask(main_task=task2, sub_name="学习排序算法"),
        SubTask(main_task=task2, sub_name="完成LeetCode练习"),
    ])

    print(f"✓ 创建任务：{task2.task_name}")

    # 创建示例主任务3
    task3 = MainTask.objects.create(
        task_name="英语单词背诵",
        task_desc="每天背诵100个常用英语单词，提高词汇量",
        deadline=timezone.now() + timedelta(days=30)
    )

    SubTask.objects.bulk_create([
        SubTask(main_task=task3, sub_name="背诵高频单词表1", is_finish=True),
        SubTask(main_task=task3, sub_name="背诵高频单词表2"),
        SubTask(main_task=task3, sub_name="背诵短语和习语"),
    ])

    print(f"✓ 创建任务：{task3.task_name}")

    # 创建示例学习记录
    print("\n正在创建学习记录...")

    # 为任务1创建学习记录
    for i in range(5):
        study_date = timezone.now() - timedelta(days=i)
        StudyRecord.objects.create(
            task=task1,
            study_start=study_date - timedelta(minutes=25),
            study_end=study_date,
            study_duration=25
        )

    # 为任务2创建学习记录
    for i in range(3):
        study_date = timezone.now() - timedelta(days=i*2)
        StudyRecord.objects.create(
            task=task2,
            study_start=study_date - timedelta(minutes=50),
            study_end=study_date,
            study_duration=50
        )

    # 为任务3创建学习记录
    StudyRecord.objects.create(
        task=task3,
        study_start=timezone.now() - timedelta(days=1, minutes=15),
        study_end=timezone.now() - timedelta(days=1),
        study_duration=15
    )

    print("✓ 学习记录创建完成")

    # 重新计算任务进度
    print("\n正在更新任务进度...")
    for task in MainTask.objects.all():
        task.calculate_progress()
        print(f"  {task.task_name}: {task.progress:.1f}%")

    print("\n" + "=" * 60)
    print("✓ 示例数据导入成功！")
    print("=" * 60)
    print("\n你现在可以：")
    print("1. 访问 http://127.0.0.1:8000/ 查看首页")
    print("2. 访问 http://127.0.0.1:8000/tasks/ 查看任务列表")
    print("3. 访问 http://127.0.0.1:8000/statistics/ 查看数据统计")
    print("\n" + "=" * 60)


def clear_all_data():
    """清空所有数据"""
    print("\n" + "=" * 60)
    print("清空所有数据")
    print("=" * 60)

    confirm = input("确定要清空所有数据吗？(y/N): ").strip().lower()
    if confirm == 'y':
        MainTask.objects.all().delete()
        SubTask.objects.all().delete()
        StudyRecord.objects.all().delete()
        print("✓ 所有数据已清空")
    else:
        print("已取消")


def show_stats():
    """显示统计信息"""
    print("\n" + "=" * 60)
    print("当前系统统计")
    print("=" * 60)

    task_count = MainTask.objects.count()
    subtask_count = SubTask.objects.count()
    record_count = StudyRecord.objects.count()

    print(f"主任务数：{task_count}")
    print(f"子任务数：{subtask_count}")
    print(f"学习记录数：{record_count}")

    if task_count > 0:
        total_duration = StudyRecord.objects.count() * 25
        print(f"总学习时长：{total_duration}分钟")

    print("=" * 60)


if __name__ == '__main__':
    print("\n学习任务管理系统 - 数据管理工具\n")
    print("选择操作:")
    print("1. 导入示例数据")
    print("2. 清空所有数据")
    print("3. 显示统计信息")
    print("4. 退出")

    choice = input("\n请选择 (1-4): ").strip()

    if choice == '1':
        create_sample_data()
    elif choice == '2':
        clear_all_data()
    elif choice == '3':
        show_stats()
    elif choice == '4':
        print("退出")
    else:
        print("无效的选择")
