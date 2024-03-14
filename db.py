from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from config import config
from contextlib import contextmanager



url = URL.create(
    drivername='mysql+mysqlconnector',
    username=config['database']['username'],
    password=config['database']['password'],
    host=config['database']['host'],
    database=config['database']['database'],
    port=config['database']['port']
)

engine = create_engine(url=url)
Session = sessionmaker(bind=engine)


# creating a context manager, which will create a new session for each incomming request, these new sessions will use connections from the connection pool maintained by the sessionmaker, hence it will be efficient and feasable to make new session for every incoming request
@contextmanager
def sessionManager():
    session = Session()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


@contextmanager
def connectionManager():
    conn = engine.connect()
    yield conn
    conn.close()


if __name__=='__main__':
    print(url)