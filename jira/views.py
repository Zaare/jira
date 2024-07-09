from rest_framework import viewsets, permissions
from .models import Organization, OrganizationAdmin, Sprint, Task, Comment, Mention
from .serializers import OrganizationSerializer, OrganizationAdminSerializer, SprintSerializer, TaskSerializer, CommentSerializer, MentionSerializer
from guardian.shortcuts import get_objects_for_user
from .permissions import IsDeveloperPermission, IsAdminUser 
from .tasks import send_task_complete_email

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return get_objects_for_user(user, 'manage_organization', Organization)

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'invite', 'block_subordinates']:
            return [IsAdminUser()]
        return super().get_permissions()


class OrganizationAdminViewSet(viewsets.ModelViewSet):
    queryset = OrganizationAdmin.objects.all()
    serializer_class = OrganizationAdminSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'invite', 'block_subordinates']:
            return [IsAdminUser()] 
        return super().get_permissions()


class SprintViewSet(viewsets.ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.user.groups.filter(name='Admin').exists():
            return [permissions.IsAdminUser()]
        return super().get_permissions()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.user.groups.filter(name='Admin').exists():
            return [permissions.IsAdminUser()]
        elif self.request.user.groups.filter(name='Developer').exists():
            return [IsDeveloperPermission()]
        return super().get_permissions()

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == 'done':
            send_task_complete_email.delay(instance.id, instance.user.email)

    def perform_create(self, serializer):
        instance = serializer.save()
        if instance.status == 'done':
            send_task_complete_email.delay(instance.id, instance.user.email)



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]


class MentionViewSet(viewsets.ModelViewSet):
    queryset = Mention.objects.all()
    serializer_class = MentionSerializer
    permission_classes = [permissions.IsAuthenticated]
