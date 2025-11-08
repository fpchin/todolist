from django.contrib import admin
from .models import Player, HandicapHistory


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'club_affiliation', 'created_at']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['club_affiliation', 'created_at']


@admin.register(HandicapHistory)
class HandicapHistoryAdmin(admin.ModelAdmin):
    list_display = ['player', 'handicap_index', 'effective_date', 'issuing_authority']
    list_filter = ['issuing_authority', 'effective_date']
    search_fields = ['player__first_name', 'player__last_name']
