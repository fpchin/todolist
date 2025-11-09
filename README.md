# Golf Tournament Management System (GTMS)

A modern, full-stack web application for managing golf tournaments, replacing legacy Excel/VBA systems with a scalable, cloud-ready solution.

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](backend/pytest.ini)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)](backend/.coveragerc)
[![Python](https://img.shields.io/badge/python-3.11+-blue)](backend/requirements/base.txt)
[![Django](https://img.shields.io/badge/django-4.2-green)](backend/requirements/base.txt)
[![React](https://img.shields.io/badge/react-18+-blue)](frontend/package.json)
[![TypeScript](https://img.shields.io/badge/typescript-5+-blue)](frontend/package.json)

## 🎯 Overview

GTMS is a comprehensive tournament management system designed to replace the legacy Excel/VBA-based "21ST SIBU AMATEUR OPEN GOLF CHAMPIONSHIP 2023.xlsm" with a modern web application offering:

✅ **Multi-user access** - Concurrent scoring from multiple devices
✅ **Real-time updates** - Live leaderboard via WebSocket
✅ **Mobile-first design** - Optimized for smartphones and tablets
✅ **Data integrity** - Automated validation and OCB calculations
✅ **Cloud-ready** - Docker containerization and scalable architecture
✅ **90%+ test coverage** - Comprehensive automated testing

## ✨ Key Features

- **Tournament Management**: Create/edit tournaments, multiple formats (Stroke Play, Stableford, etc.)
- **Player Registration**: Manage players with handicaps and division assignments
- **Mobile Scoring**: Touch-friendly 18-hole score entry interface
- **Live Leaderboard**: Real-time rankings with OCB (Order of Card Back) tiebreakers
- **Admin Dashboard**: Full tournament administration
- **Data Migration**: Import legacy Excel tournament data
- **REST API**: Complete RESTful API with OpenAPI documentation
- **WebSocket**: Real-time leaderboard updates

## 🛠 Technology Stack

**Backend**: Django 4.2 + DRF | Python 3.11 | PostgreSQL 14 | Redis 7 | Celery
**Frontend**: React 18 + TypeScript 5 | Material-UI | Redux Toolkit | Vite
**Testing**: Pytest (90%+) | Vitest (80%+) | React Testing Library
**DevOps**: Docker | Docker Compose | GitHub Actions | Nginx

## 🚀 Quick Start

### Prerequisites
- Docker 20.10+ and Docker Compose 2.0+
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Using Docker (Recommended)

```bash
# Clone repository
git clone <repository-url>
cd gtms

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Access application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/api/v1/
# Admin: http://localhost:8000/admin/
# API Docs: http://localhost:8000/api/v1/docs/
```

### Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements/development.txt
python manage.py migrate
python manage.py runserver
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📚 Documentation

- **[Developer Guide](docs/DEVELOPER_GUIDE.md)** - Comprehensive development guide
- **[Database Schema](docs/01_database_schema.md)** - 3NF schema design
- **[System Architecture](docs/02_system_architecture.md)** - Architecture blueprint
- **[API Documentation](http://localhost:8000/api/v1/docs/)** - Interactive OpenAPI docs

### Phase Completion Reports
- [Phase 2.2: Scoring Engine](docs/phase_2_2_completion_report.md)
- [Phase 2.4: Mobile Scoring UI](docs/phase_2_4_completion_report.md)
- [Phase 2.5: Admin Dashboard](docs/phase_2_5_completion_report.md)
- [Phase 3.1: Data Migration](docs/phase_3_1_completion_report.md)
- [Phase 3.2: Automated Testing](docs/phase_3_2_completion_report.md)
- [Phase 4.1: Documentation](docs/phase_4_1_completion_report.md)

## 🧪 Testing

**Backend (90%+ coverage):**
```bash
pytest                    # Run all tests
pytest --cov             # With coverage
pytest -m api            # API tests only
```

**Frontend (82% coverage):**
```bash
npm test                 # Run all tests
npm run test:coverage    # With coverage
```

## 📁 Project Structure

```
gtms/
├── backend/                    # Django backend
│   ├── apps/                   # Django apps
│   │   ├── scoring/            # Pure Python scoring engine
│   │   ├── tournaments/        # Tournament management
│   │   ├── players/            # Player management
│   │   ├── scores/             # Score entry and results
│   │   └── migration/          # Legacy data import
│   ├── gtms/settings/          # Environment-specific settings
│   └── pytest.ini              # Test configuration
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page components
│   │   ├── store/              # Redux store
│   │   └── api/                # API client
│   └── vitest.config.ts        # Test configuration
├── docs/                       # Documentation
├── docker-compose.yml          # Development environment
└── README.md                   # This file
```

## 🎮 Usage

### Import Legacy Data
```bash
python manage.py import_legacy_data tournament.xlsm --dry-run  # Validate
python manage.py import_legacy_data tournament.xlsm            # Import
```

### Run Tests
```bash
# Backend
pytest apps/tournaments/tests/
pytest --cov=apps --cov-report=html

# Frontend
npm test -- ScoreCard.test.tsx
npm test -- --coverage
```

### API Development
```bash
# Generate API schema
python manage.py spectacular --file schema.yml

# View API docs
open http://localhost:8000/api/v1/docs/
```

## 🏗 Architecture

### Three-Tier Architecture
```
┌─────────────────────┐
│  Presentation Layer │  React + TypeScript
├─────────────────────┤
│  Application Layer  │  Django + DRF
├─────────────────────┤
│     Data Layer      │  PostgreSQL + Redis
└─────────────────────┘
```

### Key Components
- **Scoring Engine**: Pure Python (100% coverage)
- **Service Layer**: Django ORM integration
- **REST API**: DRF ViewSets with serializers
- **WebSocket**: Django Channels for live updates
- **State Management**: Redux Toolkit
- **UI Components**: Material-UI with custom theme

## 📊 Project Status

### Completed Phases ✅

**Phase 1: Architecture & Design**
- ✅ Database schema (11 entities, 3NF)
- ✅ System architecture
- ✅ NFR metrics definition

**Phase 2: Core Development**
- ✅ Project setup (Docker, CI/CD)
- ✅ Scoring engine (OCB tiebreakers)
- ✅ REST APIs (11 models, ViewSets)
- ✅ Mobile scoring UI
- ✅ Admin dashboard & live leaderboard

**Phase 3: Integration & Testing**
- ✅ Data migration tool
- ✅ Automated testing (90%+ backend, 82% frontend)

### Statistics
- **70+ API endpoints**
- **11 database models**
- **38+ test suites**
- **90%+ backend coverage**
- **82% frontend coverage**
- **~15,000 lines of code**

## 🚢 Deployment

**Production:**
```bash
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

**Environment Variables:**
- `SECRET_KEY` - Django secret
- `DATABASE_URL` - PostgreSQL connection
- `REDIS_URL` - Redis connection
- `ALLOWED_HOSTS` - Allowed domains
- `CORS_ALLOWED_ORIGINS` - CORS settings

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

**Code Quality:**
- Backend: Black, Flake8, MyPy
- Frontend: ESLint, Prettier
- Tests: 90%+ backend, 80%+ frontend required

## 📄 License

[Your License Here]

## 📞 Support

- **Issues**: GitHub Issues
- **Email**: [your-email@example.com]
- **Docs**: http://localhost:8000/api/v1/docs/

---

**Built with ❤️ for golf clubs worldwide**
**Project Status**: Production-Ready | **Test Coverage**: 90%+ | **Last Updated**: 2025-11-09
