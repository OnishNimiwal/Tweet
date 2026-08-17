#!/bin/bash
# Build script for Vercel deployment

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python TweetProject/manage.py collectstatic --noinput

echo "Running migrations..."
python TweetProject/manage.py migrate

echo "Build complete!"
