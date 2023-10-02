from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import yaml
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
env = os.path.join(basedir,'./.env.local')
if os.path.exists(env):
    load_dotenv(env)

def get_connection():
    return create_engine(url=os.environ.get('DB_URL'), pool_size=100, max_overflow=0)

def session_factory():
    Base.metadata.create_all(engine)
    return SessionFactory()

# Create a new session
engine         = get_connection()
SessionFactory = sessionmaker(bind=engine)
Base           = declarative_base()