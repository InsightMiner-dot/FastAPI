"""DB connection system"""

# Create a database
from sqlalchemy import create_engine
# sessionmaker is a factory (a blueprint) that creates properly configured database sessions whenever needed.
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

# use echo Shows SQL queries in terminal.
engine = create_engine(SQLALCHEMY_DATABASE_URL,echo=True, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()