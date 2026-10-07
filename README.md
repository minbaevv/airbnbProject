# airbnbProject

An educational property-rental backend built with **Django REST Framework**.

The project includes property listings, booking and review workflows,
JWT authentication, and host/guest-related permissions.

**This is an independent learning project, not an official Airbnb product.
It is not affiliated with or endorsed by Airbnb.**

## Features

- User registration, login and logout
- JWT authentication with SimpleJWT
- User profile endpoints
- City and property-rule endpoints
- Property listings and details
- Filtering, search, ordering and pagination
- Host-related property management
- Booking and review operations
- User-scoped booking and review querysets

Features are described from source code.
Their presence does not mean that every scenario has been tested.

## Technology Stack

| Area | Technologies |
| :--- | :--- |
| Language | Python |
| Framework | Django |
| API | Django REST Framework |
| Authentication | SimpleJWT |
| Filtering | django-filter |
| Deployment configuration | Docker, Docker Compose, nginx |

A SQLite database file is included in the repository.
Use a fresh development database and sanitized sample data.

## Project Structure

```text
airbnbProject/
└── mysite/
    ├── manage.py
    ├── AirBNB_app/          # Application and API logic
    ├── nginx/               # Reverse proxy configuration
    ├── Dockerfile
    ├── docker-compose.yml
    └── req.txt              # Python dependencies
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/minbaevv/airbnbProject.git
cd airbnbProject
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

Or on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
cd mysite
python -m pip install -r req.txt
```

### 4. Configure the environment

Review the Django settings and configure the required local
environment variables before startup.

Use a newly generated local secret key. Do not publish working
credentials, private uploads or real user data.

### 5. Apply migrations and start the server

```bash
python manage.py migrate
python manage.py runserver
```

Default development address:

```text
http://127.0.0.1:8000/
```

Check the project's URL configuration for the available API paths.
An API-only project does not require a frontend homepage.

These instructions are based on the repository structure and still
require verification in a clean environment.

## Permissions and Booking Validation

Before deployment, verify that:

- Anonymous users cannot perform protected actions
- Hosts can modify only properties they are authorized to manage
- Users cannot access or modify another user's private bookings
- Review creation and modification follow the intended ownership rules
- Booking dates are valid and availability rules are enforced
- Concurrent requests cannot create conflicting reservations
- Filtering and search use the correct model fields and relationships

## Development Priorities

- Document environment variables in a safe `.env.example`
- Remove private configuration and real database contents from Git
- Add or extend authentication and object-ownership tests
- Test booking availability and concurrent reservation behavior
- Verify filtering, search, ordering and pagination
- Document request and response examples
- Verify Docker startup in a clean environment
- Configure continuous integration

## Project Status

This repository demonstrates backend development practice.
It is not presented as a production-ready rental platform.

Runtime behavior, booking rules, permissions and deployment
configuration require further validation.

## Attribution and License

Retain attribution for any course, tutorial or external code used.
Document your own additions and changes.

Check rights to code, images and other assets before reuse.
No affiliation with the Airbnb brand is claimed.

## Author

**Kubanychbek Duishekeev**

[GitHub](https://github.com/minbaevv) ·
[LinkedIn](https://www.linkedin.com/in/kubanychbek-duishekeev-7b9872427/) ·
[Telegram](https://t.me/d_kubanychbek) ·
[Gmail](mailto:duishekeevkubanychbek@gmail.com)
