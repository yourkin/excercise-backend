import asyncpg
import pytest

from ex_back.config import get_settings

DATABASE_URL = get_settings().test_database_url

# asyncpg requires the postgresql:// scheme unlike SQLAlchemy for async operations
if DATABASE_URL.startswith("postgresql+asyncpg://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://", 1)
else:
    pytest.fail("DATABASE_URL is not an async PostgreSQL URL")


@pytest.mark.asyncio
async def test_postgres_connection():
    connection = None
    try:
        connection = await asyncpg.connect(DATABASE_URL)

        # execute a statement
        result = await connection.fetchval("SELECT 1")

        assert result == 1
        print("PostgreSQL connection is successful.")
    except (Exception, asyncpg.Exceptions.PostgresError) as error:
        print(f"Error: {error}")
        pytest.fail("PostgreSQL connection test failed!")
    finally:
        if connection is not None:
            await connection.close()
            print("PostgreSQL connection is closed.")
