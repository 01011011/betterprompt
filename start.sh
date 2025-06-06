#!/bin/bash

# Production startup script for BetterPrompt

# Set default values
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-5000}
WORKERS=${WORKERS:-4}
TIMEOUT=${TIMEOUT:-30}

# Start gunicorn with optimal settings
exec gunicorn \
    --bind $HOST:$PORT \
    --workers $WORKERS \
    --timeout $TIMEOUT \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    app:app
