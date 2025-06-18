import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from app.api_router.nextgen_router import router as nextgen_router
import logging
import uvicorn
import traceback

load_dotenv()

app = FastAPI(title="NextGen 5Ws API")
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO)

# CORS Setup (use env variable for origins)
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {str(exc)}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

@app.get("/")
def index():
    logger.info("NextGen API is live!")
    return {"message": "NextGen API is live!"}

@app.post("/heartbeat")
async def heartbeat():
    try:
        logger.info("Heartbeat check")
        return JSONResponse(status_code=200, content={"info": "heartbeat OK", "role": "backend"})
    except Exception as e:
        logger.error(f"Error in /heartbeat: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": f"Error in /heartbeat: {str(e)}"})

# Include router
app.include_router(nextgen_router, prefix="/api/nextgen")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    logger.info("NextGen 5Ws API is running 🚀")