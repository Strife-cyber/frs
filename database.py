"""
This file is used for the setup of our database and the creation
of tables.
We make accessible a session instance at the end.
"""

from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define the SQLite database URL
DATABASE_URL = "sqlite:///frs.sqlite"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create all tables defined in models
Base.metadata.create_all(engine)

print("Database and tables created!")

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session instance to be used
session = Session()

print("Session instance created!")
