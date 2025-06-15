from pydantic import BaseModel
from typing import Optional, Dict

class TaskResponse(BaseModel):
    who: Optional[str]
    what: Optional[str]
    when: Optional[str]
    where: Optional[str]
    why: Optional[str]
    supplemental_info: Optional[Dict]
