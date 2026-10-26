# Multimodal Construction Intelligence Platform 🏗️

> **Skill Wallet Capstone Project 1**  
> AI-powered decision-support system for construction site safety compliance, structural diagnostics, CapEx valuation, and daily site operations.

---

## 🌟 Overview

The **Multimodal Construction Intelligence Platform** bridges civil engineering standards with multimodal artificial intelligence (Google Gemini). It automates on-site inspections, diagnoses structural defects, estimates construction costs benchmarked against Indian market conditions, and provides weather-aware actionable safety protocols.

Built with a dual interface architecture:
1. **Interactive Full-Stack Streamlit App** (`app.py`) for rapid site inspection and live diagnostic workflows.
2. **Modern Decoupled Stack**: High-performance **FastAPI Backend** (`backend/`) paired with a modern **React + Vite Frontend** (`frontend/`).

---

## 🚀 Key Features

### 1. 🦺 PPE Safety Compliance & Hazard Audit
- Automated visual inspection of worker PPE against **OSHA 1926**, **IS 15844**, and **NBC 2016 Part 7**.
- Detects safety helmets, high-visibility vests, boots, harnesses, and eye/respiratory gear.
- Generates numeric safety scores (0–100), hazard logs with severity levels, and mandatory regulatory remedies.

### 2. 🔍 Concrete Crack & Structural Diagnostics
- Forensic defect analysis for concrete beams, columns, slabs, and masonry surfaces.
- Evaluates crack width (mm), depth assessment, and compliance with **IS 456:2000 Cl. 35.3.2**.
- Provides urgency rating (1–10) and engineering repair methods (e.g., epoxy injection, CFRP stitching, PMM patching) with INR cost estimates.

### 3. 📊 Project Planning & CapEx Valuation
- Tier-based cost estimation across **Tier 1 (Metro)**, **Tier 2 (Growth Hubs)**, and **Tier 3 (Emerging)** cities.
- Breakdown of cement, steel, structural materials, labor, and plant & machinery costs.
- Projected real estate market valuation and developer margin metrics.

### 4. 🌤️ NirmanAI Daily Assistant & Weather Protocols
- Weather-aware site directives for extreme conditions (monsoon inundation, high wind crane suspensions, heat waves, fog).
- AI civil engineering copilot trained on **IS 456:2000**, **IS 1893**, **IS 800**, and **NBC 2016**.

---

## 📁 Repository Structure

```
.
├── app.py                     # Streamlit Full-Stack Application
├── requirements.txt           # Python dependencies
├── modules/                   # Core business logic & Gemini AI client
│   ├── config.py              # Constants, IS 456 benchmarks & prompts
│   ├── gemini_client.py       # Multimodal Gemini client & fallback engine
│   ├── safety_audit.py        # Safety vision & OSHA audit logic
│   ├── crack_diagnostics.py   # Structural defect assessment
│   ├── project_planning.py    # Cost estimation & CapEx valuation
│   └── daily_assistant.py     # Weather advisory & NirmanAI copilot
├── backend/                   # FastAPI REST API
│   ├── main.py                # FastAPI entry point & CORS configuration
│   ├── schemas.py             # Pydantic request/response schemas
│   └── routes/                # Modular API endpoints (safety, cracks, planning, weather)
├── frontend/                  # React + Vite Modern Web Application
│   ├── src/                   # React components, tabs & styling
│   └── package.json           # Frontend dependencies (Lucide icons, Vite, React)
└── sample_data/               # Sample test images (concrete cracks, site PPE)
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10+
- Node.js 18+ & npm (for React frontend)
- [Optional] Google Gemini API Key (`GEMINI_API_KEY`)

### 1. Clone & Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables (Optional)

Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
*(Note: If no API key is supplied, the platform runs in a resilient demonstration mode using realistic simulated inspection reports).*

---

## 🖥️ Running the Application

### Option A: Streamlit Unified App (Recommended for Quick Demo)
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

### Option B: FastAPI Backend + React Frontend

**Start the FastAPI Backend:**
```bash
uvicorn backend.main:app --reload --port 8000
```
API Documentation available at: [http://localhost:8000/docs](http://localhost:8000/docs)

**Start the React Frontend:**
```bash
cd frontend
npm install
npm run dev
```
Frontend available at: [http://localhost:5173](http://localhost:5173)

---

## 📜 Standards & Compliance Reference

- **IS 456:2000**: Indian Standard for Plain and Reinforced Concrete
- **IS 15844 / IS 15298**: Personal Protective Equipment & Safety Footwear
- **NBC 2016 Part 7**: National Building Code of India - Construction Management & Safety
- **OSHA 1926**: Safety and Health Regulations for Construction
- **IS 7861 (Part 1)**: Recommended Practice for Hot Weather Concreting

---

## 📄 License

This project is licensed under the MIT License.
