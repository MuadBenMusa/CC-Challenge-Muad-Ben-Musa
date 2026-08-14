from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from psycopg import AsyncConnection
from psycopg.rows import dict_row

from .config import settings


@asynccontextmanager
async def get_connection() -> AsyncIterator[AsyncConnection]:
    async with await AsyncConnection.connect(
        settings.database_url,
        row_factory=dict_row,
    ) as connection:
        yield connection
