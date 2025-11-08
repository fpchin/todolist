from django.contrib import admin
from .models import HoleScore, Result


@admin.register(HoleScore)
class HoleScoreAdmin(admin.ModelAdmin):
    list_display = ['player', 'round', 'hole_number', 'strokes', 'verified']
    list_filter = ['verified', 'round__tournament', 'hole_number']
    search_fields = ['player__first_name', 'player__last_name']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = [
        'player', 'tournament', 'division',
        'total_net', 'total_gross', 'rank_overall', 'rank_division'
    ]
    list_filter = ['tournament', 'division', 'verified']
    search_fields = ['player__first_name', 'player__last_name']
    readonly_fields = ['calculated_at']
