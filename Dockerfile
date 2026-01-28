# Official lightweight Python image
FROM python:3.10-slim

# Non-root user for security
RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app

# Install system deps required for some Python packages and healthcheck
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc curl \
    && rm -rf /var/lib/apt/lists/*

# Copy streamlit requirements and install
COPY streamlitapp/requirements.txt ./streamlitapp/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r streamlitapp/requirements.txt

# Copy the full project
COPY . /app

# Give appuser ownership and switch to it
RUN chown -R appuser:appuser /app
USER appuser

# Ensure app modules are importable
ENV PYTHONPATH=/app/scripts
ENV STREAMLIT_SERVER_HEADLESS=true

EXPOSE 8501

# Lightweight healthcheck (runs as root in Docker)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501/ || exit 1

# Default command: start the Streamlit web UI
CMD ["streamlit", "run", "streamlitapp/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
