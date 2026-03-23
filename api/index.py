"""
api/index.py — Vercel serverless entry point.

Vercel invokes this file for every HTTP request.
Flask's WSGI app is the `app` variable at module level.
"""
import sys
import os

# Make the project root importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app

# Vercel requires the WSGI app to be named `app`
app = create_app()

# Vercel Python runtime calls this as a WSGI handler automatically
# when the module exports a `app` callable.
