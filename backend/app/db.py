from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from psycopg import AsyncConnection

from app.config import settings


@asynccontextmanager
async def get_connection() -> AsyncIterator[AsyncConnection]:
    async with await AsyncConnection.connect(settings.database_url) as connection:
        yield connection

