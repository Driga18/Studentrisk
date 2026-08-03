import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Render provides the Postgres connection string through DATABASE_URL.
    # SQLite remains the local-development fallback.
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        # SQLAlchemy needs the driver to be explicit. Render may supply either
        # postgres:// or postgresql:// URLs.
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+psycopg2://", 1)

    SQLALCHEMY_DATABASE_URI = database_url or "sqlite:///" + os.path.join(basedir, "instance", "student_risk.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
