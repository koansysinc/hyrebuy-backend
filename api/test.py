"""
Simple test API for Vercel deployment debugging
"""

from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Simple test works"}

@app.get("/health")
def health():
    return {"status": "healthy"}

handler = Mangum(app, lifespan="off")
