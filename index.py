"""
Vercel Serverless Function Entry Point for HyreBuy API
"""

from app.main import app
from mangum import Mangum

# Mangum wraps the FastAPI app for serverless deployment
handler = Mangum(app, lifespan="off")
