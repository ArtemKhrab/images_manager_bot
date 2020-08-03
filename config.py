from dotenv import *
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(verbose=True)
token = os.getenv('token')
api_access_key = os.getenv('access_api_key')
host = os.getenv("db_host")
user = os.getenv("db_user")
password = os.getenv("db_password")
port = os.getenv("db_port")
DB = os.getenv("db_name")


engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{DB}?host={host}?port={port}', pool_recycle=1800)
Session = sessionmaker(bind=engine)
session = Session()
