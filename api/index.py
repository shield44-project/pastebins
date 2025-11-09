"""
Vercel serverless function entry point
This wraps the Flask app for Vercel deployment
"""
from app import app

# Vercel expects the app variable to be exposed
# This allows Vercel to handle the Flask app as a serverless function
app = app
