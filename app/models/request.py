from pydantic import BaseModel
from typing import List, Optional

class Document(BaseModel):
    document_type: str
    metadata: dict
    content: str
    prior_auth: Optional[List[str]] = []
    interaction_id: Optional[str] = None
    dcn: Optional[str] = None

class TaskRequest(BaseModel):
    task_name: str
    requestor_type: Optional[str]
    reading_level: Optional[str]
    document: Document
    guidelines: Optional[List[str]] = []
    glossary: Optional[str] = None
    citation: bool = False
    reasoning: bool = False
