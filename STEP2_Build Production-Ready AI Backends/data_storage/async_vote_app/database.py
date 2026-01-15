from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# the async url
DATABASE_URL = "postgresql+asyncpg://postgres:Erdisha_24800@localhost/fastapidb"

# the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# the async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

# the async dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session