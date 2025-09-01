import os
import sys
import time
import psycopg2
from psycopg2 import sql
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine, text


def wait_for_postgres(database_url: str, max_retries: int = 30):
    """Wait for PostgreSQL to be available"""
    retries = 0
    while retries < max_retries:
        try:
            # Parse database URL for connection test
            conn = psycopg2.connect(database_url)
            conn.close()
            print("PostgreSQL is ready!")
            return True
        except psycopg2.OperationalError:
            retries += 1
            print(
                f"PostgreSQL is unavailable - sleeping (attempt {retries}/{max_retries})"
            )
            time.sleep(2)

    print("Failed to connect to PostgreSQL")
    return False


def create_database_if_not_exists(database_url: str):
    """Create database if it doesn't exist"""
    try:
        # Parse the URL to get database name
        from urllib.parse import urlparse

        parsed = urlparse(database_url)
        db_name = parsed.path[1:]  # Remove leading slash

        # Connect to postgres database to create target database
        postgres_url = database_url.replace(f"/{db_name}", "/postgres")

        conn = psycopg2.connect(postgres_url)
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,)
        )
        exists = cursor.fetchone()

        if not exists:
            print(f"Creating database: {db_name}")
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
            )
            print(f"Database {db_name} created successfully")
        else:
            print(f"Database {db_name} already exists")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error creating database: {e}")
        # Don't raise, as database might already exist


def run_migrations():
    """Run database migrations"""
    database_url = os.getenv(
        "DATABASE_URL", "postgresql://user:pass@localhost:5432/medical"
    )

    print(f"Database URL: {database_url.replace('pass', '***')}")

    # Wait for PostgreSQL
    if not wait_for_postgres(
        database_url.replace(database_url.split("/")[-1], "postgres")
    ):
        sys.exit(1)

    # Create database if needed
    create_database_if_not_exists(database_url)

    # Wait a bit more for database to be ready
    time.sleep(2)

    # Configure Alembic
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", database_url)

    try:
        print("Running database migrations...")

        # Check if alembic_version table exists using SQLAlchemy 2.0 syntax
        engine = create_engine(database_url)
        with engine.connect() as conn:
            # Use text() for raw SQL queries in SQLAlchemy 2.0
            result = conn.execute(
                text(
                    """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = 'alembic_version'
                );
            """
                )
            )
            table_exists = result.fetchone()[0]

        if not table_exists:
            print("Initializing Alembic version control...")
            command.stamp(alembic_cfg, "head")

        # Run migrations
        command.upgrade(alembic_cfg, "head")
        print("✅ Migrations completed successfully")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise


if __name__ == "__main__":
    run_migrations()
