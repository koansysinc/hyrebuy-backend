# HyreBuy Backend API

FastAPI backend for HyreBuy real estate platform targeting GCC employees in Hyderabad.

## Tech Stack

- **FastAPI** 0.109+ - Modern async Python web framework
- **Python** 3.11+ - Programming language
- **PostgreSQL** 15 - Database (via Supabase free tier)
- **Redis** - Caching layer (via Upstash free tier)
- **SQLAlchemy** 2.0 - Async ORM
- **Alembic** - Database migrations
- **Pydantic** v2 - Data validation

## Features (Phase 1 - Week 1-4)

- ✅ User authentication (JWT)
- ✅ Property search with filters
- ✅ Commute score calculation (OSRM API)
- ✅ Smart property scoring algorithm
- ✅ Saved properties
- ✅ Group buying (basic: create, invite, join)

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git
- Supabase account (free tier)
- Upstash account (free tier)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/hyrebuy-backend.git
cd hyrebuy-backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required variables:
- `DATABASE_URL` - Get from Supabase project settings
- `REDIS_URL` - Get from Upstash Redis dashboard
- `SECRET_KEY` - Generate with: `openssl rand -hex 32`
- `SENDGRID_API_KEY` - Get from SendGrid account

### 5. Database Migrations

```bash
# Run migrations to create all tables
alembic upgrade head
```

### 6. Seed Data (Optional)

```bash
# Populate database with sample properties and GCC companies
python scripts/seed_data.py
```

### 7. Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Project Structure

```
hyrebuy-backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── api/
│   │   └── v1/              # API endpoints (auth, properties, groups)
│   ├── models/              # SQLAlchemy database models
│   ├── schemas/             # Pydantic validation schemas
│   ├── services/            # Business logic
│   └── utils/               # Helper functions
├── alembic/                 # Database migrations
├── tests/                   # Pytest tests
├── scripts/                 # Utility scripts (seed data, etc.)
├── requirements.txt         # Python dependencies
└── .env.example             # Environment variables template
```

## API Endpoints (Phase 1)

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login

### Properties
- `GET /api/v1/properties/search` - Search properties with filters
- `GET /api/v1/properties/{id}` - Get property details

### Commute
- `GET /api/v1/commute/calculate` - Calculate commute time

### Groups (Basic)
- `POST /api/v1/groups` - Create buying group
- `POST /api/v1/groups/{id}/invite` - Invite members
- `POST /api/v1/groups/join/{invite_code}` - Join group

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

## Deployment

### Deploy to Render.com (Free Tier)

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect GitHub repository
4. Set environment variables
5. Deploy

Auto-deployment is configured via GitHub Actions (see `.github/workflows/`).

## Database Schema

Key tables:
- `users` - User accounts
- `properties` - Property listings
- `gcc_companies` - GCC office locations
- `commute_scores` - Pre-calculated commute times
- `buying_groups` - Group buying groups
- `group_members` - Group membership
- `saved_properties` - User favorites

See `docs/database_schema.md` for ER diagram.

## Performance

- API response time: <500ms (P95)
- Property search: <1s
- Concurrent users: 100+
- Database queries: Optimized with indexes

## Security

- Passwords hashed with bcrypt
- JWT tokens for authentication
- SQL injection prevention (parameterized queries)
- CORS configured for frontend domain only
- Rate limiting on authentication endpoints

## Support

- **Documentation**: See `/docs` folder
- **Issues**: https://github.com/yourusername/hyrebuy-backend/issues

## License

Proprietary - All rights reserved

---

**Phase 1 Status**: In Development (Week 1, Day 1)
