from django.db import models
from django.utils import timezone


# 主任务模型
class MainTask(models.Model):
    """学习主任务模型
    包含任务名称、描述、创建时间、截止时间、完成进度
    """
    task_name = models.CharField(max_length=200, verbose_name="任务名称", help_text="主任务的名称")
    task_desc = models.TextField(blank=True, null=True, verbose_name="任务描述", help_text="任务的详细描述")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    deadline = models.DateTimeField(verbose_name="截止时间", help_text="任务的截止日期和时间")
    progress = models.FloatField(default=0.0, verbose_name="完成进度", help_text="任务完成进度百分比0-100")

    class Meta:
        verbose_name = "主任务"
        verbose_name_plural = "主任务列表"
        ordering = ['-create_time']

    def __str__(self):
        return self.task_name

    def calculate_progress(self):
        """自动计算任务完成进度
        进度 = 已完成子任务数 / 总子任务数 * 100
        """
        subtasks = self.subtask_set.all()
        total_count = subtasks.count()

        if total_count == 0:
            self.progress = 0.0
        else:
            finished_count = subtasks.filter(is_finish=True).count()
            self.progress = (finished_count / total_count) * 100

        self.save()
        return self.progress

    def is_overdue(self):
        """判断任务是否已过期"""
        return timezone.now() > self.deadline

    def is_nearly_due(self):
        """判断任务是否即将过期（24小时内）"""
        from datetime import timedelta
        now = timezone.now()
        return now < self.deadline <= now + timedelta(hours=24)


# 子任务模型
class SubTask(models.Model):
    """学习子任务模型
    每个主任务可以包含多个子任务
    """
    main_task = models.ForeignKey(MainTask, on_delete=models.CASCADE, verbose_name="关联主任务")
    sub_name = models.CharField(max_length=200, verbose_name="子任务名称", help_text="子任务的名称")
    is_finish = models.BooleanField(default=False, verbose_name="是否完成", help_text="子任务完成状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "子任务"
        verbose_name_plural = "子任务列表"
        ordering = ['create_time']

    def __str__(self):
        return f"{self.main_task.task_name} - {self.sub_name}"

    def save(self, *args, **kwargs):
        """保存时自动更新主任务的完成进度"""
        super().save(*args, **kwargs)
        self.main_task.calculate_progress()


# 学习记录模型
class StudyRecord(models.Model):
    """学习记录模型
    记录每次番茄钟学习的开始时间、结束时间、学习时长
    """
    task = models.ForeignKey(MainTask, on_delete=models.CASCADE, verbose_name="关联任务", related_name='study_records')
    study_start = models.DateTimeField(auto_now_add=True, verbose_name="学习开始时间")
    study_end = models.DateTimeField(verbose_name="学习结束时间")
    study_duration = models.IntegerField(verbose_name="学习时长（分钟）", help_text="本次学习的时长")

    class Meta:
        verbose_name = "学习记录"
        verbose_name_plural = "学习记录列表"
        ordering = ['-study_start']

    def __str__(self):
        return f"{self.task.task_name} - {self.study_duration}分钟"
