import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Reads DATABASE_URL from Railway environment variables
# Format: postgresql://user:password@host:port/dbname
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./dev.db")

# SQLAlchemy needs this slight tweak if Railway gives a postgres:// URL
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency — used in routers to get a DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
