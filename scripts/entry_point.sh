#!/bin/bash

# Run migrations
echo "Running migrations..."
python startup.py
echo "Migrated."

# Run app
echo "Running app..."
uvicorn app.main:app --host 0.0.0.0 --port 8080