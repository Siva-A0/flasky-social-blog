# Flasky — Social Blogging Platform

A full-featured social blogging web application built with Flask, following production-grade architecture patterns: user authentication, role-based permissions, a social follow system, a RESTful API, automated testing, and live deployment.

This project was built while working through *Flask Web Development* by Miguel Grinberg, implementing every feature end-to-end — updating deprecated library methods (e.g. `itsdangerous` token serialization) to current, supported APIs, and rebuilding the Docker setup on lightweight Alpine base images with a separate MySQL container rather than the book's original configuration.

**Live demo:** [add your Railway/Render URL here]

## Features

- **User authentication** — registration, login, email confirmation, password reset
- **Roles & permissions** — granular access control (User, Moderator, Administrator)
- **User profiles** — avatars via Gravatar, editable bios, member-since/last-seen tracking
- **Social graph** — follow/unfollow system using a self-referential many-to-many relationship
- **Blog posts** — Markdown support with sanitized HTML rendering
- **Comments** — threaded comments with moderation tools for admins
- **REST API** — JSON endpoints for posts and users, with pagination and token-based authentication
- **Automated tests** — unit tests covering models, API endpoints, and core app behavior
- **Production deployment** — configured for containerized and platform-based deployment

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask, Flask-SQLAlchemy, Flask-Login, Flask-Mail |
| Database | SQLite (dev), PostgreSQL-ready (prod) |
| Frontend | Jinja2, Bootstrap, Chart.js |
| API | Flask REST endpoints, JSON serialization |
| Testing | unittest, Flask test client, coverage.py |
| Deployment | Docker (Alpine-based image), MySQL container, Railway/Render |

## Project Structure

```
flasky-social-blog/
├── app/
│   ├── api/            # REST API blueprint (auth, posts, users, errors)
│   ├── auth/            # Authentication blueprint
│   ├── main/            # Core blog views
│   ├── static/
│   ├── templates/
│   └── models.py        # User, Post, Comment, Follow, Role models
├── migrations/           # Database migration history
├── tests/                 # Unit test suite
├── requirements/         # Split requirements (common/dev/prod/docker)
├── config.py
├── flasky.py
├── Dockerfile
└── docker-compose.yml
```

## Running Locally

```bash
git clone https://github.com/Siva-A0/flasky-social-blog.git
cd flasky-social-blog

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements/dev.txt

# Set required environment variables (see .env.example)
export FLASK_APP=flasky.py
flask db upgrade
flask run
```

Visit `http://localhost:5000`.

## Environment Variables

See `.env.example` for all required configuration (secret key, mail credentials, database URL).

## Testing

```bash
flask test
```

Run with coverage:

```bash
flask test --coverage
```

## What I'd Build Next

- Migrate API authentication from token-only to JWT
- Add Redis-backed caching for the post feed
- CI/CD pipeline via GitHub Actions for automated test runs on push