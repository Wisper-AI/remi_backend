from dataclasses import dataclass

import asyncpg
import structlog

from lib.core.redis_connector import Redis


@dataclass
class Context:
    """
    Context class represents essential connectors for each request.

    Attributes:
        logger: structlog logger
        request_id: string request ID
        redis: Redis connector
        postgres: Postgres connector
        pg_connection: Postgres connection instance
    """

    logger: structlog.stdlib.AsyncBoundLogger
    request_id: str
    redis: Redis
    postgres: asyncpg.pool.Pool
    pg_connection: asyncpg.connection.Connection | None = None
