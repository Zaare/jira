#!/bin/sh
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')"
exec gunicorn --workers=3 --bind=0.0.0.0:8000 core.wsgi:application
