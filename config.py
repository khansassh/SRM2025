import os

DB_USER = "postgres"
DB_PASSWORD = "ilovemoon19"
DB_HOST = "localhost"  # Change if using a remote server
DB_PORT = "5432"       # Default PostgreSQL port
DB_NAME = "khalza"

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
