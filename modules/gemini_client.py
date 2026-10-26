"""
Multi-Modal Gemini AI Client with Strict JSON Contract Parsing
and Resilient Demonstration Fallback Mode.
"""

import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple
from PIL import Image
import io

from modules.config import (
    SAFETY_PPE_PROMPT,
    CRACK_DIAGNOSTICS_PROMPT,
    CHATBOT_SYSTEM_PROMPT,
)

# Realistic fallback mock databases for instant 1-click evaluation without API keys
MOCK_SAFETY_AUDITS = [
    {
        "safety_score": 88,
        "overall_status": "Compliant",
        "audit_summary": "Site exhibits strong general compliance with OSHA 1926 & IS 15844. Hard hats and fluorescent high-vis jackets are actively worn by 85%+ observed personnel. Minor housekeeping hazard identified near south staging scaffolding.",
        "workers_detected": 6,
        "ppe_detection": {
            "safety_helmets": {
                "compliant_count": 6,
                "non_compliant_count": 0,
                "status": "Pass",
                "notes": "All workers wearing approved Type 1 Class E industrial hard hats (IS 2925 / OSHA 1926.100) with chinstraps fastened."
            },
            "high_visibility_vests": {
                "compliant_count": 5,
                "non_compliant_count": 1,
                "status": "Warning",
                "notes": "5 workers equipped with Class 2 fluorescent yellow/orange reflective vests (IS 15844). 1 worker vest partially unzipped."
            },
            "safety_footwear_boots": {
                "compliant_count": 6,
                "non_compliant_count": 0,
                "status": "Pass",
                "notes": "Steel-toe puncture-resistant boots (IS 15298 / ASTM F2413) confirmed on all personnel within active excavation perimeter."
            },
            "safety_harness_fall_protection": {
                "applicable": True,
                "status": "Compliant",
                "notes": "Scaffolding workers anchored to dual-lanyard shock-absorbing lifelines above 2.0m elevation (OSHA 1926.502)."
            },
            "eye_face_respiratory_protection": {
                "applicable": True,
                "status": "Pass",
                "notes": "Cutting and grinding crew equipped with polycarbonate safety spectacles and N95 particulate respirators."
            }
        },
        "hazards_identified": [
            {
                "id": 1,
                "hazard_title": "Exposed Protruding Rebar Without Mushroom Caps",
                "severity": "High",
                "regulatory_code": "OSHA 1926.701(b) / IS 456 Safety Guidelines",
                "location_in_image": "Starter column dowels at ground perimeter (lower right zone)",
                "corrective_remedy": "Fit OSHA-compliant steel-reinforced protective plastic rebar caps immediately to prevent impalement hazards."
            },
            {
                "id": 2,
                "hazard_title": "Trailing Electrical Cables Across Pedestrian Gangway",
                "severity": "Medium",
                "regulatory_code": "OSHA 1926.416(e)(1)",
                "location_in_image": "Main transit aisle adjacent to concrete pump line",
                "corrective_remedy": "Elevate temporary cables on non-conductive cable hangers or install heavy-duty ramp protectors."
            },
            {
                "id": 3,
                "hazard_title": "Missing Mid-Rail on Temporary Scaffolding Bay 3",
                "severity": "Critical",
                "regulatory_code": "OSHA 1926.451(g)(4) & IS 3696",
                "location_in_image": "Elevated perimeter scaffold platform at 4.2m height",
                "corrective_remedy": "Halt staging access until standard guardrail system (top rail at 42 inches, midrail at 21 inches, and 4-inch toeboard) is installed."
            }
        ],
        "immediate_directives": [
            "Install protective impalement caps over all starter reinforcement rebar dowels within 2 hours.",
            "Install missing scaffolding mid-rail at Bay 3 before resumption of high-elevation brickwork.",
            "Re-issue high-vis vest compliance briefing during tomorrow's 08:00 AM Toolbox Talk."
        ]
    },
    {
        "safety_score": 62,
        "overall_status": "Needs Attention",
        "audit_summary": "Multiple PPE non-compliance infractions observed. Elevated work in progress without secure anchorage. Several personnel lacking eye protection and high-visibility wear in mixed vehicular zones.",
        "workers_detected": 4,
        "ppe_detection": {
            "safety_helmets": {
                "compliant_count": 3,
                "non_compliant_count": 1,
                "status": "Warning",
                "notes": "1 worker observed without hard hat in overhead suspended load hazard quadrant."
            },
            "high_visibility_vests": {
                "compliant_count": 2,
                "non_compliant_count": 2,
                "status": "Fail",
                "notes": "2 workers in plain dark civilian clothes within reversing radius of transit mixer."
            },
            "safety_footwear_boots": {
                "compliant_count": 4,
                "non_compliant_count": 0,
                "status": "Pass",
                "notes": "Standard safety footwear worn across active team."
            },
            "safety_harness_fall_protection": {
                "applicable": True,
                "status": "Non-Compliant",
                "notes": "Worker perched on formwork edge at 3.5m without tied-off safety harness (OSHA 1926.501)."
            },
            "eye_face_respiratory_protection": {
                "applicable": True,
                "status": "Warning",
                "notes": "Dust-heavy concrete chipping underway without face shields."
            }
        },
        "hazards_identified": [
            {
                "id": 1,
                "hazard_title": "Fall Hazard: Elevated Work Without Fall Arrest Harness",
                "severity": "Critical",
                "regulatory_code": "OSHA 1926.501 / NBC 2016 Part 7",
                "location_in_image": "Slab edge beam shuttering perimeter",
                "corrective_remedy": "Issue immediate Stop-Work Notice. Install certified horizontal lifeline and harness anchor."
            },
            {
                "id": 2,
                "hazard_title": "Pedestrian Worker Struck-By Hazard Near Moving Machinery",
                "severity": "High",
                "regulatory_code": "OSHA 1926.201 / IS 15844",
                "location_in_image": "Near batching plant discharge chute",
                "corrective_remedy": "Erect physical crowd barricades and bar non-reflective personnel from heavy plant zone."
            }
        ],
        "immediate_directives": [
            "Stop work at edge beam formwork until 100% tie-off fall arrest harness is secured.",
            "Issue high-vis vests and hard hats immediately from site safety dispensary."
        ]
    }
]

MOCK_CRACK_DIAGNOSTICS = [
    {
        "defect_type": "Structural Shear",
        "surface_material": "Reinforced Concrete (RCC) Main Transfer Beam",
        "estimated_crack_width_mm": 2.4,
        "crack_depth_assessment": "Moderate Core Penetration",
        "structural_urgency": "High",
        "severity_score": 8,
        "is_structural_threat": True,
        "root_causes": [
            "Excessive diagonal tension shear stresses exceeding concrete shear capacity (IS 456 Cl. 40.1)",
            "Inadequate shear stirrup spacing or inadequate anchorage near beam-column junction",
            "Differential floor live load overload during construction material staging"
        ],
        "is456_compliance_status": "Severe Non-Compliance: Width 2.4 mm far exceeds IS 456:2000 Cl. 35.3.2 permissible crack width of 0.30 mm for moderate exposure.",
        "recommended_engineering_repairs": [
            {
                "method": "Low-Viscosity Epoxy Pressure Injection (Structural Re-bonding)",
                "specifications": "Drill injection ports at 200mm intervals along crack line. Seal surface with epoxy paste (IS 15450). Inject high-strength epoxy resin (compressive strength > 70 MPa) at 0.3 - 0.5 MPa pressure until refusal.",
                "estimated_repair_cost_range_inr": "₹18,000 - ₹32,000 per linear meter"
            },
            {
                "method": "Carbon Fiber Reinforced Polymer (CFRP) Shear Strengthening",
                "specifications": "Apply 2 layers of bidirectional CFRP wrap (300 g/m²) saturated with structural epoxy primer to beam web to restore shear load capacity.",
                "estimated_repair_cost_range_inr": "₹45,000 - ₹85,000 per beam bay"
            }
        ],
        "preventive_monitoring": [
            "Install Avongard optical crack monitor with 0.1mm vernier resolution to track dynamic opening.",
            "Conduct Ultrasonic Pulse Velocity (UPV) cross-hole sonic logging to evaluate internal honeycombing."
        ]
    },
    {
        "defect_type": "Hairline",
        "surface_material": "Cast-in-place Slab Surface (RCC)",
        "estimated_crack_width_mm": 0.15,
        "crack_depth_assessment": "Superficial",
        "structural_urgency": "Low",
        "severity_score": 2,
        "is_structural_threat": False,
        "root_causes": [
            "Plastic shrinkage cracking caused by rapid surface water evaporation during initial setting (hot weather concreting)",
            "Slight thermal contraction differentials during initial hydration cooling phase"
        ],
        "is456_compliance_status": "Compliant with IS 456:2000 Cl. 35.3.2 (width 0.15mm < 0.20mm for severe/0.30mm for moderate exposure).",
        "recommended_engineering_repairs": [
            {
                "method": "Elastomeric Polymer Crystalline Slurry Coating",
                "specifications": "Clean surface via wire brushing. Apply two coats of cementitious crystalline waterproofing penetrating slurry (IS 5966) to seal micro-capillaries.",
                "estimated_repair_cost_range_inr": "₹3,500 - ₹7,000 per 10 sq.m area"
            }
        ],
        "preventive_monitoring": [
            "Apply continuous wet hessian curing for remaining 7 days as mandated by IS 456 Clause 13.5.",
            "Periodic re-inspection after 30 days to ensure cracks remain dormant and non-progressing."
        ]
    },
    {
        "defect_type": "Spalling",
        "surface_material": "RCC Column Face & Cantilever Chajja",
        "estimated_crack_width_mm": 3.8,
        "crack_depth_assessment": "Through-and-Through Full Depth to Rebar",
        "structural_urgency": "Critical Emergency",
        "severity_score": 9,
        "is_structural_threat": True,
        "root_causes": [
            "Concrete carbonation and chloride ingress causing rebar depassivation and ferrous corrosion expansion",
            "Inadequate cover to reinforcement (< 20mm vs IS 456 prescribed 40mm for columns)",
            "Moisture seepage causing expansive rust pressure fracturing outer concrete layer"
        ],
        "is456_compliance_status": "Critical Failure: Delamination and exposed rebar violates IS 456 Cl. 26.4 cover and structural safety requirements.",
        "recommended_engineering_repairs": [
            {
                "method": "PMM (Polymer Modified Mortar) Structural Restoration & Zinc Rich Coating",
                "specifications": "Chip away delaminated concrete 20mm behind rebar. Sandblast/wire-brush steel rebar and coat with Zinc-rich epoxy anti-corrosion primer. Apply SBR/Acrylic polymer bonding agent and repair with fiber-reinforced structural repair mortar (M40 grade).",
                "estimated_repair_cost_range_inr": "₹25,000 - ₹50,000 per column zone"
            }
        ],
        "preventive_monitoring": [
            "Conduct half-cell potential electrical survey (ASTM C876) to map active corrosion zones across the building.",
            "Test core samples for depth of carbonation using phenolphthalein indicator."
        ]
    }
]

def clean_json_response(raw_text: str) -> Dict[str, Any]:
    """Cleans markdown fences or trailing characters and parses JSON."""
    text = raw_text.strip()
    # Strip markdown ```json ... ``` codeblocks
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n", "", text)
        text = re.sub(r"\n```$", "", text)
        text = text.strip()
    
    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Search for first { and last }
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            snippet = text[start : end + 1]
            return json.loads(snippet)
        raise ValueError("Could not extract valid JSON from model response")


class ConstructionAIClient:
    """Wrapper managing Google Gemini 2.5 / 2.0 / 1.5 Flash multimodal calls with automatic fallback."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "").strip()
        self.client = None
        self.is_live = False

        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                self.is_live = True
            except Exception as e:
                self.is_live = False
                self.client = None

    def analyze_site_safety(self, image: Image.Image, scenario_index: int = 0) -> Tuple[Dict[str, Any], bool, str]:
        """
        Runs multimodal PPE compliance & hazard inspection.
        Returns: (parsed_json, is_live_call, note_message)
        """
        if self.is_live and self.client:
            try:
                # Convert PIL image to bytes
                buffer = io.BytesIO()
                image.save(buffer, format="JPEG", quality=90)
                image_bytes = buffer.getvalue()

                from google.genai import types
                part_img = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")

                # Try modern models in sequence of capability
                models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
                last_err = None

                for model_name in models_to_try:
                    try:
                        response = self.client.models.generate_content(
                            model=model_name,
                            contents=[SAFETY_PPE_PROMPT, part_img],
                            config=types.GenerateContentConfig(
                                response_mime_type="application/json",
                                temperature=0.1,
                            ),
                        )
                        parsed = clean_json_response(response.text)
                        return parsed, True, f"Live Gemini Multi-Modal ({model_name})"
                    except Exception as err:
                        last_err = err
                        continue
                
                # If API call failed, fallback gracefully with explanation
                mock = MOCK_SAFETY_AUDITS[scenario_index % len(MOCK_SAFETY_AUDITS)]
                return mock, False, f"Live API call failed ({str(last_err)[:80]}...). Seamlessly engaged Demonstration Engine."
            except Exception as e:
                mock = MOCK_SAFETY_AUDITS[scenario_index % len(MOCK_SAFETY_AUDITS)]
                return mock, False, f"Live API error: {str(e)[:80]}. Running in High-Fidelity Demonstration Mode."

        # Demo mode fallback
        mock = MOCK_SAFETY_AUDITS[scenario_index % len(MOCK_SAFETY_AUDITS)]
        return mock, False, "Demonstration Mode (Pre-calibrated IS 456 & OSHA Audit Engine)"

    def analyze_crack_diagnostics(self, image: Image.Image, scenario_index: int = 0) -> Tuple[Dict[str, Any], bool, str]:
        """
        Runs multimodal concrete crack classification and structural integrity analysis.
        Returns: (parsed_json, is_live_call, note_message)
        """
        if self.is_live and self.client:
            try:
                buffer = io.BytesIO()
                image.save(buffer, format="JPEG", quality=90)
                image_bytes = buffer.getvalue()

                from google.genai import types
                part_img = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")

                models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
                last_err = None

                for model_name in models_to_try:
                    try:
                        response = self.client.models.generate_content(
                            model=model_name,
                            contents=[CRACK_DIAGNOSTICS_PROMPT, part_img],
                            config=types.GenerateContentConfig(
                                response_mime_type="application/json",
                                temperature=0.1,
                            ),
                        )
                        parsed = clean_json_response(response.text)
                        return parsed, True, f"Live Gemini Multi-Modal ({model_name})"
                    except Exception as err:
                        last_err = err
                        continue

                mock = MOCK_CRACK_DIAGNOSTICS[scenario_index % len(MOCK_CRACK_DIAGNOSTICS)]
                return mock, False, f"Live API call failed ({str(last_err)[:80]}...). Seamlessly engaged Demonstration Engine."
            except Exception as e:
                mock = MOCK_CRACK_DIAGNOSTICS[scenario_index % len(MOCK_CRACK_DIAGNOSTICS)]
                return mock, False, f"Live API error: {str(e)[:80]}. Running in High-Fidelity Demonstration Mode."

        mock = MOCK_CRACK_DIAGNOSTICS[scenario_index % len(MOCK_CRACK_DIAGNOSTICS)]
        return mock, False, "Demonstration Mode (Pre-calibrated IS 456 Forensic Diagnostics Engine)"

    def chat_response(self, messages: List[Dict[str, str]]) -> Tuple[str, bool, str]:
        """
        Multi-turn chat with NirmanAI senior civil engineering advisor.
        """
        if self.is_live and self.client:
            try:
                formatted_contents = [CHATBOT_SYSTEM_PROMPT]
                for m in messages:
                    prefix = "User: " if m["role"] == "user" else "Assistant: "
                    formatted_contents.append(f"{prefix}{m['content']}")

                models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
                for model_name in models_to_try:
                    try:
                        response = self.client.models.generate_content(
                            model=model_name,
                            contents="\n\n".join(formatted_contents),
                        )
                        return response.text, True, f"Live Gemini ({model_name})"
                    except Exception:
                        continue
            except Exception:
                pass

        # Offline / Demo intelligent heuristic answers for construction queries
        last_user_query = messages[-1]["content"].lower() if messages else ""
        
        if "cover" in last_user_query or "is 456" in last_user_query or "nominal cover" in last_user_query:
            reply = (
                "### 🏗️ IS 456:2000 Nominal Concrete Cover Mandate (Clause 26.4):\n\n"
                "To ensure durability and corrosion resistance of reinforcement, nominal cover to all reinforcement steel bars (including stirrups/links) must not be less than:\n\n"
                "1. **Footing / Raft Foundations**: **50 mm** (minimum) up to 75 mm when cast against untreated earth.\n"
                "2. **RCC Columns**: **40 mm** (or not less than bar diameter; for columns ≤ 200 mm cross-section with bars ≤ 12 mm, 25 mm is permitted).\n"
                "3. **Beams (Longitudinal reinforcement)**: **25 mm** (or bar diameter).\n"
                "4. **Slabs & Canopies**: **20 mm** (for mild exposure, 15 mm may be used if bars ≤ 12 mm).\n"
                "5. **Liquid Retaining / Water Tanks (IS 3370)**: **45 mm - 50 mm**.\n\n"
                "💡 **Site Tip**: Always mandate factory-made PVC or high-density fiber-reinforced concrete cover blocks rather than porous stone chips or mortar lumps."
            )
        elif "m25" in last_user_query or "mix ratio" in last_user_query or "concrete mix" in last_user_query:
            reply = (
                "### 🧪 M25 Concrete Mix Proportions & Engineering Guidelines:\n\n"
                "As per **IS 456:2000 Clause 9**, M25 is classified as *Standard Concrete* (Characteristic Compressive Strength $f_{ck} = 25\\text{ N/mm}^2$ at 28 days).\n\n"
                "- **Nominal / Volumetric Approximate Proportion**: **1 : 1 : 2** (1 Part Cement : 1 Part Fine Aggregate / Sand : 2 Parts Coarse Aggregate by volume).\n"
                "- **Design Mix Recommendation (IS 10262:2019)**:\n"
                "  - Cement (OPC 43 or 53): ~380 to 410 kg/m³ (minimum 300 kg/m³ for moderate exposure).\n"
                "  - Water-Cement (W/C) Ratio: **0.45 to 0.50** (Strictly ≤ 0.50 per IS 456 Table 5).\n"
                "  - Coarse Aggregate (20mm down & 10mm down blended 60:40): ~1,100 - 1,180 kg/m³.\n"
                "  - Fine Aggregate (Zone II River Sand / M-Sand): ~680 - 740 kg/m³.\n"
                "  - Polycarboxylate Ether (PCE) Superplasticizer: 0.6% - 1.0% by weight of cement for 120-150 mm slump pumpability.\n\n"
                "⚠️ **Pre-pour Quality Gate**: Conduct Slump Cone test (IS 1199) and cast 6 standard 150mm test cubes (3 tested at 7 days [≥67% strength] and 3 at 28 days [≥100% strength])."
            )
        elif "excavation" in last_user_query or "shoring" in last_user_query or "trench" in last_user_query:
            reply = (
                "### 🚜 Deep Excavation Shoring Protocol (IS 3764 & OSHA 1926 Subpart P):\n\n"
                "For any excavation exceeding **1.5 meters (5 feet)** in depth, protection against cave-in is legally mandatory:\n\n"
                "1. **Soil Classification**: Determine whether soil is Type A (Clay/Hardpan, 53° slope), Type B (Silt/Sandy loam, 45° slope), or Type C (Gravel/Submerged Sand, 34° slope).\n"
                "2. **Protective Systems Options**:\n"
                "   - **Sloping / Benching**: Cut back at 1.5H : 1V (34°) for Type C soils.\n"
                "   - **Soldier Piles with Timber Lagging / Sheet Piling**: Mandatory when adjacent buildings or roads exist within zone of influence.\n"
                "   - **Secant / Diaphragm (D-Wall)**: For deep basements in waterlogged or high water-table conditions.\n"
                "3. **Clear Zone / Surcharge Siting**: No heavy plant (excavators, dumpers) or spoil heaps within **1.5 meters or equal to excavation depth** from trench rim.\n"
                "4. **Safe Egress**: Provide secured ladders every **7.5 meters (25 feet)** of lateral travel extending 1 meter above rim."
            )
        elif "curing" in last_user_query:
            reply = (
                "### 💧 Concrete Curing Specifications (IS 456:2000 Clause 13.5):\n\n"
                "- **Minimum Curing Period**:\n"
                "  - Ordinary Portland Cement (OPC): **Minimum 7 days** under normal conditions.\n"
                "  - Mineral Admixture Blends (PPC / Slag Cement / Fly Ash): **Minimum 10 to 14 days** due to slower pozzolanic secondary reaction.\n"
                "  - Hot Weather / Arid Conditions (IS 7861 Part 1): **Minimum 14 days** with continuous wet hessian burlap wrapping.\n\n"
                "⚠️ Inadequate curing causes up to **40% loss in ultimate compressive strength** and induces plastic and drying shrinkage micro-cracks."
            )
        else:
            reply = (
                f"### 📋 Engineering Consultation on '{messages[-1]['content']}':\n\n"
                "As Senior Project Engineer, here is the technical breakdown:\n\n"
                "1. **Governing Codes**: Work must align with **IS 456:2000** (Code of Practice for Concrete), **NBC 2016 Part 7** (Construction Management), and relevant **OSHA 1926** site safety guidelines.\n"
                "2. **Methodology & Quality Assurance**: Ensure all material test certificates (MTC) for Fe500D TMT rebars (IS 1786) and OPC/PPC cement (IS 8112/IS 1489) are stamped by third-party testing labs before staging.\n"
                "3. **Risk & Safety Controls**: Conduct mandatory Pre-Task Safety Briefing (Toolbox Talk) with permit-to-work (PTW) signed off for height work, hot works, or confined space activities.\n"
                "4. **Inspection Checkpoint**: Concrete pre-pour checklist must verify shuttering alignment, rebar cover block positioning, tie-wire tail bending, and surface cleanliness prior to signing the pour card.\n\n"
                "Let me know if you would like me to detail specific calculation formulas, steel detailing, or safety mitigation procedures!"
            )

        return reply, False, "Demonstration Mode (NirmanAI Senior Engineering Knowledge Base)"
