from django.contrib import admin
from .models import Tournament, TournamentPlayer, Round, TeeTime, FlightPlayer


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'location', 'status', 'format_type']
    list_filter = ['status', 'format_type', 'start_date']
    search_fields = ['name', 'location']
    date_hierarchy = 'start_date'


@admin.register(TournamentPlayer)
class TournamentPlayerAdmin(admin.ModelAdmin):
    list_display = ['player', 'tournament', 'division', 'handicap_index', 'status']
    list_filter = ['status', 'division', 'tournament']
    search_fields = ['player__first_name', 'player__last_name', 'tournament__name']


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ['tournament', 'round_number', 'round_date', 'course', 'status']
    list_filter = ['status', 'round_date']
    search_fields = ['tournament__name', 'course__course_name']


@admin.register(TeeTime)
class TeeTimeAdmin(admin.ModelAdmin):
    list_display = ['round', 'tee_time', 'starting_hole']
    list_filter = ['round__tournament', 'tee_time']


@admin.register(FlightPlayer)
class FlightPlayerAdmin(admin.ModelAdmin):
    list_display = ['player', 'tee_time', 'position']
    list_filter = ['tee_time__round__tournament']
