import logging
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

# Create FastAPI app
app = FastAPI(
    title="High Precision Pi API",
    description="API for retrieving Pi calculated to high precision using the Chudnovsky algorithm",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """On startup, start the pi calculation service"""

    logger.info("Starting Pi calculation service...")
    pi_service.start_calculation()

    logger.info(f"Maximum decimal places: {settings.MAX_DECIMAL_POINTS}")
    logger.info("Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    """On shutdown, stop the pi calculation service gracefully"""

    logger.info("Stopping Pi calculation service...")
    pi_service.stop_calculation()
    logger.info("Application shutdown complete")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 