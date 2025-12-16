from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
import logging

                   
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

                    
app = FastAPI(
    title="ML Analytics Platform",
    description="Real-time ML-powered analytics dashboard with JAX",
    version="1.0.0"
)

                
origins = settings.cors_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

                
from app.routers import events, predictions, analytics

                 
app.include_router(events.router, prefix="/api/events", tags=["events"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["predictions"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])


@app.get("/")
def root():
                       
    return {
        "message": "ML Analytics Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
                               
    from app.ml.inference import get_ml_engine
    
    try:
        ml_engine = get_ml_engine()
        model_version = ml_engine.current_version
    except Exception as e:
        logger.error(f"ML engine health check failed: {e}")
        model_version = "unavailable"
    
    return {
        "status": "healthy",
        "model_version": model_version,
        "environment": settings.environment
    }


@app.on_event("startup")
async def startup_event():
                                         
    logger.info("Starting ML Analytics Platform...")
    try:
        from app.ml.inference import get_ml_engine
        ml_engine = get_ml_engine()
        logger.info(f"ML engine initialized with model version: {ml_engine.current_version}")
    except Exception as e:
        logger.warning(f"ML engine initialization failed: {e}")
        logger.warning("API will start but predictions may not be available")


@app.on_event("shutdown")
async def shutdown_event():
                             
    logger.info("Shutting down ML Analytics Platform...")
