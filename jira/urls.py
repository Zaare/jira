from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationViewSet, OrganizationAdminViewSet, SprintViewSet, TaskViewSet, CommentViewSet, MentionViewSet

router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet)
router.register(r'organization-admins', OrganizationAdminViewSet)
router.register(r'sprints', SprintViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'mentions', MentionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
