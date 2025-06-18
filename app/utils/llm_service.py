from app.schemas.request import RequestPayload

def dummy_extract_5ws(content: str):
    return {
        "who": "John Doe",
        "what": "Diagnosed with hypertension",
        "when": "January 5, 2023",
        "where": "NYC Hospital",
        "why": "Patient reported high BP",
        "supplemental_info": {"notes": "Follow-up in 2 weeks"}
    }

async def process_task(request: RequestPayload):
    content = request.document.content
    extracted = dummy_extract_5ws(content)
    return extracted
