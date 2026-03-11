import os
from groq import Groq
import json

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ─── Knowledge Base: Indian Constitutional Jurisdiction ───────────────────────

JURISDICTION_KB = """
You are "Jan Samasya Samadhan" — an expert on Indian constitutional law and governance structure.
Your job: Given a citizen's problem, identify the CORRECT authority responsible and guide them.

## CONSTITUTIONAL FRAMEWORK (7th Schedule)

### UNION LIST (Central Government — Parliament has exclusive power)
- Defence, Armed Forces, Nuclear Energy
- Foreign Affairs, Passports, Visas, Citizenship
- Railways (Indian Railways), National Highways
- Postal services, Telecom (TRAI, DOT)
- Banking, RBI, Currency, Stock Exchange, SEBI
- Income Tax, GST (Centre's share), Customs, Excise
- Supreme Court, High Courts
- Census, Elections (ECI for Lok Sabha/Rajya Sabha)
- Atomic Energy, Space (ISRO)
- Air & Sea Ports, Civil Aviation (DGCA)
- Central Universities (IITs, IIMs, AIIMs, BHU, AMU)
- EPFO, ESI (Central Labour)
- CBI, NIA, BSF, CRPF, paramilitary forces
- Patents, Copyrights, Trademarks

### STATE LIST (State Government — State Legislature has exclusive power)
- Police, Law & Order, Prisons
- Public Health & Hospitals (state-run)
- Agriculture, Land Revenue, Land Acquisition
- State Roads (non-national highways), State Transport (UPSRTC, etc.)
- Irrigation, Water Supply (intra-state rivers)
- State Electricity Boards, Power Distribution
- Local Government (Panchayats, Municipalities — empowered by state)
- State Universities, Colleges
- Registration of Births, Deaths, Marriages
- Forests (along with Centre)
- Liquor/Excise Policy (state-controlled)
- State Taxes (Stamp Duty, Entertainment Tax, Road Tax)
- State PCS, State Recruitment (UPPSC, BPSC, etc.)

### CONCURRENT LIST (Both Central + State — Central law prevails on conflict)
- Education (primary to higher)
- Criminal Law (IPC/BNS), Civil Procedure
- Marriage, Divorce, Adoption (Personal Laws)
- Labour laws, Trade Unions
- Electricity (generation policy)
- Price control, Food adulteration
- Environment & Forests
- Population Control, Family Planning
- Social Security, Insurance

### LOCAL BODIES (Municipal Corporation / Nagar Palika / Gram Panchayat)
- Roads within city/village (non-state/national)
- Street lights, Drainage, Sewage
- Garbage/Solid Waste Collection
- Building permits, Construction approvals
- Local Property Tax (House Tax)
- Birth/Death certificates (at local level)
- Parks, Playgrounds, Public spaces
- Local markets, Slaughterhouses
- Stray animals (within city)
- Water supply within city (often delegated)
- Local health inspections, Food stalls

## SPECIFIC AUTHORITIES & PORTALS

### Central Portals:
- CPGRAMS (Central): https://pgportal.gov.in
- PM's Office: https://pmindia.gov.in
- Railway complaints: https://railmadad.indianrailways.gov.in
- Banking/RBI: https://cms.rbi.org.in
- Telecom (TRAI): https://pgportal.trai.gov.in
- Income Tax: https://incometaxindiaefiling.gov.in
- Consumer Forum: https://consumerhelpline.gov.in
- EPFO: https://epfigms.gov.in

### State-Level (UP Example):
- UP CM Helpline: 1076
- UP Jansunwai: https://jansunwai.up.nic.in
- UP Police: https://uppolice.gov.in/
- Dial 100 (UP Police Emergency)

### Local Body:
- Contact local Municipal Corporation / Nagar Palika office
- Many cities: MyGov app, Municipal apps (like BBMP Sahaaya, BMC app, NMMC)

## RESPONSE FORMAT (always respond in this JSON structure):
{
  "jurisdiction": "Central/State/Local/Concurrent",
  "authority_name": "Full name of authority",
  "department": "Specific department/ministry",
  "why": "Brief constitutional/legal reason in simple Hindi+English",
  "action_steps": ["Step 1", "Step 2", "Step 3"],
  "grievance_portal": "URL or contact",
  "helpline": "Phone number if available",
  "common_mistake": "What people wrongly blame instead",
  "urgency_tip": "Any time-sensitive advice"
}
"""

def analyze_problem(user_problem: str, user_state: str = "Uttar Pradesh") -> dict:
    """Send user problem to Groq and get jurisdiction analysis."""
    
    prompt = f"""
Citizen's State/City: {user_state}
Problem Description: {user_problem}

Analyze this problem carefully. Identify:
1. Which level of government (Central/State/Local) is responsible
2. The exact authority/department
3. Why (constitutional basis)
4. Clear action steps for the citizen
5. Correct grievance portal

Respond ONLY in valid JSON as per the format specified. No extra text.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": JURISDICTION_KB},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1024,
    )
    
    raw = response.choices[0].message.content.strip()
    
    # Clean potential markdown fences
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip().rstrip("```").strip()
    
    return json.loads(raw)


def format_response(data: dict) -> str:
    """Pretty-print the analysis for terminal."""
    jurisdiction_colors = {
        "Central": "\033[34m",   # Blue
        "State": "\033[32m",     # Green
        "Local": "\033[33m",     # Yellow
        "Concurrent": "\033[35m" # Magenta
    }
    reset = "\033[0m"
    bold = "\033[1m"
    
    j = data.get("jurisdiction", "Unknown")
    color = jurisdiction_colors.get(j, "\033[37m")
    
    output = f"""
{'='*60}
{bold}🇮🇳 JAN SAMASYA SAMADHAN — ANALYSIS RESULT{reset}
{'='*60}

{bold}JURISDICTION:{reset} {color}{bold}{j.upper()}{reset}
{bold}Authority:{reset}   {data.get('authority_name', 'N/A')}
{bold}Department:{reset}  {data.get('department', 'N/A')}

{bold}WHY THIS AUTHORITY?{reset}
  {data.get('why', 'N/A')}

{bold}⚠️  COMMON MISTAKE:{reset}
  People often wrongly blame: {data.get('common_mistake', 'N/A')}

{bold}✅ ACTION STEPS:{reset}"""
    
    for i, step in enumerate(data.get('action_steps', []), 1):
        output += f"\n  {i}. {step}"
    
    output += f"""

{bold}🌐 Grievance Portal:{reset} {data.get('grievance_portal', 'N/A')}
{bold}📞 Helpline:{reset}        {data.get('helpline', 'N/A')}

{bold}⏰ Urgency Tip:{reset}
  {data.get('urgency_tip', 'N/A')}
{'='*60}
"""
    return output


def main():
    print("\n" + "="*60)
    print("🇮🇳  JAN SAMASYA SAMADHAN  |  जन समस्या समाधान")
    print("Know which government authority to approach!")
    print("="*60)
    
    state = input("\nYour State/City (e.g., Uttar Pradesh / Mumbai): ").strip()
    if not state:
        state = "Uttar Pradesh"
    
    print("\nDescribe your problem (in English or Hindi):")
    problem = input("> ").strip()
    
    if not problem:
        print("No problem entered. Exiting.")
        return
    
    print("\n⏳ Analyzing your problem...\n")
    
    try:
        result = analyze_problem(problem, state)
        print(format_response(result))
        
        # Offer to save
        save = input("Save this analysis? (y/n): ").strip().lower()
        if save == 'y':
            filename = f"analysis_{problem[:20].replace(' ','_')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"✅ Saved to {filename}")
            
    except json.JSONDecodeError:
        print("❌ Could not parse response. Try rephrasing your problem.")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
