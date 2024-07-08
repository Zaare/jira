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
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.assign_permissions()
        
    def assign_permissions(self):
        for admin in self.admins.all():
            assign_perm('manage_organization', admin, self)
    

class OrganizationAdmin(models.Model):
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, verbose_name='کاربر')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='سازمان')

    class Meta:
        unique_together = ('user', 'organization')
        verbose_name = 'مدیر سازمان'
        verbose_name_plural = 'مدیران سازمان'

    def __str__(self):
        return f"{self.user.username} - {self.organization.name}"
    
class Sprint(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام')
    start_date = models.DateTimeField(verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(verbose_name='تاریخ پایان')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='sprints', verbose_name='سازمان')

    class Meta:
        verbose_name = 'اسپرینت'
        verbose_name_plural = 'اسپرینت‌ها'

    def __str__(self):
        return self.name

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'کم'),
        ('medium', 'متوسط'),
        ('high', 'بالا'),
    ]

    STATUS_CHOICES = [
        ('todo', 'در انتظار'),
        ('in_progress', 'در حال انجام'),
        ('done', 'تکمیل شده'),
        ('blocked', 'مسدود شده'),
        ('cancelled', 'لغو شده'),
        ('closed', 'بسته شده'),
        ('reopened', 'بازگشایی شده'),
        ('approved', 'تایید شده'),
        ('review', 'در حال بررسی'),
        ('test', 'در حال آزمایش'),
        ('delivered', 'تحویل داده شده'),
        ('deployed', 'مستقر شده'),
        ('deferred', 'تأخیر افتاده'),
        ('duplicate', 'تکراری'),
        ('invalid', 'نامعتبر'),
        ('not_a_bug', 'خطای نیست'),
    ]

    title = models.CharField(max_length=255, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    due_date = models.DateTimeField(verbose_name='تاریخ سررسید')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, verbose_name='اولویت')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name='وضعیت')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks', verbose_name='ایجاد شده توسط')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks', verbose_name='اختصاص داده شده به')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='tasks', verbose_name='سازمان')
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, related_name='tasks', verbose_name='اسپرینت', null=True, blank=True)

    class Meta:
        permissions = (
            ("view_task_custom", "Can view task"),
            ("change_task_custom", "Can change task"),
            ("delete_task_custom", "Can delete task"),
        )
        verbose_name = 'تسک'
        verbose_name_plural = 'تسک‌ها'

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

        for admin in self.organization.admins.all():
            assign_perm('view_task_custom', admin, self)
            assign_perm('change_task_custom', admin, self)
            assign_perm('delete_task_custom', admin, self)


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments', verbose_name='تسک')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='نویسنده')
    content = models.TextField(verbose_name='محتوا')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت‌ها'

    def __str__(self):
        return f"{self.author.username} - {self.task.title}"


class Mention(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='mentions', verbose_name='کامنت')
    mentioned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentions', verbose_name='کاربر منشن شده')

    class Meta:
        verbose_name = 'منشن'
        verbose_name_plural = 'منشن‌ها'

    def __str__(self):
        return f"{self.mentioned_user.username} - {self.comment.content[:20]}"
