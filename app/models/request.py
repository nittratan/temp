from typing import Optional, List, Dict, Annotated
from enum import Enum
from pydantic import BaseModel, Field, field_validator

class TaskName(str, Enum):
    """
    Enum for supported task names.
    extractive_summarization: Extracts key sentences from the document.
    abstractive_summarization: Generates a summary in new words.
    classification: Classifies the document.
    five_ws_extraction: Extracts Who, What, When, Where, Why.
    """
    extractive_summarization = "extractive_summarization"
    abstractive_summarization = "abstractive_summarization"
    classification = "classification"
    five_ws_extraction = "five_ws_extraction"

class RequestorType(str, Enum):
    """
    Enum for the type of requestor.
    member: End user or patient.
    provider: Healthcare provider.
    admin: Administrator.
    system: Automated system.
    """
    member = "member"
    provider = "provider"
    admin = "admin"
    system = "system"

class ReadingLevel(str, Enum):
    """
    Enum for reading level of the response content.
    elementary: Elementary school level.
    middle_school: Middle school level.
    high_school: High school level.
    college: College level.
    professional: Professional/technical level.
    """
    elementary = "elementary"
    middle_school = "middle_school"
    high_school = "high_school"
    college = "college"
    professional = "professional"

class DocumentType(str, Enum):
    """
    Enum for document types.
    transcription: Transcribed text.
    document: General document.
    report: Report document.
    note: Note or memo.
    """
    transcription = "transcription"
    document = "document"
    report = "report"
    note = "note"

class Extraction5WsContainer(BaseModel):
    """
    Model representing the 5Ws (Who, What, When, Where, Why) extracted.

    Attributes:
        who (List[str], optional): Entities involved in the context.
        what (List[str], optional): Actions or elements described.
        when (List[str], optional): Time-related references.
        where (List[str], optional): Locations or places involved.
        why (List[str], optional): Reasons, causes, or motivations.
        supplemental (Dict[str, str], optional): Additional structured metadata.
    """
    who: Optional[List[str]] = Field(default=None, description="List of entities")
    what: Optional[List[str]] = Field(default=None, description="List of actions")
    when: Optional[List[str]] = Field(default=None, description="List of date and time")
    where: Optional[List[str]] = Field(default=None, description="List of locations")
    why: Optional[List[str]] = Field(default=None, description="List of reasons")
    supplemental: Optional[Dict[str, str]] = Field(default=None, description="Additional data")

    @field_validator("who", "what", "when", "where", "why", mode="before")
    @classmethod
    def non_empty_string(cls, v):
        """Ensures each list element is a non-empty, non-whitespace-only string."""
        if v is not None:
            if not isinstance(v, list):
                raise TypeError("Value must be a list")
            for item in v:
                if not item or not str(item).strip():
                    raise ValueError("List items must be non-empty strings.")
        return v

class Document(BaseModel):
    """
    Model for a document in the request payload.

    Attributes:
        document_type (str): Type of the document.
        metadata (dict): Metadata for the document.
        content (str): The main content of the document.
        prior_auth (List[str], optional): Prior authorizations.
        interaction_id (str, optional): Interaction ID.
        dcn (str, optional): Document Control Number.
    """
    document_type: str = Field(..., description="Type of the document")
    metadata: dict = Field(..., description="Metadata for the document")
    content: str = Field(..., description="The main content of the document")
    prior_auth: Optional[List[str]] = Field(default_factory=list, description="Prior authorizations")
    interaction_id: Optional[str] = Field(default=None, description="Interaction ID")
    dcn: Optional[str] = Field(default=None, description="Document Control Number")

    @field_validator("document_type", "content", mode="before")
    @classmethod
    def not_empty(cls, v):
        if v is None or (isinstance(v, str) and not v.strip()):
            raise ValueError("Field must not be empty.")
        return v

class RequestPayload(BaseModel):
    """
    Main request model for tasks like extraction or summarization.

    Attributes:
        task_name (TaskName): The task to perform (e.g., extract, summarize).
        interaction_id (str, optional): ID to trace the interaction.
        dcn (str, optional): Document Control Number; alphanumeric with optional hyphens.
        claims (List[str], optional): List of claim IDs for processing.
        prior_auth (List[str], optional): List of prior authorization references.
        citation (bool): Flag to indicate if citation references are required in the response.
        reasoning (bool): Flag to indicate if reasoning should be included in the response.
        guidelines (List[str], optional): Guidelines to be considered while processing.
        requestor_type (RequestorType, optional): Type of person or entity making the request.
        reading_level (ReadingLevel, optional): Complexity level of the response content.
    """
    task_name: TaskName = Field(..., description="The name of task")
    interaction_id: Optional[str] = Field(default=None, description="Interaction ID", min_length=3, max_length=100)
    dcn: Optional[str] = Field(default=None, description="Document Control Number")
    claims: Optional[List[str]] = Field(default=None, description="List of claims")
    prior_auth: Optional[List[str]] = Field(default=None, description="List of prior authorization references")
    citation: bool = Field(default=False, description="Flag to include citations in response.")
    reasoning: bool = Field(default=False, description="Flag to include reasoning in response.")
    guidelines: Optional[List[str]] = Field(default=None, description="List of guidelines")
    requestor_type: Optional[RequestorType] = Field(default=None, description="Type of requestor")
    reading_level: Optional[ReadingLevel] = Field(default=None, description="Desired reading level of the response")
    document: Document

    @field_validator("dcn")
    @classmethod
    def validate_dcn(cls, v):
        if v and not v.isalnum():
            raise ValueError("DCN must be alphanumeric")
        return v

    @field_validator("claims", "prior_auth", "guidelines", mode="before")
    @classmethod
    def check_non_empty_string_list(cls, v):
        if v is not None:
            if not isinstance(v, list):
                raise TypeError("Value must be a list")
            for item in v:
                if not item or not str(item).strip():
                    raise ValueError("Items in the list must be non-empty strings")
        return v

    @field_validator("citation", mode="after")
    @classmethod
    def check_citation_reasoning(cls, v, info):
        if v and not info.data.get("reasoning"):
            info.data["reasoning"] = True
        return v

    model_config = dict(
        json_schema_extra={
            "example": {
                "task_name": "five_ws_extraction",
                "interaction_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "dcn": "DOC123456",
                "citation": True,
                "reasoning": False,
                "requestor_type": "provider",
                "reading_level": "high_school",
                "claims": ["CLAIM123"],
                "prior_auth": ["AUTH456"],
                "guidelines": ["Follow up in 2 weeks"],
                "document": {
                    "document_type": "report",
                    "metadata": {"source": "hospital"},
                    "content": "Patient was diagnosed with hypertension.",
                    "prior_auth": ["AUTH456"],
                    "interaction_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "dcn": "DOC123456"
                }
            }
        }
    )
