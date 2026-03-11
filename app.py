import streamlit as st
import json
from groq import Groq

st.set_page_config(
    page_title="DEEPSI — Democratic Engine for Empowering Public Service Inquiries",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=DM+Sans:wght@300;400;500;600&family=Noto+Sans+Devanagari:wght@400;600&display=swap');

:root {
    --navy:    #0a0f2e;
    --navy2:   #111840;
    --navy3:   #1a2355;
    --saffron: #FF6B00;
    --gold:    #D4A017;
    --gold2:   #F5C842;
    --green:   #138808;
    --cream:   #FFF8F0;
    --white:   #FFFFFF;
    --muted:   rgba(255,255,255,0.55);
    --border:  rgba(212,160,23,0.25);
}

* { box-sizing: border-box; }

/* ── GLOBAL ── */
html, body, [class*="css"], .stApp {
    background: var(--navy) !important;
    color: var(--white);
    font-family: 'DM Sans', sans-serif;
}

.block-container { padding: 1.5rem 1.5rem 4rem !important; max-width: 820px !important; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── HERO ── */
.deepsi-hero {
    position: relative;
    background: linear-gradient(160deg, #0d1540 0%, #1a2a6c 50%, #0a0f2e 100%);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 3rem 2.5rem 2.5rem;
    text-align: center;
    margin-bottom: 2rem;
    overflow: hidden;
}

.deepsi-hero::before {
    content: '';
    position: absolute;
    top: -80px; left: 50%;
    transform: translateX(-50%);
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(212,160,23,0.12) 0%, transparent 70%);
    pointer-events: none;
}

.deepsi-hero::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--saffron), var(--gold2), var(--green));
    border-radius: 0 0 24px 24px;
}

.chakra-ring {
    width: 72px; height: 72px;
    border: 3px solid var(--gold);
    border-radius: 50%;
    margin: 0 auto 1.2rem;
    position: relative;
    display: flex; align-items: center; justify-content: center;
    animation: spin 20s linear infinite;
}

.chakra-ring::before {
    content: '⚖️';
    font-size: 1.8rem;
    animation: counter-spin 20s linear infinite;
}

@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes counter-spin { from { transform: rotate(0deg); } to { transform: rotate(-360deg); } }

.deepsi-wordmark {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.6rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    background: linear-gradient(135deg, var(--gold2) 0%, var(--saffron) 50%, var(--gold) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin: 0;
}

.deepsi-full-name {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 0.5rem 0 0.8rem;
    line-height: 1.6;
}

.deepsi-tagline {
    font-family: 'Noto Sans Devanagari', sans-serif;
    font-size: 1rem;
    color: rgba(255,255,255,0.75);
    margin: 0;
}

.tricolor-bar {
    display: flex; height: 4px; border-radius: 2px;
    margin: 1.5rem auto 0; width: 180px; overflow: hidden;
}
.tricolor-bar span { flex: 1; }

/* ── API KEY PANEL ── */
.api-panel {
    background: rgba(212,160,23,0.06);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1rem 1.4rem;
    margin-bottom: 1.8rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    font-size: 0.88rem;
    color: rgba(255,255,255,0.75);
}
.api-panel a { color: var(--gold2); text-decoration: none; }
.api-panel a:hover { text-decoration: underline; }

/* ── SECTION LABEL ── */
.section-label {
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--gold);
    font-weight: 600;
    margin: 0 0 0.5rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--navy2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--white) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(212,160,23,0.15) !important;
}

/* ── SELECTBOX — full override for visibility ── */
.stSelectbox > div > div {
    background: #1e2a5e !important;
    border: 1.5px solid var(--gold) !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.45rem 1rem !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.4) !important;
}
.stSelectbox > div > div > div {
    color: #FFFFFF !important;
    font-weight: 500 !important;
}
/* Arrow icon */
.stSelectbox svg { fill: var(--gold) !important; stroke: var(--gold) !important; }

/* Dropdown popup list */
div[data-baseweb="popover"],
div[data-baseweb="select"] ul,
div[role="listbox"] {
    background: #1a2460 !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.6) !important;
}
div[role="option"] {
    background: transparent !important;
    color: rgba(255,255,255,0.88) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.5rem 1rem !important;
}
div[role="option"]:hover,
div[role="option"][aria-selected="true"] {
    background: rgba(212,160,23,0.18) !important;
    color: var(--gold2) !important;
}
li[role="option"] {
    color: rgba(255,255,255,0.88) !important;
    background: transparent !important;
}
li[role="option"]:hover {
    background: rgba(212,160,23,0.18) !important;
    color: var(--gold2) !important;
}

label { color: rgba(255,255,255,0.7) !important; font-size: 0.85rem !important; }

/* ── EXAMPLE CHIPS ── */
.stButton > button {
    background: var(--navy2) !important;
    border: 1px solid var(--border) !important;
    color: rgba(255,255,255,0.8) !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.4rem 0.6rem !important;
    transition: all 0.2s ease !important;
    white-space: nowrap !important;
}
.stButton > button:hover {
    background: rgba(212,160,23,0.12) !important;
    border-color: var(--gold) !important;
    color: var(--gold2) !important;
    transform: translateY(-1px) !important;
}

/* ── PRIMARY BUTTON ── */
.stButton > button[kind="primary"],
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, var(--saffron) 0%, var(--gold) 100%) !important;
    border: none !important;
    color: var(--navy) !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.05em !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(255,107,0,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(255,107,0,0.45) !important;
}

/* ── SECONDARY BUTTON (inactive lang chips + general) ── */
.stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1.5px solid rgba(212,160,23,0.28) !important;
    color: rgba(255,255,255,0.62) !important;
    border-radius: 30px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    padding: 0.35rem 0.5rem !important;
    transition: all 0.18s ease !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: var(--gold) !important;
    color: var(--gold2) !important;
    background: rgba(212,160,23,0.1) !important;
}

/* ── RESULT CARD ── */
.result-card {
    border-radius: 18px;
    padding: 1.8rem;
    margin: 1.5rem 0 1rem;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}

.card-central { background: linear-gradient(135deg, #0d1f4a, #0a1730); border: 1px solid rgba(59,130,246,0.3); }
.card-central::before { background: linear-gradient(90deg, #3b82f6, #60a5fa); }

.card-state { background: linear-gradient(135deg, #0a2e14, #0d3a18); border: 1px solid rgba(34,197,94,0.3); }
.card-state::before { background: linear-gradient(90deg, #16a34a, #4ade80); }

.card-local { background: linear-gradient(135deg, #2d1a00, #3d2400); border: 1px solid rgba(245,158,11,0.3); }
.card-local::before { background: linear-gradient(90deg, #f59e0b, #fbbf24); }

.card-concurrent { background: linear-gradient(135deg, #1e0a3c, #2a1050); border: 1px solid rgba(168,85,247,0.3); }
.card-concurrent::before { background: linear-gradient(90deg, #a855f7, #c084fc); }

.jurisdiction-pill {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 30px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

.authority-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--white);
    line-height: 1.2;
    margin: 0 0 0.3rem;
}

.dept-subtitle {
    font-size: 0.9rem;
    color: var(--muted);
    margin: 0;
}

/* ── INFO BLOCKS ── */
.info-block {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin: 0.8rem 0;
}
.info-block-title {
    font-size: 0.68rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--gold);
    font-weight: 600;
    margin-bottom: 0.6rem;
}

/* ── STEP ITEMS ── */
.step-item {
    display: flex;
    gap: 0.9rem;
    align-items: flex-start;
    padding: 0.75rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    font-size: 0.92rem;
    color: rgba(255,255,255,0.85);
    line-height: 1.5;
}
.step-item:last-child { border-bottom: none; }

.step-num {
    min-width: 26px; height: 26px;
    border-radius: 50%;
    background: rgba(212,160,23,0.15);
    border: 1px solid var(--gold);
    color: var(--gold2);
    font-size: 0.72rem;
    font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
}

/* ── RESOLUTION LEVELS ── */
.level-row {
    display: flex;
    gap: 1rem;
    align-items: stretch;
    margin: 0.5rem 0;
}
.level-line {
    width: 2px;
    border-radius: 1px;
    flex-shrink: 0;
    min-height: 60px;
}
.level-content {
    flex: 1;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.5rem;
}
.level-title {
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 0.4rem;
}
.level-action { font-size: 0.91rem; color: rgba(255,255,255,0.82); line-height: 1.5; }
.level-meta { font-size: 0.8rem; color: var(--muted); margin-top: 0.35rem; }
.level-meta code {
    background: rgba(212,160,23,0.12);
    color: var(--gold2);
    padding: 1px 6px;
    border-radius: 4px;
    font-size: 0.78rem;
}

.nuclear-box {
    background: rgba(220,38,38,0.08);
    border: 1px solid rgba(220,38,38,0.3);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    font-size: 0.91rem;
    color: rgba(255,180,180,0.9);
    margin-top: 0.5rem;
}

/* ── RTI BOX ── */
.rti-box {
    background: linear-gradient(135deg, rgba(168,85,247,0.08), rgba(124,58,237,0.05));
    border: 1px solid rgba(168,85,247,0.25);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin: 0.8rem 0;
    font-size: 0.9rem;
    line-height: 1.7;
    color: rgba(255,255,255,0.82);
}
.rti-box a { color: #c084fc; text-decoration: none; }
.rti-box strong { color: var(--white); }

/* ── RIGHTS + TIMELINE ROW ── */
.rights-box {
    background: rgba(19,136,8,0.08);
    border: 1px solid rgba(19,136,8,0.3);
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    font-size: 0.89rem;
    color: rgba(255,255,255,0.8);
    line-height: 1.6;
    height: 100%;
}
.timeline-box {
    background: rgba(255,107,0,0.07);
    border: 1px solid rgba(255,107,0,0.25);
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    font-size: 0.89rem;
    color: rgba(255,255,255,0.8);
    line-height: 1.6;
    height: 100%;
}
.big-number {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--gold2);
    line-height: 1;
    margin: 0.4rem 0 0.2rem;
}

/* ── MISTAKE BOX ── */
.mistake-box {
    background: rgba(239,68,68,0.07);
    border: 1px solid rgba(239,68,68,0.22);
    border-left: 3px solid #ef4444;
    border-radius: 0 10px 10px 0;
    padding: 0.9rem 1.1rem;
    font-size: 0.9rem;
    color: rgba(255,200,200,0.85);
    margin: 0.8rem 0;
    line-height: 1.55;
}

/* ── LANGUAGE CHIPS ── */
.lang-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 0.5rem 0 0.2rem;
}
.lang-chip {
    padding: 6px 14px;
    border-radius: 30px;
    font-size: 0.82rem;
    font-weight: 600;
    cursor: pointer;
    border: 1.5px solid rgba(212,160,23,0.3);
    background: rgba(255,255,255,0.04);
    color: rgba(255,255,255,0.65);
    transition: all 0.18s ease;
    user-select: none;
    letter-spacing: 0.02em;
}
.lang-chip:hover {
    border-color: var(--gold);
    color: var(--gold2);
    background: rgba(212,160,23,0.1);
}
.lang-chip.active {
    background: linear-gradient(135deg, rgba(212,160,23,0.25), rgba(255,107,0,0.2));
    border-color: var(--gold);
    color: var(--gold2);
    box-shadow: 0 0 12px rgba(212,160,23,0.2);
}

/* ── DIVIDER ── */
.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 2rem 0;
    border: none;
}

/* ── FOOTER ── */
.deepsi-footer {
    text-align: center;
    font-size: 0.76rem;
    color: rgba(255,255,255,0.3);
    line-height: 2;
    padding: 1.5rem 0 0;
    border-top: 1px solid rgba(255,255,255,0.06);
}

/* ── EXAMPLE CHIPS (override secondary for non-lang buttons) ── */
.stButton > button[kind="secondary"]:not([data-testid*="lang"]) {
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    white-space: nowrap !important;
}

/* ── SPINNER ── */
.stSpinner > div { border-top-color: var(--gold) !important; }

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    background: var(--navy2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: rgba(255,255,255,0.6) !important;
    font-size: 0.82rem !important;
}
</style>
""", unsafe_allow_html=True)

# ══ HERO ══════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="deepsi-hero">
    <div class="chakra-ring"></div>
    <h1 class="deepsi-wordmark">DEEPSI</h1>
    <p class="deepsi-full-name">
        Democratic Engine for Empowering<br>Public Service Inquiries
    </p>
    <p class="deepsi-tagline">जानिए — आपकी समस्या कौन सुलझाएगा और कैसे?</p>
    <div class="tricolor-bar">
        <span style="background:#FF6B00"></span>
        <span style="background:#FFFFFF"></span>
        <span style="background:#138808"></span>
    </div>
</div>
""", unsafe_allow_html=True)

# ══ API KEY ════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="api-panel">
    <span style="font-size:1.3rem">🔑</span>
    <span>
        Enter your <strong style="color:rgba(255,255,255,0.9)">Groq API Key</strong> to begin —
        free at <a href="https://console.groq.com" target="_blank">console.groq.com</a>.
        Your key is used only in this session and is never stored.
    </span>
</div>
""", unsafe_allow_html=True)

api_key = st.text_input("", type="password", placeholder="gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                        label_visibility="collapsed")

# ══ SYSTEM PROMPT ═════════════════════════════════════════════════════════════
SYSTEM_PROMPT = """
You are DEEPSI (Democratic Engine for Empowering Public Service Inquiries) — India's most authoritative civic rights expert.
Given a citizen's problem, identify the CORRECT constitutional authority and provide a complete resolution guide.

## CONSTITUTIONAL FRAMEWORK (7th Schedule)

### UNION LIST — Central Government only:
Railways (ALL train/station/refund matters), Passports/Visa/Citizenship, Defence/Armed Forces,
Banking/RBI/SEBI/Stock exchanges, Income Tax/GST-Centre/Customs/Excise, Telecom/TRAI/DOT,
National Highways/NHAI, Civil Aviation/DGCA/Airports, Postal/Speed Post,
Central Universities (IIT/IIM/AIIMS/BHU/JNU/AMU/Delhi Univ),
EPFO/ESI (provident fund, employee insurance), CBI/NIA/BSF/CRPF/Paramilitary,
Patents/Copyright/Trademarks, Atomic Energy/Space/ISRO

### STATE LIST — State Government only:
Police/FIR/Law & Order/Prisons, State-run Hospitals/PHC/District hospitals/AYUSH,
Agriculture/Land Records/Land Acquisition/Patwari/Lekhpal, State Electricity Boards/power cuts/bill issues,
State Roads & Bridges/PWD (non-National Highway), State transport/UPSRTC/MSRTC/KSRTC,
State Universities & Colleges (non-Central), RTO/Vehicle registration/Driving licence/Road Tax,
Liquor/Excise policy, Stamp Duty/Registration of property, State Recruitment/UPPSC/BPSC/SSC-State,
Irrigation canals/intra-state rivers, Revenue department/Tehsildar/SDM, Ration card/PDS (state-run)

### CONCURRENT LIST — Both Central + State (Central law prevails in conflict):
Education (primary school to colleges — BOTH govts involved), Labour laws/Minimum wage/Trade unions/Factories,
Environment & Forests/Pollution control (CPCB Central, SPCB State), Food safety (FSSAI Central, enforcement State),
Criminal law/IPC/BNS/CrPC, Social security & insurance (non-EPFO), Family law/marriage/divorce/adoption

### LOCAL BODIES — Municipal Corporation / Nagar Palika / Gram Panchayat:
Garbage/solid waste collection/sanitation, Street lights (within city/village),
Drainage/sewage/waterlogging/open drains, LOCAL roads & lanes within city/ward/village (not NH or SH),
Building permits/construction NOC/demolition, Property/house tax, Parks/public playgrounds/open spaces,
Stray animals (dogs/cattle) within city, Water supply within city (often delegated by state),
Local food stall/restaurant/market inspection, Birth & death certificates (front-end issuance),
Unauthorized constructions in residential areas, Noise complaints within locality

## IMPORTANT DISTINCTIONS (get these right):
- Train delay / dirty coach / missing luggage / refund → Indian Railways, railmadad.indianrailways.gov.in
- Pothole on National Highway → NHAI (Central), nhidcl.nic.in or 1033
- Pothole on State Highway → State PWD
- Pothole on colony/mohalla/city road → Municipal Corporation / Nagar Palika (Local)
- Electricity bill dispute OR daily power cuts → State Electricity Board / DISCOM (State)
- Mobile overcharging / internet speed fraud → TRAI (Central), pgportal.trai.gov.in or 1800-11-0420
- Bank fraud / UPI dispute / NBFCs → RBI Ombudsman (Central), cms.rbi.org.in
- PF withdrawal stuck → EPFO (Central), epfigms.gov.in or 1800-11-8005
- Police not taking FIR → State Police; SP/SSP/DIG or online FIR portal of state
- Govt school teacher absent → State Education Dept / District Education Officer (DEO)
- IIT/NIT/AIIMS/Central Univ issue → Central (MoE / MoHFW)
- Village road / village lights / village water → Gram Panchayat (Local)
- Aadhaar issues → UIDAI (Central), uidai.gov.in or 1947
- Passport delay → MEA Passport Seva (Central), passportindia.gov.in or 1800-258-1800

Respond ONLY in this exact JSON format — no text before or after:
{
  "jurisdiction": "Central/State/Local/Concurrent",
  "authority_name": "Full official name",
  "department": "Specific ministry or department full name",
  "why": "Clear explanation of why this authority is responsible — cite constitutional list and specific subject entry. Mix Hindi naturally where helpful.",
  "action_steps": [
    "Step 1: ...",
    "Step 2: ...",
    "Step 3: ...",
    "Step 4: ..."
  ],
  "official_resolution_path": {
    "level1": {
      "action": "Exact first complaint step with specific officer/portal name",
      "portal": "Full URL or specific office",
      "deadline": "X days / X hours",
      "helpline": "Phone number or N/A"
    },
    "level2": {
      "action": "Escalation if level 1 deadline passes without response",
      "portal": "URL or office name",
      "deadline": "X days",
      "helpline": "Number or N/A"
    },
    "level3": {
      "action": "Senior authority / appellate / state-level escalation",
      "portal": "URL or name",
      "deadline": "X days",
      "helpline": "Number or N/A"
    },
    "nuclear_option": "Detailed last-resort options: RTI + specific Lokayukta/Lokpal + Consumer Forum + High Court writ + mention media/social media pressure"
  },
  "rti_tip": "Specific, actionable RTI advice: exact info to demand, which PIO office, section of RTI Act relevant, expected cost (Rs 10 Central / varies state)",
  "legal_rights": "Specific laws protecting citizen: act name + year + section if possible (e.g., RTI Act 2005 S.7, Consumer Protection Act 2019, Police Act, etc.)",
  "common_mistake": "Which authority people wrongly approach for this problem, and why constitutionally that is wrong",
  "expected_resolution_days": "Realistic timeframe like '7–15 working days' or '30 days if CPGRAMS used'",
  "urgency_tip": "Any limitation period, critical deadline, or time-sensitive action the citizen must take immediately"
}
"""

def analyze(problem: str, location: str, key: str, language: str = "Hinglish") -> dict:
    lang_instruction = {
        "Hinglish":  "Respond with all text fields in Hinglish (natural mix of Hindi and English, written in Roman script). Keep technical terms and portal URLs in English.",
        "Hindi":     "Respond with all text fields in pure Hindi (Devanagari script). Keep portal URLs and technical terms in English.",
        "English":   "Respond with all text fields in clear formal English.",
        "Bengali":   "Respond with all text fields in Bengali (বাংলা script). Keep portal URLs and technical terms in English.",
        "Tamil":     "Respond with all text fields in Tamil (தமிழ் script). Keep portal URLs and technical terms in English.",
        "Telugu":    "Respond with all text fields in Telugu (తెలుగు script). Keep portal URLs and technical terms in English.",
        "Marathi":   "Respond with all text fields in Marathi (Devanagari script). Keep portal URLs and technical terms in English.",
        "Gujarati":  "Respond with all text fields in Gujarati (ગુજરાતી script). Keep portal URLs and technical terms in English.",
        "Kannada":   "Respond with all text fields in Kannada (ಕನ್ನಡ script). Keep portal URLs and technical terms in English.",
        "Malayalam": "Respond with all text fields in Malayalam (മലയാളം script). Keep portal URLs and technical terms in English.",
        "Punjabi":   "Respond with all text fields in Punjabi (Gurmukhi script). Keep portal URLs and technical terms in English.",
        "Odia":      "Respond with all text fields in Odia (ଓଡ଼ିଆ script). Keep portal URLs and technical terms in English.",
    }.get(language, "Respond in English.")

    client = Groq(api_key=key)
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Location: {location}\nProblem: {problem}\nLanguage instruction: {lang_instruction}\n\nRespond ONLY in the specified JSON format."}
        ],
        temperature=0.15,
        max_tokens=1800,
    )
    raw = resp.choices[0].message.content.strip()
    if "```" in raw:
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else parts[0]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip().rstrip("`").strip())

# ══ LOCATION ROW ══════════════════════════════════════════════════════════════
STATES = [
    "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa",
    "Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka","Kerala",
    "Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland",
    "Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura",
    "Uttar Pradesh","Uttarakhand","West Bengal","Delhi (NCT)","Jammu & Kashmir",
    "Ladakh","Chandigarh","Puducherry","Andaman & Nicobar","Lakshadweep"
]

LANGUAGES = [
    ("Hinglish", "हिं+EN", "Mix of Hindi & English"),
    ("Hindi", "हिन्दी", "Pure Hindi"),
    ("English", "EN", "English"),
    ("Bengali", "বাংলা", "Bengali"),
    ("Tamil", "தமிழ்", "Tamil"),
    ("Telugu", "తెలుగు", "Telugu"),
    ("Marathi", "मराठी", "Marathi"),
    ("Gujarati", "ગુજરાતી", "Gujarati"),
    ("Kannada", "ಕನ್ನಡ", "Kannada"),
    ("Malayalam", "മലയാളം", "Malayalam"),
    ("Punjabi", "ਪੰਜਾਬੀ", "Punjabi"),
    ("Odia", "ଓଡ଼ିଆ", "Odia"),
]

# Init default language
if "sel_lang" not in st.session_state:
    st.session_state["sel_lang"] = "Hinglish"

st.markdown('<div class="section-label">📍 Your Location</div>', unsafe_allow_html=True)
c1, c2 = st.columns([3, 2])
with c1:
    state = st.selectbox("State / UT", STATES, index=STATES.index("Uttar Pradesh"), label_visibility="collapsed")
with c2:
    city = st.text_input("City / District", placeholder="e.g., Varanasi", label_visibility="collapsed")

# ── Language Selector ─────────────────────────────────────────────────────────
st.markdown('<div class="section-label" style="margin-top:1.2rem">🌐 Response Language</div>', unsafe_allow_html=True)

# Render chips as buttons in a wrapped row using columns trick
lang_cols = st.columns(len(LANGUAGES))
for i, (lang_key, script, label) in enumerate(LANGUAGES):
    is_active = st.session_state["sel_lang"] == lang_key
    btn_style = "primary" if is_active else "secondary"
    with lang_cols[i]:
        if st.button(
            f"{script}",
            key=f"lang_{lang_key}",
            help=label,
            type=btn_style,
            use_container_width=True
        ):
            st.session_state["sel_lang"] = lang_key
            st.rerun()

selected_language = st.session_state["sel_lang"]
st.markdown(
    f'<div style="font-size:0.78rem;color:rgba(255,255,255,0.4);margin:0.3rem 0 1rem;text-align:center">'
    f'Responding in <strong style="color:var(--gold)">{selected_language}</strong></div>',
    unsafe_allow_html=True
)

st.markdown('<div class="section-label" style="margin-top:0.5rem">✍️ Describe Your Problem</div>', unsafe_allow_html=True)
problem = st.text_area(
    "Problem",
    placeholder=(
        "Describe in English, Hindi, or Hinglish…\n\n"
        "• Meri colony mein 3 hafte se garbage nahi utha raha\n"
        "• My PF withdrawal of ₹2 lakh is stuck for 4 months\n"
        "• Police FIR likhne se saaf mana kar rahi hai\n"
        "• Road ke gadhon mein 2 accidents ho chuke hain"
    ),
    height=140,
    label_visibility="collapsed"
)

# ── Examples ──────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label" style="margin-top:1.2rem">⚡ Quick Examples</div>', unsafe_allow_html=True)
examples = [
    ("🚮", "Garbage not collected for 3 weeks"),
    ("🚂", "Railway refund stuck for 2 months"),
    ("👮", "Police refusing to register FIR"),
    ("💡", "10-hour daily electricity cuts"),
    ("💧", "No water supply in village"),
    ("🛣️", "Dangerous potholes on road"),
    ("💰", "PF withdrawal stuck for months"),
    ("📱", "Mobile company charging extra"),
    ("🏥", "Govt hospital out of medicines"),
    ("🏫", "Govt school teacher always absent"),
    ("🏠", "Illegal construction next door"),
    ("🪪", "Aadhaar correction not happening"),
]
cols = st.columns(3)
for i, (emoji, text) in enumerate(examples):
    if cols[i % 3].button(f"{emoji} {text}", key=f"ex{i}", use_container_width=True):
        st.session_state["fp"] = text
        st.rerun()
if "fp" in st.session_state:
    problem = st.session_state.pop("fp")

st.markdown("<br>", unsafe_allow_html=True)
go = st.button("⚖️ Identify Authority & Get Resolution Guide", type="primary", use_container_width=True)

# ══ RESULT ════════════════════════════════════════════════════════════════════
if go:
    if not api_key.strip():
        st.error("🔑 Please enter your Groq API key to continue.")
    elif not problem.strip():
        st.warning("Please describe your problem above.")
    else:
        loc = f"{city.strip()}, {state}" if city.strip() else state
        with st.spinner("Consulting India's constitutional framework…"):
            try:
                R = analyze(problem, loc, api_key.strip(), selected_language)

                J = R.get("jurisdiction", "")
                card_cls   = {"Central":"card-central","State":"card-state","Local":"card-local","Concurrent":"card-concurrent"}.get(J,"card-central")
                pill_bg    = {"Central":"#3b82f6","State":"#22c55e","Local":"#f59e0b","Concurrent":"#a855f7"}.get(J,"#64748b")
                level_colors = ["#22c55e","#f59e0b","#ef4444"]

                # ── Authority card ──
                st.markdown(f"""
                <div class="result-card {card_cls}">
                    <span class="jurisdiction-pill" style="background:{pill_bg}22;color:{pill_bg};border:1px solid {pill_bg}44">
                        {J.upper()} GOVERNMENT
                    </span>
                    <div class="authority-title">{R.get('authority_name','')}</div>
                    <div class="dept-subtitle">{R.get('department','')}</div>
                </div>
                """, unsafe_allow_html=True)

                # ── Why ──
                st.markdown('<div class="info-block"><div class="info-block-title">📖 Constitutional Basis</div>'
                           f'<div style="font-size:0.93rem;line-height:1.65;color:rgba(255,255,255,0.82)">{R.get("why","")}</div></div>',
                           unsafe_allow_html=True)

                # ── Common mistake ──
                st.markdown(f'<div class="mistake-box">⚠️ <strong style="color:rgba(255,180,180,1)">Common Mistake:</strong> {R.get("common_mistake","")}</div>',
                           unsafe_allow_html=True)

                st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

                # ── Action steps ──
                st.markdown('<div class="info-block-title">✅ Immediate Action Steps</div>', unsafe_allow_html=True)
                steps_html = ""
                for i, s in enumerate(R.get("action_steps", []), 1):
                    steps_html += f'<div class="step-item"><div class="step-num">{i}</div><div>{s}</div></div>'
                st.markdown(f'<div class="info-block" style="padding-bottom:0.4rem">{steps_html}</div>', unsafe_allow_html=True)

                st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

                # ── Resolution Path ──
                st.markdown('<div class="info-block-title">🏛️ Official Resolution Path</div>', unsafe_allow_html=True)
                orp = R.get("official_resolution_path", {})
                level_labels = [
                    ("level1", "Level 1 — First Complaint"),
                    ("level2", "Level 2 — Escalation"),
                    ("level3", "Level 3 — Senior Authority"),
                ]
                for (lk, lname), col in zip(level_labels, level_colors):
                    lvl = orp.get(lk, {})
                    if lvl and lvl.get("action"):
                        portal_bit = f' · <code>{lvl.get("portal","")}</code>' if lvl.get("portal") else ""
                        helpline_bit = f' · 📞 {lvl.get("helpline")}' if lvl.get("helpline") and lvl.get("helpline") != "N/A" else ""
                        deadline_bit = f' · ⏱ respond in <strong style="color:{col}">{lvl.get("deadline","")}</strong>' if lvl.get("deadline") else ""
                        st.markdown(f"""
                        <div class="level-row">
                            <div class="level-line" style="background:{col}44;border-left:2px solid {col}"></div>
                            <div class="level-content">
                                <div class="level-title" style="color:{col}">{lname}</div>
                                <div class="level-action">{lvl.get('action','')}</div>
                                <div class="level-meta">{portal_bit}{helpline_bit}{deadline_bit}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                nuke = orp.get("nuclear_option","")
                if nuke:
                    st.markdown(f'<div class="nuclear-box">💣 <strong>Last Resort:</strong> {nuke}</div>', unsafe_allow_html=True)

                st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

                # ── RTI ──
                st.markdown('<div class="info-block-title">📜 RTI — Right to Information</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="rti-box">
                    <strong>Case-specific RTI tip:</strong> {R.get('rti_tip','')}<br><br>
                    <strong>🌐 File online:</strong>
                    <a href="https://rtionline.gov.in" target="_blank">rtionline.gov.in</a> (Central) · Your state RTI portal<br>
                    <strong>💰 Fee:</strong> ₹10 Central · ₹10–50 State<br>
                    <strong>⏱ Deadline:</strong> 30 days · 48 hrs for life & liberty matters<br>
                    <strong>If ignored:</strong> First Appellate → CIC / SIC → High Court
                </div>
                """, unsafe_allow_html=True)

                # ── Rights + Timeline ──
                ca, cb = st.columns(2)
                with ca:
                    st.markdown('<div class="info-block-title">⚖️ Your Legal Rights</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="rights-box">{R.get("legal_rights","")}</div>', unsafe_allow_html=True)
                with cb:
                    st.markdown('<div class="info-block-title">⏰ Expected Timeline</div>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="timeline-box">
                        <div style="font-size:0.75rem;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:0.1em">If process followed correctly</div>
                        <div class="big-number">{R.get('expected_resolution_days','')}</div>
                        <div style="margin-top:0.5rem;font-size:0.82rem;color:rgba(255,200,150,0.85)">⚡ {R.get('urgency_tip','')}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with st.expander("{ } Raw JSON response"):
                    st.json(R)

            except json.JSONDecodeError:
                st.error("❌ Could not parse response. Please rephrase your problem and try again.")
            except Exception as e:
                err = str(e)
                if any(x in err.lower() for x in ["api_key","auth","401","invalid_api"]):
                    st.error("❌ Invalid Groq API key. Please check it and re-enter.")
                elif "rate" in err.lower():
                    st.warning("⏳ Rate limit reached. Wait a few seconds and retry.")
                elif "connect" in err.lower() or "network" in err.lower():
                    st.error("❌ Network error. Please check your internet connection.")
                else:
                    st.error(f"❌ {err}")

# ══ FOOTER ════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="deepsi-footer">
    <strong style="color:rgba(255,255,255,0.5)">DEEPSI</strong> — Democratic Engine for Empowering Public Service Inquiries<br>
    Based on Constitution of India · 7th Schedule (Union / State / Concurrent Lists)<br>
    73rd & 74th Amendments (Panchayati Raj & Nagarpalika, 1992) · RTI Act 2005 · Consumer Protection Act 2019<br>
    <em>Civic guidance only — not legal advice. Always verify with official sources.</em>
</div>
""", unsafe_allow_html=True)
