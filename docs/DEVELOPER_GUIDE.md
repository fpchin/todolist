# GTMS Developer Guide

Comprehensive guide for developers working on the Golf Tournament Management System.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Architecture Overview](#architecture-overview)
3. [Backend Development](#backend-development)
4. [Frontend Development](#frontend-development)
5. [Database](#database)
6. [API Documentation](#api-documentation)
7. [Testing](#testing)
8. [Code Style](#code-style)
9. [Common Tasks](#common-tasks)
10. [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+
- Docker & Docker Compose (recommended)

### Initial Setup

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd gtms
   ```

2. **Backend setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements/development.txt
   ```

3. **Database setup**
   ```bash
   createdb gtms_dev
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Frontend setup**
   ```bash
   cd ../frontend
   npm install
   ```

5. **Run development servers**
   ```bash
   # Terminal 1: Backend
   cd backend
   python manage.py runserver

   # Terminal 2: Frontend
   cd frontend
   npm run dev

   # Terminal 3: Redis (if not using Docker)
   redis-server

   # Terminal 4: Celery
   cd backend
   celery -A gtms worker -l info
   ```

## Architecture Overview

### System Architecture

GTMS follows a three-tier architecture:

1. **Presentation Layer**: React + TypeScript frontend
2. **Application Layer**: Django + DRF backend
3. **Data Layer**: PostgreSQL + Redis

### Key Concepts

#### Scoring Engine (Phase 2.2)

Pure Python module in `backend/apps/scoring/engine.py`:
- No Django dependencies
- 100% unit test coverage
- Implements OCB (Order of Card Back) tiebreakers
- Calculates gross/net scores with handicap strokes

#### Service Layer Pattern

`backend/apps/scores/services.py`:
- Bridges Django ORM and pure scoring engine
- Handles database transactions
- Calculates and persists tournament results

#### Redux State Management

Frontend state organized by feature:
- `roundSlice`: Tournament rounds
- `scoreSlice`: Score entry
- `tournamentSlice`: Tournament CRUD
- `leaderboardSlice`: Live rankings

## Backend Development

### Django Apps

#### Core Apps
- **authentication**: User management and JWT tokens
- **core**: Base models and utilities
- **scoring**: Pure Python scoring engine
- **tournaments**: Tournament, Round, TournamentPlayer
- **players**: Player master data
- **courses**: Course and hole configuration
- **scores**: HoleScore, Result models
- **migration**: Legacy data import tools

### Models

#### Base Model Pattern

All models inherit from `TimeStampedModel`:

```python
from apps.core.models import TimeStampedModel

class MyModel(TimeStampedModel):
    # Automatically adds:
    # - id (UUID primary key)
    # - created_at (timestamp)
    # - updated_at (timestamp)
    pass
```

#### Key Models

**Tournament**
```python
Tournament(
    name='Championship 2023',
    location='Golf Club',
    start_date=date(2023, 10, 15),
    end_date=date(2023, 10, 16),
    format_type='STROKEPLAY',
    status='OPEN',
    max_players=200
)
```

**HoleScore**
```python
HoleScore(
    round=round_obj,
    player=player_obj,
    hole_number=1,
    strokes=4,
    putts=2,
    verified=True
)
```

### API Endpoints

#### ViewSet Pattern

All API endpoints use DRF ViewSets:

```python
class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    @action(detail=True, methods=['post'])
    def register_player(self, request, pk=None):
        # Custom endpoint: POST /tournaments/{id}/register_player/
        pass
```

#### URL Routing

```python
# apps/tournaments/urls.py
router = DefaultRouter()
router.register(r'tournaments', TournamentViewSet)

urlpatterns = router.urls
```

### Serializers

#### Nested Serialization

```python
class TournamentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    players = TournamentPlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Tournament
        fields = '__all__'
```

### Celery Tasks

#### Async Task Pattern

```python
from celery import shared_task

@shared_task
def calculate_tournament_results(tournament_id):
    service = ScoringService()
    results = service.calculate_tournament_results(tournament_id)
    return len(results)
```

### WebSocket Consumers

#### Channel Layer

```python
from channels.generic.websocket import AsyncWebsocketConsumer

class LeaderboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.tournament_id = self.scope['url_route']['kwargs']['tournament_id']
        await self.channel_layer.group_add(
            f'leaderboard_{self.tournament_id}',
            self.channel_name
        )
        await self.accept()
```

## Frontend Development

### Component Structure

#### Folder Organization

```
components/
├── common/          # Shared components
│   ├── Button.tsx
│   ├── LoadingSpinner.tsx
│   └── ErrorAlert.tsx
├── scoring/         # Feature-specific
│   ├── HoleScoreInput.tsx
│   └── ScoreCard.tsx
├── admin/
│   ├── TournamentCard.tsx
│   └── TournamentForm.tsx
└── leaderboard/
    └── LeaderboardTable.tsx
```

#### Component Pattern

```typescript
interface MyComponentProps {
  title: string;
  onSubmit: (data: FormData) => void;
}

export const MyComponent: React.FC<MyComponentProps> = ({
  title,
  onSubmit
}) => {
  const [state, setState] = useState<StateType>(initialState);

  return (
    <div>
      {/* Component JSX */}
    </div>
  );
};
```

### Redux Patterns

#### Slice Creation

```typescript
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

export const fetchData = createAsyncThunk(
  'feature/fetchData',
  async (id: string, { rejectWithValue }) => {
    try {
      const response = await api.get(id);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data);
    }
  }
);

const featureSlice = createSlice({
  name: 'feature',
  initialState,
  reducers: {
    // Synchronous actions
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchData.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchData.fulfilled, (state, action) => {
        state.data = action.payload;
        state.loading = false;
      })
      .addCase(fetchData.rejected, (state, action) => {
        state.error = action.payload;
        state.loading = false;
      });
  },
});
```

#### Using in Components

```typescript
import { useAppDispatch } from '../hooks/useAppDispatch';
import { useAppSelector } from '../hooks/useAppSelector';
import { fetchData } from '../store/slices/featureSlice';

const MyComponent = () => {
  const dispatch = useAppDispatch();
  const { data, loading, error } = useAppSelector((state) => state.feature);

  useEffect(() => {
    dispatch(fetchData('123'));
  }, [dispatch]);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorAlert error={error} />;

  return <div>{/* Render data */}</div>;
};
```

### API Integration

#### API Client

```typescript
// src/api/endpoints.ts
import { apiClient } from './client';

export const myAPI = {
  list: () => apiClient.get('/my-endpoint/'),
  get: (id: string) => apiClient.get(`/my-endpoint/${id}/`),
  create: (data: CreateData) => apiClient.post('/my-endpoint/', data),
  update: (id: string, data: UpdateData) =>
    apiClient.patch(`/my-endpoint/${id}/`, data),
  delete: (id: string) => apiClient.delete(`/my-endpoint/${id}/`),
};
```

### Form Handling

#### React Hook Form + Yup

```typescript
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';

const schema = yup.object({
  name: yup.string().required('Name is required'),
  email: yup.string().email('Invalid email').required(),
}).required();

const MyForm = () => {
  const { control, handleSubmit, formState: { errors } } = useForm({
    resolver: yupResolver(schema),
  });

  const onSubmit = (data) => {
    // Handle form submission
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Controller
        name="name"
        control={control}
        render={({ field }) => (
          <TextField
            {...field}
            error={!!errors.name}
            helperText={errors.name?.message}
          />
        )}
      />
    </form>
  );
};
```

## Database

### Schema Design

11 entities in Third Normal Form (3NF):

1. **Tournament** - Tournament metadata
2. **TournamentPlayer** - Player registrations
3. **Round** - Tournament rounds
4. **TeeTime** - Starting times
5. **FlightPlayer** - Flight groupings
6. **Player** - Player master data
7. **HandicapHistory** - Handicap records
8. **CourseConfiguration** - Course setup
9. **HoleConfiguration** - Individual holes
10. **HoleScore** - Individual hole scores
11. **Result** - Calculated results with OCB

### Migrations

#### Creating Migrations

```bash
# Auto-generate migrations
python manage.py makemigrations

# Create empty migration
python manage.py makemigrations --empty myapp

# Name migration
python manage.py makemigrations --name add_field_to_model myapp
```

#### Writing Custom Migrations

```python
from django.db import migrations

def forward(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'MyModel')
    # Custom migration logic

def backward(apps, schema_editor):
    # Reverse migration logic
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
```

## API Documentation

### Interactive API Docs

Access at: `http://localhost:8000/api/v1/docs/`

Powered by drf-spectacular, provides:
- Interactive API testing
- Request/response examples
- Schema download (OpenAPI 3.0)

### Adding API Documentation

```python
from drf_spectacular.utils import extend_schema, OpenApiParameter

class MyViewSet(viewsets.ModelViewSet):
    @extend_schema(
        summary="List all items",
        description="Returns a paginated list of items",
        parameters=[
            OpenApiParameter(
                name='search',
                description='Search term',
                required=False,
                type=str
            ),
        ],
        responses={200: MySerializer(many=True)}
    )
    def list(self, request):
        # Implementation
        pass
```

## Testing

### Backend Testing

#### Test Structure

```python
import pytest
from apps.myapp.models import MyModel

@pytest.mark.django_db
class TestMyModel:
    def test_create_model(self):
        obj = MyModel.objects.create(name='Test')
        assert obj.name == 'Test'

    def test_model_str(self):
        obj = MyModel.objects.create(name='Test')
        assert str(obj) == 'Test'
```

#### Using Fixtures

```python
@pytest.fixture
def my_model(db):
    return MyModel.objects.create(name='Test')

def test_with_fixture(my_model):
    assert my_model.name == 'Test'
```

#### API Testing

```python
@pytest.mark.api
def test_list_endpoint(authenticated_client):
    response = authenticated_client.get('/api/v1/my-endpoint/')
    assert response.status_code == 200
    assert len(response.data['results']) > 0
```

### Frontend Testing

#### Component Testing

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { MyComponent } from '../MyComponent';

describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent title="Test" />);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const handleClick = vi.fn();
    render(<MyComponent onClick={handleClick} />);

    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalled();
  });
});
```

#### Redux Testing

```typescript
import reducer, { myAction } from '../mySlice';

describe('mySlice', () => {
  it('handles myAction', () => {
    const initialState = { value: 0 };
    const action = myAction(5);
    const newState = reducer(initialState, action);

    expect(newState.value).toBe(5);
  });
});
```

## Code Style

### Python (Backend)

- **Formatter**: Black (line length 100)
- **Linter**: Flake8
- **Type Checker**: MyPy
- **Import Sorter**: isort

```bash
# Format code
black apps/

# Lint
flake8 apps/

# Type check
mypy apps/

# Sort imports
isort apps/
```

### TypeScript (Frontend)

- **Linter**: ESLint
- **Formatter**: Prettier
- **Type Checking**: TypeScript strict mode

```bash
# Lint
npm run lint

# Format
npm run format

# Type check
npm run type-check
```

## Common Tasks

### Adding a New Model

1. Create model in `apps/myapp/models.py`
2. Create serializer in `apps/myapp/serializers.py`
3. Create viewset in `apps/myapp/views.py`
4. Add URL routes in `apps/myapp/urls.py`
5. Create migrations: `python manage.py makemigrations`
6. Run migrations: `python manage.py migrate`
7. Write tests in `apps/myapp/tests/`

### Adding a New API Endpoint

1. Add method to ViewSet with `@action` decorator
2. Update serializer if needed
3. Add API documentation with `@extend_schema`
4. Write tests

### Adding a New React Component

1. Create component file in appropriate directory
2. Add TypeScript interface for props
3. Implement component logic
4. Write tests in `__tests__/` directory
5. Export from index file if needed

### Running Data Migration

```bash
# Dry run
python manage.py import_legacy_data tournament.xlsm --dry-run

# Actual import
python manage.py import_legacy_data tournament.xlsm
```

## Troubleshooting

### Common Issues

#### Database Connection Error
```
Check PostgreSQL is running
Check DATABASE_URL environment variable
Verify database exists
```

#### Redis Connection Error
```
Check Redis is running: redis-cli ping
Check REDIS_URL environment variable
```

#### Migration Conflicts
```bash
# Show migrations
python manage.py showmigrations

# Fake migration if needed
python manage.py migrate --fake myapp 0001

# Reset migrations (development only!)
python manage.py migrate myapp zero
```

#### Frontend Build Errors
```bash
# Clear cache
rm -rf node_modules/.vite

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Check TypeScript errors
npm run type-check
```

### Debug Mode

#### Backend
```python
# settings/development.py
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

#### Frontend
```typescript
// Enable Redux DevTools
const store = configureStore({
  reducer: rootReducer,
  devTools: process.env.NODE_ENV !== 'production',
});
```

---

For more information, see:
- [README.md](../README.md)
- [API Documentation](http://localhost:8000/api/v1/docs/)
- [Phase Reports](.) in docs/
