from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

host_server = 'localhost'
db_server_port = '5432'
database_name = 'darcom1'
db_username = 'postgres'
db_password = '123'
ssl_mode = 'prefer'
DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)

engine = create_engine(DATABASE_URL)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:
        db.close()

