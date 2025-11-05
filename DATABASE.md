# PostgreSQL Database Setup Guide

This project uses PostgreSQL running in a Docker container with a persistent volume for data storage.

## Quick Start

1. **Start PostgreSQL:**
   ```bash
   make db-up
   ```

2. **Verify it's running:**
   ```bash
   make db-logs
   ```

3. **Connect to the database:**
   ```bash
   make db-shell
   ```

## Configuration

### Default Settings

- **User:** `flask_user`
- **Password:** `flask_password`
- **Database:** `flask_db`
- **Port:** `5432`
- **Host:** `localhost`

### Custom Configuration

Create a `.env` file in the project root to customize settings:

```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
POSTGRES_PORT=5432
POSTGRES_HOST=localhost
```

The `.env` file is already in `.gitignore` and won't be committed to version control.

## Data Persistence

The PostgreSQL data is stored in a Docker volume named `postgres_data`. This means:

✅ **Data persists** when you:
- Stop the container (`make db-down`)
- Restart the container (`make db-restart`)
- Recreate the container
- Update the Docker image

❌ **Data is lost** only when you:
- Explicitly remove the volume (`make db-clean`)

## Available Commands

| Command | Description |
|---------|-------------|
| `make db-up` | Start PostgreSQL container |
| `make db-down` | Stop PostgreSQL container (data preserved) |
| `make db-restart` | Restart PostgreSQL container |
| `make db-logs` | View PostgreSQL logs |
| `make db-shell` | Access PostgreSQL interactive shell |
| `make db-clean` | Remove container and volume (⚠️ deletes data) |

## Volume Management

### View Volumes
```bash
docker volume ls
```

### Inspect Volume
```bash
docker volume inspect python-flask-tdd_postgres_data
```

### Backup Volume
```bash
# Create backup
docker run --rm \
  -v python-flask-tdd_postgres_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/postgres_backup.tar.gz -C /data .
```

### Restore Volume
```bash
# Restore from backup
docker run --rm \
  -v python-flask-tdd_postgres_data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/postgres_backup.tar.gz -C /data
```

## Connection String

For connecting from your Flask application:

```
postgresql://flask_user:flask_password@localhost:5432/flask_db
```

Or using environment variables:
```
postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
```

## Troubleshooting

### Container won't start
- Check if port 5432 is already in use: `lsof -i :5432`
- View logs: `make db-logs`
- Try removing and recreating: `make db-clean && make db-up`

### Can't connect to database
- Verify container is running: `docker ps`
- Check connection string and credentials
- Ensure PostgreSQL is ready: `docker-compose exec postgres pg_isready -U flask_user`

### Data not persisting
- Verify volume exists: `docker volume ls | grep postgres_data`
- Check volume mount: `docker inspect flask-tdd-postgres | grep -A 10 Mounts`

## Health Check

The container includes a health check that verifies PostgreSQL is ready to accept connections. You can check the health status:

```bash
docker ps
```

The STATUS column will show "healthy" when PostgreSQL is ready.

