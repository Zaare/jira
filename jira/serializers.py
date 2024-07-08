from rest_framework import serializers
from .models import Organization, OrganizationAdmin, Sprint, Task, Comment, Mention
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class OrganizationAdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    organization = serializers.StringRelatedField()

    class Meta:
        model = OrganizationAdmin
        fields = '__all__'

class OrganizationSerializer(serializers.ModelSerializer):
    admins = OrganizationAdminSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = '__all__'

class SprintSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = Sprint
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    assigned_to = UserSerializer()
    organization = OrganizationSerializer()
    sprint = SprintSerializer()

    class Meta:
        model = Task
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'

class MentionSerializer(serializers.ModelSerializer):
    comment = CommentSerializer()
    mentioned_user = UserSerializer()

    class Meta:
        model = Mention
        fields = '__all__'
