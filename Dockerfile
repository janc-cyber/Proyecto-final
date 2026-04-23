# ── Stage 1: Builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

# Install dependencies in a virtual env so we can copy them cleanly
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# ── Stage 2: Production Image ─────────────────────────────────────────────────
FROM python:3.12-slim AS production

# Security: run as non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# Copy the virtual env from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application source
COPY app.py .
COPY templates/ templates/
COPY static/ static/

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app
USER appuser

# Render.com injects $PORT at runtime
ENV PORT=5000
EXPOSE $PORT

# Healthcheck for container orchestration
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT}/api/health')" || exit 1

# Use gunicorn for production-grade serving
CMD gunicorn --bind 0.0.0.0:${PORT} --workers 2 --threads 4 --timeout 60 app:app
