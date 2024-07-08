from django.db import models
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm
from django.contrib.auth.models import User as DjangoUser

class Organization(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام')
    admins = models.ManyToManyField(DjangoUser, through='OrganizationAdmin', related_name='managed_organizations')
    
    class Meta:
        verbose_name = 'سازمان'
        verbose_name_plural = 'سازمان‌ها'

    def __str__(self):
        return self.name
    

class OrganizationAdmin(models.Model):
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, verbose_name='کاربر')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='سازمان')

    class Meta:
        unique_together = ('user', 'organization')
        verbose_name = 'مدیر سازمان'
        verbose_name_plural = 'مدیران سازمان'

    def __str__(self):
        return f"{self.user.username} - {self.organization.name}"
    
        


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
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='tasks', verbose_name='سازمان')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)
        self.assign_permissions()

    def assign_permissions(self):
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
        verbose_name = 'تسک'
        verbose_name_plural = 'تسک‌ها'
