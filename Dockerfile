FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir uv \
    && uv pip install --system --no-cache .

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]


# # syntax=docker/dockerfile:1

# ##########
# # Builder
# ##########
# FROM python:3.13.7-slim AS builder

# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1

# WORKDIR /app

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential libpq-dev \
#  && rm -rf /var/lib/apt/lists/*

# COPY pyproject.toml uv.lock ./
# RUN pip install --no-cache-dir uv \
#  && uv pip install --no-cache --target /opt/venv --upgrade .

# COPY . .
# # Install your package into /opt/venv as well (editable not needed in prod)
# RUN uv pip install --no-cache --target /opt/venv .

# ##########
# # Runtime
# ##########
# FROM python:3.13.7-slim

# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1 \
#     PATH="/opt/venv/bin:${PATH}"

# # Create non-root user
# RUN addgroup --system app && adduser --system --ingroup app app
# WORKDIR /app

# # Copy site-packages and app code from builder
# COPY --from=builder /opt/venv /opt/venv
# COPY --from=builder /app /app

# USER app

# EXPOSE 8000

# # Optional healthcheck (hits /health if you have it)
# HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD \
#   python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health').read()" || exit 1

# # Gunicorn with Uvicorn workers
# # Adjust workers based on CPU (rule of thumb: 2–4 per CPU)
# CMD ["gunicorn", "main:app", \
#      "-k", "uvicorn.workers.UvicornWorker", \
#      "--bind", "0.0.0.0:8000", \
#      "--workers", "2", \
#      "--timeout", "60"]
