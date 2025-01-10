from dataclasses import dataclass

import asyncpg
import structlog

from lib.core.redis_connector import Redis


@dataclass
class Context:
    """
    Context class represents essential connectors for each request.
    :param logger: structlog logger
    :param request_id: string request ID
    :param redis: Redis connector
    :param postgres: Postgres connector
    :param pg_connection: Postgres connection instance
    """

    logger: structlog.stdlib.AsyncBoundLogger
    request_id: str
    redis: Redis
    postgres: asyncpg.pool.Pool
    pg_connection: asyncpg.connection.Connection = None
