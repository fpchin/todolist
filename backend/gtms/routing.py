"""
WebSocket URL routing for GTMS project.
"""
from django.urls import path

# Import consumers when apps are created
# from apps.scores.consumers import LeaderboardConsumer

websocket_urlpatterns = [
    # WebSocket routes will be added here
    # path('ws/tournament/<uuid:tournament_id>/', LeaderboardConsumer.as_asgi()),
]
