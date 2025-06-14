#!/bin/sh

echo "==> Running database population script..."
python -m app.scripts.populate_user_db

echo "==> Running document vectorization script..."
python -m app.scripts.vectorize_documents

echo "==> All pre-start scripts finished. Starting Uvicorn server..."

exec uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload