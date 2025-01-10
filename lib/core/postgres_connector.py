import os

import asyncpg

# READ postgres url from env
POSTGRES_URL = os.getenv(
    key="POSTGRES_URL",
    default=None,
)


async def get_connection_pool() -> asyncpg.pool.Pool:
    """
    Connect to postgres and return connection pool

    Returns:
        asyncpg.pool.Pool: Connection pool

    Raises:
        ValueError: If POSTGRES_URL is invalid
    """
    if not POSTGRES_URL:
        raise ValueError("Invalid POSTGRES_URL")

    pool = await asyncpg.create_pool(dsn=POSTGRES_URL)

    if not pool:
        raise ValueError("Failed to create connection pool")

    return pool
