from django.contrib import admin
from .models import Organization, OrganizationAdmin as OrgAdmin, Task

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
    list_display = ('title', 'priority', 'status', 'due_date', 'created_by', 'assigned_to', 'organization')
    search_fields = ('title', 'description', 'created_by__username', 'assigned_to__username', 'organization__name')
    list_filter = ('priority', 'status', 'due_date', 'organization')
    date_hierarchy = 'due_date'
    raw_id_fields = ('created_by', 'assigned_to', 'organization')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.assign_permissions()

@admin.register(OrgAdmin)
class OrganizationAdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization')
    search_fields = ('user__username', 'organization__name')
