"""Main FastAPI application entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="SkyOps Intelligence: High-Integrity Airline Procedure Verification API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
)

# CORS Middleware for Next.js frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root-level health probe for container orchestrators (Kubernetes / ECS)
app.include_router(health.router, prefix="")

# Versioned API routes
app.include_router(health.router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["Root"])
async def root_info():
    """Root metadata endpoint."""
    return {
        "service": settings.PROJECT_NAME,
        "version": "0.1.0",
        "status": "online",
        "docs": "/docs",
        "health": "/health",
        "api_v1": settings.API_V1_PREFIX,
    }
