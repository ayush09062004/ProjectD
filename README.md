# 🇮🇳 Jan Samasya Samadhan — जन समस्या समाधान

> **Know which government authority (Central / State / Local) to approach for your problem in India**

---

## 🎯 What This Does

Indian citizens often blame the wrong level of government. For example:
- Blaming **Central Govt** for local road potholes → Actually **Municipal Corporation** (Local)
- Blaming **State Govt** for delayed train → Actually **Indian Railways** (Central)
- Blaming **Central Govt** for no electricity → Actually **State Electricity Board** (State)

This AI agent:
1. Takes your problem as input (English/Hindi/Hinglish)
2. Analyzes it against India's constitutional framework (7th Schedule)
3. Tells you **exactly** which authority is responsible and **why**
4. Gives you action steps + grievance portal + helpline

---

## 🏗️ Architecture

```
User Problem (text)
        │
        ▼
   Groq LLaMA-3.3-70B
   (with Constitutional KB)
        │
        ▼
┌───────────────────┐
│  Jurisdiction     │ ← Union List / State List /
│  Classifier       │   Concurrent List / Local Bodies
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Authority        │ ← Exact ministry/department
│  Identifier       │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Action Guide     │ ← Steps + Portal + Helpline
└───────────────────┘
```

---

## 🚀 Setup

### 1. Get Groq API Key (FREE)
- Sign up at https://console.groq.com
- Create API key (free tier is generous)

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set API Key

**Option A: Environment variable**
```bash
export GROQ_API_KEY="your_key_here"
```

**Option B: .env file**
```
GROQ_API_KEY=your_key_here
```

**Option C: Streamlit secrets** (for deployment)
Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your_key_here"
```

---

## ▶️ Run

### CLI Version (agent.py)
```bash
python agent.py
```

### Web App (Streamlit)
```bash
streamlit run app.py
```

---

## 📦 Files

| File | Description |
|------|-------------|
| `agent.py` | Terminal-based CLI agent |
| `app.py` | Streamlit web application |
| `requirements.txt` | Python dependencies |

---

## 🧠 Knowledge Base Coverage

### Central Government (Union List)
Railways, Passports, Banking, Income Tax, Telecom (TRAI), EPFO, National Highways, Civil Aviation, CBI, Customs...

### State Government (State List)
Police/FIR, State hospitals, Agriculture, Electricity distribution, State roads, State universities, Land records, RTO...

### Local Bodies (Municipal/Panchayat)
Garbage collection, Street lights, Drainage, Building permits, Local roads, Stray animals, Property tax...

### Concurrent (Both)
Education, Labour laws, Environment, Food safety, Criminal law...

---

## 💡 Example Problems & Results

| Problem | Authority | Level |
|---------|-----------|-------|
| Garbage not collected | Municipal Corporation | Local |
| Railway refund stuck | Indian Railways / IRCTC | Central |
| Police not taking FIR | State Police | State |
| PF withdrawal stuck | EPFO | Central |
| Pothole on city road | Nagar Palika / Corporation | Local |
| Electricity outage | State Electricity Board | State |
| Telecom overcharging | TRAI / DOT | Central |
| Govt school teacher absent | State Education Dept | State |

---

## 🔮 Future Enhancements

- [ ] Add voice input (Hindi speech-to-text)
- [ ] WhatsApp/Telegram bot integration
- [ ] Auto-fill grievance forms using AI
- [ ] Multi-language: Bengali, Tamil, Marathi, Telugu
- [ ] Track grievance status
- [ ] Connect to official APIs (CPGRAMS, Jansunwai)
- [ ] Map-based jurisdiction lookup by PIN code

---

## 📜 Legal Basis

Based on:
- **Constitution of India** — 7th Schedule (Union/State/Concurrent Lists)
- **73rd Amendment** (1992) — Panchayati Raj (Rural Local Bodies)
- **74th Amendment** (1992) — Nagarpalikas (Urban Local Bodies)

---

*Built for Indian citizens. Not legal advice — always verify with official sources.*
