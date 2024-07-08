from django.contrib import admin
from .models import Organization, OrganizationAdmin as OrgAdmin, Task, Sprint, Comment, Mention

class OrganizationAdminInline(admin.TabularInline):
    model = OrgAdmin
    extra = 1

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = (OrganizationAdminInline,)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'due_date', 'created_by', 'assigned_to', 'organization', 'sprint')
    search_fields = ('title', 'description', 'created_by__username', 'assigned_to__username', 'organization__name')
    list_filter = ('priority', 'status', 'due_date', 'organization', 'sprint')
    date_hierarchy = 'due_date'
    raw_id_fields = ('created_by', 'assigned_to', 'organization', 'sprint')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.assign_permissions()

@admin.register(OrgAdmin)
class OrganizationAdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization')
    search_fields = ('user__username', 'organization__name')

@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'organization')
    search_fields = ('name', 'organization__name')
    list_filter = ('organization', 'start_date', 'end_date')
    date_hierarchy = 'start_date'
    raw_id_fields = ('organization',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author', 'created_at')
    search_fields = ('task__title', 'author__username', 'content')
    list_filter = ('task', 'author', 'created_at')
    date_hierarchy = 'created_at'
    raw_id_fields = ('task', 'author')

@admin.register(Mention)
class MentionAdmin(admin.ModelAdmin):
    list_display = ('comment', 'mentioned_user')
    search_fields = ('comment__content', 'mentioned_user__username')
    list_filter = ('mentioned_user',)
    raw_id_fields = ('comment', 'mentioned_user')
