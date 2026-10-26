"""
Tab 4 - Daily Site Assistant & Weather-Aware Advisory (Epic 5)
Weather condition selector with dynamic OSHA/IS 456 safety protocols,
crane suspension alerts, concrete curing rules, and interactive multi-turn
civil engineering chatbot (NirmanAI).
"""

import streamlit as st
from modules.config import WEATHER_CONDITIONS
from modules.gemini_client import ConstructionAIClient


def render_daily_assistant_tab(ai_client: ConstructionAIClient):
    """Renders the weather advisory matrix and interactive civil engineering chatbot."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%);
                    border-left: 5px solid #10B981; padding: 18px 24px; border-radius: 8px; margin-bottom: 24px;">
            <h3 style="margin: 0; color: #34D399; font-size: 1.35rem; font-weight: 700;">
                🌤️ Epic 5: Daily Site Assistant & Weather-Aware Advisory
            </h3>
            <p style="margin: 6px 0 0 0; color: #94A3B8; font-size: 0.95rem;">
                Dynamic environmental intelligence cross-referencing <strong>OSHA 1926.1431</strong> (Cranes), 
                <strong>IS 7861 Part 1 & 2</strong> (Extreme Weather Concreting), and <strong>IS 3764</strong> (Excavation). 
                Includes <strong>NirmanAI</strong>, an interactive multi-turn civil engineering consultant.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Section 1: Weather Condition Selector & Dynamic Protocols
    st.subheader("🌦️ Site Environmental Conditions & Safety Protocol Matrix")

    weather_keys = list(WEATHER_CONDITIONS.keys())
    selected_weather = st.selectbox(
        "Select Active Site Micro-Climate / Forecast:",
        weather_keys,
        index=0,
    )

    w_info = WEATHER_CONDITIONS[selected_weather]
    badge_col = w_info["badge_color"]
    alert_level = w_info["alert_level"]

    # Protocol Banner
    st.markdown(
        f"""
        <div style="background: #131B2A; border: 1px solid #1E293B; border-radius: 10px; padding: 18px 20px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                <h4 style="margin: 0; color: #F8FAFC;">
                    Alert Status: <span style="color: {badge_col};">{alert_level}</span>
                </h4>
                <span style="background: {badge_col}22; color: {badge_col}; border: 1px solid {badge_col};
                             padding: 4px 14px; border-radius: 16px; font-weight: 700; font-size: 0.85rem;">
                    Active Condition: {w_info['condition_key']}
                </span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px;">
                <div style="background: #0B0F17; border-left: 3px solid #F59E0B; padding: 12px 14px; border-radius: 6px;">
                    <strong style="color: #F59E0B; font-size: 0.88rem;">🏗️ Tower Crane & Lifting Status:</strong>
                    <div style="color: #E2E8F0; font-size: 0.84rem; margin-top: 4px;">{w_info['crane_status']}</div>
                </div>
                <div style="background: #0B0F17; border-left: 3px solid #38BDF8; padding: 12px 14px; border-radius: 6px;">
                    <strong style="color: #38BDF8; font-size: 0.88rem;">🧪 Concreting & Curing Protocol:</strong>
                    <div style="color: #E2E8F0; font-size: 0.84rem; margin-top: 4px;">{w_info['concreting']}</div>
                </div>
                <div style="background: #0B0F17; border-left: 3px solid #EF4444; padding: 12px 14px; border-radius: 6px;">
                    <strong style="color: #EF4444; font-size: 0.88rem;">⚡ Electrical & Plant Safeguards:</strong>
                    <div style="color: #E2E8F0; font-size: 0.84rem; margin-top: 4px;">{w_info['electrical']}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Detailed Checklist for Site Engineers
    with st.expander("📋 View Mandatory Site Protocols & Standard Operating Procedures (SOP)", expanded=True):
        st.markdown(f"**Operational Checklist for {w_info['condition_key']} Conditions:**")
        for p in w_info["protocols"]:
            st.markdown(f"- ⚠️ {p}")

    st.markdown("---")

    # Section 2: Interactive Civil Engineering Chatbot (NirmanAI)
    st.subheader("💬 NirmanAI: Senior Construction Engineering & Safety Assistant")
    st.caption("Multi-turn decision support for IS codes, structural formulas, concrete mixes, and site troubleshooting.")

    # Initialize Chat History
    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = [
            {
                "role": "assistant",
                "content": "Namaste! I am **NirmanAI**, your Senior Construction Project Director and Safety Specialist. Ask me anything regarding **IS 456 concrete standards**, **OSHA safety protocols**, **reinforcement detailing**, **rate analysis**, or **daily site execution problems**.",
            }
        ]

    # Quick Prompt Chips
    st.markdown("**Quick Technical Queries:**")
    qc1, qc2, qc3, qc4 = st.columns(4)
    quick_query = None

    with qc1:
        if st.button("📏 IS 456 Nominal Cover", use_container_width=True):
            quick_query = "What is the mandatory nominal cover to reinforcement for footings, columns, and beams as per IS 456:2000 Clause 26.4?"
    with qc2:
        if st.button("🧪 M25 Concrete Mix Design", use_container_width=True):
            quick_query = "What are the recommended mix proportions, W/C ratio, and cube testing requirements for M25 grade concrete?"
    with qc3:
        if st.button("🚜 Deep Excavation Shoring", use_container_width=True):
            quick_query = "What are the safety shoring and trench protection protocols for excavations deeper than 1.5 meters under IS 3764?"
    with qc4:
        if st.button("💧 Hot-Weather Curing Rules", use_container_width=True):
            quick_query = "What are the curing duration and hessian wrapping rules for concrete in hot weather as per IS 456 and IS 7861?"

    # Render Chat History
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state["chat_messages"]:
            with st.chat_message(msg["role"], avatar="🏗️" if msg["role"] == "assistant" else "👷"):
                st.markdown(msg["content"])

    # Chat Input Box
    user_input = st.chat_input("Ask NirmanAI a construction engineering, IS code, or safety question...")

    # Process either quick query or typed input
    prompt_to_send = quick_query or user_input

    if prompt_to_send:
        # Append User Message
        st.session_state["chat_messages"].append({"role": "user", "content": prompt_to_send})
        with st.chat_message("user", avatar="👷"):
            st.markdown(prompt_to_send)

        # Generate Assistant Response
        with st.chat_message("assistant", avatar="🏗️"):
            with st.spinner("Consulting IS Codes & Engineering Knowledge Base..."):
                response_text, is_live, chat_engine = ai_client.chat_response(
                    st.session_state["chat_messages"]
                )
                st.markdown(response_text)
                if not is_live:
                    st.caption(f"⚡ {chat_engine}")

        st.session_state["chat_messages"].append({"role": "assistant", "content": response_text})

    # Clear Chat Button
    c_left, c_right = st.columns([4, 1])
    with c_right:
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state["chat_messages"] = [
                {
                    "role": "assistant",
                    "content": "Namaste! I am **NirmanAI**, your Senior Construction Project Director and Safety Specialist. How can I assist with your site operations today?",
                }
            ]
            st.rerun()
