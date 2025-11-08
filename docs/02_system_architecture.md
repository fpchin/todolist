# Golf Tournament Management System - System Architecture Blueprint

## Executive Summary
This document defines the comprehensive architectural blueprint for the GTMS, a three-tier web application designed to replace the legacy Excel/VBA system. The architecture prioritizes maintainability, scalability, and ease of use.

## Technology Stack

### Backend (API/Application Layer)
- **Framework**: Django 4.2+ with Django Rest Framework (DRF) 3.14+
- **Language**: Python 3.11+
- **API Style**: RESTful JSON API
- **Real-time Communication**: Django Channels 4.0+ with WebSocket support
- **Authentication**: JWT (JSON Web Tokens) via djangorestframework-simplejwt
- **Task Queue**: Celery 5.3+ with Redis as broker
- **Validation**: DRF Serializers with custom validators

### Database (Data Layer)
- **Primary Database**: PostgreSQL 14+
- **Connection Pooling**: PgBouncer
- **Migrations**: Django ORM Migrations
- **Caching**: Redis 7+ (shared with Celery)

### Frontend (Presentation Layer)
- **Framework**: React 18+ with Hooks
- **Language**: TypeScript 5+
- **State Management**: Redux Toolkit with RTK Query
- **UI Components**: Material-UI (MUI) 5+ for responsive design
- **Forms**: React Hook Form with Yup validation
- **Real-time Updates**: WebSocket client (Socket.IO or native WebSocket)
- **Build Tool**: Vite
- **Mobile-First**: Responsive design with mobile-first breakpoints

### DevOps & Infrastructure
- **Containerization**: Docker 24+ with Docker Compose
- **Orchestration**: Docker Swarm or Kubernetes (production)
- **CI/CD**: GitHub Actions
- **Web Server**: Nginx (reverse proxy and static file serving)
- **WSGI Server**: Gunicorn with multiple workers
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana) or CloudWatch
- **Backup**: Automated PostgreSQL pg_dump with retention policy

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Presentation Layer                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐      │
│  │  Admin Dashboard │  │  Mobile Scoring  │  │  Live Leaderboard│      │
│  │   (React SPA)    │  │     UI (React)   │  │    (React SPA)   │      │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘      │
│           │                     │                      │                 │
│           └─────────────────────┼──────────────────────┘                 │
│                                 │                                        │
│                    HTTPS/WSS (Nginx Reverse Proxy)                      │
│                                 │                                        │
└─────────────────────────────────┼────────────────────────────────────────┘
                                  │
┌─────────────────────────────────┼────────────────────────────────────────┐
│                          Application Layer                               │
├─────────────────────────────────┼────────────────────────────────────────┤
│                                 │                                        │
│  ┌──────────────────────────────▼──────────────────────────────┐        │
│  │             Django Application (Gunicorn)                    │        │
│  ├──────────────────────────────────────────────────────────────┤        │
│  │                                                              │        │
│  │  ┌────────────────┐  ┌────────────────┐  ┌───────────────┐ │        │
│  │  │ REST API Layer │  │ WebSocket      │  │ Authentication│ │        │
│  │  │  (DRF Views)   │  │ Handler        │  │   (JWT Auth)  │ │        │
│  │  └───────┬────────┘  │ (Channels)     │  └───────────────┘ │        │
│  │          │           └───────┬────────┘                     │        │
│  │          │                   │                              │        │
│  │  ┌───────▼───────────────────▼─────────┐                   │        │
│  │  │      Business Logic Layer           │                   │        │
│  │  ├─────────────────────────────────────┤                   │        │
│  │  │ ┌─────────────────────────────────┐ │                   │        │
│  │  │ │  Scoring Calculation Engine     │ │ (Core Module)     │        │
│  │  │ │  - Stroke Play Calculator       │ │                   │        │
│  │  │ │  - Handicap Adjuster            │ │                   │        │
│  │  │ │  - Ranking Algorithm            │ │                   │        │
│  │  │ └─────────────────────────────────┘ │                   │        │
│  │  │                                     │                   │        │
│  │  │ ┌─────────────────────────────────┐ │                   │        │
│  │  │ │  Tournament Management Service  │ │                   │        │
│  │  │ │  - Player Registration          │ │                   │        │
│  │  │ │  - Flight/Pairing Management    │ │                   │        │
│  │  │ │  - Round Management             │ │                   │        │
│  │  │ └─────────────────────────────────┘ │                   │        │
│  │  │                                     │                   │        │
│  │  │ ┌─────────────────────────────────┐ │                   │        │
│  │  │ │  Score Management Service       │ │                   │        │
│  │  │ │  - Score Entry & Validation     │ │                   │        │
│  │  │ │  - Score Verification           │ │                   │        │
│  │  │ │  - Live Score Broadcasting      │ │                   │        │
│  │  │ └─────────────────────────────────┘ │                   │        │
│  │  └─────────────────────────────────────┘                   │        │
│  │                        │                                    │        │
│  │  ┌─────────────────────▼──────────────────────┐            │        │
│  │  │         Django ORM (Data Access)           │            │        │
│  │  └────────────────────────────────────────────┘            │        │
│  └──────────────────────────┬─────────────────────────────────┘        │
│                             │                                           │
│  ┌──────────────────────────▼──────────────────────────────┐           │
│  │            Celery Workers (Async Tasks)                 │           │
│  │  - Result Calculation                                   │           │
│  │  - Email Notifications                                  │           │
│  │  - Data Export Jobs                                     │           │
│  └─────────────────────────────────────────────────────────┘           │
│                             │                                           │
└─────────────────────────────┼───────────────────────────────────────────┘
                              │
┌─────────────────────────────┼───────────────────────────────────────────┐
│                          Data Layer                                     │
├─────────────────────────────┼───────────────────────────────────────────┤
│                             │                                           │
│  ┌──────────────────────────▼──────────────┐  ┌─────────────────────┐  │
│  │     PostgreSQL Database                 │  │   Redis Cache       │  │
│  │  - Tournament Data                      │  │  - Session Data     │  │
│  │  - Player & Score Data                  │  │  - Celery Queue     │  │
│  │  - Results & Rankings                   │  │  - WebSocket State  │  │
│  └─────────────────────────────────────────┘  └─────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Three-Tier Architecture Design

### 1. Presentation Layer (Frontend)

#### 1.1 Admin Dashboard
**Purpose**: Tournament management interface for administrators and officials.

**Features**:
- Tournament creation and configuration
- Player registration management
- Flight/pairing assignment
- Score verification and editing
- Real-time tournament monitoring
- Report generation

**Technical Details**:
- React SPA with TypeScript
- Redux Toolkit for state management
- Material-UI components
- Responsive design (desktop-optimized)

#### 1.2 Mobile Scoring UI
**Purpose**: Mobile-first interface for scorers to input hole-by-hole scores.

**Features**:
- Simple, touch-friendly score entry
- Per-hole score input with validation
- Real-time score submission
- Visual feedback on save success
- Offline capability (Progressive Web App)

**Technical Details**:
- Mobile-first React components
- Large touch targets (minimum 44x44px)
- Service Worker for offline support
- Optimistic UI updates

#### 1.3 Live Leaderboard
**Purpose**: Public-facing real-time leaderboard display.

**Features**:
- Real-time score updates via WebSocket
- Multiple view modes (Overall, By Division, By Round)
- Filtering and search capabilities
- Responsive design for all devices

**Technical Details**:
- WebSocket integration for live updates
- Efficient rendering with React.memo and virtualization
- Auto-refresh fallback for WebSocket failures

### 2. Application Layer (Backend)

#### 2.1 REST API Layer (Django Rest Framework)

**Core API Endpoints**:

```
Authentication:
POST   /api/v1/auth/login/          - JWT token generation
POST   /api/v1/auth/refresh/        - Token refresh
POST   /api/v1/auth/logout/         - Token invalidation

Tournaments:
GET    /api/v1/tournaments/         - List tournaments
POST   /api/v1/tournaments/         - Create tournament
GET    /api/v1/tournaments/{id}/    - Get tournament details
PUT    /api/v1/tournaments/{id}/    - Update tournament
DELETE /api/v1/tournaments/{id}/    - Delete tournament
GET    /api/v1/tournaments/{id}/leaderboard/ - Get leaderboard

Players:
GET    /api/v1/players/             - List players
POST   /api/v1/players/             - Create player
GET    /api/v1/players/{id}/        - Get player details
PUT    /api/v1/players/{id}/        - Update player
DELETE /api/v1/players/{id}/        - Delete player

Tournament Registrations:
POST   /api/v1/tournaments/{id}/register/    - Register player
GET    /api/v1/tournaments/{id}/players/     - List registered players
PUT    /api/v1/tournaments/{id}/players/{pid}/ - Update registration

Rounds & Tee Times:
GET    /api/v1/tournaments/{id}/rounds/      - List rounds
POST   /api/v1/tournaments/{id}/rounds/      - Create round
GET    /api/v1/rounds/{id}/tee-times/        - List tee times
POST   /api/v1/rounds/{id}/tee-times/        - Create tee time

Scores:
POST   /api/v1/scores/              - Submit hole score
GET    /api/v1/rounds/{id}/scores/  - Get all scores for round
PUT    /api/v1/scores/{id}/         - Update hole score
POST   /api/v1/scores/{id}/verify/  - Verify score

Results:
GET    /api/v1/tournaments/{id}/results/ - Get tournament results
POST   /api/v1/tournaments/{id}/calculate/ - Trigger result calculation
```

**API Design Principles**:
- RESTful resource design
- Consistent error handling (RFC 7807 Problem Details)
- Pagination for list endpoints (limit/offset)
- Filtering, sorting, and search via query parameters
- Versioning via URL path (`/api/v1/`)
- HATEOAS links for resource navigation

#### 2.2 Business Logic Layer

##### 2.2.1 Scoring Calculation Engine (Core Module)
**Location**: `backend/gtms/scoring/engine.py`

**Responsibilities**:
- Calculate gross scores from hole scores
- Apply handicap adjustments to produce net scores
- Calculate Stableford points (when applicable)
- Determine rankings (overall and by division)
- Handle ties using specified tie-breaking rules

**Design Principles**:
- Pure functions (no side effects)
- Idempotent operations
- Comprehensive unit test coverage
- Separated from database layer (accepts data structures, not ORM models)

**Example Function Signature**:
```python
def calculate_net_score(
    gross_score: int,
    playing_handicap: int,
    hole_scores: List[HoleScoreData],
    course_config: CourseConfigData
) -> int:
    """
    Calculate net score for a player.

    Args:
        gross_score: Total gross score
        playing_handicap: Player's playing handicap for this round
        hole_scores: List of hole score data
        course_config: Course configuration data

    Returns:
        Net score (gross - handicap applied per hole)
    """
    ...
```

##### 2.2.2 Tournament Management Service
**Location**: `backend/gtms/tournaments/services.py`

**Responsibilities**:
- Tournament lifecycle management (create, start, complete, cancel)
- Player registration and withdrawal
- Flight/pairing assignment algorithms
- Round scheduling

##### 2.2.3 Score Management Service
**Location**: `backend/gtms/scores/services.py`

**Responsibilities**:
- Score entry validation
- Score verification workflow
- Real-time score broadcasting via WebSocket
- Score correction and audit trail

#### 2.3 Real-time Communication (Django Channels)

**WebSocket Endpoint**: `wss://domain/ws/tournament/{tournament_id}/`

**Message Types**:
```json
{
  "type": "score.update",
  "data": {
    "player_id": "uuid",
    "hole_number": 1,
    "strokes": 4,
    "total_gross": 4,
    "total_net": 3
  }
}

{
  "type": "leaderboard.update",
  "data": {
    "rankings": [...]
  }
}
```

**Consumer Design**:
- Async consumer for WebSocket handling
- Channel layers with Redis backend
- Authentication via JWT in query parameter
- Automatic reconnection handling on client side

#### 2.4 Asynchronous Task Processing (Celery)

**Task Examples**:
```python
@shared_task
def calculate_tournament_results(tournament_id: str):
    """Calculate results for all players in tournament."""
    ...

@shared_task
def send_registration_confirmation_email(player_id: str, tournament_id: str):
    """Send confirmation email to registered player."""
    ...

@shared_task
def generate_scorecard_pdf(round_id: str):
    """Generate printable scorecards for a round."""
    ...
```

### 3. Data Layer

#### 3.1 PostgreSQL Database
- Refer to `01_database_schema.md` for complete schema
- Connection pooling via PgBouncer for efficient connection management
- Read replicas for leaderboard queries (optional for scale)
- Automated backups with point-in-time recovery

#### 3.2 Redis Cache
**Use Cases**:
- Session storage for authenticated users
- Celery task queue and result backend
- Django Channels channel layer
- API response caching (tournament leaderboard)
- Rate limiting for API endpoints

**Cache Keys**:
```
session:{session_id}
leaderboard:{tournament_id}
player:{player_id}
celery:task:{task_id}
```

## Service Boundaries

### Scoring Engine Service
**Boundary**: Pure calculation logic, no external dependencies
**Input**: Data structures (not ORM models)
**Output**: Calculated values (scores, rankings)
**Testing**: Unit tests with 100% coverage

### API Service
**Boundary**: HTTP request/response handling
**Dependencies**: Business logic services, ORM
**Validation**: DRF serializers
**Testing**: Integration tests, API contract tests

### WebSocket Service
**Boundary**: Real-time data broadcasting
**Dependencies**: Channel layers, Redis
**Protocol**: WebSocket with JSON messages
**Testing**: WebSocket integration tests

## Communication Protocols

### Frontend ↔ Backend
- **Primary**: REST API over HTTPS
- **Real-time**: WebSocket over WSS
- **Authentication**: JWT Bearer token in Authorization header
- **Data Format**: JSON
- **API Versioning**: URL path versioning

### Backend ↔ Database
- **Protocol**: PostgreSQL wire protocol
- **Connection**: Connection pooling via PgBouncer
- **ORM**: Django ORM with optimized queries (select_related, prefetch_related)

### Backend ↔ Cache
- **Protocol**: Redis protocol
- **Client**: django-redis
- **Serialization**: JSON or Pickle

## Security Architecture

### Authentication & Authorization
- **Authentication**: JWT (Access + Refresh tokens)
- **Authorization**: Django permissions and custom role-based access control
- **Roles**: Admin, Scorer, Player, Public
- **Token Storage**: httpOnly cookies (frontend) or localStorage with XSS protection

### API Security
- **HTTPS/TLS**: Mandatory for all communications
- **CORS**: Configured for allowed origins
- **Rate Limiting**: Per-user and per-IP rate limits
- **Input Validation**: DRF serializers + custom validators
- **SQL Injection**: Protected by ORM parameterized queries
- **XSS**: React's built-in escaping + CSP headers
- **CSRF**: CSRF tokens for state-changing operations

### Data Security
- **Encryption at Rest**: PostgreSQL encryption (if required)
- **Encryption in Transit**: TLS 1.3
- **Secret Management**: Environment variables, never hardcoded
- **Password Storage**: Django's PBKDF2 password hasher
- **Audit Logging**: All score modifications logged with timestamp and user

## Deployment Architecture

### Development Environment
```yaml
services:
  - nginx:latest
  - backend:gtms-django:dev
  - frontend:gtms-react:dev (dev server)
  - postgres:14
  - redis:7
  - celery-worker:gtms-django:dev
```

### Production Environment
```yaml
services:
  - nginx:latest (+ SSL termination)
  - backend:gtms-django:prod (Gunicorn, multiple workers)
  - frontend:gtms-react:prod (static build served by Nginx)
  - postgres:14 (+ pg_bouncer)
  - redis:7 (+ persistence)
  - celery-worker:gtms-django:prod
  - celery-beat:gtms-django:prod (scheduled tasks)
  - prometheus:latest (monitoring)
  - grafana:latest (dashboards)
```

### Scaling Strategy
- **Horizontal Scaling**: Multiple backend containers behind load balancer
- **Database Scaling**: Read replicas for leaderboard queries
- **Cache Scaling**: Redis Cluster for high availability
- **Static Assets**: CDN for frontend bundles and media files

## Non-Functional Requirements Compliance

### Performance
- **Live Score Update Latency**: < 500ms (WebSocket push)
- **API Response Time**: < 200ms (p95) for read operations
- **API Response Time**: < 1s (p95) for write operations
- **Database Query Time**: < 100ms (p95)

### Capacity
- **Concurrent Users**: 1,000+
- **Concurrent Tournaments**: 20+
- **Players per Tournament**: 200+
- **Database Size**: Designed for 10+ years of tournament data

### Availability
- **System Uptime**: > 99.5% (target)
- **Automated Health Checks**: Readiness and liveness probes
- **Graceful Degradation**: Leaderboard falls back to polling if WebSocket fails
- **Database Backups**: Daily automated backups with 30-day retention

### Maintainability
- **Code Quality**: PEP 8 compliance, TypeScript strict mode
- **Documentation**: Inline comments, API documentation (OpenAPI/Swagger)
- **Testing**: 90%+ code coverage
- **Logging**: Structured logging with correlation IDs
- **Monitoring**: Application metrics, error tracking (Sentry)

## Technology Decision Rationale

### Why Django Rest Framework?
- Mature, well-documented framework
- Built-in ORM reduces SQL complexity
- DRF provides robust serialization and validation
- Large ecosystem and community support
- Excellent for rapid, maintainable development

### Why React?
- Component-based architecture for reusability
- Strong TypeScript support for type safety
- Excellent mobile and responsive design support
- Large ecosystem of UI libraries (Material-UI)
- Virtual DOM for efficient rendering

### Why PostgreSQL?
- ACID compliance for data integrity
- Advanced indexing for query performance
- JSON support for flexible data structures
- Excellent Django integration
- Proven reliability at scale

### Why Docker?
- Consistent development and production environments
- Easy dependency management
- Simplified deployment and scaling
- Portable across cloud providers

## Next Steps
1. Setup project structure and Docker configuration
2. Implement CI/CD pipeline
3. Develop scoring calculation engine with comprehensive tests
4. Build core APIs and frontend components

---
**Document Version**: 1.0
**Last Updated**: 2024-11-08
**Status**: Final for Phase 1
