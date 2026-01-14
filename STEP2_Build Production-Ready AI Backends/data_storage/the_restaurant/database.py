from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# the connection URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Erdisha_24800@localhost/fastapidb"

# the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

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