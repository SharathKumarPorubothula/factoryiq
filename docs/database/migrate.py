import os
import psycopg2
from pathlib import Path


DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def execute_sql(database, sql_file):

    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=database,
        user=DB_USER,
        password=DB_PASSWORD
    )

    try:
        with connection.cursor() as cursor:

            sql = Path(sql_file).read_text(
                encoding="utf-8"
            )

            cursor.execute(sql)

        connection.commit()

        print(
            f"Migration completed: {database}"
        )

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


execute_sql(
    "identity_db",
    "migrations/identity.sql"
)