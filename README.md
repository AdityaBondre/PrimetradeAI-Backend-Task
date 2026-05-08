# TaskFlow – Scalable Task Management System

A production-ready full-stack application built for the Primetrade.ai Backend Developer Intern assignment.

## Features
- **Authentication**: Secure JWT (Access + Refresh tokens) with password hashing (bcrypt).
- **RBAC**: Role-Based Access Control (Admin vs. User).
- **Task Management**: Full CRUD for tasks with status and priority tracking.
- **Admin Panel**: Comprehensive user management for administrative users.
- **API Documentation**: Built-in interactive Swagger UI.
- **Scalable Architecture**: Modular service-oriented backend and component-based frontend.

## Tech Stack
- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.0 (Async), PostgreSQL, Alembic, Pydantic v2.
- **Frontend**: React.js, TypeScript, Vite, Axios, Lucide Icons.
- **DevOps**: Docker, Docker Compose.

## Getting Started

### Prerequisites
- Docker & Docker Compose

### One-Click Setup
Run the following command in the project root:
```bash
docker-compose up --build
```

The system is available at:
- **Live Frontend**: [https://primetrade-ai-backend-task-lq9o.onrender.com](https://primetrade-ai-backend-task-lq9o.onrender.com)
- **Live Backend API**: [https://primetradeai-backend-task.onrender.com](https://primetradeai-backend-task.onrender.com)
- **Interactive Swagger Docs**: [https://primetradeai-backend-task.onrender.com/api/v1/docs](https://primetradeai-backend-task.onrender.com/api/v1/docs)

### Local Development (without Docker)
1. **Backend**:
   - `cd backend`
   - `python -m venv venv`
   - `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
   - `pip install -r requirements.txt`
   - Configure `.env`
   - `alembic upgrade head`
   - `uvicorn app.main:app --reload`
2. **Frontend**:
   - `cd frontend`
   - `npm install`
   - `npm run dev`

## API Overview
| Method | Path | Auth | Role |
|---|---|---|---|
| POST | `/api/v1/auth/register` | No | - |
| POST | `/api/v1/auth/login` | No | - |
| GET | `/api/v1/auth/me` | Yes | Any |
| GET | `/api/v1/tasks/` | Yes | Any |
| POST | `/api/v1/tasks/` | Yes | Any |
| GET | `/api/v1/admin/users` | Yes | Admin |

## Security & Best Practices
- **Password Hashing**: Uses `passlib` with `bcrypt` (12 rounds).
- **Token Security**: Refresh tokens are hashed before DB storage; raw tokens never persisted.
- **Input Validation**: Strictly enforced via Pydantic v2 schemas.
- **Ownership**: Middlewares ensure users can only modify their own data (unless Admin).
- **CORS**: Restricted to authorized origins.
- **Async I/O**: Backend uses non-blocking async database drivers for high concurrency.
