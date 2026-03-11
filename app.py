import streamlit as st
import json
from groq import Groq

st.set_page_config(
    page_title="Jan Samasya Samadhan",
    page_icon="🇮🇳",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;700;800&family=Noto+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Noto Sans', sans-serif; }

.hero {
    background: linear-gradient(135deg, #ff6a00 0%, #ee0979 50%, #0f2027 100%);
    border-radius: 20px;
    padding: 2.2rem 2rem;
    text-align: center;
    color: white;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 40px rgba(238,9,121,0.25);
}
.hero h1 { font-family: 'Baloo 2', cursive; font-size: 2.1rem; margin: 0; font-weight: 800; letter-spacing: -0.5px; }
.hero p  { margin: 0.4rem 0 0; opacity: 0.88; font-size: 1rem; }

.api-box {
    background: #fffbf0;
    border: 1.5px dashed #f59e0b;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 1.2rem;
    font-size: 0.9rem;
}

.jurisdiction-badge {
    display: inline-block;
    padding: 5px 16px;
    border-radius: 30px;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-bottom: 0.4rem;
}

.result-header {
    border-radius: 14px;
    padding: 1.5rem;
    color: white;
    margin: 1rem 0 0.5rem;
}

.step-box {
    background: #f0f7ff;
    border-left: 4px solid #2563eb;
    padding: 0.7rem 1rem;
    margin: 0.4rem 0;
    border-radius: 0 8px 8px 0;
    font-size: 0.93rem;
}

.resolution-step {
    background: #f0fdf4;
    border-left: 4px solid #16a34a;
    padding: 0.7rem 1rem;
    margin: 0.4rem 0;
    border-radius: 0 8px 8px 0;
    font-size: 0.93rem;
}

.escalation-step {
    background: #fff7ed;
    border-left: 4px solid #ea580c;
    padding: 0.7rem 1rem;
    margin: 0.4rem 0;
    border-radius: 0 8px 8px 0;
    font-size: 0.93rem;
}

.warning-box {
    background: #fff1f2;
    border: 1px solid #fda4af;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    font-size: 0.93rem;
}

.rti-box {
    background: #faf5ff;
    border: 1.5px solid #a855f7;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    font-size: 0.93rem;
}

.timeline-box {
    background: #0f172a;
    color: #e2e8f0;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    font-size: 0.88rem;
    font-family: 'Courier New', monospace;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🇮🇳 Jan Samasya Samadhan</h1>
    <p>जानिए — आपकी समस्या कौन सुलझाएगा और कैसे?</p>
    <p style="font-size:0.82rem;opacity:0.7;margin-top:0.3rem">Central • State • Local — Know your rights, know your authority</p>
</div>
""", unsafe_allow_html=True)

# ── API Key Input ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="api-box">
    🔑 <strong>Groq API Key required</strong> — Free at 
    <a href="https://console.groq.com" target="_blank">console.groq.com</a> 
    &nbsp;|&nbsp; Your key is used only for this session and never stored.
</div>
""", unsafe_allow_html=True)

api_key = st.text_input(
    "Groq API Key",
    type="password",
    placeholder="gsk_xxxxxxxxxxxxxxxxxxxx",
    label_visibility="collapsed"
)

SYSTEM_PROMPT = """
You are "Jan Samasya Samadhan" — India's most knowledgeable civic rights expert.
Given a citizen's problem, provide a COMPLETE guide: who is responsible AND how to officially get it resolved.

## CONSTITUTIONAL FRAMEWORK (7th Schedule)

### UNION LIST — Central Government only:
Railways (ALL train/station matters), Passports/Visa/Citizenship, Defence,
Banking/RBI/SEBI, Income Tax/GST(Centre)/Customs, Telecom/TRAI/DOT,
National Highways/NHAI, Civil Aviation/DGCA/Airports,
Central Universities (IIT/IIM/AIIMS/BHU/JNU/AMU),
EPFO/ESI, CBI/NIA/Paramilitary, Patents/Copyright/Trademarks, Postal/Speed Post

### STATE LIST — State Government only:
Police/FIR/Law & Order, State Hospitals/PHC/District hospitals,
Agriculture/Land Records/Land Acquisition, State Electricity Boards/power cuts,
State Roads/PWD (non-NH), State transport/UPSRTC/MSRTC,
State universities/colleges, RTO/Vehicle registration/Road Tax,
Liquor/Excise policy, Stamp Duty, State recruitment/UPPSC/BPSC,
Irrigation/intra-state water, Forests (with Centre), Revenue department

### CONCURRENT LIST — Both Central + State:
Education (schools to college), Labour laws/Minimum wage/Trade unions,
Environment/pollution, Food safety/adulteration, Criminal law/IPC,
Social security/insurance, Family law/marriage/divorce

### LOCAL BODIES — Municipal Corporation / Nagar Palika / Gram Panchayat:
Garbage/waste collection, Street lights, Drainage/sewage/waterlogging,
LOCAL roads within city (not NH/SH), Building/construction permits,
Property/house tax, Parks/public spaces, Stray animals in city,
City water supply (often delegated), Local food stall inspection,
Birth/death certificates (at local level), Unauthorized constructions in colony

## KEY DISTINCTIONS:
- Train delay/refund/cleanliness → Indian Railways (Central), railmadad.indianrailways.gov.in
- Pothole on NH → NHAI (Central)
- Pothole on State Highway → State PWD
- Pothole on colony/city road → Municipal Corporation (Local)
- Electricity bill/outage → State Electricity Board (State)
- Mobile/internet overcharging → TRAI (Central), pgportal.trai.gov.in
- Bank fraud/complaint → RBI (Central), cms.rbi.org.in
- PF/EPFO stuck → Central, epfigms.gov.in
- Police not taking FIR → State, approach SP/SSP or file online FIR
- Govt school teacher absent → State Education Department
- Village road/water/light → Gram Panchayat (Local)

Respond ONLY in this exact JSON format, no extra text:
{
  "jurisdiction": "Central/State/Local/Concurrent",
  "authority_name": "Full official name",
  "department": "Specific ministry or department",
  "why": "Simple explanation with constitutional basis (mix Hindi naturally)",
  "action_steps": [
    "Step 1: ...",
    "Step 2: ...",
    "Step 3: ..."
  ],
  "official_resolution_path": {
    "level1": {
      "action": "First complaint — what to do and where",
      "portal": "URL or office address",
      "deadline": "Days by which they must respond",
      "helpline": "Phone number or N/A"
    },
    "level2": {
      "action": "If level 1 fails after deadline — escalate to whom",
      "portal": "URL or office",
      "deadline": "Timeline"
    },
    "level3": {
      "action": "If level 2 also fails — next authority",
      "portal": "URL or name",
      "deadline": "Timeline"
    },
    "nuclear_option": "Last resort — RTI / PIL / Media / Lokayukta / Consumer Forum etc. with brief how-to"
  },
  "rti_tip": "Specific RTI advice for this problem — what info to ask, which PIO, expected fee",
  "legal_rights": "Which law/act protects the citizen here (e.g., RTI Act 2005, Consumer Protection Act 2019, etc.)",
  "common_mistake": "What authority people wrongly blame and why that is incorrect",
  "expected_resolution_days": "Realistic timeline if process followed correctly",
  "urgency_tip": "Any time-sensitive advice or complaint deadlines"
}
"""

def analyze(problem: str, state: str, key: str) -> dict:
    client = Groq(api_key=key)
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"State/City: {state}\nProblem: {problem}\n\nRespond ONLY in the specified JSON format."}
        ],
        temperature=0.15,
        max_tokens=1500,
    )
    raw = resp.choices[0].message.content.strip()
    if "```" in raw:
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else parts[0]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip().rstrip("`").strip())

# ── Form ──────────────────────────────────────────────────────────────────────
STATES = [
    "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa",
    "Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka","Kerala",
    "Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland",
    "Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura",
    "Uttar Pradesh","Uttarakhand","West Bengal","Delhi (NCT)","Jammu & Kashmir",
    "Ladakh","Chandigarh","Puducherry","Andaman & Nicobar","Lakshadweep"
]

st.markdown("---")
col1, col2 = st.columns([2, 1])
with col1:
    state = st.selectbox("Your State / UT", STATES, index=STATES.index("Uttar Pradesh"))
with col2:
    city = st.text_input("City / District", placeholder="e.g., Lucknow")

problem = st.text_area(
    "अपनी समस्या बताएं / Describe your problem",
    placeholder=(
        "Examples:\n"
        "• Meri colony mein 2 hafte se garbage nahi utha...\n"
        "• My railway refund of ₹1500 is stuck for 2 months...\n"
        "• Police FIR likhne se mana kar rahi hai...\n"
        "• Electricity 8 ghante daily cut ho rahi hai..."
    ),
    height=130
)

st.markdown("**⚡ Quick examples:**")
examples = [
    ("🚮", "Garbage not collected for 2 weeks in colony"),
    ("🚂", "Railway refund pending for 3 months"),
    ("👮", "Police refusing to register FIR"),
    ("💡", "8-hour electricity cuts daily in our area"),
    ("💧", "No water supply in village for 1 week"),
    ("🛣️", "Deep potholes on road near my house"),
    ("💰", "PF withdrawal stuck for months"),
    ("📱", "Mobile company charging extra wrongly"),
    ("🏥", "Govt hospital has no medicines available"),
    ("🏫", "Govt school teacher absent for months"),
]
cols = st.columns(2)
for i, (emoji, text) in enumerate(examples):
    if cols[i % 2].button(f"{emoji} {text}", key=f"ex{i}", use_container_width=True):
        st.session_state["fill_problem"] = text
        st.rerun()

if "fill_problem" in st.session_state:
    problem = st.session_state.pop("fill_problem")

clicked = st.button("🔍 Find Authority + Get Resolution Guide", type="primary", use_container_width=True)

if clicked:
    if not api_key.strip():
        st.error("❌ Please enter your Groq API key above.")
    elif not problem.strip():
        st.warning("⚠️ Please describe your problem.")
    else:
        location = f"{city}, {state}" if city.strip() else state
        with st.spinner("Analyzing against Indian constitutional framework..."):
            try:
                R = analyze(problem, location, api_key.strip())

                J = R.get("jurisdiction", "")
                bg = {"Central":"#1e3a5f","State":"#14532d","Local":"#78350f","Concurrent":"#3b0764"}.get(J,"#1e293b")
                badge_bg = {"Central":"#3b82f6","State":"#22c55e","Local":"#f59e0b","Concurrent":"#a855f7"}.get(J,"#94a3b8")

                st.markdown(f"""
                <div class="result-header" style="background:{bg}">
                    <span class="jurisdiction-badge" style="background:{badge_bg};color:white">{J.upper()} GOVERNMENT</span>
                    <div style="font-size:1.55rem;font-weight:700;margin:0.3rem 0">{R.get('authority_name','')}</div>
                    <div style="opacity:0.82;font-size:0.97rem">{R.get('department','')}</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("#### 📖 Why this authority?")
                st.info(R.get("why", ""))

                st.markdown(f"""
                <div class="warning-box">
                    ⚠️ <strong>Common Mistake People Make:</strong><br>{R.get('common_mistake','')}
                </div>
                """, unsafe_allow_html=True)

                st.markdown("#### ✅ Immediate Action Steps")
                for s in R.get("action_steps", []):
                    st.markdown(f'<div class="step-box">{s}</div>', unsafe_allow_html=True)

                st.markdown("#### 🏛️ Official Resolution Path")
                orp = R.get("official_resolution_path", {})

                levels = [
                    ("level1", "🟢 Level 1 — First Complaint", "resolution-step"),
                    ("level2", "🟡 Level 2 — Escalation", "escalation-step"),
                    ("level3", "🔴 Level 3 — Senior Escalation", "escalation-step"),
                ]
                for lkey, label, css in levels:
                    lvl = orp.get(lkey, {})
                    if lvl and lvl.get("action"):
                        st.markdown(f"**{label}**")
                        detail = f"📌 {lvl.get('action','')}"
                        if lvl.get("portal"): detail += f"<br>🌐 <code>{lvl.get('portal')}</code>"
                        if lvl.get("helpline") and lvl.get("helpline") != "N/A": detail += f"<br>📞 <strong>{lvl.get('helpline')}</strong>"
                        if lvl.get("deadline"): detail += f"<br>⏱️ Response deadline: <strong>{lvl.get('deadline')}</strong>"
                        st.markdown(f'<div class="{css}">{detail}</div>', unsafe_allow_html=True)

                nuclear = orp.get("nuclear_option", "")
                if nuclear:
                    st.markdown(f"""
                    <div style="background:#450a0a;color:#fca5a5;border-radius:10px;padding:1rem 1.2rem;margin:0.5rem 0;font-size:0.93rem">
                        💣 <strong>Last Resort (if all levels fail):</strong> {nuclear}
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("#### 📜 RTI — Right to Information")
                st.markdown(f"""
                <div class="rti-box">
                    <strong>🔍 RTI Tip for your specific case:</strong><br>
                    {R.get('rti_tip','')}<br><br>
                    <strong>🌐 File RTI Online:</strong> 
                    <a href="https://rtionline.gov.in" target="_blank">rtionline.gov.in</a> (Central) | Your state RTI portal<br>
                    <strong>💰 Fee:</strong> ₹10 for Central Govt | ₹10–50 for State Govt<br>
                    <strong>⏱️ Response deadline:</strong> 30 days | Life & liberty matters: 48 hours<br>
                    <strong>If ignored:</strong> First Appellate Authority (30 days) → CIC/SIC → High Court
                </div>
                """, unsafe_allow_html=True)

                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("#### ⚖️ Your Legal Rights")
                    st.success(R.get("legal_rights", ""))
                with col_b:
                    st.markdown("#### ⏰ Expected Timeline")
                    st.markdown(f"""
                    <div class="timeline-box">
                        ✅ If process followed correctly:<br>
                        <strong style="font-size:1.05rem;color:#4ade80">{R.get('expected_resolution_days','')}</strong>
                        <br><br>⚡ {R.get('urgency_tip','')}
                    </div>
                    """, unsafe_allow_html=True)

                with st.expander("📄 View raw JSON"):
                    st.json(R)

            except json.JSONDecodeError:
                st.error("❌ Could not parse response. Try rephrasing your problem.")
            except Exception as e:
                err = str(e)
                if "api_key" in err.lower() or "auth" in err.lower() or "401" in err:
                    st.error("❌ Invalid Groq API key. Please check and re-enter.")
                elif "rate" in err.lower():
                    st.warning("⏳ Rate limit hit. Wait a few seconds and retry.")
                else:
                    st.error(f"❌ Error: {err}")

st.markdown("---")
st.markdown("""
<div style="text-align:center;opacity:0.55;font-size:0.82rem;line-height:1.8">
    Based on <strong>Constitution of India — 7th Schedule</strong> (Union/State/Concurrent Lists)<br>
    + <strong>73rd & 74th Amendment</strong> (Panchayati Raj & Nagarpalika Acts, 1992)<br>
    + <strong>RTI Act, 2005</strong> | <strong>Consumer Protection Act, 2019</strong><br>
    <em>Civic guidance only — not legal advice. Always verify with official sources.</em>
</div>
""", unsafe_allow_html=True)
