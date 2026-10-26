"""
FastAPI Concrete Crack Diagnostics & Structural Integrity Route.
"""

import os
import io
from typing import Optional
from fastapi import APIRouter, File, UploadFile, Form, Header
from PIL import Image

from backend.schemas import CrackDiagnosticResponse
from modules.gemini_client import ConstructionAIClient
from sample_data.sample_images import CRACK_SAMPLE_PATH, CRACK_HAIRLINE_PATH

router = APIRouter(prefix="/api/cracks", tags=["Crack Diagnostics & Structural Integrity"])


@router.post("/diagnose", response_model=CrackDiagnosticResponse)
async def diagnose_crack(
    file: Optional[UploadFile] = File(None),
    defect_scenario: int = Form(0),
    x_api_key: Optional[str] = Header(None, alias="X-Gemini-API-Key"),
):
    """
    Forensic crack classification (Hairline, Settlement, Structural Shear, Thermal, Spalling)
    and IS 456 / ACI structural compliance check.
    """
    ai_client = ConstructionAIClient(api_key=x_api_key)

    if file and file.filename:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    else:
        # Load calibrated sample based on scenario
        target_path = CRACK_HAIRLINE_PATH if defect_scenario == 1 else CRACK_SAMPLE_PATH
        if os.path.exists(target_path):
            image = Image.open(target_path).convert("RGB")
        else:
            image = Image.new("RGB", (600, 400), color="#4A5568")

    diag_result, is_live, engine_note = ai_client.analyze_crack_diagnostics(
        image, scenario_index=defect_scenario
    )

    diag_result["is_live"] = is_live
    diag_result["engine_note"] = engine_note
    return diag_result
