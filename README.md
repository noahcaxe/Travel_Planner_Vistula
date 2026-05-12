# Travel Project API

Backend REST API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy Async ORM**, **JWT Authentication**, and **Docker**.

The application allows users to create and manage travel projects with saved places.

---

# Features

## Authentication
- User registration
- JWT login authentication
- Access & refresh tokens
- Logout with token revoke support

## Projects
- Create travel project
- Get all user projects
- Get project by ID
- Update project
- Delete project

## Places
- Add place to project
- Get all project places
- Update place
- Delete place
- Maximum 10 places per project

---

# Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy Async ORM
- Alembic
- Docker & Docker Compose
- JWT Authentication
- Pydantic

---

# Project Structure

```bash
backend/
├── app/
│   ├── core/          # config, security, dependencies
│   ├── model/         # SQLAlchemy models
│   ├── repository/    # database queries layer
│   ├── service/       # business logic layer
│   ├── router/        # API endpoints
│   ├── schemas/       # Pydantic schemas
│   ├── db/            # database setup & session
│   └── utils/
│
├── migrations/        # Alembic migrations
├── logs/
├── Dockerfile
├── requirements.txt
└── docker-compose.yml
```

---

# Environment Variables

Create `.env` file:

```env
APP_NAME=Travel Project API

DATABASE_URL=postgresql+asyncpg://user:password@db:5432/db_name

POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=db_name
POSTGRES_HOST=db
POSTGRES_PORT=5432

JWT_SECRET=super_secret_key
JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

# Run Project

Build and start containers:

```bash
docker compose up --build -d
```

---

# Database Setup (IMPORTANT)

## Enter Backend Container

```bash
docker exec -it testapp sh
```

---

## Create Initial Migration

```bash
alembic revision --autogenerate -m "init_tables"
```

---

## Apply Migration

```bash
alembic upgrade head
```

---

# Alembic Commands

## Create New Migration

```bash
alembic revision --autogenerate -m "message"
```

Example:

```bash
alembic revision --autogenerate -m "add_places_table"
```

---

## Apply Migrations

```bash
alembic upgrade head
```

---

## Rollback Last Migration

```bash
alembic downgrade -1
```

---

## Show Current Revision

```bash
alembic current
```

---

# API Documentation

Swagger UI:

```bash
http://localhost:8000/docs
```

ReDoc:

```bash
http://localhost:8000/redoc
```

---

# Main Endpoints

## Authentication

| Method | Endpoint |
|---|---|
| POST | `/auth/register` |
| POST | `/auth/login` |
| POST | `/auth/refresh` |
| POST | `/auth/logout` |

---

## Projects

| Method | Endpoint |
|---|---|
| POST | `/projects` |
| GET | `/projects` |
| GET | `/projects/{project_id}` |
| PATCH | `/projects/{project_id}` |
| DELETE | `/projects/{project_id}` |

---

## Places

| Method | Endpoint |
|---|---|
| POST | `/projects/{project_id}/places` |
| GET | `/projects/{project_id}/places` |
| PATCH | `/projects/{project_id}/places/{place_id}` |
| DELETE | `/projects/{project_id}/places/{place_id}` |

---

# Notes

- Maximum 10 places per project
- Users can access only their own projects
- Logs are stored in `/logs`
- All database schema changes should go through Alembic migrations

---

# Author

**Nazar Koldun**
