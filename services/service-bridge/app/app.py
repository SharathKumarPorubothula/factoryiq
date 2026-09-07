import json
import os
import time
import uuid

import jwt
import redis
import requests

from flask import Flask, request, jsonify

from ace_logger import get_logger


# ============================================================
# Application
# ============================================================

app = Flask(__name__)
logger = get_logger(__name__)


# ============================================================
# Configuration
# ============================================================

CONFIG_FILE = os.getenv("BRIDGE_CONFIG", "/app/bridge_config.json")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "5"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))


# ============================================================
# JWT Configuration
# ============================================================

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


# ============================================================
# Redis Configuration
# ============================================================

REDIS_HOST = os.getenv("REDIS_HOST", "host.docker.internal")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_RATE_LIMIT = int(os.getenv("REDIS_RATE_LIMIT", "100"))
REDIS_RATE_WINDOW = int(os.getenv("REDIS_RATE_WINDOW", "60"))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


# ============================================================
# Load Bridge Configuration
# ============================================================

def load_bridge_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
        logger.info("Bridge configuration loaded successfully")
        return config
    except Exception:
        logger.exception("Failed to load bridge configuration")
        raise


BRIDGE_CONFIG = load_bridge_config()


# ============================================================
# Step 1 / Step 5 - Generate or Propagate Trace ID
# ============================================================

def get_trace_id():
    trace_id = request.headers.get("X-Trace-ID")
    if trace_id:
        return trace_id
    return str(uuid.uuid4())


# ============================================================
# Step 2 - Validate Request
# ============================================================

def validate_request(path):
    if not path:
        return False, "Request path is required"
    return True, None


# ============================================================
# Step 3 - Authentication
# ============================================================

def authenticate_request():
    authorization = request.headers.get("Authorization")

    if not authorization:
        return False, None

    if not authorization.startswith("Bearer "):
        return False, None

    token = authorization.split(" ", 1)[1].strip()

    if not token:
        return False, None

    if not JWT_SECRET:
        logger.error("JWT_SECRET is not configured")
        return False, None

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return True, payload
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token expired")
        return False, None
    except jwt.InvalidTokenError:
        logger.warning("Invalid JWT token")
        return False, None


# ============================================================
# Step 3 - Authorization
# ============================================================

def authorize_request(payload, route_name):
    if not payload:
        return False

    user_id = payload.get("sub")
    roles = payload.get("roles", [])
    permissions = payload.get("permissions", [])

    logger.debug(
        "Authorization check user_id=%s route=%s roles=%s permissions=%s",
        user_id, route_name, roles, permissions
    )

    # --------------------------------------------------------
    # TODO: Add your actual RBAC / permission rules here.
    #
    # Example:
    #
    # required_permission = {
    #     "create_user": "user:create",
    #     "users": "user:read",
    #     "projects": "project:read"
    # }.get(route_name)
    #
    # if required_permission:
    #     if required_permission not in permissions:
    #         return False
    # --------------------------------------------------------

    return True


# ============================================================
# Step 4 - Redis Rate Limiting
# ============================================================

def check_rate_limit():
    try:
        user_id = request.headers.get("X-User-ID") or request.remote_addr
        key = f"factoryiq:rate_limit:{user_id}"

        current_count = redis_client.incr(key)

        if current_count == 1:
            redis_client.expire(key, REDIS_RATE_WINDOW)

        if current_count > REDIS_RATE_LIMIT:
            logger.warning(
                "Rate limit exceeded user=%s count=%s",
                user_id, current_count
            )
            return False

        return True

    except redis.RedisError:
        logger.exception("Redis rate limit check failed")
        # Development behavior: allow request if Redis is unavailable.
        # For production, choose fail-closed depending on security needs.
        return True


# ============================================================
# Step 6 - Route Matching
# ============================================================

def resolve_route(path):
    # Example: /api/login -> route_name = "login"
    #          /api/projects -> route_name = "projects"
    route_name = path.strip("/").split("/")[-1]
    service_config = BRIDGE_CONFIG.get(route_name)

    if not service_config:
        return None, route_name

    return service_config, route_name


# ============================================================
# Step 7 + Step 8 - Resolve Service and Build URL
# ============================================================

def build_service_url(service_config, route_name):
    service_name = service_config["service_name"]
    port = int(service_config["port"])
    return f"http://{service_name}:{port}/{route_name}"


# ============================================================
# Step 9 - Forward Headers
# ============================================================

def build_forward_headers(trace_id):
    headers = {}

    authorization = request.headers.get("Authorization")
    if authorization:
        headers["Authorization"] = authorization

    content_type = request.headers.get("Content-Type")
    if content_type:
        headers["Content-Type"] = content_type

    headers["X-Trace-ID"] = trace_id

    return headers


# ============================================================
# Retry Policy
# ============================================================

def is_retryable_method(method):
    return method.upper() in {"GET", "HEAD", "OPTIONS"}


# ============================================================
# Step 10 + Step 11 + Step 12
# Call Domain Service / Timeout / Controlled Retry
# ============================================================

def call_domain_service(url, headers, method, body, query_params, trace_id):
    retry_count = 0

    while True:
        try:
            logger.info(
                "trace_id=%s calling service url=%s attempt=%s",
                trace_id, url, retry_count + 1
            )

            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                data=body,
                params=query_params,
                timeout=REQUEST_TIMEOUT
            )

            return response, retry_count

        except requests.exceptions.Timeout:
            logger.warning(
                "trace_id=%s downstream service timeout url=%s",
                trace_id, url
            )

            if retry_count >= MAX_RETRIES or not is_retryable_method(method):
                raise

            retry_count += 1
            time.sleep(0.5)

        except requests.exceptions.ConnectionError:
            logger.warning(
                "trace_id=%s downstream connection error url=%s",
                trace_id, url
            )

            if retry_count >= MAX_RETRIES or not is_retryable_method(method):
                raise

            retry_count += 1
            time.sleep(0.5)


# ============================================================
# Step 13 + Step 14 - Build Response
# ============================================================

def build_response(response):
    try:
        response_data = response.json()
        return jsonify(response_data), response.status_code
    except ValueError:
        return (
            response.text,
            response.status_code,
            {"Content-Type": response.headers.get("Content-Type", "text/plain")}
        )


# ============================================================
# Main Service Bridge
# ============================================================

@app.route("/api/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def service_bridge(path):
    start_time = time.time()

    # ========================================================
    # Step 1 - Receive Request
    # ========================================================

    trace_id = get_trace_id()
    method = request.method

    logger.info(
        "trace_id=%s request received method=%s path=%s",
        trace_id, method, request.path
    )

    try:
        # ====================================================
        # Step 2 - Validate
        # ====================================================

        valid, error = validate_request(path)

        if not valid:
            return jsonify({"error": error, "trace_id": trace_id}), 400

        # ====================================================
        # Step 6 - Match Route
        # ====================================================

        service_config, route_name = resolve_route(path)

        if not service_config:
            logger.warning(
                "trace_id=%s route not configured route=%s",
                trace_id, route_name
            )
            return jsonify({
                "error": "Route not configured",
                "trace_id": trace_id
            }), 404

        # ====================================================
        # Step 3 - Authentication
        #
        # LOGIN IS THE ONLY PUBLIC ROUTE (/api/login).
        # No JWT required. Every other route requires JWT.
        # ====================================================

        if route_name != "login":
            authenticated, payload = authenticate_request()

            if not authenticated:
                logger.warning(
                    "trace_id=%s authentication failed route=%s",
                    trace_id, route_name
                )
                return jsonify({
                    "error": "Authentication failed",
                    "trace_id": trace_id
                }), 401

            # ================================================
            # Step 3 - Authorization
            # ================================================

            authorized = authorize_request(payload, route_name)

            if not authorized:
                logger.warning(
                    "trace_id=%s authorization failed route=%s",
                    trace_id, route_name
                )
                return jsonify({
                    "error": "Access denied",
                    "trace_id": trace_id
                }), 403

        else:
            logger.info("trace_id=%s login route - JWT not required", trace_id)

        # ====================================================
        # Step 4 - Redis Rate Limit
        # ====================================================

        if not check_rate_limit():
            return jsonify({
                "error": "Rate limit exceeded",
                "trace_id": trace_id
            }), 429

        # ====================================================
        # Step 7 + Step 8 - Resolve Service
        # ====================================================

        service_name = service_config["service_name"]
        port = service_config["port"]
        service_url = build_service_url(service_config, route_name)

        logger.info(
            "trace_id=%s route resolved service=%s port=%s url=%s",
            trace_id, service_name, port, service_url
        )

        # ====================================================
        # Step 9 - Forward Request
        # ====================================================

        headers = build_forward_headers(trace_id)
        body = request.get_data()
        query_params = request.args.to_dict(flat=False)

        # ====================================================
        # Step 10 + 11 + 12
        # Call Domain Service / Timeout / Controlled Retry
        # ====================================================

        response, retry_count = call_domain_service(
            url=service_url,
            headers=headers,
            method=method,
            body=body,
            query_params=query_params,
            trace_id=trace_id
        )

        # ====================================================
        # Step 13 - Receive Response
        # ====================================================

        logger.info(
            "trace_id=%s downstream response status=%s",
            trace_id, response.status_code
        )

        # ====================================================
        # Step 14 - Return Response
        # ====================================================

        result = build_response(response)

        # ====================================================
        # Step 15 - Structured Logging
        # ====================================================

        duration_ms = (time.time() - start_time) * 1000

        logger.info(
            "trace_id=%s request completed service=%s status=%s "
            "retry_count=%s duration_ms=%.2f",
            trace_id, service_name, response.status_code,
            retry_count, duration_ms
        )

        return result

    except requests.exceptions.Timeout:
        logger.exception("trace_id=%s downstream service timeout", trace_id)
        return jsonify({"error": "Service timeout", "trace_id": trace_id}), 504

    except requests.exceptions.ConnectionError:
        logger.exception("trace_id=%s downstream service unavailable", trace_id)
        return jsonify({"error": "Service unavailable", "trace_id": trace_id}), 503

    except Exception:
        logger.exception("trace_id=%s unexpected Service Bridge error", trace_id)
        return jsonify({
            "error": "Internal Service Bridge error",
            "trace_id": trace_id
        }), 500


# ============================================================
# Health Check
# ============================================================

@app.route("/health", methods=["GET"])
def health():
    redis_status = "UP"

    try:
        redis_client.ping()
    except redis.RedisError:
        redis_status = "DOWN"

    return jsonify({"status": "UP", "redis": redis_status}), 200


# ============================================================
# Application Startup
# ============================================================

if __name__ == "__main__":
    logger.info("Starting FactoryIQ Service Bridge")
    app.run(host="0.0.0.0", port=5002, debug=False)