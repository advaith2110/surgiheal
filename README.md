# 🩺 SurgiHeal — Post-Operative Wound & Recovery Guardian

> **AI-Powered Surgical Site Infection (SSI) Surveillance, Multimodal Wound Intelligence & Emergency Post-Op Triage**  
> *Built for Hackathon: Medical Technology / Surgery & Post-Op Recovery Track*

---

## 🌟 The Problem
- **#1 Cause of Preventable Readmissions**: Surgical Site Infections (SSIs) account for over \$3 billion in annual healthcare costs and are the leading reason patients return to the hospital after surgery.
- **Patient Anxiety & Miscommunication**: Discharged patients receive dense, confusing discharge packets and don't know whether redness or fluid is normal inflammation or early sepsis.
- **Post-Op Emergencies**: Life-threatening conditions like **Deep Vein Thrombosis (DVT)** or pulmonary embolisms develop silently at home. Patients often delay calling until it is too late, or rush to crowded emergency rooms for benign healing itchiness.

---

## 💡 The Solution: SurgiHeal
SurgiHeal acts as an intelligent medical co-pilot bridging the high-risk gap between hospital discharge and outpatient follow-up:

1. **Multimodal Wound Guardian (Gemini 2.5 Flash Vision)**:
   - Evaluates surgical incisions from photos (mobile upload or webcam).
   - Measures **erythema spread (0-10 score)**, detects **exudate types** (serous vs. purulent), and assesses **edge approximation / dehiscence**.
   - Calculates a predictive **SSI Risk Score (%)**.
   - Offers a **Dual Perspective Switcher**:
     - *Clinician Technical Analysis* (objective clinical findings for surgeons).
     - *Patient Reassurance Card* (calm, compassionate, plain-English advice).
2. **Discharge Intelligence & Recovery Roadmap**:
   - Ingests hospital discharge summaries.
   - Extracts daily medication schedules with dosages, clinical purpose, and tapering instructions.
   - Automatically builds an interactive day-by-day recovery checklist.
3. **24/7 Urgent Triage Copilot**:
   - Real-time chat assistant actively screening for surgical red flags: **DVT/PE, Sepsis, Hematoma, and Dehiscence**.
   - Instant visual emergency alerts with immediate, life-saving protocols.
4. **Surgeon Remote Command Center**:
   - Population health dashboard triaging outpatients by infection probability.
   - One-click clinical actions (Reassure patient, dispatch home health nurse, or escalate to same-day clinic).

---

## 🏗️ Architecture & Tech Stack
- **AI Core**: Google Gemini 2.5 Flash (`google-genai` SDK) utilizing Multimodal Vision, Structured Outputs (`response_schema`), and clinical system prompting.
- **Backend & Logic**: Python 3.14, Pydantic schemas, Pillow for image processing.
- **Frontend / UI**: Streamlit with custom clinical CSS styling, interactive metrics, and responsive multi-tab layout.
- **Failsafe Clinical Simulation**: Built-in deterministic clinical fallback engine ensures seamless presentations even during network interruptions or offline judging.

---

## 🚀 Quickstart & Setup

### 1. Prerequisites
Ensure Python is installed:
```bash
python --version
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
# or: py -m pip install google-genai pillow streamlit pandas altair pytest python-dotenv
```

### 3. Configure Gemini API Key (Optional for live inference)
Copy the example environment file:
```bash
copy .env.example .env
```
Add your key inside `.env` or input it directly in the app sidebar:
```env
GEMINI_API_KEY="your_api_key_here"
```

### 4. Run the Application
```bash
py -m streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Running Automated Tests
Run unit tests verifying models, image pipeline, and emergency triage screening:
```bash
py -m pytest tests/ -v
```

---

## 🏆 1-Click Judging Demos
In the sidebar, select any of the 3 pre-configured clinical case studies:
- **Case A: Sarah Jenkins (Day 4 Knee Arthroplasty)**: Normal healing trajectory, low erythema, intact staples.
- **Case B: Marcus Vance (Day 6 Appendectomy)**: Early surgical site infection warning with spreading erythema > 2.5cm, purulent exudate, and fever alert.
- **Case C: Robert Chen (Day 3 Hip Replacement)**: Sudden right calf pain and warmth — triggers urgent DVT/PE emergency protocol.
