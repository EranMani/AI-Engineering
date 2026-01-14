from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# the connection URL
DATABASE_URL = "sqlite:///api_database.db"

# the engine
engine = create_engine(DATABASE_URL, echo=True)

# the session factory
# it will create a new session for each request
SessionLocal = sessionmaker(autoflush=False, bind=engine)

# the base class. all models will inherit from it
class Base(DeclarativeBase):
    pass

# the dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()