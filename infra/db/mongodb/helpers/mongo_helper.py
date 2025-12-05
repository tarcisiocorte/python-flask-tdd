"""MongoDB connection helper."""
import os
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database


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

        cls._client = MongoClient(connection_uri)

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

