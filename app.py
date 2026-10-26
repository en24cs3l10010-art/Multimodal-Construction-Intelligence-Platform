"""
Multimodal Construction Intelligence Platform
Skill Wallet Capstone Project 1 - Full-Stack Streamlit Application

Decision-support system analyzing site photos to audit PPE safety compliance,
classify concrete cracks with severity scores, estimate construction costs
and real estate valuation in INR, and provide weather-aware daily protocols.
"""

import os
import streamlit as st
from PIL import Image

# Page Configuration - Must be first Streamlit command
st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom High-End Modern CSS Injection
st.markdown(
    """
    <style>
        /* Modern Glassmorphic Dark Architecture Theme */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Streamlit Top Header & Menu clean up */
        header[data-testid="stHeader"] {
            background-color: transparent !important;
        }

        /* Container padding */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 3rem !important;
            max-width: 96% !important;
        }

        /* Main App Header Banner */
        .platform-header {
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%);
            border: 1px solid rgba(245, 158, 11, 0.25);
            border-radius: 12px;
            padding: 24px 30px;
            margin-bottom: 24px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.4);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .platform-title {
            color: #F8FAFC;
            font-size: 1.85rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .platform-title span.badge {
            background: #F59E0B;
            color: #0F172A;
            font-size: 0.75rem;
            font-weight: 800;
            padding: 4px 10px;
            border-radius: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .platform-desc {
            color: #94A3B8;
            font-size: 0.92rem;
            margin-top: 8px;
            line-height: 1.5;
            max-width: 850px;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0A0E17 !important;
            border-right: 1px solid #1E293B;
        }

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #111827;
            padding: 8px;
            border-radius: 10px;
            border: 1px solid #1F2937;
        }

        .stTabs [data-baseweb="tab"] {
            height: 48px;
            white-space: pre-wrap;
            border-radius: 8px;
            color: #94A3B8;
            font-weight: 600;
            padding: 8px 20px;
            transition: all 0.2s ease;
        }

        .stTabs [aria-selected="true"] {
            background-color: #1F2937 !important;
            color: #F59E0B !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
            border-bottom: 2px solid #F59E0B !important;
        }

        /* Buttons */
        .stButton>button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }

        .stButton>button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.25);
        }

        /* Code block font */
        code {
            font-family: 'JetBrains Mono', monospace !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Import Application Modules
from modules.config import APP_TITLE, APP_SUBTITLE, APP_VERSION
from modules.gemini_client import ConstructionAIClient
from modules.safety_audit import render_safety_audit_tab
from modules.crack_diagnostics import render_crack_diagnostics_tab
from modules.project_planning import render_project_planning_tab
from modules.daily_assistant import render_daily_assistant_tab

# Ensure sample assets exist
import sample_data.sample_images


def main():
    # ----------------- SIDEBAR CONFIGURATION -----------------
    with st.sidebar:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                <span style="font-size: 2rem;">🏗️</span>
                <div>
                    <h3 style="margin: 0; color: #F1F5F9; font-size: 1.15rem; font-weight: 700;">NirmanVision AI</h3>
                    <span style="color: #64748B; font-size: 0.75rem;">Skill Wallet Capstone 1</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # 1. Secure Gemini API Key Input with Graceful Fallback
        st.markdown("### 🔑 AI Engine Configuration")
        api_key_input = st.text_input(
            "Google Gemini API Key:",
            type="password",
            value=os.environ.get("GEMINI_API_KEY", ""),
            placeholder="AIzaSy... (Leave empty for Demo Mode)",
            help="Your key is stored securely in session state only. If left blank, the platform seamlessly engages pre-calibrated Demonstration Mode.",
        )

        # Initialize AI Client
        ai_client = ConstructionAIClient(api_key=api_key_input.strip() if api_key_input else None)

        if ai_client.is_live:
            st.success("🟢 Live Gemini Multi-Modal Connected (Gemini 2.5 / 2.0 Flash)")
        else:
            st.info("⚡ Mode: **High-Fidelity Demonstration** (Fallback active; pre-calibrated IS 456 & OSHA dataset ready).")

        st.markdown("---")

        # 2. Kanban Epics Coverage Guide
        with st.expander("📌 Kanban Epics Coverage", expanded=False):
            st.markdown(
                """
                - **Pre-reqs**: Python 3.9+, Streamlit, Zero DB dependencies.
                - **Epic 1**: Requirements & Secure Environment.
                - **Epic 2**: PPE Safety Vision & Forensic Crack Diagnostics.
                - **Epic 3**: Project Planning, Real Estate CapEx & Valuation.
                - **Epic 4**: Multimodal AI & Strict JSON Contracts.
                - **Epic 5**: Daily Site Assistant & Weather Protocols.
                - **Epic 6**: Interface Polish, Testing & Streamlit Cloud 1-Click Deploy.
                """
            )

        # 3. Governing Engineering Standards
        with st.expander("🏛️ Indian & Global Standards", expanded=False):
            st.markdown(
                """
                - **IS 456:2000**: Plain & Reinforced Concrete
                - **IS 15844 / IS 2925**: High-Vis & Industrial Hard Hats
                - **IS 15298**: Safety Footwear
                - **IS 3764**: Excavation Safety
                - **IS 7861 (Part 1)**: Hot-Weather Concreting
                - **OSHA 1926**: US Construction Safety
                - **NBC 2016**: National Building Code of India
                """
            )

        st.markdown("---")
        st.caption("🚀 Designed for 1-Click Streamlit Community Cloud Deployment.")
        st.caption(f"{APP_VERSION} • Skill Wallet")

    # ----------------- MAIN INTERFACE -----------------
    # Hero Title Banner
    st.markdown(
        f"""
        <div class="platform-header">
            <div>
                <h1 class="platform-title">
                    🏗️ {APP_TITLE}
                    <span class="badge">CAPSTONE 1</span>
                </h1>
                <div class="platform-desc">
                    {APP_SUBTITLE}
                </div>
            </div>
            <div style="text-align: right; display: none; @media(min-width: 768px){{display: block;}}">
                <span style="color: #64748B; font-size: 0.78rem;">Standards Compliant</span><br/>
                <span style="color: #10B981; font-weight: 700; font-size: 0.9rem;">IS 456 • OSHA 1926 • NBC 2016</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 4 Main Feature Tabs
    tab_safety, tab_cracks, tab_planning, tab_assistant = st.tabs(
        [
            "🦺 1. Site Safety & PPE Audit",
            "🧱 2. Crack Diagnostics & Integrity",
            "📊 3. Planning & Real Estate Valuation",
            "🌤️ 4. Daily Assistant & Weather Advisory",
        ]
    )

    with tab_safety:
        render_safety_audit_tab(ai_client)

    with tab_cracks:
        render_crack_diagnostics_tab(ai_client)

    with tab_planning:
        render_project_planning_tab()

    with tab_assistant:
        render_daily_assistant_tab(ai_client)


if __name__ == "__main__":
    main()
