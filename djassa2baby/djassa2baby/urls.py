from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Djassa2baby API",
        default_version='v1',
        description="API for Djassa2baby",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="abdoullahcoulibaly2@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),
    path('api/', include('core.urls.role')),
    path('api/', include('core.urls.coupon')),
    path('api/users/', include('users.urls')),
    path('api/', include('shop.urls.product')),
    path('api/', include('shop.urls.shop')),
    path('api/', include('shop.urls.order')),
    path('api/', include('shop.urls.subscription')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)