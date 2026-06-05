# Python Flask TDD API

Python Flask TDD API is a clean-architecture API project built to practice and demonstrate test-driven development in Python. The current HTTP surface focuses on account signup, login, health checks, validation, password hashing, JWT authentication, and persistence adapters that can be evolved toward survey workflows.

## Goals

- Keep business rules isolated from Flask, databases, and external libraries.
- Use TDD as the default workflow: write focused tests, implement the behavior, then refactor.
- Provide clear request validation and predictable HTTP responses.
- Keep secrets out of source control. Runtime keys, database passwords, and tokens must come from environment variables.
- Make the project easy to run locally, test in CI, and package in a container.

## Project Structure

```text
data/            Use case implementations and repository protocols
domain/          Business models and use case contracts
infra/           Cryptography and database adapters
main/            Flask app factory, server startup, adapters, middleware
presentation/    Controllers, HTTP helpers, validation-facing protocols
tests/           Unit and integration tests
validation/      Validation rules and composites
utils/           Library adapters such as bcrypt and email validation
```

## Requirements

- Python 3.9 or newer
- Docker and Docker Compose
- `make` for the shortcut commands

## Local Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
```

Edit `.env` and replace every placeholder value before running the app or containers.

Start the API:

```bash
make start
```

The server runs on `http://localhost:5000` by default.

## Environment Variables

Do not commit real values. Use `.env` locally and your hosting provider's secret manager in deployed environments.

```text
PORT=5000
JWT_SECRET=<long-random-secret>
BCRYPT_SALT=12
MONGO_URL=<mongodb-connection-string>
MONGO_DB_NAME=flask_db
POSTGRES_USER=<postgres-user>
POSTGRES_PASSWORD=<postgres-password>
POSTGRES_DB=flask_db
POSTGRES_PORT=5432
MONGO_USER=<mongo-user>
MONGO_PASSWORD=<mongo-password>
MONGO_PORT=27017
```

If `JWT_SECRET` is not set during direct local Python execution, the app creates a temporary in-memory value for that process. For containers, CI, staging, and production, set `JWT_SECRET` explicitly.

## Unit Testing

Run unit tests with either Make or pytest:

```bash
make test-unit
```

Equivalent direct command:

```bash
python -m pytest tests/ -v --tb=short -m "not integration and not slow"
```

Other useful test commands:

```bash
make test
make test-coverage
make test-ci
```

Coverage output is written to `htmlcov/` when coverage reports are enabled.

## Integration Testing

Integration tests use real infrastructure, currently MongoDB. The Makefile target
starts an isolated temporary MongoDB container on port `27018`, runs the tests,
and removes the container when the run finishes:

```bash
make test-integration
```

If you run pytest directly instead of using Make, start MongoDB yourself and set
`MONGO_URL` first. Example:

```bash
docker-compose up -d mongodb
export MONGO_URL="mongodb://<mongo-user>:<mongo-password>@localhost:27017/?authSource=admin"
python -m pytest tests/ -v --tb=short -m "integration"
```

## Running Containers

The repository includes a `Dockerfile` for the API and `docker-compose.yml` for the API plus database services.

Build and run the full local stack:

```bash
cp .env.example .env
# Edit .env and replace the placeholder values.
docker-compose up --build
```

Run only the API image:

```bash
docker build -t python-flask-tdd-api .
docker run --rm --env-file .env -p 5000:5000 python-flask-tdd-api
```

Run only database services:

```bash
docker-compose up -d mongodb postgres
```

Stop containers:

```bash
docker-compose down
```

Remove containers and database volumes:

```bash
docker-compose down -v
```

## Deployment

1. Build the API image:

```bash
docker build -t python-flask-tdd-api .
```

2. Push it to your registry:

```bash
docker tag python-flask-tdd-api <registry>/<namespace>/python-flask-tdd-api:<version>
docker push <registry>/<namespace>/python-flask-tdd-api:<version>
```

3. Configure environment variables in the platform secret manager:

```text
JWT_SECRET
BCRYPT_SALT
MONGO_URL
MONGO_DB_NAME
PORT
```

4. Run the container with `python main/server.py` as the startup command, or use the image default command.

5. Verify the deployment:

```bash
curl https://<your-api-host>/health
```

## API Reference

Base URL for local development:

```text
http://localhost:5000
```

### Health Check

`GET /health`

```bash
curl -i http://localhost:5000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

### Signup

`POST /api/signup`

Creates an account and returns an access token.

```bash
curl -i -X POST http://localhost:5000/api/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test.user@example.com",
    "password": "StrongPassword123",
    "passwordConfirmation": "StrongPassword123"
  }'
```

Postman body:

```json
{
  "name": "Test User",
  "email": "test.user@example.com",
  "password": "StrongPassword123",
  "passwordConfirmation": "StrongPassword123"
}
```

Successful response shape:

```json
{
  "access_token": "<jwt-token>",
  "name": "Test User"
}
```

Validation errors return:

```json
{
  "error": "Missing param: email"
}
```

### Login

`POST /api/login`

Authenticates an existing account and returns an access token.

```bash
curl -i -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test.user@example.com",
    "password": "StrongPassword123"
  }'
```

Postman body:

```json
{
  "email": "test.user@example.com",
  "password": "StrongPassword123"
}
```

Successful response shape:

```json
{
  "access_token": "<jwt-token>",
  "name": "Test User"
}
```

Unauthorized response:

```json
{
  "error": "Unauthorized"
}
```

### Legacy Signup

`POST /signup`

This route is kept for compatibility. Prefer `/api/signup` for new clients.

```bash
curl -i -X POST http://localhost:5000/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "legacy.user@example.com",
    "password": "StrongPassword123",
    "passwordConfirmation": "StrongPassword123"
  }'
```

Successful legacy response shape:

```json
{
  "success": true,
  "data": {
    "access_token": "<jwt-token>",
    "name": "Test User"
  }
}
```

## Current API Notes

The active Flask app uses an in-memory account repository in `main/config/app.py`, so account data resets when the process restarts. MongoDB repository implementations and survey controllers exist in the codebase, but the survey routes are not currently registered in the Flask app.

## Quality Commands

```bash
make lint
make lint-all
make format
make format-check
make type-check
make security
```

## Development Workflow

1. Add or update tests first.
2. Run `make test-unit`.
3. Implement the smallest behavior that passes.
4. Run integration tests when database behavior changes.
5. Run `make test-ci` before opening a pull request.

## Security

- Never commit `.env` or real credentials.
- Rotate any secret that was ever shared in plain text.
- Use different secrets for local, staging, and production.
- Store production values in a secret manager, not in Docker images or Git history.
- Treat access tokens returned by the API as sensitive values.
