from django.contrib import admin
from django.urls import path, include

from rest_framework.permissions import AllowAny

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.views.generic import RedirectView
from django.middleware.csrf import get_token
from django.http import JsonResponse


def csrf_token_view(request):
    return JsonResponse({
        "csrfToken": get_token(request)
    })


schema_view = get_schema_view(
    openapi.Info(
        title="Django Authentication API",
        default_version='v1',
        description="Cookie Based Authentication API",
    ),
    public=True,
    permission_classes=[AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('authentication.urls')),

    path('csrf/', csrf_token_view),

    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),

    path('', RedirectView.as_view(url='/swagger/')),
]