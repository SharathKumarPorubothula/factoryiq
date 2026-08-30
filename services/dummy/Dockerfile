# ============================================================
# FactoryIQ - Custom Apache + Python + Flask + Redis Base Image
# Base: Ubuntu 24.04
# ============================================================

FROM ubuntu:24.04

# ------------------------------------------------------------
# 1. Install system packages
# ------------------------------------------------------------

RUN apt-get update && apt-get install -y --no-install-recommends \
    apache2 \
    libapache2-mod-wsgi-py3 \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    gcc \
    g++ \
    curl \
    wget \
    ca-certificates \
    git \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# 2. Enable Apache modules
# ------------------------------------------------------------

RUN a2enmod \
    wsgi \
    rewrite \
    headers \
    proxy \
    proxy_http \
    ssl \
    expires

# ------------------------------------------------------------
# 3. Application directory
# ------------------------------------------------------------

WORKDIR /app

RUN mkdir -p /app

# ------------------------------------------------------------
# 4. Python virtual environment
# ------------------------------------------------------------

RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

# ------------------------------------------------------------
# 5. Upgrade Python packaging tools
# ------------------------------------------------------------

RUN pip install --no-cache-dir --upgrade \
    pip \
    setuptools \
    wheel

# ------------------------------------------------------------
# 6. Copy Apache reverse proxy configuration
# ------------------------------------------------------------

COPY factoryiq.conf /etc/apache2/sites-available/factoryiq.conf

RUN a2dissite 000-default.conf && \
    a2ensite factoryiq.conf

# ------------------------------------------------------------
# 7. Copy application files
# ------------------------------------------------------------

COPY . /app/

# ------------------------------------------------------------
# 8. Install common Python libraries
# ------------------------------------------------------------

RUN pip install --no-cache-dir \
    Flask \
    Flask-SQLAlchemy \
    psycopg2-binary \
    redis \
    requests \
    PyJWT

# ------------------------------------------------------------
# 9. Health check
# ------------------------------------------------------------

HEALTHCHECK --interval=30s \
            --timeout=5s \
            --start-period=10s \
            --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# ------------------------------------------------------------
# 10. Expose Apache
# ------------------------------------------------------------

EXPOSE 80

# ------------------------------------------------------------
# 11. Start Apache
# ------------------------------------------------------------

CMD ["apachectl", "-D", "FOREGROUND"]