from rest_framework import viewsets, permissions
from .models import Organization, OrganizationAdmin, Sprint, Task, Comment, Mention
from .serializers import OrganizationSerializer, OrganizationAdminSerializer, SprintSerializer, TaskSerializer, CommentSerializer, MentionSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrganizationAdminViewSet(viewsets.ModelViewSet):
    queryset = OrganizationAdmin.objects.all()
    serializer_class = OrganizationAdminSerializer
    permission_classes = [permissions.IsAuthenticated]

class SprintViewSet(viewsets.ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    permission_classes = [permissions.IsAuthenticated]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

class MentionViewSet(viewsets.ModelViewSet):
    queryset = Mention.objects.all()
    serializer_class = MentionSerializer
    permission_classes = [permissions.IsAuthenticated]
