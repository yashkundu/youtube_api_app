from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from config import config


url = URL.create(
    drivername='mysql+mysqlconnector',
    username=config['database']['username'],
    password=config['database']['password'],
    host=config['database']['host'],
    database=config['database']['database'],
    port=config['database']['port']
)

sqlEngine = create_engine(url=url)



if __name__=='__main__':
    print(url)