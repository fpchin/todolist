# Golf Tournament Management System (GTMS)

Modern web application for end-to-end golf tournament management, replacing the legacy Excel/VBA system.

## Project Overview

**Target**: Replace `21ST SIBU AMATEUR OPEN GOLF CHAMPIONSHIP 2023.xlsm` with a scalable, maintainable web application

**Tech Stack**:
- **Backend**: Django 4.2+ with Django Rest Framework
- **Frontend**: React 18+ with TypeScript
- **Database**: PostgreSQL 14+
- **Cache**: Redis 7+
- **Container**: Docker with Docker Compose
- **CI/CD**: GitHub Actions

## Features

- Tournament creation and configuration
- Player registration management
- Mobile-first score entry interface
- Real-time live leaderboard (WebSocket)
- Automated handicap calculation
- Multi-division support
- Results generation and ranking
- Data migration from legacy Excel system

## Project Structure

```
gtms/
├── backend/                  # Django backend application
│   ├── gtms/                # Main Django project
│   │   ├── settings/        # Environment-specific settings
│   │   ├── urls.py          # Root URL configuration
│   │   └── wsgi.py          # WSGI application
│   ├── apps/                # Django apps
│   │   ├── authentication/  # JWT auth
│   │   ├── tournaments/     # Tournament management
│   │   ├── players/         # Player management
│   │   ├── scores/          # Score management
│   │   ├── scoring/         # Scoring calculation engine
│   │   └── results/         # Results and leaderboard
│   ├── requirements/        # Python dependencies
│   ├── manage.py            # Django management script
│   └── pytest.ini           # Pytest configuration
├── frontend/                # React frontend application
│   ├── public/              # Static assets
│   ├── src/                 # React source code
│   │   ├── components/      # Reusable components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   ├── store/           # Redux store
│   │   └── App.tsx          # Root component
│   ├── package.json         # npm dependencies
│   └── tsconfig.json        # TypeScript configuration
├── database/                # Database migrations and scripts
│   └── migrations/          # PostgreSQL DDL scripts
├── docs/                    # Project documentation
├── docker/                  # Docker configuration files
│   ├── backend/             # Backend Dockerfile
│   ├── frontend/            # Frontend Dockerfile
│   └── nginx/               # Nginx configuration
├── scripts/                 # Utility scripts
├── .github/                 # GitHub Actions workflows
│   └── workflows/
├── docker-compose.yml       # Development environment
├── docker-compose.prod.yml  # Production environment
└── README.md                # This file
```

## Quick Start

### Prerequisites

- Docker 24+ and Docker Compose
- Git

### Development Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd todolist
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Build and start services**:
   ```bash
   docker-compose up --build
   ```

4. **Run database migrations**:
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

5. **Create superuser**:
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

6. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/v1/
   - Admin Panel: http://localhost:8000/admin/

### Running Tests

**Backend tests**:
```bash
docker-compose exec backend pytest
```

**Frontend tests**:
```bash
docker-compose exec frontend npm test
```

**Coverage report**:
```bash
docker-compose exec backend pytest --cov=apps --cov-report=html
```

## API Documentation

Once the backend is running, API documentation is available at:
- **Swagger UI**: http://localhost:8000/api/v1/docs/
- **ReDoc**: http://localhost:8000/api/v1/redoc/

## Development Workflow

### Backend Development

1. Create a new Django app:
   ```bash
   docker-compose exec backend python manage.py startapp <app_name> apps/<app_name>
   ```

2. Make migrations:
   ```bash
   docker-compose exec backend python manage.py makemigrations
   docker-compose exec backend python manage.py migrate
   ```

3. Run linting:
   ```bash
   docker-compose exec backend flake8
   docker-compose exec backend black . --check
   ```

### Frontend Development

1. Install new package:
   ```bash
   docker-compose exec frontend npm install <package-name>
   ```

2. Run linting:
   ```bash
   docker-compose exec frontend npm run lint
   ```

3. Build for production:
   ```bash
   docker-compose exec frontend npm run build
   ```

## Deployment

### Production Deployment

1. **Build production images**:
   ```bash
   docker-compose -f docker-compose.prod.yml build
   ```

2. **Run database migrations**:
   ```bash
   docker-compose -f docker-compose.prod.yml run --rm backend python manage.py migrate
   ```

3. **Collect static files**:
   ```bash
   docker-compose -f docker-compose.prod.yml run --rm backend python manage.py collectstatic --noinput
   ```

4. **Start services**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Environment Variables

Key environment variables (see `.env.example` for complete list):

- `DJANGO_SECRET_KEY`: Django secret key
- `DJANGO_DEBUG`: Debug mode (False in production)
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins

## Data Migration

To migrate data from the legacy Excel system:

```bash
# Place legacy file in legacy/ directory
cp "21ST SIBU AMATEUR OPEN GOLF CHAMPIONSHIP 2023.xlsm" legacy/

# Run migration script
docker-compose exec backend python manage.py migrate_legacy_data legacy/21ST\ SIBU\ AMATEUR\ OPEN\ GOLF\ CHAMPIONSHIP\ 2023.xlsm
```

## Monitoring

### Application Monitoring
- **Prometheus**: http://localhost:9090 (production)
- **Grafana**: http://localhost:3001 (production)

### Logs

View logs in real-time:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Contributing

### Code Quality Standards

- **Python**: PEP 8 compliance, enforced by flake8 and black
- **TypeScript**: ESLint + Prettier
- **Test Coverage**: Minimum 90% for backend, 80% for frontend
- **Documentation**: All public functions must have docstrings

### Git Workflow

1. Create feature branch from `main`
2. Make changes with clear, descriptive commits
3. Ensure all tests pass
4. Submit pull request
5. Wait for CI/CD checks to pass
6. Request code review

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat(scores): add real-time WebSocket score updates

- Implement Django Channels consumer
- Add WebSocket client in React
- Update leaderboard component for live updates

Closes #42
```

## License

TBD

## Support

For issues and questions, please open a GitHub issue or contact the development team.

## Roadmap

### Phase 1: Inception and Architecture (✅ Complete)
- [x] Database schema design
- [x] System architecture blueprint
- [x] NFR metrics definition
- [x] Legacy analysis preparation

### Phase 2: Core Development (🔄 In Progress)
- [x] Project structure setup
- [ ] Scoring calculation engine
- [ ] Core REST APIs
- [ ] Mobile scoring UI
- [ ] Admin dashboard and leaderboard

### Phase 3: Integration & Testing
- [ ] Data migration tool
- [ ] Comprehensive automated testing
- [ ] User acceptance testing
- [ ] Deployment setup

### Phase 4: Maintenance
- [ ] Documentation
- [ ] Monitoring and error remediation
- [ ] Feature roadmap implementation

---

**Project Status**: Phase 2 - Core Development
**Last Updated**: 2024-11-08
