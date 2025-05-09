import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import uvicorn

from app.api.routes import router
from app.api.dependencies import limiter, pi_service
from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting Pi calculation service...")
    pi_service.start_calculation()
    logger.info(f"Maximum decimal places: {settings.MAX_DECIMAL_POINTS}")
    logger.info("Application startup complete")
    
    yield  # Here the FastAPI application runs
    
    # Shutdown
    logger.info("Stopping Pi calculation service...")
    pi_service.stop_calculation()
    logger.info("Application shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="High Precision Pi API",
    description="API for retrieving Pi calculated to high precision using the Chudnovsky algorithm",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
# In production, replace with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Register routes
app.include_router(router)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 