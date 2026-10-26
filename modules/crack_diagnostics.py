"""
Tab 2 - Crack Diagnostics & Structural Integrity (Epic 2)
Analyzes concrete/wall surfaces, classifies defect types (Hairline, Settlement,
Structural Shear, Thermal Expansion, Spalling), evaluates width & severity,
and prescribes engineering repairs per IS 456 / ACI standards.
"""

import json
import os
import streamlit as st
from PIL import Image

from modules.gemini_client import ConstructionAIClient
from sample_data.sample_images import CRACK_SAMPLE_PATH, CRACK_HAIRLINE_PATH


def render_crack_diagnostics_tab(ai_client: ConstructionAIClient):
    """Renders the forensic concrete crack diagnostic and structural integrity interface."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%);
                    border-left: 5px solid #EF4444; padding: 18px 24px; border-radius: 8px; margin-bottom: 24px;">
            <h3 style="margin: 0; color: #F87171; font-size: 1.35rem; font-weight: 700;">
                🧱 Epic 2: Concrete Crack Diagnostics & Structural Integrity
            </h3>
            <p style="margin: 6px 0 0 0; color: #94A3B8; font-size: 0.95rem;">
                Forensic structural AI classifying crack types (<strong>Hairline</strong>, <strong>Settlement</strong>, 
                <strong>Structural Shear</strong>, <strong>Thermal Expansion</strong>, <strong>Spalling</strong>). 
                Measures crack aperture width (mm), quantifies collapse risks against <strong>IS 456:2000 Cl. 35.3.2</strong>, 
                and prescribes structural repair engineering specs (Epoxy Pressure Injection, PMM, CFRP Stitching).
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_input, col_preview = st.columns([1, 1], gap="large")

    with col_input:
        st.subheader("📸 Surface Image Ingestion")
        
        input_source = st.radio(
            "Select Crack Image Source:",
            ["Use Built-in Calibrated Defect Samples", "Upload Custom Surface Photo"],
            horizontal=True,
        )

        selected_image = None
        scenario_idx = 0

        if input_source == "Use Built-in Calibrated Defect Samples":
            sample_choice = st.selectbox(
                "Choose Calibrated Defect Scenario:",
                [
                    "Defect 1: Structural Shear Diagonal Crack (RCC Transfer Beam - Critical)",
                    "Defect 2: Superficial Hairline Shrinkage Crazing (Slab Surface - Minor)",
                    "Defect 3: Concrete Spalling & Exposed Corroded Rebar (Column Face - Emergency)",
                ],
            )
            if "Defect 1" in sample_choice:
                scenario_idx = 0
                target_path = CRACK_SAMPLE_PATH
            elif "Defect 2" in sample_choice:
                scenario_idx = 1
                target_path = CRACK_HAIRLINE_PATH
            else:
                scenario_idx = 2
                target_path = CRACK_SAMPLE_PATH

            if os.path.exists(target_path):
                selected_image = Image.open(target_path)
                st.caption(f"📁 Loaded calibrated defect asset: `{os.path.basename(target_path)}`")
        else:
            uploaded_file = st.file_uploader(
                "Upload Concrete / Masonry Surface Photo (JPG/PNG)",
                type=["jpg", "jpeg", "png"],
                help="Ensure good lighting and include scale or rebar if available.",
            )
            if uploaded_file:
                selected_image = Image.open(uploaded_file)

        diagnose_button = st.button(
            "🔬 Perform Forensic Structural Diagnosis",
            type="primary",
            use_container_width=True,
            disabled=(selected_image is None),
        )

    with col_preview:
        st.subheader("🔍 Surface Inspection Lens")
        if selected_image:
            st.image(selected_image, caption="Analyzed Surface Geometry", use_container_width=True)
        else:
            st.info("👈 Please select or upload a concrete/wall defect image to begin analysis.")

    # Execute Diagnostic Analysis
    if diagnose_button and selected_image:
        with st.spinner("🔬 Running Forensic Vision Model (IS 456 & ACI 224R Structural Diagnosis)..."):
            diag_result, is_live, engine_note = ai_client.analyze_crack_diagnostics(
                selected_image, scenario_index=scenario_idx
            )
            st.session_state["crack_diag_data"] = diag_result
            st.session_state["crack_diag_engine"] = engine_note
            st.session_state["crack_is_live"] = is_live

    # Display Results
    if "crack_diag_data" in st.session_state:
        diag = st.session_state["crack_diag_data"]
        engine_note = st.session_state.get("crack_diag_engine", "")
        is_live = st.session_state.get("crack_is_live", False)

        st.markdown("---")
        badge_color = "#10B981" if is_live else "#EF4444"
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <h3 style="margin: 0; color: #F1F5F9;">📋 Forensic Structural Diagnostic Report</h3>
                <span style="background: {badge_color}22; color: {badge_color}; border: 1px solid {badge_color};
                             padding: 4px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 600;">
                    {engine_note}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        defect_type = diag.get("defect_type", "Unknown")
        width_mm = diag.get("estimated_crack_width_mm", 0.0)
        urgency = diag.get("structural_urgency", "Medium")
        severity_score = diag.get("severity_score", 5)
        is_threat = diag.get("is_structural_threat", False)

        # Style colors based on severity
        if severity_score >= 8 or urgency in ["High", "Critical Emergency"]:
            sev_color = "#EF4444"
            urgency_bg = "#7F1D1D"
        elif severity_score >= 5 or urgency in ["Medium"]:
            sev_color = "#F59E0B"
            urgency_bg = "#78350F"
        else:
            sev_color = "#10B981"
            urgency_bg = "#064E3B"

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(
                f"""
                <div style="background: #131B2A; border: 1px solid #1E293B; border-radius: 10px; padding: 16px; text-align: center;">
                    <span style="color: #94A3B8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">Defect Classification</span>
                    <h2 style="color: #F8FAFC; margin: 8px 0; font-size: 1.5rem; font-weight: 700;">{defect_type}</h2>
                    <span style="color: #94A3B8; font-size: 0.8rem;">{diag.get('surface_material', 'RCC Element')}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m2:
            st.markdown(
                f"""
                <div style="background: #131B2A; border: 1px solid #1E293B; border-radius: 10px; padding: 16px; text-align: center;">
                    <span style="color: #94A3B8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">Aperture Width</span>
                    <h1 style="color: {sev_color}; margin: 8px 0; font-size: 2.5rem; font-weight: 800;">{width_mm} <span style="font-size: 1.1rem; color: #94A3B8;">mm</span></h1>
                    <span style="color: #94A3B8; font-size: 0.8rem;">{diag.get('crack_depth_assessment', 'Depth Profile')}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m3:
            st.markdown(
                f"""
                <div style="background: #131B2A; border: 1px solid #1E293B; border-radius: 10px; padding: 16px; text-align: center;">
                    <span style="color: #94A3B8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">Severity Index</span>
                    <h1 style="color: {sev_color}; margin: 8px 0; font-size: 2.5rem; font-weight: 800;">{severity_score}<span style="font-size: 1.1rem; color: #64748B;">/10</span></h1>
                    <span style="color: #94A3B8; font-size: 0.8rem;">Structural Risk Metric</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m4:
            st.markdown(
                f"""
                <div style="background: #131B2A; border: 1px solid #1E293B; border-radius: 10px; padding: 16px; text-align: center;">
                    <span style="color: #94A3B8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">Structural Urgency</span>
                    <div style="margin: 12px 0;">
                        <span style="background: {urgency_bg}; color: #F8FAFC; border: 1px solid {sev_color};
                                     padding: 6px 12px; border-radius: 8px; font-weight: 700; font-size: 0.95rem;">
                            {urgency}
                        </span>
                    </div>
                    <span style="color: {'#EF4444' if is_threat else '#10B981'}; font-weight: 600; font-size: 0.8rem;">
                        {'⚠️ THREATENS INTEGRITY' if is_threat else '✅ Non-Structural'}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # IS 456 Compliance Banner
        is456_status = diag.get("is456_compliance_status", "")
        if is456_status:
            st.markdown(
                f"""
                <div style="margin: 20px 0; background: #0F172A; border-left: 4px solid {sev_color}; padding: 14px 18px; border-radius: 6px;">
                    <strong style="color: {sev_color};">IS 456:2000 Code Compliance Audit:</strong>
                    <span style="color: #CBD5E1; margin-left: 8px;">{is456_status}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Root Causes & Engineering Repairs
        col_causes, col_repairs = st.columns([1, 1], gap="large")

        with col_causes:
            st.markdown("#### 🔬 Forensic Root Cause Analysis")
            causes = diag.get("root_causes", [])
            for c in causes:
                st.markdown(
                    f"""
                    <div style="background: #131B2A; border: 1px solid #1E293B; border-radius: 8px; padding: 12px 14px; margin-bottom: 10px;">
                        <div style="display: flex; align-items: flex-start;">
                            <span style="color: #F59E0B; font-size: 1.1rem; margin-right: 10px;">🔍</span>
                            <span style="color: #E2E8F0; font-size: 0.9rem; line-height: 1.4;">{c}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("#### 📡 Preventive Structural Monitoring Protocols")
            monitoring = diag.get("preventive_monitoring", [])
            for m in monitoring:
                st.markdown(f"- 📈 **{m}**")

        with col_repairs:
            st.markdown("#### 🛠️ Recommended Engineering Repair Methodologies")
            repairs = diag.get("recommended_engineering_repairs", [])
            for r in repairs:
                st.markdown(
                    f"""
                    <div style="background: #131B2A; border-left: 4px solid #10B981; border-top: 1px solid #1E293B;
                                border-right: 1px solid #1E293B; border-bottom: 1px solid #1E293B;
                                border-radius: 8px; padding: 14px 16px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <strong style="color: #34D399; font-size: 0.95rem;">{r.get('method', 'Repair Method')}</strong>
                            <span style="background: #064E3B; color: #6EE7B7; border: 1px solid #059669;
                                         padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 700;">
                                {r.get('estimated_repair_cost_range_inr', 'Est. Cost')}
                            </span>
                        </div>
                        <p style="color: #94A3B8; font-size: 0.85rem; margin: 0; line-height: 1.4;">
                            {r.get('specifications', '')}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Download Report
        st.markdown("---")
        st.markdown("#### 📥 Diagnostic Report Contract")
        json_str = json.dumps(diag, indent=2)
        c1, c2 = st.columns([1, 2])
        with c1:
            st.download_button(
                label="📥 Download Crack Diagnostic JSON",
                data=json_str,
                file_name="structural_crack_diagnostic_report.json",
                mime="application/json",
                use_container_width=True,
            )
        with c2:
            with st.expander("👁️ View Full JSON Contract"):
                st.code(json_str, language="json")
