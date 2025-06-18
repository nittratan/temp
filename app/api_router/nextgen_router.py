from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import NextGenException, InvalidPayloadException, NotFoundException
from app.utils.error_codes import ErrorCode
from app.schemas.request import RequestPayload
from app.schemas.response import ResponsePayload
from app.utils.llm_service import process_task
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO
)

router = APIRouter()


@router.get("/capabilities")
async def get_capabilities():
    try:
        models = ["03-mini-openai", "gpt-4", "llama-3"]
        logger.info("Fetching capabilities")
        return JSONResponse(status_code=ErrorCode.SUCCESS, content={"models": models})
    except Exception as e:
        logger.error(f"Error in /capabilities: {str(e)}")
        raise NextGenException(detail=f"Error in /capabilities: {str(e)}")


@router.post("/generate")
async def generate_5ws(request: RequestPayload):
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
