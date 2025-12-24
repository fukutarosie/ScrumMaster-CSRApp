"""
Vercel Serverless Function Handler for Flask Backend
This file exports the Flask app for Vercel's serverless environment
"""
import sys
import os

# Add parent directory to path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app

# Vercel expects the WSGI app to be named 'app'
# No need to run app.run() - Vercel handles that
