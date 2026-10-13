# Job Application Tracker

A REST API for keeping track of the jobs you've applied for. Register an account, log in, and manage your own list of applications, from the day you apply through to an offer or a rejection.

Built with **FastAPI**, **SQLAlchemy** and **SQLite**, with JWT-based authentication.

## Features

- User registration and login (passwords hashed with bcrypt)
- JWT bearer-token authentication (tokens expire after 30 minutes)
- Full CRUD for job applications
- Per-user data isolation: you can only see and change your own applications
- Application status tracking: `Applied`, `Online Assessment`, `Interviewing`, `Offer`, `Rejected`
- Automatic interactive API docs (Swagger UI)
- Pytest suite with an isolated test database

## Tech Stack

| Area | Tool |
| --- | --- |
| Web framework | FastAPI |
| Server | Uvicorn |
| ORM | SQLAlchemy 2.x |
| Database | SQLite |
| Validation | Pydantic v2 |
| Auth | PyJWT + bcrypt |
| Testing | pytest + FastAPI `TestClient` |

## Project Structure

```
.
├── main.py            # FastAPI app, auth logic and all endpoints
├── models.py          # SQLAlchemy models (User, Application)
├── schemas.py         # Pydantic request/response schemas
├── enums.py           # StatusEnum for application status
├── DataBase.py        # Engine, session factory and Base
├── requirements.txt
└── tests/
    ├── conftest.py    # Fixtures: test DB, client, users, applications
    ├── test_auth.py
    ├── test_applications.py
    └── DataBase_test.py
```

## Getting Started

### Prerequisites

- Python 3.10 or newer

### Installation

```bash
git clone <your-repo-url>
cd Job-Tracking-Application

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### Configuration

The JWT signing key is read from the `JWT_SECRET_KEY` environment variable, and the app will not start without it. For local development, put it in a `.env` file in the project root (this file is git-ignored and must never be committed):

```bash
cp .env.example .env
```

Then edit `.env` and set a real value. Generate one with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Run the server

```bash
uvicorn main:app --reload
```

The API is now available at <http://127.0.0.1:8000>. The SQLite database (`Applications.db`) and its tables are created automatically on first start.

Interactive docs:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## API Reference

### Authentication

| Method | Endpoint | Description | Auth |
| --- | --- | --- | --- |
| `POST` | `/auth/register` | Create a new account | No |
| `POST` | `/auth/login` | Log in and receive a JWT | No |

**Register** (`201 Created`)

```json
{
  "username": "jane",
  "email": "jane@example.com",
  "password": "Password123!"
}
```

Returns `409 Conflict` if the email or username is already in use.

**Login** takes **form-encoded** data (OAuth2 password flow), and the `username` field holds the account's **email**:

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -d "username=jane@example.com&password=Password123!"
```

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

Send the token on every protected request:

```
Authorization: Bearer <jwt>
```

### Applications

All application endpoints require authentication.

| Method | Endpoint | Description | Success |
| --- | --- | --- | --- |
| `GET` | `/applications` | List your applications | `200` |
| `POST` | `/applications` | Create an application | `201` |
| `GET` | `/applications/{application_id}` | Get one application | `200` |
| `PUT` | `/applications/{application_id}` | Update an application | `200` |
| `DELETE` | `/applications/{application_id}` | Delete an application | `200` |

**Application fields**

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `company_name` | string | Yes | |
| `job_title` | string | Yes | |
| `status` | enum | Yes | `Applied`, `Online Assessment`, `Interviewing`, `Offer`, `Rejected` |
| `location` | string | No | |
| `salary` | string | No | Free text, e.g. `"£45,000"` |
| `date_applied` | date | No | ISO format `YYYY-MM-DD` |
| `notes` | string | No | |
| `job_url` | string | No | |

**Example: create an application**

```bash
curl -X POST http://127.0.0.1:8000/applications \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{
        "company_name": "Acme Ltd",
        "job_title": "Backend Developer",
        "location": "London",
        "salary": "£45,000",
        "status": "Applied",
        "date_applied": "2026-09-25",
        "notes": "Referred by a friend",
        "job_url": "https://example.com/jobs/123"
      }'
```

`PUT` accepts a partial body: only the fields you include are changed.

### Status codes

| Code | Meaning |
| --- | --- |
| `200` | OK |
| `201` | Created |
| `401` | Missing, expired or invalid token, or bad login credentials |
| `404` | Application not found (or it belongs to another user) |
| `409` | Email or username already in use |
| `422` | Request body failed validation |

## Running the Tests

```bash
pytest
```

The tests use a separate SQLite database (`test.db`) and override the app's database dependency, so your real `Applications.db` is never touched. Tables are created and dropped around each test for a clean slate.

## Roadmap

- Move from SQLite to PostgreSQL
- Move secrets and database configuration into environment/config files
- Filtering and sorting of applications by status or date

## License

No license has been specified yet.
