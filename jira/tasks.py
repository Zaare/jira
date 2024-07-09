from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_task_complete_email(task_id, user_email):
    subject = f'Task {task_id} Completed'
    message = f'Your task with ID {task_id} has been marked as completed.'
    send_mail(subject, message, 'from@example.com', [user_email])
