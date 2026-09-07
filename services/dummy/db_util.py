import os

import psycopg2
from psycopg2 import pool

from ace_logger import get_logger


logger = get_logger(__name__)


class Database:
    def __init__(self, database=None):

        # ====================================================
        # Service
        # ====================================================

        self.service_name = os.getenv("SERVICE_NAME")

        if not self.service_name:
            raise RuntimeError("SERVICE_NAME is not configured")

        # ====================================================
        # PostgreSQL Configuration
        # ====================================================

        self.host = os.getenv("DB_HOST", "postgres")

        self.port = int(os.getenv("DB_PORT", "5432"))

        self.user = os.getenv("DB_USER")

        self.password = os.getenv("DB_PASSWORD")

        if not self.user:
            raise RuntimeError("DB_USER is not configured")

        if not self.password:
            raise RuntimeError("DB_PASSWORD is not configured")

        # ====================================================
        # Database Name
        #
        # Priority:
        #
        # 1. Database name passed to Database()
        # 2. DB_NAME from environment (.env)
        #
        # Examples:
        #
        # Database("identity_db")
        #       -> identity_db
        #
        # Database("project_db")
        #       -> project_db
        #
        # Database()
        # DB_NAME=project_db
        #       -> project_db
        # ====================================================

        self.database = database or os.getenv("DB_NAME")

        if not self.database:
            raise RuntimeError("DB_NAME is not configured")

        logger.info("Initializing database for service: %s", self.service_name)

        logger.info("Database name: %s", self.database)

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
            password=self.password,
        )

        logger.info("Database connection pool created")

    # ========================================================
    # Convert ? to PostgreSQL %s
    # ========================================================

    def _prepare_query(self, query):

        return query.replace("?", "%s")

    # ========================================================
    # EXECUTE ANY QUERY
    #
    # Supports:
    # SELECT
    # INSERT
    # UPDATE
    # DELETE
    #
    # SELECT returns:
    #     list[dict]
    #
    # INSERT/UPDATE/DELETE returns:
    #     affected row count
    # ========================================================

    def execute(self, query, params=None):

        connection = None
        cursor = None

        try:
            # ------------------------------------------------
            # Prepare query
            # ------------------------------------------------

            query = self._prepare_query(query)

            logger.debug("Executing database query")

            # ------------------------------------------------
            # Get connection from pool
            # ------------------------------------------------

            connection = self.pool.getconn()

            # ------------------------------------------------
            # Create cursor
            # ------------------------------------------------

            cursor = connection.cursor()

            # ------------------------------------------------
            # Execute query
            # ------------------------------------------------

            cursor.execute(query, params or ())

            # ------------------------------------------------
            # Check whether query returns rows
            #
            # cursor.description is available for
            # SELECT / RETURNING queries.
            # ------------------------------------------------

            if cursor.description:
                columns = [description[0] for description in cursor.description]

                rows = cursor.fetchall()

                result = [dict(zip(columns, row)) for row in rows]

                # ------------------------------------------------
                # Commit transaction
                # ------------------------------------------------

                connection.commit()

                return result

            # ------------------------------------------------
            # INSERT / UPDATE / DELETE
            # ------------------------------------------------

            row_count = cursor.rowcount

            connection.commit()

            return row_count

        except Exception:
            # ------------------------------------------------
            # Rollback on failure
            # ------------------------------------------------

            if connection:
                connection.rollback()

            logger.exception("Database query execution failed")

            raise

        finally:
            # ------------------------------------------------
            # Close cursor
            # ------------------------------------------------

            if cursor:
                cursor.close()

            # ------------------------------------------------
            # Return connection to pool
            # ------------------------------------------------

            if connection:
                self.pool.putconn(connection)

    # ========================================================
    # Health Check
    # ========================================================

    def health_check(self):

        connection = None
        cursor = None

        try:
            connection = self.pool.getconn()

            cursor = connection.cursor()

            cursor.execute("SELECT 1")

            cursor.fetchone()

            connection.commit()

            return True

        except Exception:
            if connection:
                connection.rollback()

            logger.exception("Database health check failed")

            return False

        finally:
            if cursor:
                cursor.close()

            if connection:
                self.pool.putconn(connection)

    # ========================================================
    # Close Connection Pool
    # ========================================================

    def close(self):

        if self.pool:
            self.pool.closeall()

            logger.info("Database connection pool closed")
