"""
Tests for tournament API endpoints
"""
import pytest
from decimal import Decimal
from datetime import date
from rest_framework import status
from apps.tournaments.models import Tournament, TournamentPlayer


@pytest.mark.django_db
@pytest.mark.api
class TestTournamentAPI:
    """Test Tournament API endpoints"""

    def test_list_tournaments(self, authenticated_client, tournament):
        """Test listing tournaments"""
        response = authenticated_client.get('/api/v1/tournaments/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == tournament.name

    def test_create_tournament(self, authenticated_client):
        """Test creating tournament"""
        data = {
            'name': 'New Championship',
            'location': 'New Golf Club',
            'start_date': str(date.today()),
            'end_date': str(date.today()),
            'format_type': 'STROKEPLAY',
            'status': 'DRAFT',
            'max_players': 150
        }

        response = authenticated_client.post('/api/v1/tournaments/', data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Championship'
        assert Tournament.objects.count() == 1

    def test_retrieve_tournament(self, authenticated_client, tournament):
        """Test retrieving single tournament"""
        response = authenticated_client.get(f'/api/v1/tournaments/{tournament.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == tournament.name

    def test_update_tournament(self, authenticated_client, tournament):
        """Test updating tournament"""
        data = {'name': 'Updated Championship'}

        response = authenticated_client.patch(
            f'/api/v1/tournaments/{tournament.id}/',
            data
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated Championship'

        tournament.refresh_from_db()
        assert tournament.name == 'Updated Championship'

    def test_delete_tournament(self, authenticated_client, tournament):
        """Test deleting tournament"""
        response = authenticated_client.delete(f'/api/v1/tournaments/{tournament.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Tournament.objects.count() == 0

    def test_register_player(self, authenticated_client, tournament, player):
        """Test player registration endpoint"""
        data = {
            'player_id': str(player.id),
            'handicap_index': '15.5',
            'division': 'A Division'
        }

        response = authenticated_client.post(
            f'/api/v1/tournaments/{tournament.id}/register_player/',
            data
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert TournamentPlayer.objects.count() == 1

    def test_unauthenticated_access(self, api_client, tournament):
        """Test that unauthenticated users cannot access API"""
        response = api_client.get('/api/v1/tournaments/')

        # Should require authentication
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
