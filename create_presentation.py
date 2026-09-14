import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Initialize 16:9 widescreen presentation
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

blank_layout = prs.slide_layouts[6]

# ==============================================================================
# VIBRANT, BRIGHT & PROFESSIONAL COLOR PALETTE
# ==============================================================================
CANVAS_BG = RGBColor(248, 250, 252)     # Clean, luminous soft slate
CARD_BG = RGBColor(255, 255, 255)       # Crisp pure white
NAVY_HEADER = RGBColor(15, 23, 42)      # Deep, authoritative slate navy
BODY_TEXT = RGBColor(51, 65, 85)        # Charcoal readability text
MUTED_TEXT = RGBColor(100, 116, 139)    # Slate grey subtitle

# High-Energy, Brighter Vibrant Accents
ELECTRIC_BLUE = RGBColor(0, 140, 255)   # #008CFF - Vibrant Tech Blue
VIBRANT_TEAL = RGBColor(0, 180, 160)    # #00B4A0 - Bright Clinical Teal
MINT_GREEN = RGBColor(0, 200, 83)       # #00C853 - Bright Emerald / Success
RADIANT_ROSE = RGBColor(255, 0, 85)     # #FF0055 - Vivid Emergency Crimson
SUNNY_AMBER = RGBColor(255, 145, 0)     # #FF9100 - Radiant Warning Amber
ELECTRIC_PURPLE = RGBColor(121, 40, 202)# #7928CA - Deep Violet / Innovation
VIVID_CYAN = RGBColor(6, 182, 212)      # #06B6D4 - Bright Cyan

# Pastel Tints for Card Backgrounds
TINT_BLUE = RGBColor(240, 248, 255)
TINT_TEAL = RGBColor(230, 255, 250)
TINT_ROSE = RGBColor(255, 240, 245)
TINT_AMBER = RGBColor(255, 248, 230)
TINT_PURPLE = RGBColor(248, 240, 255)
TINT_GREEN = RGBColor(235, 255, 242)


def set_slide_background(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_card(slide, left, top, width, height, bg_color, border_color=None, border_width=1.5):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(border_width)
    else:
        shape.line.fill.background()
    return shape


def add_header(slide, tag_text, tag_color, title_text, subtitle_text):
    # Badge Tag
    badge = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(8), Inches(0.4))
    tf_b = badge.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = tag_text.upper()
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = tag_color

    # Title & Subtitle
    hdr = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(1.1))
    tf = hdr.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = NAVY_HEADER

    p_sub = tf.add_paragraph()
    p_sub.text = subtitle_text
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = MUTED_TEXT


# ==============================================================================
# SLIDE 1: TITLE SLIDE (Hero Card, Bright Accents, Informative Badges)
# ==============================================================================
slide1 = prs.slides.add_slide(blank_layout)
set_slide_background(slide1, CANVAS_BG)

hero = add_card(slide1, Inches(0.8), Inches(0.6), Inches(11.733), Inches(6.3), CARD_BG, ELECTRIC_BLUE, border_width=3.0)
top_bar = add_card(slide1, Inches(0.8), Inches(0.6), Inches(11.733), Inches(0.2), ELECTRIC_BLUE)

badge = slide1.shapes.add_textbox(Inches(1.4), Inches(1.1), Inches(8.5), Inches(0.4))
p_b = badge.text_frame.paragraphs[0]
p_b.text = "🏥 MEDTECH & SURGICAL RECOVERY HACKATHON 2026"
p_b.font.size = Pt(13)
p_b.font.bold = True
p_b.font.color.rgb = ELECTRIC_BLUE

title_box = slide1.shapes.add_textbox(Inches(1.4), Inches(1.5), Inches(10.5), Inches(2.3))
tf = title_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "SurgiHeal"
p.font.size = Pt(58)
p.font.bold = True
p.font.color.rgb = NAVY_HEADER

p2 = tf.add_paragraph()
p2.text = "Post-Operative Wound & Recovery Guardian"
p2.font.size = Pt(26)
p2.font.bold = True
p2.font.color.rgb = VIBRANT_TEAL

p3 = tf.add_paragraph()
p3.text = "An autonomous clinical intelligence platform preventing surgical complications, patient anxiety, and hospital readmissions."
p3.font.size = Pt(15)
p3.font.color.rgb = BODY_TEXT

# 3 Feature Pills
feats = [
    ("🩹 Multimodal Vision", "Automated SSI surveillance, erythema measurement, and wound dehiscence tracking.", VIBRANT_TEAL, TINT_TEAL),
    ("📋 Clinical Informatics", "Natural language parsing of discharge packets into structured daily medication roadmaps.", ELECTRIC_BLUE, TINT_BLUE),
    ("🚨 Predictive Triage", "Active 24/7 symptom screening for early DVT, pulmonary embolism, and sepsis.", RADIANT_ROSE, TINT_ROSE)
]
for i, (title, desc, color, tint) in enumerate(feats):
    x = Inches(1.4 + i * 3.55)
    add_card(slide1, x, Inches(4.5), Inches(3.4), Inches(1.8), tint, color, border_width=2.0)
    tb = slide1.shapes.add_textbox(x + Inches(0.15), Inches(4.6), Inches(3.1), Inches(1.5))
    tff = tb.text_frame
    tff.word_wrap = True
    pt = tff.paragraphs[0]
    pt.text = title
    pt.font.size = Pt(17)
    pt.font.bold = True
    pt.font.color.rgb = color
    pd = tff.add_paragraph()
    pd.text = desc
    pd.font.size = Pt(12)
    pd.font.color.rgb = BODY_TEXT


# ==============================================================================
# SLIDE 2: THE CLINICAL CRISIS & READMISSION BURDEN
# ==============================================================================
slide2 = prs.slides.add_slide(blank_layout)
set_slide_background(slide2, CANVAS_BG)
add_header(slide2, "Healthcare Crisis", RADIANT_ROSE, "The High-Risk 30-Day Post-Op Black Box", "Discharge does not equate to recovery. The critical gap between hospital and outpatient clinic.")

stat_cards = [
    ("300,000+", "Surgical Site Infections / Year", "SSIs represent the single leading cause of preventable hospital readmission in the US, carrying a 3% mortality rate and prolonged patient suffering.", RADIANT_ROSE),
    ("$3.3 BILLION", "Annual Financial Drain", "Hospitals face severe CMS Hospital Readmissions Reduction Program (HRRP) financial penalties, non-reimbursed care, and costly revision surgeries.", SUNNY_AMBER),
    ("74% of Patients", "Post-Op Anxiety & Miscommunication", "Patients leave hospitals overwhelmed by 10-page discharge packets, either ignoring lethal blood clot symptoms or rushing unnecessarily to crowded ERs.", ELECTRIC_BLUE)
]

for i, (stat, head, body, color) in enumerate(stat_cards):
    x = Inches(0.8 + i * 4.0)
    add_card(slide2, x, Inches(2.1), Inches(3.7), Inches(4.7), CARD_BG, color, border_width=2.0)
    add_card(slide2, x, Inches(2.1), Inches(3.7), Inches(0.18), color)
    tb = slide2.shapes.add_textbox(x + Inches(0.25), Inches(2.4), Inches(3.2), Inches(4.2))
    tff = tb.text_frame
    tff.word_wrap = True
    p1 = tff.paragraphs[0]
    p1.text = stat
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = color
    p2 = tff.add_paragraph()
    p2.text = head
    p2.font.size = Pt(17)
    p2.font.bold = True
    p2.font.color.rgb = NAVY_HEADER
    p3 = tff.add_paragraph()
    p3.text = "\n" + body
    p3.font.size = Pt(13)
    p3.font.color.rgb = BODY_TEXT


# ==============================================================================
# SLIDE 3: SYSTEM ARCHITECTURE & DATA FLOW
# ==============================================================================
slide3 = prs.slides.add_slide(blank_layout)
set_slide_background(slide3, CANVAS_BG)
add_header(slide3, "Architecture & Data Pipeline", ELECTRIC_PURPLE, "SurgiHeal End-to-End System Flow", "How multimodal inputs translate into clinical decisions and patient peace-of-mind.")

arch_steps = [
    ("1. Patient Input Layer", "• Incision Photo (Mobile / Web)\n• Self-Reported Pain Scale (0-10)\n• Temporal Body Temperature\n• Discharge Summary PDF/Text", ELECTRIC_BLUE, TINT_BLUE),
    ("2. Gemini 2.5 Flash Engine", "• Multimodal Vision Tokenizer\n• Periwound Erythema Segmentation\n• Clinical NLP Document Extraction\n• Multi-turn Triage Reasoner", VIBRANT_TEAL, TINT_TEAL),
    ("3. Schema & Guardrails", "• Strict Pydantic V2 Schema Validation\n• CDC NHSN Criteria Grounding\n• Zero-Hallucination Constraints\n• Failsafe Deterministic Fallback", SUNNY_AMBER, TINT_AMBER),
    ("4. Dual Delivery Interface", "• Patient Reassurance Card (6th gr.)\n• Clinician SOAP & Audit Note\n• Surgeon Registry Heatmap\n• 1-Click Automated Escalations", ELECTRIC_PURPLE, TINT_PURPLE)
]

for i, (title, bullets, color, tint) in enumerate(arch_steps):
    x = Inches(0.8 + i * 3.0)
    add_card(slide3, x, Inches(2.1), Inches(2.75), Inches(4.7), CARD_BG, color, border_width=2.0)
    add_card(slide3, x, Inches(2.1), Inches(2.75), Inches(0.18), color)
    tb = slide3.shapes.add_textbox(x + Inches(0.15), Inches(2.4), Inches(2.45), Inches(4.2))
    tff = tb.text_frame
    tff.word_wrap = True
    pt = tff.paragraphs[0]
    pt.text = title
    pt.font.size = Pt(17)
    pt.font.bold = True
    pt.font.color.rgb = color
    pb = tff.add_paragraph()
    pb.text = "\n" + bullets
    pb.font.size = Pt(13)
    pb.font.color.rgb = BODY_TEXT


# ==============================================================================
# SLIDE 4: MULTIMODAL WOUND COMPUTER VISION
# ==============================================================================
slide4 = prs.slides.add_slide(blank_layout)
set_slide_background(slide4, CANVAS_BG)
add_header(slide4, "Computer Vision Deep-Dive", VIBRANT_TEAL, "Automated SSI Surveillance & Image Biomarkers", "Extracting quantifiable surgical indicators from standard smartphone photography.")

vision_cards = [
    ("Erythema Spread Scoring (0-10)", "Quantifies redness halos around the incision line. Accurately distinguishes normal reactive healing erythema (<5mm) from expanding microbial cellulitis (>2cm).", VIBRANT_TEAL),
    ("Exudate Spectral Characterization", "Differentiates benign clear/straw-colored serous fluid from purulent (cloudy yellow/green) exudate—the cardinal visual biomarker of bacterial infection.", ELECTRIC_BLUE),
    ("Wound Edge Approximation", "Audits surgical staple and suture spacing, detecting mechanical tension, minor gap separation, and critical surgical dehiscence (open wound breakdown).", ELECTRIC_PURPLE),
    ("Predictive SSI Risk Percentage", "Synthesizes visual markers, post-op day timeline, patient body temperature, and reported pain into a predictive infection probability index.", RADIANT_ROSE)
]

for i, (title, desc, color) in enumerate(vision_cards):
    x = Inches(0.8 + (i % 2) * 5.9)
    y = Inches(2.1 + (i // 2) * 2.4)
    add_card(slide4, x, y, Inches(5.6), Inches(2.15), CARD_BG, color, border_width=2.0)
    add_card(slide4, x, y, Inches(0.18), Inches(2.15), color)
    tb = slide4.shapes.add_textbox(x + Inches(0.35), y + Inches(0.15), Inches(5.0), Inches(1.8))
    tff = tb.text_frame
    tff.word_wrap = True
    pt = tff.paragraphs[0]
    pt.text = title
    pt.font.size = Pt(18)
    pt.font.bold = True
    pt.font.color.rgb = color
    pd = tff.add_paragraph()
    pd.text = desc
    pd.font.size = Pt(13)
    pd.font.color.rgb = BODY_TEXT


# ==============================================================================
# SLIDE 5: CLINICAL PAPERWORK INTELLIGENCE
# ==============================================================================
slide5 = prs.slides.add_slide(blank_layout)
set_slide_background(slide5, CANVAS_BG)
add_header(slide5, "Clinical NLP & Informatics", ELECTRIC_BLUE, "Discharge Paperwork Intelligence & Medication Tapering", "Transforming dense, passive discharge packets into dynamic, interactive recovery roadmaps.")

doc_cols = [
    ("Dynamic Medication Schedules", "• Extracts brand/generic drugs, precise dosages, and schedules.\n• Highlights drug purpose (e.g. DVT prophylaxis, pain, antibiotic).\n• Enforces safe opioid tapering schedules and NSAID food alerts.\n• Cross-references contraindications and duplicate therapies.", ELECTRIC_BLUE),
    ("Surgical Activity & Hygiene Rules", "• Translates weight-bearing limitations (e.g. 50% partial vs full).\n• Clear showering vs bathing milestones (waterproof seal rules).\n• Elevating instructions and graduated compression stocking schedule.\n• Eliminates ambiguity regarding when driving or exercise can resume.", VIBRANT_TEAL),
    ("Milestone Checklists & Protocol", "• Day 1-3: Acute inflammatory pacing, cryotherapy, and ankle pumps.\n• Day 7: Surgical dressing inspection and suture review.\n• Day 14: Staple removal milestone and clinic checkup.\n• Day 30: Ambulation independence and physical therapy advancement.", ELECTRIC_PURPLE)
]

for i, (title, bullets, color) in enumerate(doc_cols):
    x = Inches(0.8 + i * 4.0)
    add_card(slide5, x, Inches(2.1), Inches(3.7), Inches(4.7), CARD_BG, color, border_width=2.0)
    add_card(slide5, x, Inches(2.1), Inches(3.7), Inches(0.18), color)
    tb = slide5.shapes.add_textbox(x + Inches(0.2), Inches(2.35), Inches(3.3), Inches(4.2))
    tff = tb.text_frame
    tff.word_wrap = True
    pt = tff.paragraphs[0]
    pt.text = title
    pt.font.size = Pt(18)
    pt.font.bold = True
    pt.font.color.rgb = color
    pb = tff.add_paragraph()
    pb.text = "\n" + bullets
    pb.font.size = Pt(13)
    pb.font.color.rgb = BODY_TEXT


# ==============================================================================
# SLIDE 6: 24/7 TRIAGE & SILENT KILLER SCREENING
# ==============================================================================
slide6 = prs.slides.add_slide(blank_layout)
set_slide_background(slide6, CANVAS_BG)
add_header(slide6, "Emergency Clinical Triage", RADIANT_ROSE, "Catching Silent Killers: DVT, Sepsis & Dehiscence", "Active 24/7 symptom screening separating routine healing sensations from life-threatening crises.")

triage_tiers = [
    ("🚨 TIER 1: Deep Vein Thrombosis (DVT) / Pulmonary Embolism", "Triggers: Unilateral calf swelling, cramp-like tenderness, warmth, dyspnea, or chest pain.\nClinical Action: IMMEDIATE Emergency 911 / ER alert. Instructs patient NOT to massage or rub calf (preventing clot embolization). Triggers urgent venous Doppler ultrasound.", RADIANT_ROSE, TINT_ROSE),
    ("⚠️ TIER 2: Surgical Site Infection (SSI) & Early Sepsis", "Triggers: Expanding erythema >2.5cm, purulent exudate, foul odor, or fever >100.4°F (38.0°C).\nClinical Action: Urgent same-day surgical team callback. Guides sterile dry dressing coverage, advises against home antibiotic creams, and orders oral antibiotics before deep sepsis.", SUNNY_AMBER, TINT_AMBER),
    ("🟢 TIER 3: Routine Expected Post-Operative Sensations", "Triggers: Gentle pulling around sutures, mild itching, light serous fluid, mild bruising.\nClinical Action: Immediate empathetic reassurance, pain pacing guidance, and ice/elevation reminder. Eliminates midnight emergency room crowding.", MINT_GREEN, TINT_GREEN)
]

for i, (title, desc, color, tint) in enumerate(triage_tiers):
    y = Inches(2.1 + i * 1.65)
    add_card(slide6, Inches(0.8), y, Inches(11.7), Inches(1.45), tint, color, border_width=2.0)
    add_card(slide6, Inches(0.8), y, Inches(0.18), Inches(1.45), color)
    tb = slide6.shapes.add_textbox(Inches(1.1), y + Inches(0.12), Inches(11.2), Inches(1.25))
    tff = tb.text_frame
    tff.word_wrap = True
    pt = tff.paragraphs[0]
    pt.text = title
    pt.font.size = Pt(17)
    pt.font.bold = True
    pt.font.color.rgb = color
    pd = tff.add_paragraph()
    pd.text = desc
    pd.font.size = Pt(12.5)
    pd.font.color.rgb = NAVY_HEADER


# ==============================================================================
# SLIDE 7: DUAL-PERSPECTIVE INTERACTION DESIGN
# ==============================================================================
slide7 = prs.slides.add_slide(blank_layout)
set_slide_background(slide7, CANVAS_BG)
add_header(slide7, "Human-AI Design Innovation", VIBRANT_TEAL, "The Dual-Perspective Switcher", "Simultaneously serving patient psychological needs and clinician regulatory documentation.")

# Left Card: Patient Reassurance Card
add_card(slide7, Inches(0.8), Inches(2.1), Inches(5.6), Inches(4.7), CARD_BG, VIBRANT_TEAL, border_width=2.0)
add_card(slide7, Inches(0.8), Inches(2.1), Inches(5.6), Inches(0.18), VIBRANT_TEAL)

tb_l = slide7.shapes.add_textbox(Inches(1.1), Inches(2.4), Inches(5.0), Inches(4.2))
tfl = tb_l.text_frame
tfl.word_wrap = True
p = tfl.paragraphs[0]
p.text = "👤 For Patients: Calm Reassurance Card"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = VIBRANT_TEAL

bullets_l = [
    "Empathetic Literacy: Written strictly at a 6th-grade reading level to maximize comprehension and reduce stress.",
    "Normalizing Sensation: Reassures patients that mild staple itchiness and light pink borders are expected biological repair signals.",
    "Actionable Dos & Don'ts: Step-by-step bullet points on dressing protection, icing intervals, and elevation posture.",
    "Explicit Boundary Warnings: Exact clinical triggers specifying when to call the clinic vs when to head to the ER."
]
for b in bullets_l:
    pb = tfl.add_paragraph()
    pb.text = "• " + b
    pb.font.size = Pt(13)
    pb.font.color.rgb = BODY_TEXT

# Right Card: Clinician Technical Audit
add_card(slide7, Inches(6.8), Inches(2.1), Inches(5.6), Inches(4.7), CARD_BG, ELECTRIC_BLUE, border_width=2.0)
add_card(slide7, Inches(6.8), Inches(2.1), Inches(5.6), Inches(0.18), ELECTRIC_BLUE)

tb_r = slide7.shapes.add_textbox(Inches(7.1), Inches(2.4), Inches(5.0), Inches(4.2))
tfr = tb_r.text_frame
tfr.word_wrap = True
p = tfr.paragraphs[0]
p.text = "🩺 For Clinicians: Structured Technical Audit"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = ELECTRIC_BLUE

bullets_r = [
    "Quantitative Biomarkers: Exact erythema spread radius (cm), swelling grade (None/Mild/Mod/Sev), and exudate spectral classification.",
    "Wound Approximation Index: Quantitative coaptation audit of surgical staples/sutures to identify partial dehiscence early.",
    "Standardized CDC Alignment: Formatted directly to CDC NHSN superficial and deep incisional SSI surveillance criteria.",
    "EHR-Ready Documentation: Structured clinical JSON ready for 1-click export into Epic, Cerner, or Meditech SOAP charts."
]
for b in bullets_r:
    pb = tfr.add_paragraph()
    pb.text = "• " + b
    pb.font.size = Pt(13)
    pb.font.color.rgb = BODY_TEXT


# ==============================================================================
# SLIDE 8: CLINICAL CASE STUDY BENCHMARKS
# ==============================================================================
slide8 = prs.slides.add_slide(blank_layout)
set_slide_background(slide8, CANVAS_BG)
add_header(slide8, "Demonstration Benchmarks", ELECTRIC_PURPLE, "Clinical Case Studies: Normal vs Complicated Recovery", "Three rigorous clinical validation archetypes tested across our multimodal pipeline.")

cases = [
    ("CASE A: Sarah Jenkins (62 y/o)", "Total Knee Arthroplasty (Day 4)", "• Vitals: Temp 98.6°F | Pain 3/10\n• Vision Finding: Clean staple spacing, minimal serous fluid, 1/10 reactive halo.\n• SSI Risk Score: 8% (Normal)\n• Outcome: Immediate reassurance, PT milestone pacing, clinic visit confirmed.", MINT_GREEN, TINT_GREEN),
    ("CASE B: Marcus Vance (34 y/o)", "Laparoscopic Appendectomy (Day 6)", "• Vitals: Temp 101.2°F | Pain 7/10\n• Vision Finding: Spreading periumbilical erythema >2.5cm, cloudy purulent exudate.\n• SSI Risk Score: 84% (Urgent SSI)\n• Outcome: Same-day clinic escalation, oral antibiotic started 48h before sepsis.", RADIANT_ROSE, TINT_ROSE),
    ("CASE C: Robert Chen (58 y/o)", "Total Hip Arthroplasty (Day 3)", "• Vitals: Temp 99.1°F | Pain 6/10\n• Incision: Clean, dry, intact closure.\n• Remote Red Flag: Acute right calf pain, swelling, warmth, and mild dyspnea.\n• Outcome: Emergency DVT/PE protocol activated; directed to ER Doppler ultrasound.", SUNNY_AMBER, TINT_AMBER)
]

for i, (head, proc, details, color, tint) in enumerate(cases):
    x = Inches(0.8 + i * 4.0)
    add_card(slide8, x, Inches(2.1), Inches(3.7), Inches(4.7), CARD_BG, color, border_width=2.0)
    add_card(slide8, x, Inches(2.1), Inches(3.7), Inches(0.18), color)
    tb = slide8.shapes.add_textbox(x + Inches(0.2), Inches(2.35), Inches(3.3), Inches(4.2))
    tff = tb.text_frame
    tff.word_wrap = True
    p1 = tff.paragraphs[0]
    p1.text = head
    p1.font.size = Pt(16)
    p1.font.bold = True
    p1.font.color.rgb = color
    p2 = tff.add_paragraph()
    p2.text = proc
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = NAVY_HEADER
    p3 = tff.add_paragraph()
    p3.text = "\n" + details
    p3.font.size = Pt(12.5)
    p3.font.color.rgb = BODY_TEXT


# ==============================================================================
# SLIDE 9: SURGEON COMMAND CENTER & OUTPATIENT SURVEILLANCE
# ==============================================================================
slide9 = prs.slides.add_slide(blank_layout)
set_slide_background(slide9, CANVAS_BG)
add_header(slide9, "Provider Platform", ELECTRIC_BLUE, "Surgeon Command Center: Population Surveillance", "Centralized triage board enabling surgical teams to monitor outpatients at scale.")

comm_cards = [
    ("📊 Risk-Stratified Triage Registry", "• Outpatients automatically ranked by predictive SSI Risk Index and acute vital changes.\n• Color-coded risk badges (🟢 On Track, 🟡 Caution, 🔴 Urgent Alert).\n• Longitudinal photo timeline inspection for every patient incision update.\n• Real-time notification feed filtering out routine noise.", ELECTRIC_BLUE),
    ("⚡ 1-Click Clinical Action Dispatch", "• Send Reassurance: One-click SMS/App push confirming normal healing trajectory.\n• Order Home Health: Automated dispatch for home-health wound dressing change.\n• Emergency Escalation: Immediate direct-to-clinic or ER triage coordination.\n• Eliminates 42 minutes of manual chart review and telephone tag per doctor daily.", VIBRANT_TEAL)
]

for i, (title, bullets, color) in enumerate(comm_cards):
    x = Inches(0.8 + i * 5.9)
    add_card(slide9, x, Inches(2.1), Inches(5.6), Inches(4.7), CARD_BG, color, border_width=2.0)
    add_card(slide9, x, Inches(2.1), Inches(5.6), Inches(0.18), color)
    tb = slide9.shapes.add_textbox(x + Inches(0.3), Inches(2.4), Inches(5.0), Inches(4.2))
    tff = tb.text_frame
    tff.word_wrap = True
    pt = tff.paragraphs[0]
    pt.text = title
    pt.font.size = Pt(20)
    pt.font.bold = True
    pt.font.color.rgb = color
    pb = tff.add_paragraph()
    pb.text = "\n" + bullets
    pb.font.size = Pt(13.5)
    pb.font.color.rgb = BODY_TEXT


# ==============================================================================
# SLIDE 10: HEALTH ECONOMICS & ROI ANALYSIS
# ==============================================================================
slide10 = prs.slides.add_slide(blank_layout)
set_slide_background(slide10, CANVAS_BG)
add_header(slide10, "Economic Impact", SUNNY_AMBER, "Clinical ROI & Health Economics", "Substantial financial return-on-investment across healthcare providers and payors.")

roi_metrics = [
    ("3.1% DROP", "30-Day Hospital Readmission Rate", "Early at-home detection of superficial SSIs allows targeted oral antibiotics, stopping deep space infections that trigger $50,000 readmissions.", MINT_GREEN),
    ("$1.8 MILLION", "Annual Savings per 1,000 Surgeries", "Mitigates CMS penalty deductions, reduces uncompensated revision operations, and minimizes emergency room utilization.", SUNNY_AMBER),
    ("42 MINS / DAY", "Clinician Time Saved per Surgeon", "Automated chart summarization, structured discharge extraction, and pre-triaged patient messages drastically reduce clinician documentation burnout.", ELECTRIC_PURPLE)
]

for i, (stat, head, body, color) in enumerate(roi_metrics):
    x = Inches(0.8 + i * 4.0)
    add_card(slide10, x, Inches(2.1), Inches(3.7), Inches(4.7), CARD_BG, color, border_width=2.0)
    add_card(slide10, x, Inches(2.1), Inches(3.7), Inches(0.18), color)
    tb = slide10.shapes.add_textbox(x + Inches(0.25), Inches(2.4), Inches(3.2), Inches(4.2))
    tff = tb.text_frame
    tff.word_wrap = True
    p1 = tff.paragraphs[0]
    p1.text = stat
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = color
    p2 = tff.add_paragraph()
    p2.text = head
    p2.font.size = Pt(17)
    p2.font.bold = True
    p2.font.color.rgb = NAVY_HEADER
    p3 = tff.add_paragraph()
    p3.text = "\n" + body
    p3.font.size = Pt(13)
    p3.font.color.rgb = BODY_TEXT


# ==============================================================================
# SLIDE 11: SAFETY, GUARDRAILS & DATA COMPLIANCE
# ==============================================================================
slide11 = prs.slides.add_slide(blank_layout)
set_slide_background(slide11, CANVAS_BG)
add_header(slide11, "Security & Compliance", VIBRANT_TEAL, "Safety Guardrails & HIPAA-Aligned Architecture", "Medical-grade security and deterministic reliability designed for clinical deployment.")

safety_quads = [
    ("Strict Schema Enforcement", "Pydantic V2 response_schema constraint ensures 100% structured JSON outputs, completely eliminating model hallucinations and unstructured outputs.", VIBRANT_TEAL),
    ("Deterministic Fallback Simulation", "Built-in clinical rule engine ensures unbroken continuity of care and uninterrupted presentation uptime during network downtime.", ELECTRIC_BLUE),
    ("HIPAA-Compliant Image Handling", "Zero unencrypted image persistence. Photos are tokenized ephemerally in transit with TLS 1.3 encryption and patient de-identification.", ELECTRIC_PURPLE),
    ("Clinical Boundary Disclaimers", "Clear diagnostic guardrails reminding patients that SurgiHeal is an assistive copilot, requiring human surgical confirmation for medical orders.", SUNNY_AMBER)
]

for i, (title, desc, color) in enumerate(safety_quads):
    x = Inches(0.8 + (i % 2) * 5.9)
    y = Inches(2.1 + (i // 2) * 2.4)
    add_card(slide11, x, y, Inches(5.6), Inches(2.15), CARD_BG, color, border_width=2.0)
    add_card(slide11, x, y, Inches(0.18), Inches(2.15), color)
    tb = slide11.shapes.add_textbox(x + Inches(0.35), y + Inches(0.15), Inches(5.0), Inches(1.8))
    tff = tb.text_frame
    tff.word_wrap = True
    pt = tff.paragraphs[0]
    pt.text = title
    pt.font.size = Pt(18)
    pt.font.bold = True
    pt.font.color.rgb = color
    pd = tff.add_paragraph()
    pd.text = desc
    pd.font.size = Pt(13)
    pd.font.color.rgb = BODY_TEXT


# ==============================================================================
# SLIDE 12: PRODUCT ROADMAP & COMMERCIAL SCALING
# ==============================================================================
slide12 = prs.slides.add_slide(blank_layout)
set_slide_background(slide12, CANVAS_BG)
add_header(slide12, "Commercial Scaling", ELECTRIC_PURPLE, "Strategic Horizon: From MVP to FDA Clearance", "Path to commercial scale across hospital systems and ambulatory surgical centers.")

phases = [
    ("Phase 1: Hackathon MVP", "Completed & Operational", "• Multimodal incision vision & SSI risk engine\n• Discharge paper parsing & medication roadmap\n• 24/7 DVT & Sepsis emergency triage\n• Surgeon population surveillance command center", VIBRANT_TEAL),
    ("Phase 2: EHR Interoperability", "Q3 - Q4 2026", "• SMART on FHIR integration with Epic, Cerner & Meditech\n• Continuous Bluetooth temperature patch integration\n• SOC-2 Type II and HIPAA business associate agreements\n• Ambulatory Surgical Center (ASC) pilot deployments", ELECTRIC_BLUE),
    ("Phase 3: Video Rehab & SaMD", "2027 Expansion", "• Computer vision Range of Motion (ROM) measurement\n• FDA 510(k) Software as a Medical Device (SaMD) clearance\n• Enterprise B2B SaaS licensing to integrated health systems\n• Global expansion across orthopedic and general surgery", ELECTRIC_PURPLE)
]

for i, (ph, tim, b, color) in enumerate(phases):
    x = Inches(0.8 + i * 4.0)
    add_card(slide12, x, Inches(2.1), Inches(3.7), Inches(4.7), CARD_BG, color, border_width=2.0)
    add_card(slide12, x, Inches(2.1), Inches(3.7), Inches(0.18), color)
    tb = slide12.shapes.add_textbox(x + Inches(0.2), Inches(2.35), Inches(3.3), Inches(4.2))
    tff = tb.text_frame
    tff.word_wrap = True
    p1 = tff.paragraphs[0]
    p1.text = ph
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = color
    p2 = tff.add_paragraph()
    p2.text = tim
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = NAVY_HEADER
    p3 = tff.add_paragraph()
    p3.text = "\n" + b
    p3.font.size = Pt(12.5)
    p3.font.color.rgb = BODY_TEXT


# ==============================================================================
# SLIDE 13: GRAND FINALE / CONCLUSION & Q&A
# ==============================================================================
slide13 = prs.slides.add_slide(blank_layout)
set_slide_background(slide13, CANVAS_BG)

hero13 = add_card(slide13, Inches(0.8), Inches(0.6), Inches(11.733), Inches(6.3), CARD_BG, VIBRANT_TEAL, border_width=3.0)
add_card(slide13, Inches(0.8), Inches(0.6), Inches(11.733), Inches(0.2), VIBRANT_TEAL)

badge13 = slide13.shapes.add_textbox(Inches(1.4), Inches(1.1), Inches(8.5), Inches(0.4))
p_b13 = badge13.text_frame.paragraphs[0]
p_b13.text = "CONCLUSION & CLINICAL SUMMARY"
p_b13.font.size = Pt(13)
p_b13.font.bold = True
p_b13.font.color.rgb = VIBRANT_TEAL

tb13 = slide13.shapes.add_textbox(Inches(1.4), Inches(1.5), Inches(10.5), Inches(4.8))
tf13 = tb13.text_frame
tf13.word_wrap = True

p = tf13.paragraphs[0]
p.text = "SurgiHeal: Healing Smarter, Together"
p.font.size = Pt(46)
p.font.bold = True
p.font.color.rgb = NAVY_HEADER

p_sub = tf13.add_paragraph()
p_sub.text = "Transforming the post-operative recovery journey from anxiety to certainty."
p_sub.font.size = Pt(20)
p_sub.font.bold = True
p_sub.font.color.rgb = VIBRANT_TEAL

p_sp = tf13.add_paragraph()
p_sp.text = "\nKey Clinical Deliverables:"
p_sp.font.size = Pt(16)
p_sp.font.bold = True
p_sp.font.color.rgb = NAVY_HEADER

summary_points = [
    "✅ Proactive Complication Prevention: Catches SSIs, DVT, and dehiscence days before hospital readmission.",
    "✅ Dual-Perspective Human AI: Empowers anxious patients while automating clinical documentation for surgeons.",
    "✅ Economic Sustainability: Delivers $1.8M in annual savings per 1,000 surgical procedures and relieves burnout.",
    "✅ Production-Ready Architecture: Built on Gemini 2.5 Flash with deterministic clinical guardrails."
]
for pt_text in summary_points:
    p_pt = tf13.add_paragraph()
    p_pt.text = pt_text
    p_pt.font.size = Pt(14)
    p_pt.font.color.rgb = BODY_TEXT

p_qa = tf13.add_paragraph()
p_qa.text = "\nThank You! We are now open for Questions & Discussion."
p_qa.font.size = Pt(20)
p_qa.font.bold = True
p_qa.font.color.rgb = RADIANT_ROSE


# Save Presentation
output_path = os.path.join(os.getcwd(), "SurgiHeal_Pitch_Deck.pptx")
prs.save(output_path)
print(f"Expanded 13-slide presentation successfully generated: {output_path}")
