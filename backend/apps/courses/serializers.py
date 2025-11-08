"""
Course configuration serializers for GTMS API.
"""
from rest_framework import serializers
from .models import CourseConfiguration, HoleConfiguration


class HoleConfigurationSerializer(serializers.ModelSerializer):
    """Serializer for hole configuration."""

    class Meta:
        model = HoleConfiguration
        fields = [
            'id',
            'hole_number',
            'par',
            'handicap_stroke_index',
            'distance',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class CourseConfigurationSerializer(serializers.ModelSerializer):
    """Serializer for course configuration."""

    holes = HoleConfigurationSerializer(many=True, read_only=True)
    stroke_indices = serializers.ReadOnlyField()

    class Meta:
        model = CourseConfiguration
        fields = [
            'id',
            'course_name',
            'tee_color',
            'rating',
            'slope',
            'par',
            'holes',
            'stroke_indices',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class CourseConfigurationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating course configuration with holes."""

    holes = HoleConfigurationSerializer(many=True)

    class Meta:
        model = CourseConfiguration
        fields = [
            'course_name',
            'tee_color',
            'rating',
            'slope',
            'par',
            'holes'
        ]

    def create(self, validated_data):
        """Create course with holes."""
        holes_data = validated_data.pop('holes')
        course = CourseConfiguration.objects.create(**validated_data)

        for hole_data in holes_data:
            HoleConfiguration.objects.create(course=course, **hole_data)

        return course
