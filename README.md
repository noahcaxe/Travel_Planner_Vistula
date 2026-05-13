# Travel Planner

Full-stack travel planning application built with **FastAPI**, **React**, **PostgreSQL**, **SQLAlchemy Async ORM**, **JWT Authentication**, and **Docker**.

Users can create personal travel projects and organize places inside them. Each project is linked to a user, and places are connected to projects. Integrates OpenStreetMap API for location search.

🔗 **Live Demo:** [https://frontend-travel-planner.onrender.com](https://frontend-travel-planner.onrender.com)  
📖 **API Docs:** [https://travel-planner-vistula.onrender.com/docs](https://travel-planner-vistula.onrender.com/docs)

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
- Location search via OpenStreetMap (Nominatim API)

---

# Tech Stack

**Backend**
- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy Async ORM
- Alembic
- JWT Authentication
- Pydantic

**Frontend**
- React
- Vite
- Nginx

**Infrastructure**
- Docker & Docker Compose
- Render (cloud deployment)

---

# Project Structure

```bash
Travel_Planner_Vistula/
├── backend/
│   ├── app/
│   │   ├── core/          # config, security, dependencies
│   │   ├── model/         # SQLAlchemy models
│   │   ├── repository/    # database queries layer
│   │   ├── service/       # business logic layer
│   │   ├── router/        # API endpoints
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── db/            # database setup & session
│   │   └── clients/       # external API clients
│   ├── migrations/        # Alembic migrations
│   │   └── versions/
│   ├── logs/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   └── src/
│       ├── components/
│       └── pages/
│   ├── Dockerfile
│   └── nginx.conf
│
├── docker-compose.yml     # local development only
└── .env                   # local environment variables
```

---

# Local Development

## Environment Variables

Create `.env` file in the root:

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

## Run Project

Build and start containers:

```bash
docker compose up --build -d
```

## Database Setup

Enter backend container:

```bash
docker exec -it testapp sh
```

Create initial migration:

```bash
alembic revision --autogenerate -m "init_tables"
```

Apply migration:

```bash
alembic upgrade head
```

---

# Alembic Commands

| Command | Description |
|---|---|
| `alembic revision --autogenerate -m "message"` | Create new migration |
| `alembic upgrade head` | Apply all migrations |
| `alembic downgrade -1` | Rollback last migration |
| `alembic current` | Show current revision |

---

# Deployment (Render)

The project is deployed on [Render](https://render.com) as three separate services:

| Service | Type | Description |
|---|---|---|
| PostgreSQL | Database | Managed PostgreSQL instance |
| Backend | Web Service | FastAPI app via Docker |
| Frontend | Web Service | React + Nginx via Docker |

**Backend environment variables on Render:**

```env
APP_NAME=Travel Project API
DATABASE_URL=postgresql+asyncpg://user:password@host/dbname
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_DB=...
POSTGRES_HOST=...
POSTGRES_PORT=5432
JWT_SECRET=...
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

> ⚠️ Free tier PostgreSQL on Render expires after 30 days.  
> ⚠️ Free web services spin down after 15 minutes of inactivity (cold start ~1 min).  
> ⚠️ `docker-compose.yml` is for local development only — not used on Render.

---

# API Documentation

| Interface | URL |
|---|---|
| Swagger UI | `http://localhost:8000/docs` |
| ReDoc | `http://localhost:8000/redoc` |

---

# Main Endpoints

## Authentication

| Method | Endpoint |
|---|---|
| POST | `/auth/register` |
| POST | `/auth/login` |
| POST | `/auth/refresh` |
| POST | `/auth/logout` |

## Projects

| Method | Endpoint |
|---|---|
| POST | `/projects` |
| GET | `/projects` |
| GET | `/projects/{project_id}` |
| PATCH | `/projects/{project_id}` |
| DELETE | `/projects/{project_id}` |

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
