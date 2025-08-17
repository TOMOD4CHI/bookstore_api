import os
import dotenv
from sqlalchemy import create_engine, MetaData

dotenv.load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()
