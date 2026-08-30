import os
import psycopg2
from psycopg2 import pool

from ace_logger import get_logger


logger = get_logger(__name__)


class Database:

    def __init__(self):

        # ====================================================
        # Service
        # ====================================================

        self.service_name = os.getenv(
            "SERVICE_NAME"
        )

        if not self.service_name:
            raise RuntimeError(
                "SERVICE_NAME is not configured"
            )

        # ====================================================
        # PostgreSQL Configuration
        # ====================================================

        self.host = os.getenv(
            "DB_HOST",
            "postgres"
        )

        self.port = int(
            os.getenv(
                "DB_PORT",
                "5432"
            )
        )

        self.user = os.getenv(
            "DB_USER"
        )

        self.password = os.getenv(
            "DB_PASSWORD"
        )

        if not self.user:
            raise RuntimeError(
                "DB_USER is not configured"
            )

        if not self.password:
            raise RuntimeError(
                "DB_PASSWORD is not configured"
            )

        # ====================================================
        # Database Name
        # ====================================================

        self.database = (
            f"{self.service_name}_db"
        )

        logger.info(
            "Initializing database for service: %s",
            self.service_name
        )

        logger.info(
            "Database name: %s",
            self.database
        )

        # ====================================================
        # Connection Pool
        # ====================================================

        self.pool = psycopg2.pool.ThreadedConnectionPool(
            1,
            10,
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )

        logger.info(
            "Database connection pool created"
        )

    # ========================================================
    # Convert ? to PostgreSQL %s
    # ========================================================

    def _prepare_query(self, query):

        return query.replace(
            "?",
            "%s"
        )

    # ========================================================
    # SELECT MANY
    # ========================================================

    def fetch_all(
        self,
        query,
        params=None
    ):

        connection = None
        cursor = None

        try:

            query = self._prepare_query(query)

            connection = self.pool.getconn()

            cursor = connection.cursor()

            cursor.execute(
                query,
                params or ()
            )

            columns = [
                description[0]
                for description in cursor.description
            ]

            rows = cursor.fetchall()

            return [
                dict(zip(columns, row))
                for row in rows
            ]

        except Exception:

            logger.exception(
                "Database fetch_all failed"
            )

            raise

        finally:

            if cursor:
                cursor.close()

            if connection:
                self.pool.putconn(
                    connection
                )

    # ========================================================
    # SELECT ONE
    # ========================================================

    def fetch_one(
        self,
        query,
        params=None
    ):

        connection = None
        cursor = None

        try:

            query = self._prepare_query(query)

            connection = self.pool.getconn()

            cursor = connection.cursor()

            cursor.execute(
                query,
                params or ()
            )

            row = cursor.fetchone()

            if row is None:
                return None

            columns = [
                description[0]
                for description in cursor.description
            ]

            return dict(
                zip(columns, row)
            )

        except Exception:

            logger.exception(
                "Database fetch_one failed"
            )

            raise

        finally:

            if cursor:
                cursor.close()

            if connection:
                self.pool.putconn(
                    connection
                )

    # ========================================================
    # INSERT / UPDATE / DELETE
    # ========================================================

    def execute(
        self,
        query,
        params=None
    ):

        connection = None
        cursor = None

        try:

            query = self._prepare_query(query)

            connection = self.pool.getconn()

            cursor = connection.cursor()

            cursor.execute(
                query,
                params or ()
            )

            row_count = cursor.rowcount

            connection.commit()

            return row_count

        except Exception:

            if connection:
                connection.rollback()

            logger.exception(
                "Database execute failed"
            )

            raise

        finally:

            if cursor:
                cursor.close()

            if connection:
                self.pool.putconn(
                    connection
                )

    # ========================================================
    # Health Check
    # ========================================================

    def health_check(self):

        connection = None
        cursor = None

        try:

            connection = self.pool.getconn()

            cursor = connection.cursor()

            cursor.execute(
                "SELECT 1"
            )

            cursor.fetchone()

            return True

        except Exception:

            logger.exception(
                "Database health check failed"
            )

            return False

        finally:

            if cursor:
                cursor.close()

            if connection:
                self.pool.putconn(
                    connection
                )

    # ========================================================
    # Close
    # ========================================================

    def close(self):

        self.pool.closeall()

        logger.info(
            "Database connection pool closed"
        )