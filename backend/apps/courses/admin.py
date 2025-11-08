from django.contrib import admin
from .models import CourseConfiguration, HoleConfiguration


class HoleConfigurationInline(admin.TabularInline):
    model = HoleConfiguration
    extra = 18
    max_num = 18


@admin.register(CourseConfiguration)
class CourseConfigurationAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'tee_color', 'par', 'rating', 'slope']
    search_fields = ['course_name']
    list_filter = ['tee_color']
    inlines = [HoleConfigurationInline]
