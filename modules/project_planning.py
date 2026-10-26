"""
Tab 3 - Planning & Real Estate Valuation (Epic 3)
Interactive CapEx & market asset valuation in INR (Lakhs / Crores),
steel/cement requirement metrics per IS 456, milestone progress,
and conceptual 3D architectural rendering via Pollinations AI.
"""

import urllib.parse
import streamlit as st
import pandas as pd

from modules.config import CITY_TIERS


def format_inr(amount: float) -> str:
    """Formats a number into Indian Rupee denomination (Lakhs / Crores)."""
    if amount >= 10_000_000:
        crores = amount / 10_000_000
        return f"₹{crores:.2f} Cr"
    elif amount >= 100_000:
        lakhs = amount / 100_000
        return f"₹{lakhs:.2f} L"
    else:
        return f"₹{amount:,.0f}"


def render_project_planning_tab():
    """Renders the Planning, CapEx Valuation, and 3D Architectural Studio interface."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
                    border-left: 5px solid #3B82F6; padding: 18px 24px; border-radius: 8px; margin-bottom: 24px;">
            <h3 style="margin: 0; color: #60A5FA; font-size: 1.35rem; font-weight: 700;">
                🏗️ Epic 3: Construction Project Planning & Real Estate Valuation
            </h3>
            <p style="margin: 6px 0 0 0; color: #94A3B8; font-size: 0.95rem;">
                Dynamic cost estimation, CapEx expenditure modeling, and finished asset valuation in <strong>INR (Lakhs / Crores)</strong> 
                calibrated against <strong>Tier 1 / 2 / 3 Indian Metro benchmarks</strong>. Computes IS 456 material requirements 
                (Cement bags, Fe500D TMT Steel metric tonnes) and synthesizes conceptual 3D architectural renders.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Input Control Panel
    c1, c2, c3 = st.columns([1.2, 1, 1], gap="medium")

    with c1:
        city_tier_key = st.selectbox(
            "📍 Location Tier & Metro Cluster:",
            list(CITY_TIERS.keys()),
            index=0,
        )
        tier_data = CITY_TIERS[city_tier_key]
        tier_label = tier_data["tier"]

    with c2:
        available_structures = [k for k in tier_data.keys() if k != "tier"]
        structure_type = st.selectbox(
            "🏢 Structure & Asset Typology:",
            available_structures,
            index=1,
        )

    with c3:
        built_up_sqft = st.number_input(
            "📐 Built-Up Area (Sq.Ft):",
            min_value=500,
            max_value=2_000_000,
            value=25_000,
            step=1_000,
            help="Total gross super built-up area including common circulation and stilt parking.",
        )

    col_slider, col_style = st.columns([2, 1], gap="large")
    with col_slider:
        completion_pct = st.slider(
            "⏳ Construction Execution Progress (% Complete):",
            min_value=0,
            max_value=100,
            value=45,
            step=1,
            help="Current milestone completion status.",
        )
    with col_style:
        arch_style = st.selectbox(
            "🎨 Architectural Concept Style:",
            [
                "Modern Glass & Steel Biophilic High-Rise",
                "Brutalist Exposed RCC Minimalist Architecture",
                "Sustainable Contemporary Indian Vernacular with Terracotta",
                "Sleek Neo-Classical Luxury Development",
                "Industrial High-Tech Pre-Engineered Structure"
            ],
            index=0,
        )

    # Calculations
    struct_benchmark = tier_data[structure_type]
    cost_per_sqft = struct_benchmark["cost_per_sqft"]
    market_rate_sqft = struct_benchmark["market_rate_sqft"]
    cement_factor = struct_benchmark["cement_factor"]
    steel_factor_kg = struct_benchmark["steel_factor_kg"]

    total_project_budget = built_up_sqft * cost_per_sqft
    capex_incurred = total_project_budget * (completion_pct / 100.0)
    capex_remaining = total_project_budget - capex_incurred

    # Current asset valuation based on completion stage + land & intrinsic development value
    # Land & appreciation factor usually accounts for 40% intrinsic floor + 60% construction delta
    stage_multiplier = 0.40 + (0.60 * (completion_pct / 100.0))
    current_asset_valuation = (built_up_sqft * market_rate_sqft) * stage_multiplier
    finished_market_valuation = built_up_sqft * market_rate_sqft
    unrealized_equity_spread = finished_market_valuation - total_project_budget

    # Material calculations per IS 456
    total_cement_bags = int(built_up_sqft * cement_factor)
    total_steel_tonnes = (built_up_sqft * steel_factor_kg) / 1000.0
    cement_used = int(total_cement_bags * (completion_pct / 100.0))
    steel_used = total_steel_tonnes * (completion_pct / 100.0)

    # Milestone identification
    if completion_pct < 15:
        milestone_title = "Substructure: Earthwork, Piling & Foundation Raft"
        milestone_color = "#3B82F6"
    elif completion_pct < 45:
        milestone_title = "Superstructure: RCC Columns, Shear Walls & Slabs"
        milestone_color = "#F59E0B"
    elif completion_pct < 75:
        milestone_title = "Building Envelope: AAC Blockwork, MEP Piping & Plaster"
        milestone_color = "#8B5CF6"
    elif completion_pct < 95:
        milestone_title = "Finishing: Flooring, Glazing, Electrical Substation & Elevators"
        milestone_color = "#10B981"
    else:
        milestone_title = "Handover & Commissioning: Occupancy Certificate (OC) Stage"
        milestone_color = "#059669"

    st.markdown("---")

    # Milestone Progress Bar
    st.markdown(
        f"""
        <div style="background: #131B2A; border: 1px solid #1E293B; border-radius: 10px; padding: 16px 20px; margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-weight: 700; color: #F1F5F9; font-size: 1.05rem;">
                    📍 Active Construction Milestone: <span style="color: {milestone_color};">{milestone_title}</span>
                </span>
                <span style="background: #1E293B; color: #38BDF8; padding: 4px 12px; border-radius: 12px; font-weight: 700;">
                    {completion_pct}% Complete
                </span>
            </div>
            <div style="background: #0B0F17; height: 12px; border-radius: 6px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #3B82F6 0%, #10B981 100%); width: {completion_pct}%; height: 100%;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 8px; color: #64748B; font-size: 0.78rem;">
                <span>0% Earthwork</span>
                <span>25% RCC Staging</span>
                <span>50% Mid-Rise Slab</span>
                <span>75% MEP & Facade</span>
                <span>100% Handover</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Primary Financial & Valuation Cards
    st.markdown("#### 💰 Capital Expenditure (CapEx) & Real Estate Valuation (INR)")
    f1, f2, f3, f4 = st.columns(4)

    with f1:
        st.markdown(
            f"""
            <div style="background: #131B2A; border: 1px solid #1E293B; border-radius: 10px; padding: 16px; text-align: center;">
                <span style="color: #94A3B8; font-size: 0.85rem; text-transform: uppercase;">Total Project Budget</span>
                <h1 style="color: #F8FAFC; margin: 8px 0; font-size: 2.2rem; font-weight: 800;">{format_inr(total_project_budget)}</h1>
                <span style="color: #64748B; font-size: 0.8rem;">₹{cost_per_sqft:,}/sqft Base Cost</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f2:
        st.markdown(
            f"""
            <div style="background: #131B2A; border: 1px solid #1E293B; border-radius: 10px; padding: 16px; text-align: center;">
                <span style="color: #94A3B8; font-size: 0.85rem; text-transform: uppercase;">CapEx Incurred to Date</span>
                <h1 style="color: #F59E0B; margin: 8px 0; font-size: 2.2rem; font-weight: 800;">{format_inr(capex_incurred)}</h1>
                <span style="color: #64748B; font-size: 0.8rem;">Remaining: {format_inr(capex_remaining)}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f3:
        st.markdown(
            f"""
            <div style="background: #131B2A; border: 1px solid #1E293B; border-radius: 10px; padding: 16px; text-align: center;">
                <span style="color: #94A3B8; font-size: 0.85rem; text-transform: uppercase;">Current Stage Asset Value</span>
                <h1 style="color: #38BDF8; margin: 8px 0; font-size: 2.2rem; font-weight: 800;">{format_inr(current_asset_valuation)}</h1>
                <span style="color: #64748B; font-size: 0.8rem;">Market Stage Equity</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f4:
        st.markdown(
            f"""
            <div style="background: #131B2A; border: 1px solid #1E293B; border-radius: 10px; padding: 16px; text-align: center;">
                <span style="color: #94A3B8; font-size: 0.85rem; text-transform: uppercase;">Finished Market Valuation</span>
                <h1 style="color: #10B981; margin: 8px 0; font-size: 2.2rem; font-weight: 800;">{format_inr(finished_market_valuation)}</h1>
                <span style="color: #34D399; font-size: 0.8rem; font-weight: 600;">Gain: +{format_inr(unrealized_equity_spread)}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Material Quantification Section per IS 456
    st.markdown("---")
    col_mat, col_render = st.columns([1, 1], gap="large")

    with col_mat:
        st.markdown("#### 🧱 IS 456 Material Quantification & Thumb Rules")

        st.markdown(
            f"""
            <div style="background: #131B2A; border: 1px solid #1E293B; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #F8FAFC; font-weight: 600;">🏗️ Cement Requirement (50 kg Bags)</span>
                    <strong style="color: #60A5FA; font-size: 1.15rem;">{total_cement_bags:,} Bags</strong>
                </div>
                <div style="color: #94A3B8; font-size: 0.82rem; margin-top: 4px;">
                    Factor: {cement_factor} bags/sq.ft | Consumed so far: <strong>{cement_used:,} Bags</strong>
                </div>
            </div>

            <div style="background: #131B2A; border: 1px solid #1E293B; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #F8FAFC; font-weight: 600;">⚙️ TMT Fe500D Reinforcement Steel</span>
                    <strong style="color: #F59E0B; font-size: 1.15rem;">{total_steel_tonnes:.1f} MT</strong>
                </div>
                <div style="color: #94A3B8; font-size: 0.82rem; margin-top: 4px;">
                    Factor: {steel_factor_kg} kg/sq.ft | Procured & tied: <strong>{steel_used:.1f} MT</strong>
                </div>
            </div>

            <div style="background: #131B2A; border: 1px solid #1E293B; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #F8FAFC; font-weight: 600;">🪨 Coarse Aggregate (20mm / 10mm)</span>
                    <strong style="color: #A78BFA; font-size: 1.15rem;">{int(built_up_sqft * 1.25):,} cu.ft</strong>
                </div>
                <div style="color: #94A3B8; font-size: 0.82rem; margin-top: 4px;">
                    Standard IS 383 grading for high-performance concrete.
                </div>
            </div>

            <div style="background: #131B2A; border: 1px solid #1E293B; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #F8FAFC; font-weight: 600;">🏖️ Manufactured Sand (M-Sand / Zone II)</span>
                    <strong style="color: #34D399; font-size: 1.15rem;">{int(built_up_sqft * 1.65):,} cu.ft</strong>
                </div>
                <div style="color: #94A3B8; font-size: 0.82rem; margin-top: 4px;">
                    Eco-compliant washed quarry sand conforming to IS 383 Zone II.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_render:
        st.markdown("#### 🎨 Conceptual 3D Architectural Rendering Studio")
        st.caption("Integrated Pollinations AI generative prompt builder synthesizing photorealistic project visuals.")

        # Construct dynamic prompt
        clean_style = arch_style.replace("Architecture", "").strip()
        pollinations_prompt = (
            f"Photorealistic 8k architectural exterior photograph of {structure_type}, "
            f"{built_up_sqft:,} sq ft built up, {clean_style}, located in modern {tier_label} Indian metropolis, "
            f"golden hour lighting, architectural digest masterpiece photography, ray tracing, ultra-detailed landscaping"
        )

        encoded_prompt = urllib.parse.quote(pollinations_prompt)
        pollinations_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=500&seed=42&nologo=true"

        with st.expander("📝 View AI Architectural Prompt"):
            st.text_area("Synthesized Vision Prompt:", value=pollinations_prompt, height=85)

        generate_render = st.button("✨ Generate 3D Concept Visual", type="secondary", use_container_width=True)

        # Show render either if user clicked or by default preview
        if generate_render or "show_render" in st.session_state:
            st.session_state["show_render"] = True
            with st.spinner("🎨 Synthesizing 3D Architectural Visualization via Pollinations Engine..."):
                try:
                    st.image(
                        pollinations_url,
                        caption=f"Conceptual 3D Visual: {structure_type} ({tier_label})",
                        use_container_width=True,
                    )
                    st.success("✅ Photorealistic AI Architectural Concept Render Generated Successfully!")
                except Exception as e:
                    st.info(f"Visual generation endpoint ready: [Open Direct Concept Link]({pollinations_url})")
        else:
            st.info("Click 'Generate 3D Concept Visual' to synthesize a custom architectural perspective.")
