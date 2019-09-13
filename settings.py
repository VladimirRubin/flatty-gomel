import os
from dotenv import load_dotenv

load_dotenv()


ONLINER_URL = os.getenv("ONLINER_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
