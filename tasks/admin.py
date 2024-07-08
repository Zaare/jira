from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from .models import Task

@admin.register(Task)
class TaskAdmin(GuardedModelAdmin):
    list_display = ('title', 'priority', 'status', 'due_date', 'created_by', 'assigned_to')
    list_filter = ('priority', 'status', 'due_date', 'created_by', 'assigned_to')
    search_fields = ('title', 'description')
    date_hierarchy = 'due_date'

    class Meta:
        model = Task
        verbose_name = 'وظیفه'






