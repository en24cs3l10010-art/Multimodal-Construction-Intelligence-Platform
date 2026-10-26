"""
Strict Pydantic JSON Data Contracts for FastAPI Endpoints.
Ensures schema stability and reliable frontend integration.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PPEItemDetail(BaseModel):
    compliant_count: Optional[Any] = None
    non_compliant_count: Optional[Any] = None
    status: str
    notes: str


class HazardItem(BaseModel):
    id: int
    hazard_title: str
    severity: str
    regulatory_code: str
    location_in_image: str
    corrective_remedy: str


class SafetyAuditResponse(BaseModel):
    safety_score: int = Field(..., ge=0, le=100)
    overall_status: str
    audit_summary: str
    workers_detected: int
    ppe_detection: Dict[str, Any]
    hazards_identified: List[HazardItem]
    immediate_directives: List[str]
    engine_note: str
    is_live: bool


class EngineeringRepair(BaseModel):
    method: str
    specifications: str
    estimated_repair_cost_range_inr: str


class CrackDiagnosticResponse(BaseModel):
    defect_type: str
    surface_material: str
    estimated_crack_width_mm: float
    crack_depth_assessment: str
    structural_urgency: str
    severity_score: int = Field(..., ge=1, le=10)
    is_structural_threat: bool
    root_causes: List[str]
    is456_compliance_status: str
    recommended_engineering_repairs: List[EngineeringRepair]
    preventive_monitoring: List[str]
    engine_note: str
    is_live: bool


class PlanningRequest(BaseModel):
    city_tier_key: str
    structure_type: str
    built_up_sqft: float = Field(..., gt=0)
    completion_pct: float = Field(..., ge=0, le=100)
    arch_style: str = "Modern Glass & Steel Biophilic High-Rise"


class PlanningResponse(BaseModel):
    tier_label: str
    cost_per_sqft: float
    market_rate_sqft: float
    total_project_budget: float
    total_project_budget_formatted: str
    capex_incurred: float
    capex_incurred_formatted: str
    capex_remaining: float
    capex_remaining_formatted: str
    current_asset_valuation: float
    current_asset_valuation_formatted: str
    finished_market_valuation: float
    finished_market_valuation_formatted: str
    unrealized_equity_spread: float
    unrealized_equity_spread_formatted: str
    milestone_title: str
    milestone_color: str
    materials: Dict[str, Any]
    pollinations_prompt: str
    pollinations_url: str


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    api_key: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    is_live: bool
    engine_note: str
