from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.api import positions, health
from app.core.config import settings

app = FastAPI(
    title="KalaChakra API",
    description="Astronomical and Vedic astrology calculations API",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(positions.router, prefix="/api", tags=["positions"])


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "message": "KalaChakra API",
        "version": "0.1.0",
        "docs": "/api/docs",
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",  
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_RELOAD,
        log_level="debug" if settings.APP_RELOAD else "info",
    )