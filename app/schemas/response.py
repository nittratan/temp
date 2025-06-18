from typing import Optional, List, Dict, Annotated
from pydantic import BaseModel
from .request import Extraction5WsContainer

class ResponsePayload(BaseModel):
    """
    Response model for 5Ws extraction and related tasks.

    Attributes:
        extraction (Extraction5WsContainer): The extracted 5Ws data.
        info (Dict[str, str], optional): Additional information.
        role (str, optional): Role of the responder.
        response (str, optional): Main response content.
    """
    extraction: Extraction5WsContainer
    info: Optional[Dict[str, str]] = None
    role: Optional[str] = None
    response: Optional[str] = None
