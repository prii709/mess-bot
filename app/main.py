from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat_service import chat_service
from app.services.scheduler_service import scheduler_service
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - startup and shutdown"""
    # Startup
    logger.info("Starting Mess Bot API...")
    scheduler_service.start()
    logger.info("Application started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Mess Bot API...")
    scheduler_service.shutdown()
    logger.info("Application shut down successfully")


# Create FastAPI app
app = FastAPI(
    title="Mess Bot API",
    description="FastAPI automation bot for hostel/college mess management using Google Sheets",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "status": "running",
        "message": "Mess Bot API is operational",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": scheduler_service.scheduler.running,
        "scheduler": "running" if scheduler_service.scheduler.running else "stopped"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for interacting with the mess bot
    
    Supports the following intents:
    - inventory_query: Query inventory items and stock levels
    - low_stock_alert: Get alerts for items with low stock
    - attendance_stats: Get attendance statistics
    - attendance_prediction: Predict next day's attendance
    - feedback_average: Get average feedback ratings
    - low_rating_alert: Get alerts for low-rated meals
    """
    try:
        response = chat_service.process_message(request.message)
        return response
    except Exception as e:
        logger.error(f"Error processing chat message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/scheduler/jobs")
async def get_scheduled_jobs():
    """Get information about scheduled jobs"""
    return {
        "jobs": scheduler_service.get_jobs()
    }


@app.get("/config")
async def get_config():
    """Get current configuration (excluding sensitive data)"""
    return {
        "low_stock_threshold": settings.low_stock_threshold,
        "low_rating_threshold": settings.low_rating_threshold,
        "host": settings.host,
        "port": settings.port
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )
