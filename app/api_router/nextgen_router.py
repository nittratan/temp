from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import NextGenException, InvalidPayloadException, NotFoundException
from app.config.error_codes import ErrorCode
from app.models.request import TaskRequest
from app.services.llm_service import process_task
from app.config.logger import logger

router = APIRouter()

@router.get("/", tags=["Index"])
def index():
    logger.info("NextGen API is live!")
    return {"message": "NextGen API is live!"}

@router.get("/capabilities", tags=["Core"])
async def get_capabilities():
    try:
        models = ["03-mini-openai", "gpt-4", "llama-3"]
        logger.info("Fetching capabilities")
        return JSONResponse(status_code=ErrorCode.SUCCESS, content={"models": models})
    except Exception as e:
        logger.error(f"Error in /capabilities: {str(e)}")
        raise NextGenException(detail=f"Error in /capabilities: {str(e)}")


@router.post("/heartbeat", tags=["Core"])
async def heartbeat():
    try:
        logger.info("Heartbeat check")
        return JSONResponse(status_code=ErrorCode.SUCCESS, content={"info": "heartbeat OK", "role": "backend"})
    except Exception as e:
        logger.error(f"Error in /heartbeat: {str(e)}")
        raise NextGenException(detail=f"Error in /heartbeat: {str(e)}")


@router.post("/generate", tags=["LLM"])
async def generate_5ws(request: TaskRequest):
    try:
        logger.info(f"Received task: {request.task_name}")
        response = await process_task(request)
        return JSONResponse(status_code=ErrorCode.SUCCESS, content=response)
    except InvalidPayloadException as ipe:
        logger.warning(f"Invalid payload: {ipe.detail}")
        raise ipe
    except NextGenException as ne:
        logger.error(f"NextGen error: {ne.detail}")
        raise ne
    except Exception as e:
        logger.error(f"Error in /generate: {str(e)}")
        raise NextGenException(detail=f"Error in /generate: {str(e)}")
