from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://neondb_owner:npg_BV5rHioZIuP6@ep-wandering-flower-a2ai13cs-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require" 

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()