from typing import Optional, TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine.url import URL

from .sqlalchemy_base import db

if TYPE_CHECKING:
    from config import Config


class Database:
    def __init__(self, config: "Config"):
        self.config = config
        self._engine: Optional[AsyncEngine] = None
        self._db: Optional[declarative_base] = None
        self.session: Optional[AsyncSession] = None

    async def connect(self, *_: list, **__: dict) -> None:
        self._db = db
        self._engine = create_async_engine(
            URL(
                drivername="postgresql+asyncpg",
                host=self.config.database.host,
                database=self.config.database.database,
                username=self.config.database.user,
                password=self.config.database.password,
                port=self.config.database.port,
                ),
            echo=True,
            future=True
        )
        self.session = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)

    async def disconnect(self, *_: list, **__: dict) -> None:
        if self._engine:
            await self._engine.dispose()
