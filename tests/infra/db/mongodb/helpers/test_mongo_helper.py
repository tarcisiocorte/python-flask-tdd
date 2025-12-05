"""Tests for MongoHelper."""
import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from infra.db.mongodb.helpers import MongoHelper


class TestMongoHelper:
    """Test suite for MongoHelper."""

    def setup_method(self):
        """Reset MongoHelper state before each test."""
        MongoHelper._client = None
        MongoHelper._db = None

    def teardown_method(self):
        """Clean up after each test."""
        MongoHelper._client = None
        MongoHelper._db = None

    @pytest.mark.asyncio
    async def test_connect_with_uri(self):
        """Test connecting to MongoDB with provided URI."""
        mock_client = Mock()
        uri = "mongodb://localhost:27017"

        with patch("infra.db.mongodb.helpers.mongo_helper.MongoClient", return_value=mock_client) as mock_mongo_client:
            await MongoHelper.connect(uri)

            mock_mongo_client.assert_called_once_with(uri)
            assert MongoHelper._client == mock_client

    @pytest.mark.asyncio
    async def test_connect_with_env_variable(self):
        """Test connecting to MongoDB using MONGO_URL environment variable."""
        mock_client = Mock()
        uri = "mongodb://localhost:27017"

        with patch.dict(os.environ, {"MONGO_URL": uri}):
            with patch("infra.db.mongodb.helpers.mongo_helper.MongoClient", return_value=mock_client) as mock_mongo_client:
                await MongoHelper.connect()

                mock_mongo_client.assert_called_once_with(uri)
                assert MongoHelper._client == mock_client

    @pytest.mark.asyncio
    async def test_connect_without_uri_raises_error(self):
        """Test that connecting without URI or env variable raises ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                await MongoHelper.connect()

            assert "MongoDB URI must be provided" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_disconnect(self):
        """Test disconnecting from MongoDB."""
        mock_client = Mock()
        MongoHelper._client = mock_client

        await MongoHelper.disconnect()

        mock_client.close.assert_called_once()
        assert MongoHelper._client is None
        assert MongoHelper._db is None

    @pytest.mark.asyncio
    async def test_disconnect_without_client(self):
        """Test disconnecting when no client is connected."""
        MongoHelper._client = None

        # Should not raise an error
        await MongoHelper.disconnect()

        assert MongoHelper._client is None

    def test_get_db_with_db_name(self):
        """Test getting database with provided name."""
        mock_client = MagicMock()
        mock_db = Mock()
        mock_client.__getitem__.return_value = mock_db
        MongoHelper._client = mock_client

        db = MongoHelper.get_db("test_db")

        mock_client.__getitem__.assert_called_once_with("test_db")
        assert db == mock_db

    def test_get_db_with_env_variable(self):
        """Test getting database using MONGO_DB_NAME environment variable."""
        mock_client = MagicMock()
        mock_db = Mock()
        mock_client.__getitem__.return_value = mock_db
        MongoHelper._client = mock_client

        with patch.dict(os.environ, {"MONGO_DB_NAME": "env_db"}):
            db = MongoHelper.get_db()

            mock_client.__getitem__.assert_called_once_with("env_db")
            assert db == mock_db

    def test_get_db_with_default_name(self):
        """Test getting database with default name when no env variable is set."""
        mock_client = MagicMock()
        mock_db = Mock()
        mock_client.__getitem__.return_value = mock_db
        MongoHelper._client = mock_client

        with patch.dict(os.environ, {}, clear=True):
            db = MongoHelper.get_db()

            mock_client.__getitem__.assert_called_once_with("flask_db")
            assert db == mock_db

    def test_get_db_without_connection_raises_error(self):
        """Test that getting database without connection raises RuntimeError."""
        MongoHelper._client = None

        with pytest.raises(RuntimeError) as exc_info:
            MongoHelper.get_db()

        assert "MongoDB client is not connected" in str(exc_info.value)

    def test_get_collection(self):
        """Test getting collection from database."""
        mock_client = MagicMock()
        mock_db = MagicMock()
        mock_collection = Mock()
        mock_client.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_collection
        MongoHelper._client = mock_client

        collection = MongoHelper.get_collection("users")

        mock_db.__getitem__.assert_called_once_with("users")
        assert collection == mock_collection

    def test_get_collection_with_db_name(self):
        """Test getting collection from specific database."""
        mock_client = MagicMock()
        mock_db = MagicMock()
        mock_collection = Mock()
        mock_client.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_collection
        MongoHelper._client = mock_client

        collection = MongoHelper.get_collection("users", "custom_db")

        mock_client.__getitem__.assert_called_once_with("custom_db")
        mock_db.__getitem__.assert_called_once_with("users")
        assert collection == mock_collection

    def test_get_collection_without_connection_raises_error(self):
        """Test that getting collection without connection raises RuntimeError."""
        MongoHelper._client = None

        with pytest.raises(RuntimeError) as exc_info:
            MongoHelper.get_collection("users")

        assert "MongoDB client is not connected" in str(exc_info.value)

