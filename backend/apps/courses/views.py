"""
Course configuration API views.
"""
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import CourseConfiguration
from .serializers import (
    CourseConfigurationSerializer,
    CourseConfigurationCreateSerializer
)


class CourseConfigurationViewSet(viewsets.ModelViewSet):
    """ViewSet for course configuration CRUD operations."""

    queryset = CourseConfiguration.objects.all()
    serializer_class = CourseConfigurationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['course_name', 'tee_color']
    filterset_fields = ['tee_color']

    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'create':
            return CourseConfigurationCreateSerializer
        return CourseConfigurationSerializer
