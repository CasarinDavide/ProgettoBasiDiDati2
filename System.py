from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker

user = "root"
password = ""
port = 3306
hostname = "localhost"
database_name = "e-commerce"

# Create SQLAlchemy engine globally
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{hostname}:{port}/{database_name}')
Session = sessionmaker(bind=engine)
session = Session()


def hasTable(table_name):
    return inspect(engine).has_table(table_name)







