import asyncpg
from src.config.settings import get_settings
from typing import AsyncGenerator

class Database:
    def __init__(self):
        self.pool: asyncpg.Pool | None = None

    async def connect(self):
        settings = get_settings()
        self.pool = await asyncpg.create_pool(
            dsn=settings.DATABASE_URL,
            min_size=5,
            max_size=20
        )
        print("✅ Database connection pool created")

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            print("🔌 Database pool closed")

db = Database()

async def get_db() -> AsyncGenerator[asyncpg.Pool, None]:
    if db.pool:
        yield db.pool