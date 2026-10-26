"""
Configuration, Constants, Indian Construction Standards (IS 456 / NBC 2016),
OSHA Compliance Rules, City Tier Benchmarks, and System Prompts.
"""

APP_TITLE = "Multimodal Construction Intelligence Platform"
APP_SUBTITLE = "Decision-Support AI for Safety Vision, Structural Diagnostics, CapEx Valuation & Daily Site Operations"
APP_VERSION = "v1.0 (Skill Wallet Capstone Project 1)"

# Tier-based Construction Cost & Real Estate Valuation Benchmarks (in INR / sqft)
CITY_TIERS = {
    "Tier 1 (Metro: Mumbai, Delhi-NCR, Bengaluru, Hyderabad, Chennai)": {
        "tier": "Tier 1",
        "Residential - Standard": {"cost_per_sqft": 2100, "market_rate_sqft": 9500, "cement_factor": 0.42, "steel_factor_kg": 3.8},
        "Residential - Premium / Luxury": {"cost_per_sqft": 3200, "market_rate_sqft": 19500, "cement_factor": 0.48, "steel_factor_kg": 4.5},
        "Commercial - Grade A Office": {"cost_per_sqft": 3600, "market_rate_sqft": 22000, "cement_factor": 0.50, "steel_factor_kg": 5.2},
        "Industrial / Warehouse Pre-Engineered": {"cost_per_sqft": 1950, "market_rate_sqft": 6500, "cement_factor": 0.32, "steel_factor_kg": 3.0},
        "Infrastructure / Bridges & Flyovers": {"cost_per_sqft": 4800, "market_rate_sqft": 14000, "cement_factor": 0.58, "steel_factor_kg": 6.8},
    },
    "Tier 2 (Growth Hubs: Pune, Ahmedabad, Kolkata, Jaipur, Lucknow, Chandigarh, Kochi)": {
        "tier": "Tier 2",
        "Residential - Standard": {"cost_per_sqft": 1750, "market_rate_sqft": 5800, "cement_factor": 0.40, "steel_factor_kg": 3.6},
        "Residential - Premium / Luxury": {"cost_per_sqft": 2500, "market_rate_sqft": 10500, "cement_factor": 0.45, "steel_factor_kg": 4.2},
        "Commercial - Grade A Office": {"cost_per_sqft": 2800, "market_rate_sqft": 12000, "cement_factor": 0.48, "steel_factor_kg": 4.8},
        "Industrial / Warehouse Pre-Engineered": {"cost_per_sqft": 1600, "market_rate_sqft": 4200, "cement_factor": 0.30, "steel_factor_kg": 2.8},
        "Infrastructure / Bridges & Flyovers": {"cost_per_sqft": 4200, "market_rate_sqft": 9500, "cement_factor": 0.55, "steel_factor_kg": 6.2},
    },
    "Tier 3 (Emerging: Indore, Coimbatore, Vadodara, Bhubaneswar, Nagpur, Visakhapatnam)": {
        "tier": "Tier 3",
        "Residential - Standard": {"cost_per_sqft": 1450, "market_rate_sqft": 3800, "cement_factor": 0.38, "steel_factor_kg": 3.4},
        "Residential - Premium / Luxury": {"cost_per_sqft": 2100, "market_rate_sqft": 6800, "cement_factor": 0.42, "steel_factor_kg": 3.9},
        "Commercial - Grade A Office": {"cost_per_sqft": 2300, "market_rate_sqft": 7500, "cement_factor": 0.45, "steel_factor_kg": 4.4},
        "Industrial / Warehouse Pre-Engineered": {"cost_per_sqft": 1350, "market_rate_sqft": 3100, "cement_factor": 0.28, "steel_factor_kg": 2.6},
        "Infrastructure / Bridges & Flyovers": {"cost_per_sqft": 3600, "market_rate_sqft": 7200, "cement_factor": 0.52, "steel_factor_kg": 5.8},
    }
}

# Weather Advisory Rules & Safety Protocols
WEATHER_CONDITIONS = {
    "Normal / Clear Skies (25°C - 34°C, Wind < 20 km/h)": {
        "condition_key": "Normal",
        "alert_level": "Optimal",
        "badge_color": "#10B981",
        "crane_status": "Operational (Full Capacity)",
        "concreting": "Standard curing protocols apply (minimum 7-day water curing as per IS 456 Cl. 13.5).",
        "electrical": "Routine ground-fault circuit interrupter (GFCI) checks.",
        "protocols": [
            "Maintain standard OSHA 1926.100 PPE gear compliance.",
            "Normal working hours with designated 15-minute mid-shift refreshment pause.",
            "Continue standard deep foundation excavation and formwork shuttering.",
            "Monitor dust suppression via water sprinkling at haul roads."
        ]
    },
    "High Wind Advisory (> 45 km/h, Gusts up to 65 km/h)": {
        "condition_key": "High Wind",
        "alert_level": "Critical Caution",
        "badge_color": "#EF4444",
        "crane_status": "SUSPEND TOWER CRANE & HOIST OPERATIONS (OSHA 1926.1431). Free-weathervane jib.",
        "concreting": "Avoid elevated bucket pouring; high wind accelerates surface desiccation causing plastic shrinkage cracks.",
        "electrical": "Inspect overhead temporary power lines for sway and clearance infringements.",
        "protocols": [
            "IMMEDIATELY suspend crane slewing and elevated lift basket operations.",
            "Secure or lower all loose corrugated GI sheets, formwork panels, and scaffolding tarpaulins.",
            "Prohibit roofing, external perimeter cladding, and window glazing installation.",
            "Enforce mandatory fall arrest safety harnesses (OSHA 1926.502) on any workers on fixed scaffolds."
        ]
    },
    "Heavy Rain & Monsoon Inundation (Precipitation > 60mm/day)": {
        "condition_key": "Heavy Rain",
        "alert_level": "High Hazard",
        "badge_color": "#3B82F6",
        "crane_status": "Restricted slewing; outrigger ground bearing capacity verification mandatory.",
        "concreting": "HALT fresh open concrete pours immediately; rainwater compromises Water-Cement (W/C) ratio.",
        "electrical": "DE-ENERGIZE all non-waterproof temporary power distribution boards (PDBs).",
        "protocols": [
            "Activate multi-stage submersible dewatering pumps in basements and lift pits.",
            "Inspect trench shoring and soil revetments for mudslide or collapse risks (IS 3764).",
            "Cover freshly poured concrete (< 4 hours old) with impermeable plastic sheets.",
            "Mandate vulcanized rubber safety gumboots with anti-slip tread (IS 15298) across muddy ground."
        ]
    },
    "Extreme Heat Wave (> 42°C, Wet Bulb > 30°C)": {
        "condition_key": "Extreme Heat",
        "alert_level": "Severe Environmental",
        "badge_color": "#F59E0B",
        "crane_status": "Operator cabin air conditioning verification; thermal expansion hydraulic checks.",
        "concreting": "HOT WEATHER CONCRETING PROTOCOL (IS 7861 Part 1): Use chilled mixing water or ice flakes.",
        "electrical": "Thermal scanning of distribution switchboards to detect overload heating.",
        "protocols": [
            "Continuous wet hessian burlap wrapping for columns and vertical concrete elements.",
            "Shift mass concrete casting to twilight/night hours (6 PM - 4 AM) to curb thermal cracking.",
            "Mandate 15-minute shaded hydration breaks every 45 minutes; supply oral rehydration salts (ORS).",
            "Provide UV protective neck flaps on safety helmets and electrolyte hydration stations."
        ]
    },
    "Dense Fog & Poor Visibility (< 100m Visibility)": {
        "condition_key": "Dense Fog",
        "alert_level": "Moderate Hazard",
        "badge_color": "#8B5CF6",
        "crane_status": "Prohibit blind crane lifts; two-way radio signalling and spotters required.",
        "concreting": "Permitted with adequate high-lumen floodlighting (> 150 lux at pouring deck).",
        "electrical": "Inspect fog moisture condensation on high-voltage junction terminals.",
        "protocols": [
            "Enforce Class 3 high-visibility fluorescent vests with retro-reflective tape on all site personnel.",
            "Install high-intensity amber strobe flashers on dumpers, JCBs, and transit concrete mixers.",
            "Speed limit restriction to 10 km/h within site perimeter haulage tracks.",
            "Maintain continuous sound horn warnings before reversing earthmoving plant."
        ]
    }
}

# Prompt Templates for Multimodal Gemini Analysis

SAFETY_PPE_PROMPT = """
You are an expert Chief Construction Safety Inspector and Senior OSHA / IS 456 Compliance Auditor.
Analyze the provided construction site photo thoroughly for safety compliance and hazard mitigation.

Evaluate compliance against:
1. OSHA 1926 Safety & Health Regulations for Construction
2. IS 456 / IS 15844 / IS 15298 Indian Safety Standards
3. NBC 2016 (National Building Code of India) Part 7 Construction Management and Safety

You MUST return ONLY a valid, strictly formatted JSON object with this EXACT schema:
{
  "safety_score": <integer from 0 to 100>,
  "overall_status": "<Compliant | Needs Attention | Critical Violation>",
  "audit_summary": "<concise 2-sentence executive summary of the safety posture>",
  "workers_detected": <integer estimated number of workers observed>,
  "ppe_detection": {
    "safety_helmets": {
      "compliant_count": <int>,
      "non_compliant_count": <int>,
      "status": "<Pass | Warning | Fail>",
      "notes": "<observation description>"
    },
    "high_visibility_vests": {
      "compliant_count": <int>,
      "non_compliant_count": <int>,
      "status": "<Pass | Warning | Fail>",
      "notes": "<observation description>"
    },
    "safety_footwear_boots": {
      "compliant_count": <int>,
      "non_compliant_count": <int>,
      "status": "<Pass | Warning | Fail>",
      "notes": "<observation description>"
    },
    "safety_harness_fall_protection": {
      "applicable": <boolean>,
      "status": "<Compliant | Non-Compliant | Not Applicable>",
      "notes": "<harness / lanyard / lifeline observation>"
    },
    "eye_face_respiratory_protection": {
      "applicable": <boolean>,
      "status": "<Pass | Warning | Not Applicable>",
      "notes": "<protective eyewear, dust masks, welding face shields>"
    }
  },
  "hazards_identified": [
    {
      "id": 1,
      "hazard_title": "<e.g., Unprotected Edge at Height, Missing Toe-Boards, Exposed Rebar, Trip Hazard>",
      "severity": "<Low | Medium | High | Critical>",
      "regulatory_code": "<e.g., OSHA 1926.501(b)(1) or IS 3764 / IS 456>",
      "location_in_image": "<e.g., Upper right scaffolding deck / Foreground ground surface>",
      "corrective_remedy": "<exact engineering or administrative corrective action required>"
    }
  ],
  "immediate_directives": [
    "<imperative action item 1>",
    "<imperative action item 2>"
  ]
}
Do not include any conversational filler, backticks, or markdown formatting outside the JSON block. Return ONLY pure valid JSON.
"""

CRACK_DIAGNOSTICS_PROMPT = """
You are an expert Senior Forensic Structural Engineer and Concrete Technology Specialist (IS 456 / ACI 224R-01).
Analyze the uploaded image of the concrete or masonry surface for defect identification, structural integrity diagnostics, and repair methodologies.

You MUST return ONLY a valid, strictly formatted JSON object with this EXACT schema:
{
  "defect_type": "<Hairline | Settlement | Structural Shear | Thermal Expansion | Spalling | Honeycombing>",
  "surface_material": "<e.g., Reinforced Concrete Beam / Slab, Brick Masonry with Plaster, Retaining Wall>",
  "estimated_crack_width_mm": <float, estimated average or maximum crack width in millimeters>,
  "crack_depth_assessment": "<Superficial | Moderate Core Penetration | Through-and-Through Full Depth>",
  "structural_urgency": "<Low | Medium | High | Critical Emergency>",
  "severity_score": <integer from 1 to 10, where 10 is immediate collapse danger>,
  "is_structural_threat": <boolean, true if compromises load-bearing capacity>,
  "root_causes": [
    "<specific root cause 1, e.g. Differential foundation settlement, Inadequate shear stirrups, Plastic shrinkage, Rebar corrosion carbonation>",
    "<specific root cause 2>"
  ],
  "is456_compliance_status": "<e.g., Exceeds IS 456:2000 Cl. 35.3.2 limit of 0.3mm for moderate exposure>",
  "recommended_engineering_repairs": [
    {
      "method": "<e.g., Low-Viscosity Epoxy Pressure Injection, Polymer Modified Mortar (PMM) Patching, Carbon Fiber Reinforced Polymer (CFRP) Laminate Stitching, Structural Re-Grouting>",
      "specifications": "<exact technical procedure, material grade, and application steps>",
      "estimated_repair_cost_range_inr": "<e.g., ₹12,000 - ₹28,000 per linear meter or patch>"
    }
  ],
  "preventive_monitoring": [
    "<e.g., Install Avongard acrylic crack tell-tale width gauge to track active movement over 60 days>",
    "<e.g., Conduct Non-Destructive Ultrasonic Pulse Velocity (UPV) and Rebound Hammer testing>"
  ]
}
Do not include any conversational filler, backticks, or markdown formatting outside the JSON block. Return ONLY pure valid JSON.
"""

CHATBOT_SYSTEM_PROMPT = """
You are "NirmanAI", an expert Senior Construction Project Director, Chief Civil Engineer, and Safety Specialist with 25+ years of experience across Indian and International megaprojects.
You are thoroughly versed in:
- IS 456:2000 (Plain and Reinforced Concrete)
- IS 1893 (Earthquake Resistant Design)
- IS 800 (Code of Practice for General Construction in Steel)
- NBC 2016 (National Building Code of India)
- OSHA 1926 (Construction Safety Regulations)
- CPM/PERT Project Scheduling, Primavera P6 & MS Project workflows
- Quantity Surveying, Rate Analysis, and Cost Estimation in INR (Lakhs & Crores)

Tone & Style:
- Authoritative, precise, pragmatic, and safety-conscious.
- Cite specific code clauses (e.g. "As per IS 456:2000 Clause 26.5.1...") whenever advising on concrete, steel, cover, curing, or reinforcement detailing.
- Format responses cleanly with bold key points, bullet lists, and clear calculation steps.
- Always recommend safety-first protocols.
"""
