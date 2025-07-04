from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

def engine():
    url_connection = "postgresql://neondb_owner:npg_abcnWBkzpu43@ep-summer-firefly-a8kuk7p7-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require"
    # Create SQLAlchemy engine globally
    return create_engine(url_connection)

class Base(DeclarativeBase):
    pass