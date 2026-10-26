"""
Tab 1 - Site Safety & PPE Audit (Epic 2)
Analyzes worker PPE compliance, OSHA & IS 456 regulations,
renders metrics, hazard breakdown, and structured downloadable reports.
"""

import json
import os
import streamlit as st
from PIL import Image

from modules.config import APP_TITLE
from modules.gemini_client import ConstructionAIClient
from sample_data.sample_images import PPE_SAMPLE_PATH


def render_safety_audit_tab(ai_client: ConstructionAIClient):
    """Renders the comprehensive Site Safety & PPE Audit interface."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%);
                    border-left: 5px solid #F59E0B; padding: 18px 24px; border-radius: 8px; margin-bottom: 24px;">
            <h3 style="margin: 0; color: #F59E0B; font-size: 1.35rem; font-weight: 700;">
                🦺 Epic 2: Site Safety Vision & PPE Compliance Audit
            </h3>
            <p style="margin: 6px 0 0 0; color: #94A3B8; font-size: 0.95rem;">
                Automated multi-modal inspection under <strong>OSHA 1926</strong>, <strong>IS 15844</strong> (High-Vis), 
                <strong>IS 2925</strong> (Helmets), and <strong>NBC 2016 Part 7</strong>. Detects worker protective equipment, 
                quantifies risk severity, and issues imperative corrective action remedies.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_input, col_preview = st.columns([1, 1], gap="large")

    with col_input:
        st.subheader("📷 Site Photo Ingestion")
        
        input_source = st.radio(
            "Select Photo Source:",
            ["Use Built-in Calibrated Sample", "Upload Custom Site Image"],
            horizontal=True,
        )

        selected_image = None
        scenario_idx = 0

        if input_source == "Use Built-in Calibrated Sample":
            sample_choice = st.selectbox(
                "Choose Sample Incident Scenario:",
                [
                    "Scenario A: Multi-Level Scaffolding & Excavation Zone (Mixed Compliance)",
                    "Scenario B: High-Elevation Shuttering Deck (Critical Fall Hazards)",
                ],
            )
            scenario_idx = 0 if "Scenario A" in sample_choice else 1
            if os.path.exists(PPE_SAMPLE_PATH):
                selected_image = Image.open(PPE_SAMPLE_PATH)
                st.caption(f"📁 Loaded calibrated test asset: `{os.path.basename(PPE_SAMPLE_PATH)}`")
        else:
            uploaded_file = st.file_uploader(
                "Upload Construction Site Photo (JPG/PNG)",
                type=["jpg", "jpeg", "png"],
                help="Max recommended resolution 4K. Supported standards: OSHA 1926, IS 456.",
            )
            if uploaded_file:
                selected_image = Image.open(uploaded_file)

        analyze_button = st.button(
            "🚀 Run AI Multimodal Safety Audit",
            type="primary",
            use_container_width=True,
            disabled=(selected_image is None),
        )

    with col_preview:
        st.subheader("🖼️ Site Visual Inspection")
        if selected_image:
            st.image(selected_image, caption="Analyzed Construction Zone Visual", use_container_width=True)
        else:
            st.info("👈 Please select or upload a construction site photo to begin.")

    # Execute Audit Analysis
    if analyze_button and selected_image:
        with st.spinner("🔍 Running Multi-Modal Vision Model (OSHA & IS 456 Compliance Inspection)..."):
            audit_result, is_live, engine_note = ai_client.analyze_site_safety(
                selected_image, scenario_index=scenario_idx
            )
            st.session_state["safety_audit_data"] = audit_result
            st.session_state["safety_audit_engine"] = engine_note
            st.session_state["safety_is_live"] = is_live

    # Display Results if Available in Session State
    if "safety_audit_data" in st.session_state:
        audit = st.session_state["safety_audit_data"]
        engine_note = st.session_state.get("safety_audit_engine", "")
        is_live = st.session_state.get("safety_is_live", False)

        st.markdown("---")
        
        # Engine execution badge
        badge_color = "#10B981" if is_live else "#F59E0B"
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <h3 style="margin: 0; color: #F1F5F9;">📊 Safety Audit Inspection Report</h3>
                <span style="background: {badge_color}22; color: {badge_color}; border: 1px solid {badge_color};
                             padding: 4px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 600;">
                    {engine_note}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Primary Metrics Row
        safety_score = audit.get("safety_score", 0)
        overall_status = audit.get("overall_status", "Needs Attention")
        workers_count = audit.get("workers_detected", 0)

        # Determine metric color
        if safety_score >= 80:
            score_color = "#10B981"
            status_badge_bg = "#064E3B"
        elif safety_score >= 60:
            score_color = "#F59E0B"
            status_badge_bg = "#78350F"
        else:
            score_color = "#EF4444"
            status_badge_bg = "#7F1D1D"

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(
                f"""
                <div style="background: #131B2A; border: 1px solid #1E293B; border-radius: 10px; padding: 16px; text-align: center;">
                    <span style="color: #94A3B8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">Safety Score</span>
                    <h1 style="color: {score_color}; margin: 8px 0; font-size: 2.8rem; font-weight: 800;">{safety_score}<span style="font-size: 1.2rem; color: #64748B;">/100</span></h1>
                    <span style="color: #94A3B8; font-size: 0.8rem;">OSHA / IS Index</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m2:
            st.markdown(
                f"""
                <div style="background: #131B2A; border: 1px solid #1E293B; border-radius: 10px; padding: 16px; text-align: center;">
                    <span style="color: #94A3B8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">Site Status</span>
                    <div style="margin: 12px 0;">
                        <span style="background: {status_badge_bg}; color: #F8FAFC; border: 1px solid {score_color};
                                     padding: 6px 14px; border-radius: 8px; font-weight: 700; font-size: 1.1rem;">
                            {overall_status}
                        </span>
                    </div>
                    <span style="color: #94A3B8; font-size: 0.8rem;">Audit Classification</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m3:
            st.markdown(
                f"""
                <div style="background: #131B2A; border: 1px solid #1E293B; border-radius: 10px; padding: 16px; text-align: center;">
                    <span style="color: #94A3B8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">Workers Inspected</span>
                    <h1 style="color: #38BDF8; margin: 8px 0; font-size: 2.8rem; font-weight: 800;">{workers_count}</h1>
                    <span style="color: #94A3B8; font-size: 0.8rem;">Personnel in Visual Field</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m4:
            hazards_list = audit.get("hazards_identified", [])
            critical_count = sum(1 for h in hazards_list if h.get("severity") in ["High", "Critical"])
            hazard_color = "#EF4444" if critical_count > 0 else "#10B981"
            st.markdown(
                f"""
                <div style="background: #131B2A; border: 1px solid #1E293B; border-radius: 10px; padding: 16px; text-align: center;">
                    <span style="color: #94A3B8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">Severe Hazards</span>
                    <h1 style="color: {hazard_color}; margin: 8px 0; font-size: 2.8rem; font-weight: 800;">{critical_count}</h1>
                    <span style="color: #94A3B8; font-size: 0.8rem;">Immediate Attention Required</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Executive Summary Alert
        summary = audit.get("audit_summary", "")
        if summary:
            st.markdown(
                f"""
                <div style="margin-top: 20px; background: #0F172A; border-left: 4px solid #38BDF8; padding: 14px 18px; border-radius: 6px;">
                    <strong style="color: #38BDF8;">Audit Executive Summary:</strong>
                    <span style="color: #CBD5E1; margin-left: 8px;">{summary}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Tabular PPE Checklist & Hazard Breakdown
        col_ppe, col_hazards = st.columns([1, 1], gap="large")

        with col_ppe:
            st.markdown("#### 🛡️ PPE Compliance Verification Matrix")
            ppe_data = audit.get("ppe_detection", {})

            for item_key, item_title in [
                ("safety_helmets", "Hard Hats / Safety Helmets (IS 2925 / OSHA 1926.100)"),
                ("high_visibility_vests", "High-Visibility Fluorescent Vests (IS 15844)"),
                ("safety_footwear_boots", "Puncture-Resistant Steel-Toe Boots (IS 15298)"),
                ("safety_harness_fall_protection", "Fall Arrest System & Harness (OSHA 1926.502)"),
                ("eye_face_respiratory_protection", "Eye, Face & Respiratory Shielding"),
            ]:
                val = ppe_data.get(item_key, {})
                status = val.get("status", "N/A")
                notes = val.get("notes", "No notes recorded.")
                comp = val.get("compliant_count", "-")
                non_comp = val.get("non_compliant_count", "-")

                if status in ["Pass", "Compliant"]:
                    pill_style = "background: #064E3B; color: #34D399; border: 1px solid #059669;"
                    icon = "✅"
                elif status in ["Warning"]:
                    pill_style = "background: #78350F; color: #FBBF24; border: 1px solid #D97706;"
                    icon = "⚠️"
                elif status in ["Fail", "Non-Compliant"]:
                    pill_style = "background: #7F1D1D; color: #F87171; border: 1px solid #DC2626;"
                    icon = "❌"
                else:
                    pill_style = "background: #1E293B; color: #94A3B8; border: 1px solid #475569;"
                    icon = "ℹ️"

                counts_str = f"Compliant: {comp} | Non-Compliant: {non_comp}" if comp != "-" else ""

                st.markdown(
                    f"""
                    <div style="background: #131B2A; border: 1px solid #1E293B; border-radius: 8px; padding: 12px 16px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <span style="font-weight: 600; color: #F1F5F9; font-size: 0.95rem;">{icon} {item_title}</span>
                            <span style="{pill_style} padding: 2px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700;">{status}</span>
                        </div>
                        <div style="color: #94A3B8; font-size: 0.85rem; line-height: 1.4;">{notes}</div>
                        {f'<div style="color: #64748B; font-size: 0.78rem; margin-top: 4px; font-weight: 500;">{counts_str}</div>' if counts_str else ''}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with col_hazards:
            st.markdown("#### 🚨 Identified Hazards & OSHA Directives")
            hazards = audit.get("hazards_identified", [])
            
            if not hazards:
                st.success("No critical or high-risk hazards identified in visual sweep.")
            else:
                for h in hazards:
                    sev = h.get("severity", "Low")
                    if sev == "Critical":
                        border_col = "#EF4444"
                        sev_bg = "#7F1D1D"
                        sev_text = "#FCA5A5"
                    elif sev == "High":
                        border_col = "#F97316"
                        sev_bg = "#7C2D12"
                        sev_text = "#FDBA74"
                    elif sev == "Medium":
                        border_col = "#F59E0B"
                        sev_bg = "#78350F"
                        sev_text = "#FDE68A"
                    else:
                        border_col = "#3B82F6"
                        sev_bg = "#1E3A8A"
                        sev_text = "#93C5FD"

                    st.markdown(
                        f"""
                        <div style="background: #131B2A; border-left: 4px solid {border_col}; border-top: 1px solid #1E293B;
                                    border-right: 1px solid #1E293B; border-bottom: 1px solid #1E293B;
                                    border-radius: 8px; padding: 12px 16px; margin-bottom: 12px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <strong style="color: #F8FAFC; font-size: 0.95rem;">{h.get('hazard_title', 'Hazard')}</strong>
                                <span style="background: {sev_bg}; color: {sev_text}; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 700;">
                                    {sev.upper()} SEVERITY
                                </span>
                            </div>
                            <div style="color: #64748B; font-size: 0.78rem; margin: 4px 0;">
                                📜 Standard: <span style="color: #94A3B8;">{h.get('regulatory_code', 'OSHA 1926')}</span> | 
                                📍 Zone: <span style="color: #94A3B8;">{h.get('location_in_image', 'General Site')}</span>
                            </div>
                            <div style="background: #0B0F17; border-radius: 4px; padding: 8px 10px; margin-top: 6px;">
                                <span style="color: #10B981; font-size: 0.8rem; font-weight: 600;">🛠️ Remedy:</span>
                                <span style="color: #CBD5E1; font-size: 0.82rem;"> {h.get('corrective_remedy', '')}</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            directives = audit.get("immediate_directives", [])
            if directives:
                st.markdown("#### ⚡ Immediate Directives")
                for d in directives:
                    st.markdown(f"- ⚠️ **{d}**")

        # Downloadable JSON Report & Export Section
        st.markdown("---")
        st.markdown("#### 📥 Official Audit Export & Structured JSON Contract")
        
        json_str = json.dumps(audit, indent=2)
        c_exp1, c_exp2 = st.columns([1, 2])
        with c_exp1:
            st.download_button(
                label="📥 Download Structured JSON Report",
                data=json_str,
                file_name="construction_site_safety_audit.json",
                mime="application/json",
                use_container_width=True,
            )
        with c_exp2:
            with st.expander("👁️ View Pure JSON Contract"):
                st.code(json_str, language="json")
