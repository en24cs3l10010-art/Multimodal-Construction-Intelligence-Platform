"""
FastAPI Safety Vision & PPE Audit Route.
"""

import os
import io
from typing import Optional
from fastapi import APIRouter, File, UploadFile, Form, Header
from PIL import Image

from backend.schemas import SafetyAuditResponse
from modules.gemini_client import ConstructionAIClient
from sample_data.sample_images import PPE_SAMPLE_PATH

router = APIRouter(prefix="/api/safety", tags=["Site Safety & PPE"])


@router.post("/audit", response_model=SafetyAuditResponse)
async def audit_site_safety(
    file: Optional[UploadFile] = File(None),
    sample_scenario: int = Form(0),
    x_api_key: Optional[str] = Header(None, alias="X-Gemini-API-Key"),
):
    """
    Multimodal PPE inspection under OSHA 1926 and IS 15844.
    Accepts uploaded site photo or calibrated scenario index.
    """
    ai_client = ConstructionAIClient(api_key=x_api_key)

    if file and file.filename:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    else:
        # Load calibrated sample
        if os.path.exists(PPE_SAMPLE_PATH):
            image = Image.open(PPE_SAMPLE_PATH).convert("RGB")
        else:
            image = Image.new("RGB", (600, 400), color="#1E293B")

    audit_result, is_live, engine_note = ai_client.analyze_site_safety(
        image, scenario_index=sample_scenario
    )

    audit_result["is_live"] = is_live
    audit_result["engine_note"] = engine_note
    return audit_result
