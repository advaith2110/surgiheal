import streamlit as st
import datetime
import pandas as pd
from PIL import Image
import io

import config
import ai_service
from sample_data import SAMPLE_CASES, create_synthetic_incision_image, get_case_image_bytes
from models import WoundAnalysisResult, DischargeSummary, TriageAssessment

# Page configuration
st.set_page_config(
    page_title="SurgiHeal — Post-Operative Wound & Recovery Guardian",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern clinical UI styling
st.markdown("""
<style>
    /* Medical color scheme & typography */
    .metric-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
        margin-bottom: 12px;
    }
    .badge-normal {
        background-color: #dcfce7;
        color: #166534;
        padding: 6px 14px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
        border: 1px solid #86efac;
    }
    .badge-caution {
        background-color: #fef9c3;
        color: #854d0e;
        padding: 6px 14px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
        border: 1px solid #fde047;
    }
    .badge-urgent {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 6px 14px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
        border: 1px solid #fca5a5;
    }
    .callout-box {
        border-left: 4px solid #0284c7;
        background-color: #f0f9ff;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin: 12px 0;
    }
    .emergency-box {
        border-left: 4px solid #dc2626;
        background-color: #fef2f2;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin: 12px 0;
        animation: pulse 2s infinite;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        font-weight: 600;
        border-radius: 8px 8px 0 0;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Session State
if "patient_case_key" not in st.session_state:
    st.session_state.patient_case_key = "case_a"

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = {}

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Hello! I am your SurgiHeal Recovery Copilot. How are you feeling today? You can describe any sensations around your incision or ask questions about medications and recovery milestones."}
    ]

# Sidebar: Controls & Patient Profile
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=400&q=80", use_container_width=True)
    st.title("🩺 SurgiHeal")
    st.caption("Post-Operative Wound & Recovery Guardian")
    st.divider()

    st.subheader("⚡ 1-Click Hackathon Demo")
    demo_case = st.selectbox(
        "Select Clinical Case Study:",
        options=["case_a", "case_custom"],
        format_func=lambda k: {
            "case_a": "Case A: Sarah Jenkins (Day 4 Knee - Normal)",
            "case_custom": "➕ Custom Patient Case (Upload Your Own)"
        }[k],
        key="selected_case_select"
    )

    if demo_case != st.session_state.patient_case_key:
        st.session_state.patient_case_key = demo_case
        # Reset active chat for new patient context
        st.session_state.chat_messages = [
            {"role": "assistant", "content": f"Hello! I am monitoring recovery for {SAMPLE_CASES[demo_case]['name']}. How are you feeling today?"}
        ]
        st.rerun()

    active_case = SAMPLE_CASES[st.session_state.patient_case_key]

    if demo_case == "case_custom":
        with st.expander("✏️ Customize Patient Details", expanded=False):
            c_name = st.text_input("Patient Name:", value=SAMPLE_CASES["case_custom"]["name"], key="c_name")
            c_age = st.number_input("Age:", value=int(SAMPLE_CASES["case_custom"]["age"]), min_value=1, max_value=120, key="c_age")
            c_proc = st.text_input("Procedure:", value=SAMPLE_CASES["case_custom"]["procedure_name"], key="c_proc")
            c_day = st.number_input("Post-Op Day:", value=int(SAMPLE_CASES["case_custom"]["post_op_day"]), min_value=1, max_value=90, key="c_day")
            c_surgeon = st.text_input("Surgeon:", value=SAMPLE_CASES["case_custom"]["surgeon_name"], key="c_surgeon")

            SAMPLE_CASES["case_custom"]["name"] = c_name
            SAMPLE_CASES["case_custom"]["age"] = c_age
            SAMPLE_CASES["case_custom"]["procedure_name"] = c_proc
            SAMPLE_CASES["case_custom"]["post_op_day"] = c_day
            SAMPLE_CASES["case_custom"]["surgeon_name"] = c_surgeon
            active_case = SAMPLE_CASES["case_custom"]

    st.divider()
    st.subheader("🔑 Gemini API Settings")
    api_key_input = st.text_input(
        "Google Gemini API Key:",
        type="password",
        value=config.GEMINI_API_KEY,
        help="Enter your Google GenAI API key for live Gemini 2.5 Flash inference. If left empty, clinical simulation mode is used."
    )
    if api_key_input:
        config.GEMINI_API_KEY = api_key_input
        st.success("🟢 Gemini 2.5 Flash Connected", icon="✅")
    else:
        st.info("⚡ Mode: Clinical Fallback Engine (No API key needed for demo)", icon="💡")

    st.divider()
    st.subheader("👤 Active Patient Card")
    st.markdown(f"**Name:** {active_case['name']} ({active_case['age']} y/o)")
    st.markdown(f"**ID:** `{active_case['id']}`")
    st.markdown(f"**Procedure:** {active_case['procedure_name']}")
    st.markdown(f"**Surgery Date:** {active_case['surgery_date']}")
    st.markdown(f"**Timeline:** Post-Op Day **{active_case['post_op_day']}**")
    st.markdown(f"**Surgeon:** {active_case['surgeon_name']}")


# Top Header Banner
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.title("🩺 SurgiHeal Clinical Guardian")
    st.markdown(f"**Active Monitoring**: *{active_case['name']}* | **Procedure**: *{active_case['procedure_name']}* | **Day {active_case['post_op_day']}**")
with col_head2:
    st.markdown("<br>", unsafe_allow_html=True)
    if active_case["case_type"] == "infection":
        st.markdown('<div class="badge-urgent">⚠️ CLINICAL ALERT: SSI RISK</div>', unsafe_allow_html=True)
    elif "DVT" in active_case.get("summary_snippet", ""):
        st.markdown('<div class="badge-urgent">🚨 EMERGENCY: DVT TRIAGE</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="badge-normal">🟢 ON TRACK: NORMAL HEALING</div>', unsafe_allow_html=True)


# Main Tabs Navigation
tab_wound, tab_roadmap, tab_triage, tab_surgeon = st.tabs([
    "🩹 Wound Guardian (Vision)",
    "📋 Recovery Roadmap & Meds",
    "💬 24/7 Triage Copilot",
    "🩺 Surgeon Command Center"
])


# ==========================================
# TAB 1: WOUND GUARDIAN (MULTIMODAL VISION)
# ==========================================
with tab_wound:
    st.subheader("Multimodal Surgical Incision Inspection")
    st.caption("Inspect surgical incisions for erythema spread, wound edge dehiscence, exudate characteristics, and early Surgical Site Infection (SSI) detection.")

    col_w1, col_w2 = st.columns([1, 1])

    with col_w1:
        st.markdown("### 📸 1. Incision Photo")
        photo_options = ["Upload Photo (PNG/JPG)", "Webcam Snapshot", "Realistic Clinical Case Photo"] if st.session_state.patient_case_key == "case_custom" else ["Realistic Clinical Case Photo", "Upload Photo (PNG/JPG)", "Webcam Snapshot"]
        photo_source = st.radio(
            "Select Photo Source:",
            photo_options,
            horizontal=True
        )

        image_bytes = None
        if photo_source == "Upload Photo (PNG/JPG)":
            uploaded_file = st.file_uploader("Upload incision photo:", type=["png", "jpg", "jpeg"], key="wound_file_uploader")
            if uploaded_file:
                image_bytes = uploaded_file.getvalue()
                st.session_state["uploaded_wound_img"] = image_bytes
                st.session_state["uploaded_wound_case"] = st.session_state.patient_case_key
                st.image(image_bytes, caption=f"Uploaded Incision Photo — {active_case['name']}", use_container_width=True)
            elif (
                "uploaded_wound_img" in st.session_state
                and st.session_state.get("uploaded_wound_case") == st.session_state.patient_case_key
            ):
                image_bytes = st.session_state["uploaded_wound_img"]
                st.image(image_bytes, caption=f"Uploaded Incision Photo — {active_case['name']} (Active)", use_container_width=True)
            else:
                image_bytes = get_case_image_bytes(st.session_state.patient_case_key)
                st.info("Upload your patient incision photo above, or review default case photo:")
                st.image(image_bytes, caption="Case Incision Photo", use_container_width=True)
        elif photo_source == "Webcam Snapshot":
            cam_file = st.camera_input("Take a photo of the incision:")
            if cam_file:
                image_bytes = cam_file.getvalue()
                st.session_state["uploaded_wound_img"] = image_bytes
                st.session_state["uploaded_wound_case"] = st.session_state.patient_case_key
                st.image(image_bytes, caption="Webcam Incision Photo", use_container_width=True)
            else:
                image_bytes = get_case_image_bytes(st.session_state.patient_case_key)
        else:
            image_bytes = get_case_image_bytes(st.session_state.patient_case_key)
            st.image(image_bytes, caption=f"Clinical Photo — {active_case['procedure_name']} (Day {active_case['post_op_day']})", use_container_width=True)

        st.markdown("### 🌡️ 2. Clinical Context & Vitals")
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            curr_temp = st.number_input("Body Temperature (°F):", value=float(active_case["temperature_f"]), step=0.1)
        with col_v2:
            curr_pain = st.slider("Reported Pain Level (0-10):", 0, 10, int(active_case["reported_pain"]))

        user_notes = st.text_input("Patient Symptoms or Notes:", value=active_case["summary_snippet"])

        analyze_btn = st.button("🔍 Run Gemini SSI Surveillance Analysis", type="primary", use_container_width=True)

    with col_w2:
        st.markdown("### 📊 3. Clinical Intelligence & Healing Assessment")

        # Check if already analyzed or if analyze button pressed
        case_id = active_case["id"]
        if analyze_btn or (case_id not in st.session_state.analysis_results):
            with st.spinner("Analyzing incision with Gemini 2.5 Flash Vision..."):
                patient_ctx = {
                    "procedure_name": active_case["procedure_name"],
                    "post_op_day": active_case["post_op_day"],
                    "reported_pain": curr_pain,
                    "temperature_f": curr_temp,
                    "notes": user_notes
                }
                res = ai_service.analyze_wound_image(
                    image_bytes=image_bytes,
                    patient_context=patient_ctx,
                    api_key=config.GEMINI_API_KEY
                )
                st.session_state.analysis_results[case_id] = res

        result: WoundAnalysisResult = st.session_state.analysis_results[case_id]

        # Status Banner
        if "Urgent" in result.healing_status:
            st.markdown(f'<div class="badge-urgent" style="font-size:1.1rem; width:100%; text-align:center;">🔴 {result.healing_status}</div>', unsafe_allow_html=True)
        elif "Borderline" in result.healing_status:
            st.markdown(f'<div class="badge-caution" style="font-size:1.1rem; width:100%; text-align:center;">🟡 {result.healing_status}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="badge-normal" style="font-size:1.1rem; width:100%; text-align:center;">🟢 {result.healing_status}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Metrics Row
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("SSI Risk Probability", f"{result.infection_risk_percentage}%", delta=f"{result.infection_risk_percentage - 20}%" if result.infection_risk_percentage > 20 else None, delta_color="inverse")
        with m2:
            st.metric("Erythema Spread Score", f"{result.erythema_score} / 10")
        with m3:
            st.metric("Wound Drainage", result.drainage_type.split(' ')[0])

        st.divider()

        # Perspective Switcher: Clinician View vs Patient View
        perspective = st.radio("Display Perspective:", ["Patient Reassurance Card", "Clinician Technical Analysis"], horizontal=True)

        if perspective == "Patient Reassurance Card":
            st.markdown(f"""
            <div class="callout-box">
                <h4>💬 Plain-English Recovery Summary</h4>
                <p style="font-size: 1.05rem; line-height: 1.5;">{result.patient_plain_english_summary}</p>
            </div>
            """, unsafe_allow_html=True)

            if result.red_flags:
                st.error("⚠️ Red Flag Symptoms Detected:")
                for rf in result.red_flags:
                    st.markdown(f"- 🔴 **{rf}**")

            st.markdown("#### ✅ Recommended Patient Next Steps:")
            for action in result.action_recommendations:
                st.markdown(f"- {action}")

        else:
            st.markdown("#### 🩺 Objective Clinical Findings:")
            for obs in result.clinical_observations:
                st.markdown(f"- {obs}")

            st.markdown(f"**Wound Edge Approximation:** `{result.edge_approximation}`")
            st.markdown(f"**Periwound Swelling / Edema:** `{result.swelling_level}`")
            st.markdown(f"**Exudate / Drainage Type:** `{result.drainage_type}`")

            if result.red_flags:
                st.markdown("#### 🚨 Clinical Escalation Criteria:")
                for rf in result.red_flags:
                    st.markdown(f"- ⚠️ `{rf}`")

# ==========================================
# TAB 2: RECOVERY ROADMAP & MEDICATIONS
# ==========================================
with tab_roadmap:
    st.subheader("Intelligent Discharge Paperwork & Recovery Plan")
    st.caption("Extracts surgical orders, medication tapering schedules, and hygiene milestones directly from hospital discharge summaries.")

    if st.session_state.patient_case_key == "case_custom":
        with st.expander("📤 Upload / Paste Custom Discharge Paperwork (AI Structured Parser)", expanded=True):
            st.markdown("Paste real hospital discharge paperwork, doctor instructions, or medication orders to extract a personalized recovery roadmap:")
            pasted_notes = st.text_area(
                "Discharge Summary Text:",
                height=120,
                placeholder="e.g.: Patient discharged Day 1 post right knee arthroplasty by Dr. Vance. Instructions: Elevate operative leg. Weight-bearing as tolerated with walker. Shower allowed after 48 hours with Aquacel dressing sealed. Medications: Lovenox 40mg daily subcutaneously x 14 days, Tylenol 1000mg q8h PRN pain, Keflex 500mg BID x 7 days. Return to clinic Day 14 for staple removal.",
                key="custom_discharge_input"
            )
            parse_col1, parse_col2 = st.columns([1, 2])
            with parse_col1:
                if st.button("⚡ Parse Discharge Orders with AI", type="secondary", use_container_width=True):
                    if pasted_notes.strip():
                        with st.spinner("Analyzing discharge instructions with Gemini 2.5 Flash..."):
                            parsed_summary = ai_service.parse_discharge_document(
                                document_text=pasted_notes,
                                api_key=config.GEMINI_API_KEY
                            )
                            SAMPLE_CASES["case_custom"]["discharge"] = parsed_summary
                            st.success("Recovery roadmap & medications extracted!")
                            st.rerun()
                    else:
                        st.warning("Please paste or type discharge document text above.")
        st.divider()

    discharge: DischargeSummary = active_case["discharge"]

    col_r1, col_r2 = st.columns([1, 1])

    with col_r1:
        st.markdown("### 📄 Post-Operative Clinical Orders")
        st.markdown(f"**Procedure:** {discharge.procedure_name}")
        st.markdown(f"**Operating Surgeon:** {discharge.surgeon_name}")
        st.markdown(f"**Weight-Bearing Restrictions:** {discharge.weight_bearing_status}")
        st.markdown(f"**Showering & Bathing Guidelines:** {discharge.showering_guidelines}")

        st.markdown("#### 🩹 Daily Wound Care Protocol")
        for step in discharge.wound_care_routine:
            st.markdown(f"- {step}")

        st.markdown("#### 🚨 Hospital Red Flag Warning Symptoms")
        for sym in discharge.emergency_symptoms:
            st.markdown(f"- 🔴 {sym}")

    with col_r2:
        st.markdown("### 💊 Daily Medication Schedule & Safety")
        med_data = []
        for m in discharge.medications:
            med_data.append({
                "Medication": m.name,
                "Dosage": m.dosage,
                "Frequency": m.frequency,
                "Clinical Purpose": m.purpose,
                "Special Instructions": m.instructions
            })
        df_meds = pd.DataFrame(med_data)
        st.dataframe(df_meds, use_container_width=True, hide_index=True)

        st.divider()
        st.markdown("### 🗓️ Recovery Milestone Checklist")
        for ms in discharge.milestones:
            checked = st.checkbox(
                f"**Day {ms.day_offset}: {ms.title}** — {ms.description}",
                value=ms.is_completed,
                key=f"milestone_{active_case['id']}_{ms.day_offset}"
            )


# ==========================================
# TAB 3: 24/7 POST-OP TRIAGE COPILOT
# ==========================================
with tab_triage:
    st.subheader("24/7 Post-Operative Symptom & Triage Copilot")
    st.caption("Real-time clinical screening for postoperative emergencies (Deep Vein Thrombosis, Pulmonary Embolism, Sepsis, and Wound Dehiscence).")

    # Quick test prompts for judges
    st.markdown("**⚡ 1-Click Test Scenarios for Judges:**")
    tcol1, tcol2, tcol3 = st.columns(3)
    quick_query = None
    with tcol1:
        if st.button("🧪 Test DVT Symptom", help="Triggers deep vein thrombosis screening alert"):
            quick_query = "My right calf is swollen, hot, and cramps painfully. I feel slightly short of breath."
    with tcol2:
        if st.button("🧪 Test SSI / Infection", help="Triggers infection protocol"):
            quick_query = "The skin around my incision is burning hot, bright red, and I have a fever of 101.4°F with yellowish fluid leaking."
    with tcol3:
        if st.button("🧪 Test Normal Recovery Question", help="Routine inquiry"):
            quick_query = "Is it normal to feel a gentle pinching around the surgical staples when I bend my joint?"

    # Display Chat History
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "triage" in msg:
                t: TriageAssessment = msg["triage"]
                if "Emergency" in t.urgency_level:
                    st.markdown(f"""
                    <div class="emergency-box">
                        <h4 style="color:#b91c1c; margin:0;">🚨 URGENCY: {t.urgency_level}</h4>
                        <p><strong>Suspected Issue:</strong> {t.suspected_condition}</p>
                        <p><strong>Primary Clinical Concern:</strong> {t.primary_concern}</p>
                        <p><strong>Immediate Emergency Actions:</strong></p>
                        <ul>{''.join([f'<li>{act}</li>' for act in t.immediate_actions])}</ul>
                    </div>
                    """, unsafe_allow_html=True)
                elif "Urgent" in t.urgency_level:
                    st.markdown(f"""
                    <div class="callout-box" style="border-left-color:#f59e0b; background-color:#fffbeb;">
                        <h4 style="color:#b45309; margin:0;">⚠️ URGENCY: {t.urgency_level}</h4>
                        <p><strong>Suspected Issue:</strong> {t.suspected_condition}</p>
                        <p><strong>Recommended Actions:</strong></p>
                        <ul>{''.join([f'<li>{act}</li>' for act in t.immediate_actions])}</ul>
                    </div>
                    """, unsafe_allow_html=True)

    # Chat Input
    prompt = st.chat_input("Type your question or symptom (e.g. pain changes, swelling, fever, meds)...") or quick_query
    if prompt:
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Clinical triage reasoning in progress..."):
                patient_info = {
                    "name": active_case["name"],
                    "procedure_name": active_case["procedure_name"],
                    "post_op_day": active_case["post_op_day"],
                    "last_reported_pain": active_case["reported_pain"],
                    "last_temp_f": active_case["temperature_f"]
                }
                triage_res = ai_service.screen_symptoms_chat(
                    user_query=prompt,
                    patient_profile=patient_info,
                    api_key=config.GEMINI_API_KEY
                )

                response_text = f"**Clinical Assessment**: {triage_res.clinical_rationale}"
                st.markdown(response_text)

                if "Emergency" in triage_res.urgency_level:
                    st.markdown(f"""
                    <div class="emergency-box">
                        <h4 style="color:#b91c1c; margin:0;">🚨 URGENCY: {triage_res.urgency_level}</h4>
                        <p><strong>Suspected Condition:</strong> {triage_res.suspected_condition}</p>
                        <p><strong>Primary Concern:</strong> {triage_res.primary_concern}</p>
                        <p><strong>Required Immediate Protocol:</strong></p>
                        <ul>{''.join([f'<li>{act}</li>' for act in triage_res.immediate_actions])}</ul>
                    </div>
                    """, unsafe_allow_html=True)
                elif "Urgent" in triage_res.urgency_level:
                    st.markdown(f"""
                    <div class="callout-box" style="border-left-color:#f59e0b; background-color:#fffbeb;">
                        <h4 style="color:#b45309; margin:0;">⚠️ URGENCY: {triage_res.urgency_level}</h4>
                        <p><strong>Suspected Condition:</strong> {triage_res.suspected_condition}</p>
                        <p><strong>Actions:</strong></p>
                        <ul>{''.join([f'<li>{act}</li>' for act in triage_res.immediate_actions])}</ul>
                    </div>
                    """, unsafe_allow_html=True)

                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": response_text,
                    "triage": triage_res
                })


# ==========================================
# TAB 4: SURGEON COMMAND CENTER
# ==========================================
with tab_surgeon:
    st.subheader("Surgeon & Clinical Team Command Center")
    st.caption("Remote Outpatient Monitoring Dashboard for surgical practices to triage complications before readmission occurs.")

    # High-level statistics
    scol1, scol2, scol3, scol4 = st.columns(4)
    with scol1:
        st.metric("Monitored Outpatients", "28 Patients", "+3 Today")
    with scol2:
        st.metric("High SSI Risk Alerts", "2 Urgent", delta="1 Pending Review", delta_color="inverse")
    with scol3:
        st.metric("30-Day Readmission Rate", "1.4%", "-3.1% vs National Benchmark")
    with scol4:
        st.metric("Avg Clinical Scribe Time Saved", "42 mins/day", "+15%")

    st.divider()

    # Outpatient Registry
    st.markdown("### 📋 Outpatient Surveillance Registry")
    registry_patients = [
        {
            "Patient ID": "PAT-2094",
            "Name": "Marcus Vance",
            "Procedure": "Laparoscopic Appendectomy",
            "Post-Op Day": "Day 6",
            "Temp (°F)": 101.2,
            "Pain (0-10)": 7,
            "SSI Risk": "84%",
            "Triage Status": "🔴 Urgent SSI Warning",
            "Last Incision Update": "14 mins ago"
        },
        {
            "Patient ID": "PAT-3041",
            "Name": "Robert Chen",
            "Procedure": "Total Hip Arthroplasty",
            "Post-Op Day": "Day 3",
            "Temp (°F)": 99.1,
            "Pain (0-10)": 6,
            "SSI Risk": "6%",
            "Triage Status": "🚨 DVT Emergency Alert",
            "Last Incision Update": "1 hour ago"
        },
        {
            "Patient ID": "PAT-1082",
            "Name": "Sarah Jenkins",
            "Procedure": "Total Knee Arthroplasty",
            "Post-Op Day": "Day 4",
            "Temp (°F)": 98.6,
            "Pain (0-10)": 3,
            "SSI Risk": "8%",
            "Triage Status": "🟢 On Track / Normal",
            "Last Incision Update": "2 hours ago"
        },
        {
            "Patient ID": "PAT-4103",
            "Name": "Elena Rostova",
            "Procedure": "Cesarean Section (C-Section)",
            "Post-Op Day": "Day 5",
            "Temp (°F)": 98.4,
            "Pain (0-10)": 2,
            "SSI Risk": "11%",
            "Triage Status": "🟢 On Track / Normal",
            "Last Incision Update": "3 hours ago"
        }
    ]

    if st.session_state.patient_case_key == "case_custom":
        cp = SAMPLE_CASES["case_custom"]
        c_res = st.session_state.analysis_results.get(cp["id"])
        c_risk = f"{c_res.infection_risk_percentage}%" if c_res else "Pending"
        c_status = "🟢 Active Surveillance"
        if c_res:
            if "Urgent" in c_res.healing_status:
                c_status = "🔴 Urgent SSI Warning"
            elif "Borderline" in c_res.healing_status:
                c_status = "🟡 Needs Monitoring"
            else:
                c_status = "🟢 On Track / Normal"
        registry_patients.insert(0, {
            "Patient ID": cp["id"],
            "Name": cp["name"],
            "Procedure": cp["procedure_name"],
            "Post-Op Day": f"Day {cp['post_op_day']}",
            "Temp (°F)": float(cp["temperature_f"]),
            "Pain (0-10)": int(cp["reported_pain"]),
            "SSI Risk": c_risk,
            "Triage Status": c_status,
            "Last Incision Update": "Just now"
        })

    df_reg = pd.DataFrame(registry_patients)
    st.dataframe(df_reg, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("### ⚡ Quick Surgeon Action Bar")
    acol1, acol2, acol3 = st.columns(3)
    with acol1:
        if st.button("✅ Send Routine Reassurance Note", use_container_width=True):
            st.success(f"Sent reassurance confirmation to {active_case['name']} for routine recovery.")
    with acol2:
        if st.button("⚠️ Order Home Health Wound Check", use_container_width=True):
            st.warning(f"Home Health nursing dispatch request submitted for {active_case['name']}.")
    with acol3:
        if st.button("🚨 Direct Patient to Same-Day Emergency Clinic", use_container_width=True):
            st.error(f"Urgent clinical escalation SMS and push alert dispatched to {active_case['name']}.")
