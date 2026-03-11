import streamlit as st
import os
import json
from groq import Groq

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Jan Samasya Samadhan",
    page_icon="🇮🇳",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;700&family=Space+Grotesk:wght@400;600;700&display=swap');

body { font-family: 'Space Grotesk', sans-serif; }

.header-box {
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 50%, #138808 100%);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(255,107,53,0.3);
}
.header-box h1 { font-size: 2rem; margin: 0; font-weight: 700; }
.header-box p { margin: 0.5rem 0 0; opacity: 0.9; font-size: 1rem; }

.jurisdiction-central { background: #1a3a6b; color: white; }
.jurisdiction-state    { background: #1a6b2a; color: white; }
.jurisdiction-local    { background: #6b5a1a; color: white; }
.jurisdiction-concurrent { background: #5a1a6b; color: white; }

.result-card {
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    border: 1px solid rgba(255,255,255,0.1);
}
.tag {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.step-item {
    background: #f0f7ff;
    border-left: 4px solid #2563eb;
    padding: 0.75rem 1rem;
    margin: 0.5rem 0;
    border-radius: 0 8px 8px 0;
    font-size: 0.95rem;
}
.warning-box {
    background: #fff7ed;
    border: 1px solid #fb923c;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
}
.portal-box {
    background: #f0fdf4;
    border: 1px solid #4ade80;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── Jurisdiction Knowledge Base ───────────────────────────────────────────────
SYSTEM_PROMPT = """
You are "Jan Samasya Samadhan" — an expert on Indian constitutional law and governance.
Given a citizen's problem, identify the CORRECT authority responsible and guide them clearly.

## CONSTITUTIONAL FRAMEWORK (7th Schedule)

### UNION LIST (Central Government):
- Defence, Armed Forces, Nuclear Energy
- Foreign Affairs, Passports, Visas, Citizenship
- Railways (Indian Railways — ALL railway matters)
- National Highways
- Postal services, Telecom (TRAI, DOT)
- Banking, RBI, Currency, Stock Exchange, SEBI
- Income Tax, GST (Centre), Customs, Excise
- Supreme Court, High Courts
- Elections for Parliament (ECI)
- Air & Sea Ports, Civil Aviation (DGCA)
- Central Universities (IIT, IIM, AIIMS, BHU, JNU, AMU)
- EPFO, ESI (Central Labour)
- CBI, NIA, paramilitary forces
- Patents, Copyrights, Trademarks

### STATE LIST (State Government):
- Police, Law & Order, Prisons, Crime
- State-run Public Health & Hospitals (PHC, District hospitals)
- Agriculture, Land Revenue, Land Acquisition, Farmers
- State Roads (not NH), State Transport (UPSRTC, etc.)
- Irrigation, Water supply (intra-state)
- State Electricity Boards, Power distribution (local cuts/outages)
- Local Government supervision
- State Universities & Colleges
- Registration of Birth, Death, Marriage
- Liquor/Excise Policy
- Stamp Duty, Vehicle Registration (RTO), Road Tax
- State Recruitment (UPPSC, SSC-state)

### CONCURRENT LIST (Both Central + State):
- Education (schools to colleges — both involved)
- Criminal Laws, Civil Procedure
- Labour laws, Trade Unions, Minimum Wage
- Environment & Forests
- Food safety, Price control
- Social Security, Insurance (non-central)

### LOCAL BODIES (Municipal Corporation / Nagar Palika / Gram Panchayat):
- Roads WITHIN city/ward/village (non-NH, non-state highway)
- Street lights, Drainage, Sewage, Waterlogging
- Garbage/Solid Waste Collection, Sanitation
- Building permits, Construction approvals (residential)
- Local/House Property Tax
- Parks, Playgrounds, Encroachments on local public land
- Stray animals/dogs in city areas
- Water supply within city (often delegated)
- Local food stalls/market inspection
- Unauthorized constructions in localities

## IMPORTANT DISTINCTIONS:
- Electricity bill issues (distribution) → State Electricity Board (State)
- Electricity production policy → Concurrent
- Road potholes on small local roads → Local Body (Municipal)
- National Highway potholes → NHAI (Central)
- State highway → State PWD
- Railway platform/train complaints → Indian Railways (Central)
- Local bus (city bus) → State/Municipal
- Police complaint → State Police
- CBI/serious fraud → Central (CBI)
- School (govt) teacher salary → State
- IIT/AIIMS issues → Central (Ministry of Education/Health)
- Water supply in village → Gram Panchayat (Local)
- Water supply pipeline (major project) → State Jal Board

Always respond with this EXACT JSON format only, no extra text:
{
  "jurisdiction": "Central/State/Local/Concurrent",
  "authority_name": "Full official name",
  "department": "Specific ministry or department",
  "why": "Simple explanation why this authority is responsible (can mix Hindi words naturally)",
  "action_steps": ["Step 1", "Step 2", "Step 3", "Step 4"],
  "grievance_portal": "URL or how to contact",
  "helpline": "Phone number if available, else N/A",
  "common_mistake": "What authority people wrongly blame and why that's wrong",
  "urgency_tip": "Time limit for complaint or any urgent advice"
}
"""

# ── Groq Client ───────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
    return Groq(api_key=api_key)

def analyze_problem(problem: str, state: str) -> dict:
    client = get_client()
    prompt = f"""
Citizen's State/City: {state}
Problem: {problem}

Analyze and respond ONLY in the specified JSON format.
"""
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.15,
        max_tokens=1024,
    )
    raw = resp.choices[0].message.content.strip()
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip().rstrip("`").strip()
    return json.loads(raw)

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <h1>🇮🇳 Jan Samasya Samadhan</h1>
    <p>जन समस्या समाधान — Know which government to approach</p>
</div>
""", unsafe_allow_html=True)

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Delhi (NCT)", "Jammu & Kashmir", "Ladakh", "Chandigarh", "Puducherry"
]

col1, col2 = st.columns([2, 1])
with col1:
    state = st.selectbox("Your State / UT", INDIAN_STATES, index=INDIAN_STATES.index("Uttar Pradesh"))
with col2:
    language = st.selectbox("Preferred Language", ["Hinglish", "English", "Hindi"])

problem = st.text_area(
    "Describe your problem / अपनी समस्या बताएं",
    placeholder="e.g., Meri colony mein garbage collection nahi ho rahi last 2 weeks se...\nor: The road near my house has big potholes and nobody is fixing it...\nor: My railway refund of ₹1200 is stuck for 3 months...",
    height=120
)

# ── Example Problems ──────────────────────────────────────────────────────────
st.markdown("**💡 Try these examples:**")
examples = [
    "🚮 Garbage not collected in my locality for 2 weeks",
    "💡 Electricity cut for 8 hours daily in our area",
    "🚂 Railway refund pending for 3 months",
    "👮 Police not registering my FIR",
    "🏫 Government school teacher absent for months",
    "🏥 District hospital has no medicines",
    "🛣️ Pothole on road near my house causing accidents",
    "💰 My PF (Provident Fund) withdrawal is stuck",
    "📱 Telecom company cheating, extra charges on bill",
    "💧 No water supply in village for 1 week",
]

cols = st.columns(2)
for i, ex in enumerate(examples):
    if cols[i % 2].button(ex, key=f"ex_{i}", use_container_width=True):
        st.session_state["auto_problem"] = ex[2:].strip()  # strip emoji
        st.rerun()

if "auto_problem" in st.session_state:
    problem = st.session_state.pop("auto_problem")

# ── Analysis ──────────────────────────────────────────────────────────────────
if st.button("🔍 Analyze & Find Authority", type="primary", use_container_width=True):
    if not problem.strip():
        st.warning("Please describe your problem first!")
    else:
        with st.spinner("Analyzing your problem against Indian constitutional framework..."):
            try:
                result = analyze_problem(problem, state)
                
                J = result.get("jurisdiction", "")
                color_map = {
                    "Central": "#1a3a6b",
                    "State": "#1a5c2a",
                    "Local": "#6b4a1a",
                    "Concurrent": "#4a1a6b"
                }
                bg = color_map.get(J, "#333")
                
                st.markdown(f"""
                <div style="background:{bg};color:white;border-radius:12px;padding:1.5rem;margin:1rem 0;">
                    <div style="font-size:0.85rem;opacity:0.8;margin-bottom:0.3rem">RESPONSIBLE AUTHORITY</div>
                    <div style="font-size:1.6rem;font-weight:700">{result.get('authority_name','')}</div>
                    <div style="font-size:1rem;opacity:0.85;margin-top:0.3rem">{result.get('department','')}</div>
                    <div style="margin-top:0.8rem">
                        <span style="background:rgba(255,255,255,0.2);padding:4px 12px;border-radius:20px;font-size:0.85rem;font-weight:600">
                            {J.upper()} GOVERNMENT
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("#### 📖 Why this authority?")
                st.info(result.get('why', ''))

                st.markdown(f"""
                <div class="warning-box">
                    <strong>⚠️ Common Mistake:</strong><br>
                    {result.get('common_mistake', '')}
                </div>
                """, unsafe_allow_html=True)

                st.markdown("#### ✅ Steps to take action:")
                for i, step in enumerate(result.get('action_steps', []), 1):
                    st.markdown(f"""
                    <div class="step-item"><strong>Step {i}:</strong> {step}</div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="portal-box">
                    <strong>🌐 Grievance Portal:</strong> {result.get('grievance_portal','N/A')}<br>
                    <strong>📞 Helpline:</strong> {result.get('helpline','N/A')}
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"⏰ **Urgency Tip:** {result.get('urgency_tip','')}")

                with st.expander("📄 View Raw JSON"):
                    st.json(result)

            except json.JSONDecodeError:
                st.error("Could not parse response. Please try rephrasing your problem.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.divider()
st.markdown("""
<div style="text-align:center;opacity:0.6;font-size:0.85rem">
    Based on Indian Constitution — 7th Schedule (Union/State/Concurrent Lists) + 73rd & 74th Amendment (Local Bodies)<br>
    <em>Always verify with official portals. This tool provides guidance, not legal advice.</em>
</div>
""", unsafe_allow_html=True)
