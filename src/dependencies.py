import os
import databases
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
DATABASE_URL = os.environ.get("DATABASE_URL")


db = databases.Database(DATABASE_URL)
