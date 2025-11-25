"""
Vercel Serverless Function Entry Point for HyreBuy API
"""

from app.main import app

# This is the entry point for Vercel
handler = app
