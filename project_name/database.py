import databases
import sqlalchemy
from sqlalchemy.engine.url import make_url
from sqlalchemy_utils import database_exists, create_database

from project_name.config import config
from project_name.database_schemas.admin_user import create_admin_user_table


metadata = sqlalchemy.MetaData()
print(config.DATABASE_URL)

# Create tables
admin_user_table = create_admin_user_table(metadata)

# Create the database if it does not exist
url = make_url(config.DATABASE_URL)
if not database_exists(url):
    create_database(url)
    print(f"Database {url.database} created.")

connect_args = {"check_same_thread": False} if "sqlite" in config.DATABASE_URL else {}
engine = sqlalchemy.create_engine(
    config.DATABASE_URL, connect_args=connect_args
)

metadata.create_all(engine)

db_args = {"min_size": 1, "max_size": 3} if "postgres" in config.DATABASE_URL else {}

database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK, **db_args
)