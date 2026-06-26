"""MongoDB connection helper."""
import os
from typing import Any, Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError


def _is_test_environment() -> bool:
    environment = (
        os.getenv("ENV")
        or os.getenv("APP_ENV")
        or os.getenv("FLASK_ENV")
        or os.getenv("PYTHON_ENV")
        or ""
    ).lower()
    return environment in {"test", "testing"}


class MongoHelper:
    """Helper class for managing MongoDB connections."""

    _client: Optional[MongoClient] = None
    _db: Optional[Database] = None

    @classmethod
    async def connect(cls, uri: Optional[str] = None) -> None:
        """
        Connect to MongoDB.

        Args:
            uri: MongoDB connection URI. If not provided, uses MONGO_URL env variable.
        """
        connection_uri = uri or os.getenv("MONGO_URL")
        if not connection_uri:
            raise ValueError("MongoDB URI must be provided or set in MONGO_URL environment variable")

        cls._client = MongoClient(connection_uri, serverSelectionTimeoutMS=500)
        try:
            cls._client.admin.command("ping")
        except ServerSelectionTimeoutError:
            if not _is_test_environment():
                cls._client.close()
                cls._client = None
                raise
            import mongomock

            cls._client = mongomock.MongoClient()

    @classmethod
    async def disconnect(cls) -> None:
        """Disconnect from MongoDB."""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None

    @classmethod
    def get_db(cls, db_name: Optional[str] = None) -> Database:
        """
        Get database instance.

        Args:
            db_name: Database name. If not provided, uses MONGO_DB_NAME env variable.

        Returns:
            Database instance.
        """
        if not cls._client:
            raise RuntimeError("MongoDB client is not connected. Call connect() first.")

        database_name = db_name or os.getenv("MONGO_DB_NAME", "flask_db")
        return cls._client[database_name]

    @classmethod
    def get_collection(cls, collection_name: str, db_name: Optional[str] = None):
        """
        Get collection instance.

        Args:
            collection_name: Name of the collection.
            db_name: Database name. If not provided, uses MONGO_DB_NAME env variable.

        Returns:
            Collection instance.
        """
        db = cls.get_db(db_name)
        return db[collection_name]

    @staticmethod
    def map(data: dict[str, Any]) -> dict[str, Any]:
        if not data:
            return data
        mapped = dict(data)
        object_id = mapped.pop("_id", None)
        if object_id is not None:
            mapped["id"] = str(object_id)
        return mapped

    @classmethod
    def map_collection(cls, collection: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [cls.map(item) for item in collection]
