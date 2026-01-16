from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    print("Starting up Todo API...")
    yield
    # Shutdown
    print("Shutting down Todo API...")


# Create FastAPI application
app = FastAPI(
    title="Todo Application API",
    version="1.0.0",
    description="RESTful API for full-stack web todo application with JWT authentication",
    lifespan=lifespan,
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from .api.auth import router as auth_router
from .api.todos import router as todos_router
from .api.tags import router as tags_router

app.include_router(auth_router, prefix="/api/v1")
app.include_router(todos_router, prefix="/api/v1")
app.include_router(tags_router, prefix="/api/v1")


@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring."""
    from datetime import datetime
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0",
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Todo API",
        "version": "1.0.0",
        "docs": "/docs",
    }
