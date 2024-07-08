from django.db import models
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'کم'),
        ('medium', 'متوسط'),
        ('high', 'بالا'),
    ]

    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('in_progress', 'در حال انجام'),
        ('completed', 'تکمیل شده'),
    ]

    title = models.CharField(max_length=255, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    due_date = models.DateTimeField(verbose_name='تاریخ سررسید')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, verbose_name='اولویت')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name='وضعیت')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks', verbose_name='ایجاد شده توسط')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks', verbose_name='اختصاص داده شده به')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)
        self.assign_permissions()

    def assign_permissions(self):
    # Assign view and change permissions to created_by and assigned_to users
        assign_perm('view_task_custom', self.created_by, self)
        assign_perm('change_task_custom', self.created_by, self)
        assign_perm('view_task_custom', self.assigned_to, self)
        assign_perm('change_task_custom', self.assigned_to, self)

    class Meta:
        permissions = (
            ("view_task_custom", "Can view task"),
            ("change_task_custom", "Can change task"),
            ("delete_task_custom", "Can delete task"),
        )
