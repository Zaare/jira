from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Docs",
        default_version='v1',
        description="Jira App",
        # terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="farhadzaare@gmail.com"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('', include('dj_rest_auth.urls')),
    path('jira/', include('jira.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
