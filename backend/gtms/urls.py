"""
URL configuration for GTMS project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from apps.core.views import health_check

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # API v1
    path('api/v1/', include([
        # Health check
        path('health/', health_check, name='health_check'),

        # API Schema and Documentation
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

        # Authentication
        path('auth/', include('apps.authentication.urls')),

        # Core API endpoints (to be added)
        # path('tournaments/', include('apps.tournaments.urls')),
        # path('players/', include('apps.players.urls')),
        # path('scores/', include('apps.scores.urls')),
        # path('results/', include('apps.results.urls')),
    ])),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Django Debug Toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

# Custom admin site header
admin.site.site_header = "GTMS Administration"
admin.site.site_title = "GTMS Admin Portal"
admin.site.index_title = "Welcome to GTMS Administration"
