# MongoDB Database Setup Guide

This project supports MongoDB running in a Docker container with a persistent volume for data storage.

## Quick Start

1. **Start MongoDB:**
   ```bash
   docker-compose up -d mongodb
   ```

2. **Verify it's running:**
   ```bash
   docker-compose logs mongodb
   ```

3. **Connect to the MongoDB shell:**
   ```bash
   docker-compose exec mongodb mongosh -u flask_user -p flask_password
   ```

## Configuration

### Default Settings

- **User:** `flask_user`
- **Password:** `flask_password`
- **Database:** `flask_db`
- **Port:** `27017`
- **Host:** `localhost`

### Custom Configuration

Create a `.env` file in the project root to customize settings:

```env
MONGO_USER=your_user
MONGO_PASSWORD=your_password
MONGO_DB_NAME=your_database
MONGO_PORT=27017
MONGO_URL=mongodb://your_user:your_password@localhost:27017
```

The `.env` file is already in `.gitignore` and won't be committed to version control.

## Using MongoHelper in Your Code

The `MongoHelper` class provides a simple interface for managing MongoDB connections:

```python
from infra.db.mongodb.helpers import MongoHelper
import os

# Set environment variable
os.environ["MONGO_URL"] = "mongodb://flask_user:flask_password@localhost:27017"

# Connect to MongoDB
await MongoHelper.connect()

# Get database
db = MongoHelper.get_db("flask_db")

# Get collection
users_collection = MongoHelper.get_collection("users")

# Use the collection
users_collection.insert_one({"name": "John Doe", "email": "john@example.com"})

# Disconnect when done
await MongoHelper.disconnect()
```

## Data Persistence

The MongoDB data is stored in a Docker volume named `mongodb_data`. This means:

✅ **Data persists** when you:
- Stop the container
- Restart the container
- Recreate the container
- Update the Docker image

❌ **Data is lost** only when you:
- Explicitly remove the volume (`docker volume rm python-flask-tdd_mongodb_data`)

## Available Commands

| Command | Description |
|---------|-------------|
| `docker-compose up -d mongodb` | Start MongoDB container |
| `docker-compose down` | Stop all containers (data preserved) |
| `docker-compose restart mongodb` | Restart MongoDB container |
| `docker-compose logs mongodb` | View MongoDB logs |
| `docker-compose exec mongodb mongosh -u flask_user -p flask_password` | Access MongoDB shell |

## Connection String

For connecting from your Flask application:

```
mongodb://flask_user:flask_password@localhost:27017
```

Or using environment variables:
```
mongodb://${MONGO_USER}:${MONGO_PASSWORD}@localhost:${MONGO_PORT}
```

With authentication database:
```
mongodb://${MONGO_USER}:${MONGO_PASSWORD}@localhost:${MONGO_PORT}/?authSource=admin
```

## Troubleshooting

### Container won't start
- Check if port 27017 is already in use: `lsof -i :27017`
- View logs: `docker-compose logs mongodb`
- Try removing and recreating: `docker-compose down && docker volume rm python-flask-tdd_mongodb_data && docker-compose up -d mongodb`

### Can't connect to database
- Verify container is running: `docker ps`
- Check connection string and credentials
- Ensure MongoDB is ready: `docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')"`

### Data not persisting
- Verify volume exists: `docker volume ls | grep mongodb_data`
- Check volume mount: `docker inspect flask-tdd-mongodb | grep -A 10 Mounts`

## Health Check

The container includes a health check that verifies MongoDB is ready to accept connections. You can check the health status:

```bash
docker ps
```

The STATUS column will show "healthy" when MongoDB is ready.

## Example: Account Repository with MongoDB

Here's an example of how to use MongoHelper in a repository:

```python
from infra.db.mongodb.helpers import MongoHelper
from typing import Dict, Any


class MongoAccountRepository:
    """Account repository using MongoDB."""

    @staticmethod
    async def add(account_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new account to the database.
        
        Args:
            account_data: Account information to store
            
        Returns:
            The created account with its ID
        """
        collection = MongoHelper.get_collection("accounts")
        result = collection.insert_one(account_data)
        
        # Return the account with its new ID
        account_data["_id"] = result.inserted_id
        return account_data

    @staticmethod
    async def find_by_email(email: str) -> Dict[str, Any]:
        """
        Find an account by email.
        
        Args:
            email: Email address to search for
            
        Returns:
            Account data if found, None otherwise
        """
        collection = MongoHelper.get_collection("accounts")
        return collection.find_one({"email": email})
```

## Running Both PostgreSQL and MongoDB

You can run both databases simultaneously:

```bash
docker-compose up -d
```

This will start both PostgreSQL and MongoDB containers.

