import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User, Group
from .models import Organization, OrganizationAdmin, Sprint, Task, Comment, Mention
from django.urls import reverse
from django.utils import timezone


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def admin_group():
    return Group.objects.create(name='Admin')

@pytest.fixture
def developer_group():
    return Group.objects.create(name='Developer')

@pytest.fixture
def organization():
    return Organization.objects.create(name='Test Organization')

@pytest.fixture
def organization_admin(user, organization):
    return OrganizationAdmin.objects.create(user=user, organization=organization)

@pytest.fixture
def sprint(organization):
    return Sprint.objects.create(
        name='Test Sprint',
        start_date=timezone.now(),
        end_date=timezone.now() + timezone.timedelta(days=7),
        organization=organization
    )

@pytest.fixture
def task(sprint, user, organization): 
    return Task.objects.create(
        title='Test Task',
        description='Test Description',
        due_date=timezone.now(),
        priority='low',
        status='in_progress',
        created_by=user,
        assigned_to=user,
        organization=organization,
        sprint=sprint
    )

@pytest.fixture
def comment(task, user):
    return Comment.objects.create(task=task, author=user, content='Test Comment')

@pytest.fixture
def mention(comment, user):
    return Mention.objects.create(user=user, comment=comment)

def test_is_admin_user_permission(api_client, user, organization, admin_group):
    user.groups.add(admin_group)
    api_client.force_authenticate(user=user)
    url = reverse('organization-list')
    response = api_client.post(url, {'name': 'New Organization'})
    assert response.status_code == status.HTTP_201_CREATED

def test_is_developer_permission(api_client, user, developer_group, task):
    user.groups.add(developer_group)
    api_client.force_authenticate(user=user)
    url = reverse('task-detail', kwargs={'pk': task.id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

def test_is_admin_user_can_create_organization(api_client, user, admin_group):
    user.groups.add(admin_group)
    api_client.force_authenticate(user=user)
    url = reverse('organization-list')
    response = api_client.post(url, {'name': 'New Organization'})
    assert response.status_code == status.HTTP_201_CREATED

def test_is_developer_can_delete_task(api_client, user, developer_group, task):
    user.groups.add(developer_group)
    api_client.force_authenticate(user=user)
    url = reverse('task-detail', kwargs={'pk': task.id})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_is_developer_cannot_delete_other_task(api_client, user, developer_group, task):
    other_user = User.objects.create_user(username='otheruser', password='otherpass')
    task.assigned_to = other_user 
    task.save()
    user.groups.add(developer_group)
    api_client.force_authenticate(user=user)
    url = reverse('task-detail', kwargs={'pk': task.id})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_developer_cannot_change_to_closed_status(api_client, user, developer_group, task):
    user.groups.add(developer_group)
    api_client.force_authenticate(user=user)
    url = reverse('task-detail', kwargs={'pk': task.id})
    data = {'status': 'closed'}  
    
    response = api_client.patch(url, data, format='json')
    
    assert response.status_code == status.HTTP_403_FORBIDDEN
    
    task.refresh_from_db()
    assert task.status != 'closed'
