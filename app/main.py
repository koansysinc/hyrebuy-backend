"""
HyreBuy Backend API - Main Application Entry Point
FastAPI application for HyreBuy real estate platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Version will be imported from config later
VERSION = "1.0.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events"""
    print("🚀 Starting HyreBuy API...")
    # Database connection will be initialized here in Day 2
    yield
    print("👋 Shutting down HyreBuy API...")
    # Database cleanup will happen here


app = FastAPI(
    title="HyreBuy API",
    description="Real Estate Platform for GCC Employees in Hyderabad",
    version=VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware - will be configured with environment variables
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Will be restricted to frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "HyreBuy API is running",
        "version": VERSION,
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "hyrebuy-api",
        "version": VERSION
    }


# API routes will be added here in Week 1-2
# from app.api.v1 import auth, properties, commute, groups
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
# app.include_router(properties.router, prefix="/api/v1/properties", tags=["Properties"])
# app.include_router(commute.router, prefix="/api/v1/commute", tags=["Commute"])
# app.include_router(groups.router, prefix="/api/v1/groups", tags=["Groups"])
