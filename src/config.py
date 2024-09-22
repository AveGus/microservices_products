from dotenv import load_dotenv
import os


load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

DB_HOST_TEST = os.getenv("DB_HOST_TEST", default="0.0.0.0")
DB_USER_TEST = os.getenv("DB_USER_TEST", default="test_db")
DB_PASS_TEST = os.getenv("DB_PASS_TEST", default="test_db")
DB_NAME_TEST = os.getenv("DB_NAME_TEST", default="test_db")
DB_PORT_TEST = os.getenv("DB_PORT_TEST", default="5432")
