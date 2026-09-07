import os
import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from flask import Flask, request, jsonify

from ace_logger import get_logger
from db_util import Database


# ============================================================
# Application
# ============================================================

app = Flask(__name__)

logger = get_logger(__name__)


# ============================================================
# Database
# ============================================================

db = Database("identity_db")


# ============================================================
# JWT Configuration
# ============================================================

JWT_SECRET = os.getenv("JWT_SECRET")

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", "60"))


# ============================================================
# Validate JWT Configuration
# ============================================================

if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET is not configured")


# ============================================================
# Health Check
# ============================================================


@app.route("/health", methods=["GET"])
def health():

    try:
        database_status = db.health_check()

        if not database_status:
            return jsonify({"status": "DOWN", "database": "DOWN"}), 503

        return jsonify({"status": "UP", "database": "UP"}), 200

    except Exception:
        logger.exception("Identity health check failed")

        return jsonify({"status": "DOWN"}), 503


# ============================================================
# LOGIN
# ============================================================


@app.route("/login", methods=["POST"])
def login():

    try:
        # ====================================================
        # 1. Read request body
        # ====================================================

        data = request.get_json(silent=True)
        logger.info("Login request received: %s", data)

        if not data:
            return jsonify({"error": "Request body is required"}), 400

        # ====================================================
        # 2. Read username/password
        # ====================================================

        username = data.get("username")
        password = data.get("password")

        # ====================================================
        # 3. Validate input
        # ====================================================

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        logger.info("Login attempt username=%s", username)

        # ====================================================
        # 4. Find user
        #
        # db.execute() returns a list[dict] for SELECT
        # queries, so we pull out the first row ourselves.
        # ====================================================

        users = db.execute(
            """
            SELECT
                id,
                username,
                email,
                password_hash,
                first_name,
                last_name,
                is_active
            FROM users
            WHERE username = ?
            """,
            (username,),
        )

        logger.info("User query result: %s", users)

        user = users[0] if users else None

        logger.info("User found: %s", user)

        # ====================================================
        # 5. User not found
        # ====================================================

        if not user:
            logger.warning("Login failed - invalid username")

            return jsonify({"error": "Invalid username or password"}), 401

        # ====================================================
        # 6. Check active user
        # ====================================================

        if not user["is_active"]:
            logger.warning("Login failed - inactive user username=%s", username)

            return jsonify({"error": "User account is inactive"}), 403

        # ====================================================
        # 7. Verify password
        # ====================================================

        password_valid = bcrypt.checkpw(
            password.encode("utf-8"), user["password_hash"].encode("utf-8")
        )

        if not password_valid:
            logger.warning("Login failed - invalid password username=%s", username)

            return jsonify({"error": "Invalid username or password"}), 401

        # ====================================================
        # 8. Get user roles
        # ====================================================

        role_rows = (
            db.execute(
                """
            SELECT
                r.id,
                r.name
            FROM user_roles ur
            INNER JOIN roles r
                ON ur.role_id = r.id
            WHERE ur.user_id = ?
              AND r.is_active = TRUE
            """,
                (user["id"],),
            )
            or []
        )

        roles = [row["name"] for row in role_rows]

        # ====================================================
        # 9. Get permissions
        # ====================================================

        permission_rows = (
            db.execute(
                """
            SELECT DISTINCT
                p.name
            FROM user_roles ur

            INNER JOIN roles r
                ON ur.role_id = r.id

            INNER JOIN role_permissions rp
                ON r.id = rp.role_id

            INNER JOIN permissions p
                ON rp.permission_id = p.id

            WHERE ur.user_id = ?
              AND r.is_active = TRUE
            """,
                (user["id"],),
            )
            or []
        )

        permissions = [row["name"] for row in permission_rows]

        # ====================================================
        # 10. Create JWT
        # ====================================================

        now = datetime.now(timezone.utc)

        expiration = now + timedelta(minutes=JWT_EXPIRATION_MINUTES)

        payload = {
            # User ID
            "sub": str(user["id"]),
            # Username
            "username": user["username"],
            # Email
            "email": user["email"],
            # Roles
            "roles": roles,
            # Permissions
            "permissions": permissions,
            # Issued at
            "iat": now,
            # Expiration
            "exp": expiration,
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        # ====================================================
        # 11. Update last login
        # ====================================================

        db.execute(
            """
            UPDATE users
            SET
                last_login_at = NOW(),
                updated_at = NOW()
            WHERE id = ?
            """,
            (user["id"],),
        )

        logger.info("Login successful username=%s roles=%s", username, roles)

        # ====================================================
        # 12. Return response
        # ====================================================

        return jsonify(
            {
                "message": "Login successful",
                "access_token": token,
                "token_type": "Bearer",
                "expires_in": JWT_EXPIRATION_MINUTES * 60,
                "user": {
                    "id": str(user["id"]),
                    "username": user["username"],
                    "email": user["email"],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "roles": roles,
                },
            }
        ), 200

    except Exception:
        logger.exception("Identity login failed")

        return jsonify({"error": "Internal server error"}), 500


# ============================================================
# CREATE USER
# ============================================================


@app.route("/create_user", methods=["POST"])
def create_user():
    try:
        # ====================================================
        # 1. Read request body
        # ====================================================

        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "Request body is required"}), 400

        # ====================================================
        # 2. Read fields
        # ====================================================

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        first_name = data.get("first_name")

        last_name = data.get("last_name")

        role_name = data.get("role_name")

        # ====================================================
        # 3. Validate required fields
        # ====================================================

        if not username:
            return jsonify({"error": "username is required"}), 400

        if not email:
            return jsonify({"error": "email is required"}), 400

        if not password:
            return jsonify({"error": "password is required"}), 400

        if not role_name:
            return jsonify({"error": "role_name is required"}), 400

        # ====================================================
        # 4. Validate password length
        # ====================================================

        if len(password) < 8:
            return jsonify(
                {"error": "Password must contain at least 8 characters"}
            ), 400

        # ====================================================
        # 5. Check username already exists
        # ====================================================

        existing_username_rows = db.execute(
            """
            SELECT id
            FROM users
            WHERE username = ?
            """,
            (username,),
        )

        if existing_username_rows:
            return jsonify({"error": "Username already exists"}), 409

        # ====================================================
        # 6. Check email already exists
        # ====================================================

        existing_email_rows = db.execute(
            """
            SELECT id
            FROM users
            WHERE email = ?
            """,
            (email,),
        )

        if existing_email_rows:
            return jsonify({"error": "Email already exists"}), 409

        # ====================================================
        # 7. Find requested role
        # ====================================================

        role_rows = db.execute(
            """
            SELECT
                id,
                name,
                is_active
            FROM roles
            WHERE name = ?
            """,
            (role_name,),
        )

        role = role_rows[0] if role_rows else None

        if not role:
            return jsonify({"error": "Role not found"}), 400

        if not role["is_active"]:
            return jsonify({"error": "Role is inactive"}), 400

        # ====================================================
        # 8. Hash password
        # ====================================================

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        # ====================================================
        # 9. Create user
        # ====================================================

        user_id = str(uuid.uuid4())

        db.execute(
            """
            INSERT INTO users
            (
                id,
                username,
                email,
                password_hash,
                first_name,
                last_name,
                is_active
            )
            VALUES
            (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                TRUE
            )
            """,
            (user_id, username, email, password_hash, first_name, last_name),
        )

        # ====================================================
        # 10. Assign role
        # ====================================================

        db.execute(
            """
            INSERT INTO user_roles
            (
                user_id,
                role_id
            )
            VALUES
            (
                ?,
                ?
            )
            """,
            (user_id, role["id"]),
        )

        # ====================================================
        # 11. Get assigned permissions
        # ====================================================

        permission_rows = (
            db.execute(
                """
            SELECT DISTINCT
                p.name
            FROM role_permissions rp

            INNER JOIN permissions p
                ON rp.permission_id = p.id

            WHERE rp.role_id = ?
            """,
                (role["id"],),
            )
            or []
        )

        permissions = [row["name"] for row in permission_rows]

        # ====================================================
        # 12. Log successful creation
        # ====================================================

        logger.info("User created username=%s role=%s", username, role_name)

        # ====================================================
        # 13. Return response
        # ====================================================

        return jsonify(
            {
                "message": "User created successfully",
                "user": {
                    "id": user_id,
                    "username": username,
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "role": role_name,
                    "permissions": permissions,
                    "is_active": True,
                },
            }
        ), 201

    except Exception:
        logger.exception("Create user failed")

        return jsonify({"error": "Internal server error"}), 500


# ============================================================
# Application Startup
# ============================================================

if __name__ == "__main__":
    logger.info("Starting FactoryIQ Identity Service")

    app.run(host="0.0.0.0", port=5001, debug=False)