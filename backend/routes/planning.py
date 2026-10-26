"""
FastAPI Project Planning, CapEx Valuation, and 3D Studio Route.
"""

import urllib.parse
from fastapi import APIRouter, HTTPException
from backend.schemas import PlanningRequest, PlanningResponse
from modules.config import CITY_TIERS

router = APIRouter(prefix="/api/planning", tags=["Project Planning & Valuation"])


def format_inr(amount: float) -> str:
    if amount >= 10_000_000:
        crores = amount / 10_000_000
        return f"₹{crores:.2f} Cr"
    elif amount >= 100_000:
        lakhs = amount / 100_000
        return f"₹{lakhs:.2f} L"
    else:
        return f"₹{amount:,.0f}"


@router.get("/metadata")
async def get_planning_metadata():
    """Returns available Indian city tiers, structure typologies, and cost parameters."""
    metadata = {}
    for tier_k, data in CITY_TIERS.items():
        structures = [k for k in data.keys() if k != "tier"]
        metadata[tier_k] = {
            "tier_label": data["tier"],
            "structures": structures,
            "details": {s: data[s] for s in structures},
        }
    return metadata


@router.post("/estimate", response_model=PlanningResponse)
async def calculate_planning_estimate(req: PlanningRequest):
    """
    Computes total project budget, CapEx incurred, finished asset valuation in INR,
    IS 456 material quantities, and Pollinations AI 3D architectural rendering URL.
    """
    if req.city_tier_key not in CITY_TIERS:
        raise HTTPException(status_code=400, detail=f"Invalid city tier: {req.city_tier_key}")

    tier_data = CITY_TIERS[req.city_tier_key]
    tier_label = tier_data["tier"]

    if req.structure_type not in tier_data:
        raise HTTPException(status_code=400, detail=f"Invalid structure type: {req.structure_type}")

    benchmark = tier_data[req.structure_type]
    cost_per_sqft = benchmark["cost_per_sqft"]
    market_rate_sqft = benchmark["market_rate_sqft"]
    cement_factor = benchmark["cement_factor"]
    steel_factor_kg = benchmark["steel_factor_kg"]

    total_project_budget = req.built_up_sqft * cost_per_sqft
    capex_incurred = total_project_budget * (req.completion_pct / 100.0)
    capex_remaining = total_project_budget - capex_incurred

    # Valuation modeling with intrinsic stage multiplier
    stage_multiplier = 0.40 + (0.60 * (req.completion_pct / 100.0))
    current_asset_valuation = (req.built_up_sqft * market_rate_sqft) * stage_multiplier
    finished_market_valuation = req.built_up_sqft * market_rate_sqft
    unrealized_equity_spread = finished_market_valuation - total_project_budget

    # Materials per IS 456
    total_cement_bags = int(req.built_up_sqft * cement_factor)
    total_steel_tonnes = (req.built_up_sqft * steel_factor_kg) / 1000.0
    cement_used = int(total_cement_bags * (req.completion_pct / 100.0))
    steel_used = total_steel_tonnes * (req.completion_pct / 100.0)

    # Milestones
    if req.completion_pct < 15:
        milestone_title = "Substructure: Earthwork, Piling & Foundation Raft"
        milestone_color = "#3B82F6"
    elif req.completion_pct < 45:
        milestone_title = "Superstructure: RCC Columns, Shear Walls & Slabs"
        milestone_color = "#F59E0B"
    elif req.completion_pct < 75:
        milestone_title = "Building Envelope: AAC Blockwork, MEP Piping & Plaster"
        milestone_color = "#8B5CF6"
    elif req.completion_pct < 95:
        milestone_title = "Finishing: Flooring, Glazing, Substation & Elevators"
        milestone_color = "#10B981"
    else:
        milestone_title = "Handover & Commissioning: Occupancy Certificate (OC) Stage"
        milestone_color = "#059669"

    # Pollinations AI Prompt & URL
    clean_style = req.arch_style.replace("Architecture", "").strip()
    pollinations_prompt = (
        f"Photorealistic 8k architectural exterior photograph of {req.structure_type}, "
        f"{req.built_up_sqft:,.0f} sq ft built up, {clean_style}, located in modern {tier_label} Indian metropolis, "
        f"golden hour lighting, architectural digest masterpiece photography, ray tracing, ultra-detailed landscaping"
    )
    encoded_prompt = urllib.parse.quote(pollinations_prompt)
    pollinations_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=500&seed=42&nologo=true"

    return PlanningResponse(
        tier_label=tier_label,
        cost_per_sqft=cost_per_sqft,
        market_rate_sqft=market_rate_sqft,
        total_project_budget=total_project_budget,
        total_project_budget_formatted=format_inr(total_project_budget),
        capex_incurred=capex_incurred,
        capex_incurred_formatted=format_inr(capex_incurred),
        capex_remaining=capex_remaining,
        capex_remaining_formatted=format_inr(capex_remaining),
        current_asset_valuation=current_asset_valuation,
        current_asset_valuation_formatted=format_inr(current_asset_valuation),
        finished_market_valuation=finished_market_valuation,
        finished_market_valuation_formatted=format_inr(finished_market_valuation),
        unrealized_equity_spread=unrealized_equity_spread,
        unrealized_equity_spread_formatted=format_inr(unrealized_equity_spread),
        milestone_title=milestone_title,
        milestone_color=milestone_color,
        materials={
            "cement_bags_total": total_cement_bags,
            "cement_bags_used": cement_used,
            "cement_factor": cement_factor,
            "steel_tonnes_total": round(total_steel_tonnes, 2),
            "steel_tonnes_used": round(steel_used, 2),
            "steel_factor_kg": steel_factor_kg,
            "coarse_aggregate_cuft": int(req.built_up_sqft * 1.25),
            "msand_cuft": int(req.built_up_sqft * 1.65),
        },
        pollinations_prompt=pollinations_prompt,
        pollinations_url=pollinations_url,
    )
