import io
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from models import (
    PatientProfile,
    WoundAnalysisResult,
    DischargeSummary,
    MedicationItem,
    RecoveryMilestone,
    TriageAssessment
)

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets" / "cases"
PROGRESSION_DIR = BASE_DIR / "assets" / "progression"

CASE_IMAGE_MAP = {
    "case_a": ASSETS_DIR / "case_a_knee.jpg",
    "case_b": ASSETS_DIR / "case_b_appendix.jpg",
    "case_c": ASSETS_DIR / "case_c_hip.jpg",
    "case_custom": ASSETS_DIR / "case_a_knee.jpg",
}

PROGRESSION_IMAGE_MAP = {
    "case_a": {
        "day_1": PROGRESSION_DIR / "day_1_knee_baseline.jpg",
        "final_day": PROGRESSION_DIR / "day_14_knee_healed.jpg",
    },
    "case_c": {
        "day_1": PROGRESSION_DIR / "day_1_hip.jpg",
        "final_day": PROGRESSION_DIR / "day_14_hip.jpg",
    },
    "case_custom": {
        "day_1": PROGRESSION_DIR / "custom_day1.jpg",
        "final_day": PROGRESSION_DIR / "custom_final.jpg",
    },
}


def get_progression_image_bytes(stage: str = "day_1", case_key: str = "case_a") -> bytes:
    """
    Returns realistic clinical medical photography for healing progression
    (Day 1 fresh incision baseline vs Day 14 fully healed scar).
    """
    stage_key = "final_day" if stage.lower() in ("day_14", "final_day") else "day_1"
    case_images = PROGRESSION_IMAGE_MAP.get(case_key, PROGRESSION_IMAGE_MAP["case_a"])
    if stage_key in case_images:
        p = case_images[stage_key]
        if p.exists():
            return p.read_bytes()
    return create_synthetic_incision_image("normal")


def get_case_image_bytes(case_key_or_type: str = "case_a") -> bytes:
    """
    Returns realistic clinical medical photography for the selected case study.
    Falls back to synthetic illustration if the image file is unavailable.
    """
    if case_key_or_type in CASE_IMAGE_MAP:
        img_path = CASE_IMAGE_MAP[case_key_or_type]
        if img_path.exists():
            return img_path.read_bytes()

    if case_key_or_type == "infection":
        inf_path = CASE_IMAGE_MAP.get("case_b")
        if inf_path and inf_path.exists():
            return inf_path.read_bytes()
    elif case_key_or_type in ("normal", "dvt"):
        norm_path = CASE_IMAGE_MAP.get("case_a")
        if norm_path and norm_path.exists():
            return norm_path.read_bytes()

    return create_synthetic_incision_image(case_key_or_type)


def create_synthetic_incision_image(case_type: str = "normal") -> bytes:
    """
    Generates a synthetic medical illustration of a surgical incision
    to ensure seamless demo and testing without needing private clinical photos.
    """
    width, height = 400, 300
    
    if case_type == "infection":
        # Flushed, erythematous skin tone with spreading redness halo
        bg_color = (235, 180, 170)
        img = Image.new("RGB", (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Spreading erythema / cellulitic halo around incision
        for r in range(120, 20, -10):
            alpha_red = int(220 + (120 - r) * 0.2)
            draw.ellipse(
                [width//2 - r*1.2, height//2 - r*0.7, width//2 + r*1.2, height//2 + r*0.7],
                fill=(alpha_red, 130 + r//2, 130 + r//2)
            )
        
        # Surgical incision line (slightly widened / inflamed)
        draw.line([width//2, 70, width//2, 230], fill=(160, 20, 20), width=6)
        
        # Purulent exudate spot simulation
        draw.ellipse([width//2 - 8, 140, width//2 + 8, 160], fill=(230, 220, 140))
        
        # Surgical sutures / staples with inflammation halos
        for y in range(90, 220, 25):
            draw.ellipse([width//2 - 25, y - 6, width//2 + 25, y + 6], fill=(220, 100, 100))
            draw.line([width//2 - 20, y, width//2 + 20, y], fill=(60, 60, 60), width=3)
            # Punctures
            draw.ellipse([width//2 - 22, y - 2, width//2 - 18, y + 2], fill=(120, 20, 20))
            draw.ellipse([width//2 + 18, y - 2, width//2 + 22, y + 2], fill=(120, 20, 20))
            
    else:
        # Healthy skin tone (clean pinkish-tan)
        bg_color = (240, 215, 200)
        img = Image.new("RGB", (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Subtle healthy inflammatory margin (< 5mm)
        draw.ellipse(
            [width//2 - 25, 75, width//2 + 25, 225],
            fill=(245, 195, 185)
        )
        
        # Well-approximated, crisp incision line
        draw.line([width//2, 80, width//2, 220], fill=(180, 70, 70), width=3)
        
        # Neat surgical staples / sutures
        for y in range(95, 215, 25):
            draw.line([width//2 - 16, y, width//2 + 16, y], fill=(70, 70, 80), width=2)
            draw.ellipse([width//2 - 18, y - 1, width//2 - 14, y + 3], fill=(150, 90, 90))
            draw.ellipse([width//2 + 14, y - 1, width//2 + 18, y + 3], fill=(150, 90, 90))

    # Caption badge
    draw.rectangle([10, 10, 160, 32], fill=(40, 40, 50))
    # We draw simple text if default font allows
    draw.text((16, 14), f"Case: {case_type.upper()}", fill=(255, 255, 255))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# Curated Demo Case Studies
SAMPLE_CASES = {
    "case_a": {
        "id": "PAT-1082",
        "name": "Sarah Jenkins",
        "age": 62,
        "procedure_name": "Total Knee Arthroplasty (Left Knee)",
        "surgery_date": "2026-09-10",
        "post_op_day": 4,
        "surgeon_name": "Dr. Eleanor Vance, MD (Orthopedic Surgery)",
        "reported_pain": 3,
        "temperature_f": 98.6,
        "case_type": "normal",
        "image_path": str(ASSETS_DIR / "case_a_knee.jpg"),
        "summary_snippet": "Day 4 post-op knee replacement. Normal post-surgical healing with minimal serous exudate and intact surgical staples.",
        "discharge": DischargeSummary(
            procedure_name="Total Knee Arthroplasty (Left)",
            surgery_date="2026-09-10",
            surgeon_name="Dr. Eleanor Vance, MD",
            weight_bearing_status="Weight-bearing as tolerated with rolling walker or crutches.",
            showering_guidelines="Shower permitted with waterproof dressing intact. Do not submerge leg in bathtub or pool for 4 weeks.",
            wound_care_routine=[
                "Inspect incision daily for redness, warmth, or drainage.",
                "Keep Aquacel surgical dressing intact until Day 7 follow-up.",
                "Elevate operative leg above heart level when resting to minimize swelling."
            ],
            medications=[
                MedicationItem(
                    name="Enoxaparin (Lovenox)",
                    dosage="40 mg",
                    frequency="Once daily subcutaneously",
                    purpose="DVT / Blood clot prophylaxis",
                    instructions="Take at the same time every evening for 14 days."
                ),
                MedicationItem(
                    name="Acetaminophen (Tylenol)",
                    dosage="1000 mg",
                    frequency="Every 8 hours as needed",
                    purpose="Baseline pain management",
                    instructions="Do not exceed 3000 mg in 24 hours."
                ),
                MedicationItem(
                    name="Oxycodone",
                    dosage="5 mg",
                    frequency="Every 6 hours PRN for breakthrough pain (pain > 6)",
                    purpose="Severe breakthrough pain",
                    instructions="Use only when necessary. Taper off as pain improves."
                ),
                MedicationItem(
                    name="Cephalexin (Keflex)",
                    dosage="500 mg",
                    frequency="Twice daily",
                    purpose="Post-operative antibiotic prophylaxis",
                    instructions="Complete full 7-day course."
                )
            ],
            emergency_symptoms=[
                "Calf swelling, redness, or pain (DVT warning).",
                "Shortness of breath or sudden chest pain (PE warning).",
                "Fever greater than 101.0°F (38.3°C).",
                "Purulent (cloudy, thick yellow) drainage from incision."
            ],
            milestones=[
                RecoveryMilestone(day_offset=3, title="First physical therapy session", description="Active assisted knee flexion to 70 degrees.", is_completed=True),
                RecoveryMilestone(day_offset=7, title="Dressing change & wound inspection", description="Remove surgical seal and inspect periwound tissue.", is_completed=False),
                RecoveryMilestone(day_offset=14, title="Staple removal at clinic", description="Remove 24 surgical skin staples with Dr. Vance.", is_completed=False),
                RecoveryMilestone(day_offset=30, title="Independent ambulation milestone", description="Transition from walker to single-point cane.", is_completed=False)
            ]
        ),
        "expected_analysis": WoundAnalysisResult(
            healing_status="Normal / On Track",
            erythema_score=2,
            swelling_level="Mild",
            drainage_type="Serous (Clear/Yellowish)",
            edge_approximation="Well-approximated (Cleanly Closed)",
            infection_risk_percentage=8,
            clinical_observations=[
                "Surgical staples intact with uniform spacing along anterior knee incision.",
                "Mild localized erythema (< 6mm) consistent with normal early inflammatory phase.",
                "Edges cleanly approximated without dehiscence or gap.",
                "Minimal serous exudate; zero purulent drainage noted."
            ],
            patient_plain_english_summary="Your knee incision is healing nicely! The slight pinkness around the staples is a completely normal part of your body's repair process. There are no signs of infection.",
            red_flags=[],
            action_recommendations=[
                "Keep the waterproof dressing clean and dry.",
                "Continue elevating your left leg 3 times a day for 30 minutes.",
                "Continue prescribed physical therapy ankle pumps and quad sets.",
                "Keep your follow-up clinic appointment on Day 7 for staple check."
            ]
        ),
        "mock_chat_query": "My knee feels tight and slightly warm to the touch when I bend it. Is that normal on Day 4?"
    },

    "case_b": {
        "id": "PAT-2094",
        "name": "Marcus Vance",
        "age": 34,
        "procedure_name": "Laparoscopic Appendectomy",
        "surgery_date": "2026-09-08",
        "post_op_day": 6,
        "surgeon_name": "Dr. Carlos Mendez, MD (General Surgery)",
        "reported_pain": 7,
        "temperature_f": 101.2,
        "case_type": "infection",
        "image_path": str(ASSETS_DIR / "case_b_appendix.jpg"),
        "summary_snippet": "Day 6 appendectomy. Presenting with fever 101.2°F, expanding umbilical incision erythema > 2.5cm, and early purulent drainage.",
        "discharge": DischargeSummary(
            procedure_name="Laparoscopic Appendectomy (Complicated)",
            surgery_date="2026-09-08",
            surgeon_name="Dr. Carlos Mendez, MD",
            weight_bearing_status="No lifting over 15 lbs for 2 weeks.",
            showering_guidelines="Shower allowed after 48h; gently pat dry umbilical site. No scrubbing.",
            wound_care_routine=[
                "Check all 3 port sites (umbilicus, left lower quadrant, suprapubic).",
                "Keep Steri-Strips in place until they curl and fall off on their own.",
                "Call clinic if any port exhibits warmth, bad odor, or yellowish discharge."
            ],
            medications=[
                MedicationItem(
                    name="Amoxicillin-Clavulanate (Augmentin)",
                    dosage="875/125 mg",
                    frequency="Twice daily with meals",
                    purpose="Infection control (perforated appendix)",
                    instructions="Take until entire 10-day prescription is finished."
                ),
                MedicationItem(
                    name="Ibuprofen",
                    dosage="600 mg",
                    frequency="Every 6 hours with food",
                    purpose="Inflammation and moderate pain",
                    instructions="Take with food to prevent gastric irritation."
                )
            ],
            emergency_symptoms=[
                "Temperature above 100.4°F.",
                "Spreading redness larger than a coin around any incision.",
                "Foul odor or thick yellowish fluid leaking from wounds.",
                "Worsening abdominal cramping or inability to tolerate liquids."
            ],
            milestones=[
                RecoveryMilestone(day_offset=2, title="Tolerate regular diet", description="Transition from clear liquids to soft solids.", is_completed=True),
                RecoveryMilestone(day_offset=7, title="Post-op tele-visit", description="Review port healing and bowel regularity.", is_completed=False),
                RecoveryMilestone(day_offset=14, title="Full activity clearance", description="Resume gym workouts and heavy lifting.", is_completed=False)
            ]
        ),
        "expected_analysis": WoundAnalysisResult(
            healing_status="Urgent / High Risk of SSI",
            erythema_score=7,
            swelling_level="Moderate",
            drainage_type="Purulent (Pus/Cloudy)",
            edge_approximation="Minor Gap / Separation",
            infection_risk_percentage=84,
            clinical_observations=[
                "Expanding periumbilical erythema extending > 2.5 cm from the incision margin.",
                "Cloudy yellowish exudate (purulent) pooling at inferior aspect of wound.",
                "Localized periwound edema and induration visible.",
                "Reported low-grade/moderate fever (101.2°F) strongly correlates with early superficial SSI."
            ],
            patient_plain_english_summary="Warning: Your incision shows signs of an early infection (Surgical Site Infection). The redness is spreading past the incision line, there is cloudy fluid, and your fever is 101.2°F. Please contact your surgeon right away.",
            red_flags=[
                "Spreading periwound redness > 2.5 cm",
                "Cloudy/purulent exudate detected",
                "Active fever of 101.2°F (above clinical threshold 100.4°F)",
                "Pain increasing on Day 6 instead of improving"
            ],
            action_recommendations=[
                "Call Dr. Carlos Mendez's clinic immediately at (555) 349-8000 or proceed to urgent care/ER.",
                "Do not apply antibiotic ointments or creams without the surgeon's explicit instruction.",
                "Place a sterile dry gauze lightly over the site to absorb drainage.",
                "Take a photo now to show the doctor how much the redness is expanding."
            ]
        ),
        "mock_chat_query": "The skin around my belly button is hot and red, and I feel feverish. Should I wait until tomorrow to see my doctor?"
    },

    "case_c": {
        "id": "PAT-3041",
        "name": "Robert Chen",
        "age": 58,
        "procedure_name": "Total Hip Arthroplasty (Right Anterior)",
        "surgery_date": "2026-09-11",
        "post_op_day": 3,
        "surgeon_name": "Dr. Sarah Patel, MD (Orthopedic Surgery)",
        "reported_pain": 6,
        "temperature_f": 99.1,
        "case_type": "normal",
        "image_path": str(ASSETS_DIR / "case_c_hip.jpg"),
        "summary_snippet": "Day 3 hip replacement. Hip incision itself is intact, but patient presents with acute right calf tenderness, swelling, and mild dyspnea (Suspected DVT/PE Emergency).",
        "discharge": DischargeSummary(
            procedure_name="Total Hip Arthroplasty (Right Anterior Approach)",
            surgery_date="2026-09-11",
            surgeon_name="Dr. Sarah Patel, MD",
            weight_bearing_status="Full weight-bearing with walker support.",
            showering_guidelines="Shower permitted with waterproof Aquacel dressing.",
            wound_care_routine=[
                "Leave incision sealed; change outer pad if saturated.",
                "Wear graduated compression stockings (TED hose) on both legs during daytime.",
                "Perform ankle pump exercises 10 times every waking hour."
            ],
            medications=[
                MedicationItem(
                    name="Aspirin (EC)",
                    dosage="81 mg",
                    frequency="Twice daily",
                    purpose="VTE / DVT prevention",
                    instructions="Take with meals for 30 days post-op."
                ),
                MedicationItem(
                    name="Celecoxib (Celebrex)",
                    dosage="200 mg",
                    frequency="Once daily",
                    purpose="Anti-inflammatory pain management",
                    instructions="Take in morning."
                )
            ],
            emergency_symptoms=[
                "Unilateral calf cramp, swelling, or tenderness (Deep Vein Thrombosis).",
                "Sudden shortness of breath, rapid heart rate, or chest pain (Pulmonary Embolism).",
                "Sudden inability to bear weight on the operative leg."
            ],
            milestones=[
                RecoveryMilestone(day_offset=1, title="Hospital discharge home", description="Achieved independent transfer and stair climbing.", is_completed=True),
                RecoveryMilestone(day_offset=14, title="2-Week clinical checkup", description="Wound evaluation and hip range check.", is_completed=False),
                RecoveryMilestone(day_offset=42, title="6-Week X-ray evaluation", description="Bony ingrowth verification of hip implant.", is_completed=False)
            ]
        ),
        "expected_analysis": WoundAnalysisResult(
            healing_status="Normal / On Track",
            erythema_score=1,
            swelling_level="Mild",
            drainage_type="None",
            edge_approximation="Well-approximated (Cleanly Closed)",
            infection_risk_percentage=6,
            clinical_observations=[
                "Right anterior hip incision clean, dry, and intact.",
                "Dermabond/Steri-strip closure without dehiscence.",
                "Periwound margins show no signs of cellulitis or erythema spread.",
                "Note: Clinical emergency focus is remote from incision (lower leg DVT suspicion)."
            ],
            patient_plain_english_summary="Your hip incision is physically healing very well with no signs of wound infection. However, your reported calf symptoms require immediate medical attention.",
            red_flags=[
                "EMERGENCY RED FLAG: Right calf throbbing, severe swelling, and warmth reported.",
                "Concurrent mild shortness of breath reported — high clinical index of suspicion for DVT/PE."
            ],
            action_recommendations=[
                "EMERGENCY: Seek immediate emergency evaluation (ER or call 911) for urgent lower extremity venous Doppler ultrasound to evaluate for DVT.",
                "Do not massage or vigorously rub your calf.",
                "Keep leg elevated while waiting for medical transport."
            ]
        ),
        "mock_chat_query": "My hip incision looks clean, but my right calf is swollen, hot, and cramps terribly when I put my foot down. I also feel slightly out of breath."
    },

    "case_custom": {
        "id": "PAT-USER",
        "name": "Custom Patient",
        "age": 45,
        "procedure_name": "Post-Operative Wound Evaluation",
        "surgery_date": "2026-09-14",
        "post_op_day": 3,
        "surgeon_name": "Dr. Attending Surgeon, MD",
        "reported_pain": 3,
        "temperature_f": 98.6,
        "case_type": "custom",
        "image_path": str(ASSETS_DIR / "case_a_knee.jpg"),
        "summary_snippet": "Custom patient case: Upload your own incision photo, specify vitals, and parse your custom discharge paperwork.",
        "discharge": DischargeSummary(
            procedure_name="Post-Operative Wound Evaluation",
            surgery_date="2026-09-14",
            surgeon_name="Dr. Attending Surgeon, MD",
            weight_bearing_status="Weight-bearing as tolerated or per surgical instructions.",
            showering_guidelines="Shower permitted with waterproof dressing intact. Gently pat dry; do not soak in tub.",
            wound_care_routine=[
                "Inspect incision daily for erythema, warmth, or drainage.",
                "Keep surgical dressing clean and dry.",
                "Follow postoperative elevation and movement guidance."
            ],
            medications=[
                MedicationItem(
                    name="Acetaminophen / Prescribed Analgesic",
                    dosage="Standard prescribed dose",
                    frequency="Every 6-8 hours as needed",
                    purpose="Baseline post-op pain management",
                    instructions="Take with water after meals."
                ),
                MedicationItem(
                    name="Prophylactic Antibiotic (if prescribed)",
                    dosage="As directed",
                    frequency="Twice daily",
                    purpose="Infection prevention",
                    instructions="Complete full prescribed regimen."
                )
            ],
            emergency_symptoms=[
                "Temperature greater than 100.4°F (38°C).",
                "Spreading periwound redness expanding > 1.5 cm.",
                "Foul odor or cloudy yellowish/purulent drainage.",
                "Sudden calf swelling, warmth, or chest pain / shortness of breath."
            ],
            milestones=[
                RecoveryMilestone(day_offset=1, title="Discharge home baseline", description="Safe departure from clinic or hospital.", is_completed=True),
                RecoveryMilestone(day_offset=7, title="Post-op wound check", description="Clinical or telehealth wound progress evaluation.", is_completed=False),
                RecoveryMilestone(day_offset=14, title="Follow-up & suture evaluation", description="Closure check and physical recovery assessment.", is_completed=False)
            ]
        ),
        "expected_analysis": WoundAnalysisResult(
            healing_status="Ready for AI Analysis",
            erythema_score=1,
            swelling_level="Mild",
            drainage_type="None",
            edge_approximation="Well-approximated (Cleanly Closed)",
            infection_risk_percentage=10,
            clinical_observations=[
                "Custom patient case loaded.",
                "Ready to evaluate uploaded clinical photo with Gemini 2.5 Flash Vision."
            ],
            patient_plain_english_summary="Your custom case is loaded! Upload your incision photo and click 'Run Gemini SSI Surveillance Analysis' to get an instant AI evaluation.",
            red_flags=[],
            action_recommendations=[
                "Upload a clear, focused photo of the incision or use the webcam.",
                "Update patient vitals (temperature and pain score) if known.",
                "Click 'Run Gemini SSI Surveillance Analysis'."
            ]
        ),
        "mock_chat_query": "How does my incision look today, and what signs of healing or infection should I watch for?"
    }
}
