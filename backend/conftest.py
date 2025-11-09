"""
Pytest configuration and fixtures for GTMS tests
"""
import pytest
from decimal import Decimal
from datetime import date, timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    """DRF API client"""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    """Authenticated API client"""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def user(db):
    """Create test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def tournament(db):
    """Create test tournament"""
    from apps.tournaments.models import Tournament
    return Tournament.objects.create(
        name='Test Championship 2023',
        location='Test Golf Club',
        start_date=date.today(),
        end_date=date.today() + timedelta(days=1),
        format_type='STROKEPLAY',
        status='OPEN',
        max_players=200
    )


@pytest.fixture
def course(db):
    """Create test course with 18 holes"""
    from apps.courses.models import CourseConfiguration, HoleConfiguration

    course = CourseConfiguration.objects.create(
        course_name='Test Course',
        tee_color='White',
        rating=Decimal('72.0'),
        slope=113,
        par=72
    )

    # Create 18 holes
    pars = [4, 4, 4, 3, 4, 5, 4, 3, 5, 4, 4, 3, 5, 4, 4, 4, 3, 4]
    stroke_indices = [1, 11, 5, 15, 3, 9, 7, 17, 13, 2, 8, 16, 6, 12, 4, 10, 18, 14]

    for i in range(18):
        HoleConfiguration.objects.create(
            course=course,
            hole_number=i + 1,
            par=pars[i],
            handicap_stroke_index=stroke_indices[i],
            distance=350 + (i * 10)
        )

    return course


@pytest.fixture
def player(db):
    """Create test player"""
    from apps.players.models import Player
    return Player.objects.create(
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        phone='1234567890',
        club_affiliation='Test Golf Club'
    )


@pytest.fixture
def tournament_player(db, tournament, player):
    """Create tournament player registration"""
    from apps.tournaments.models import TournamentPlayer
    return TournamentPlayer.objects.create(
        tournament=tournament,
        player=player,
        handicap_index=Decimal('12.5'),
        playing_handicap=12,
        division='Championship',
        status='CONFIRMED'
    )


@pytest.fixture
def round_obj(db, tournament, course):
    """Create tournament round"""
    from apps.tournaments.models import Round
    return Round.objects.create(
        tournament=tournament,
        round_number=1,
        round_date=date.today(),
        course=course,
        status='IN_PROGRESS'
    )


@pytest.fixture
def hole_scores(db, round_obj, player):
    """Create 18 hole scores"""
    from apps.scores.models import HoleScore

    scores = [4, 5, 4, 3, 5, 6, 4, 3, 5, 4, 4, 3, 6, 5, 4, 4, 3, 4]
    hole_scores = []

    for i in range(18):
        score = HoleScore.objects.create(
            round=round_obj,
            player=player,
            hole_number=i + 1,
            strokes=scores[i],
            verified=True
        )
        hole_scores.append(score)

    return hole_scores
