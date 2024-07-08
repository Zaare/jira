import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Organization, OrganizationAdmin, Sprint, Task, Comment, Mention
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def organization():
    return Organization.objects.create(name='Test Organization')

@pytest.fixture
def task(organization, user):
    return Task.objects.create(
        title='Test Task',
        description='Test Description',
        due_date='2024-07-08T00:00:00Z',
        priority='medium',
        status='pending',
        created_by=user,
        assigned_to=user,
        organization=organization
    )

@pytest.mark.django_db
def test_create_organization(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('organization-list')
    data = {'name': 'New Organization'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Organization.objects.count() == 1
    assert Organization.objects.get().name == 'New Organization'

@pytest.mark.django_db
def test_retrieve_organization(api_client, organization, user):
    api_client.force_authenticate(user=user)
    url = reverse('organization-detail', args=[organization.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == organization.name

@pytest.mark.django_db
def test_update_organization(api_client, organization, user):
    api_client.force_authenticate(user=user)
    url = reverse('organization-detail', args=[organization.id])
    data = {'name': 'Updated Organization'}
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    organization.refresh_from_db()
    assert organization.name == 'Updated Organization'

@pytest.mark.django_db
def test_delete_organization(api_client, organization, user):
    api_client.force_authenticate(user=user)
    url = reverse('organization-detail', args=[organization.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Organization.objects.count() == 0

@pytest.mark.django_db
def test_create_task(api_client, organization, user):
    api_client.force_authenticate(user=user)
    url = reverse('task-list')
    data = {
        'title': 'New Task',
        'description': 'New Description',
        'due_date': '2024-07-08T00:00:00Z',
        'priority': 'medium',
        'status': 'pending',
        'created_by': user.id,
        'assigned_to': user.id,
        'organization': organization.id
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Task.objects.count() == 1
    assert Task.objects.get().title == 'New Task'

@pytest.mark.django_db
def test_retrieve_task(api_client, task, user):
    api_client.force_authenticate(user=user)
    url = reverse('task-detail', args=[task.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == task.title

@pytest.mark.django_db
def test_update_task(api_client, task, user):
    api_client.force_authenticate(user=user)
    url = reverse('task-detail', args=[task.id])
    data = {
        'title': 'Updated Task',
        'description': 'Updated Description',
        'due_date': '2024-07-08T00:00:00Z',
        'priority': 'high',
        'status': 'in_progress',
        'created_by': user.id,
        'assigned_to': user.id,
        'organization': task.organization.id
    }
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    task.refresh_from_db()
    assert task.title == 'Updated Task'
    assert task.priority == 'high'
    assert task.status == 'in_progress'

@pytest.mark.django_db
def test_delete_task(api_client, task, user):
    api_client.force_authenticate(user=user)
    url = reverse('task-detail', args=[task.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Task.objects.count() == 0
