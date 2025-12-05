# MongoDB Infrastructure

This module provides MongoDB infrastructure support for the Flask TDD project.

## Structure

```
infra/db/mongodb/
├── helpers/
│   ├── __init__.py
│   └── mongo_helper.py    # MongoDB connection helper
└── README.md
```

## MongoHelper

The `MongoHelper` class is a singleton-style helper that manages MongoDB connections throughout your application.

### Features

- **Connection Management**: Connect and disconnect from MongoDB
- **Database Access**: Get database instances by name
- **Collection Access**: Get collection instances directly
- **Environment Configuration**: Supports configuration via environment variables

### Usage

```python
from infra.db.mongodb.helpers import MongoHelper
import os

# Configure MongoDB URL
os.environ["MONGO_URL"] = "mongodb://flask_user:flask_password@localhost:27017"
os.environ["MONGO_DB_NAME"] = "flask_db"

# Connect to MongoDB
await MongoHelper.connect()

# Get database
db = MongoHelper.get_db()  # Uses MONGO_DB_NAME env var
# or
db = MongoHelper.get_db("my_custom_db")  # Use specific database

# Get collection
users = MongoHelper.get_collection("users")  # From default database
# or
users = MongoHelper.get_collection("users", "my_custom_db")  # From specific database

# Use the collection
user_data = {"name": "John Doe", "email": "john@example.com"}
result = users.insert_one(user_data)

# Disconnect when done
await MongoHelper.disconnect()
```

### Environment Variables

- `MONGO_URL`: MongoDB connection URI (required)
- `MONGO_DB_NAME`: Default database name (optional, defaults to "flask_db")

### Methods

#### `connect(uri: Optional[str] = None) -> None`

Connect to MongoDB.

**Parameters:**
- `uri` (optional): MongoDB connection URI. If not provided, uses `MONGO_URL` environment variable.

**Raises:**
- `ValueError`: If no URI is provided and `MONGO_URL` is not set.

#### `disconnect() -> None`

Disconnect from MongoDB and clean up resources.

#### `get_db(db_name: Optional[str] = None) -> Database`

Get a database instance.

**Parameters:**
- `db_name` (optional): Database name. If not provided, uses `MONGO_DB_NAME` environment variable (default: "flask_db").

**Returns:**
- `Database`: PyMongo database instance.

**Raises:**
- `RuntimeError`: If MongoDB client is not connected.

#### `get_collection(collection_name: str, db_name: Optional[str] = None) -> Collection`

Get a collection instance.

**Parameters:**
- `collection_name`: Name of the collection.
- `db_name` (optional): Database name. If not provided, uses `MONGO_DB_NAME` environment variable.

**Returns:**
- `Collection`: PyMongo collection instance.

**Raises:**
- `RuntimeError`: If MongoDB client is not connected.

## Testing

Tests are located in `tests/infra/db/mongodb/helpers/test_mongo_helper.py`.

Run tests with:

```bash
pytest tests/infra/db/mongodb/helpers/test_mongo_helper.py -v
```

## Dependencies

- `pymongo>=4.0.0`: MongoDB driver for Python
- `pytest-asyncio>=0.21.0`: For testing async methods

## Integration with Docker

The project includes MongoDB support in `docker-compose.yml`. To start MongoDB:

```bash
docker-compose up -d mongodb
```

See `MONGODB.md` in the project root for more details on MongoDB setup and configuration.

