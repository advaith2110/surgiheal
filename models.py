from typing import List, Optional
from pydantic import BaseModel, Field


class WoundAnalysisResult(BaseModel):
    healing_status: str = Field(
        description="Overall status: 'Normal / On Track', 'Borderline / Needs Monitoring', or 'Urgent / High Risk of SSI'"
    )
    erythema_score: int = Field(
        description="Redness spread and intensity from 0 (none) to 10 (severe diffuse cellulitis)"
    )
    swelling_level: str = Field(
        description="'None', 'Mild', 'Moderate', or 'Severe'"
    )
    drainage_type: str = Field(
        description="'None', 'Serous (Clear/Yellowish)', 'Sanguineous (Bloody)', or 'Purulent (Pus/Cloudy)'"
    )
    edge_approximation: str = Field(
        description="'Well-approximated (Cleanly Closed)', 'Minor Gap / Separation', or 'Dehiscence (Open Wound)'"
    )
    infection_risk_percentage: int = Field(
        description="Estimated probability (0-100%) of early surgical site infection"
    )
    clinical_observations: List[str] = Field(
        default_factory=list,
        description="Objective clinical signs observed in incision margin, sutures/staples, periwound tissue"
    )
    patient_plain_english_summary: str = Field(
        description="Empathetic, clear, calm explanation tailored for the patient"
    )
    red_flags: List[str] = Field(
        default_factory=list,
        description="Critical warning flags requiring surgical escalation (empty if none)"
    )
    action_recommendations: List[str] = Field(
        default_factory=list,
        description="Step-by-step guidance for the patient (e.g. dressing protocol, hygiene, doctor contact)"
    )


class MedicationItem(BaseModel):
    name: str = Field(description="Generic or brand medication name")
    dosage: str = Field(description="Dose and unit (e.g., 500mg, 10ml)")
    frequency: str = Field(description="How often to take (e.g. Twice daily with food)")
    purpose: str = Field(description="Clinical reason (e.g., Pain control, Blood clot prevention, Infection prevention)")
    instructions: str = Field(description="Important precautions or tapering rules")


class RecoveryMilestone(BaseModel):
    day_offset: int = Field(description="Postoperative day target (e.g., 3, 7, 14)")
    title: str = Field(description="Milestone name (e.g., Suture removal, First shower without dressing)")
    description: str = Field(description="Details on what to expect or achieve")
    is_completed: bool = False


class DischargeSummary(BaseModel):
    procedure_name: str = Field(description="Type of surgery performed")
    surgery_date: str = Field(description="Date of procedure")
    surgeon_name: str = Field(description="Attending surgeon name")
    weight_bearing_status: str = Field(description="e.g., Non-weight bearing, Partial 50%, Full as tolerated")
    showering_guidelines: str = Field(description="When and how the patient may bathe/shower")
    wound_care_routine: List[str] = Field(default_factory=list, description="Daily steps for dressing changes and cleaning")
    medications: List[MedicationItem] = Field(default_factory=list, description="Prescribed post-op medications")
    emergency_symptoms: List[str] = Field(default_factory=list, description="Red flag signs that demand calling the surgeon")
    milestones: List[RecoveryMilestone] = Field(default_factory=list, description="Planned recovery milestones")


class TriageAssessment(BaseModel):
    urgency_level: str = Field(
        description="'Routine / Reassuring', 'Caution / Self-Monitor', 'Urgent / Contact Surgeon', or 'Emergency / Call 911 / Go to ER'"
    )
    suspected_condition: str = Field(
        description="Clinical impression (e.g. 'Normal Healing Response', 'Suspected DVT', 'Early SSI', 'Wound Hematoma')"
    )
    primary_concern: str = Field(
        description="Main risk or symptomatic trigger"
    )
    immediate_actions: List[str] = Field(
        default_factory=list,
        description="Immediate actions for the patient to take right now"
    )
    clinical_rationale: str = Field(
        description="Reasoning linking reported symptoms to the assigned urgency"
    )


class PatientProfile(BaseModel):
    patient_id: str
    name: str
    age: int
    procedure_name: str
    surgery_date: str
    post_op_day: int
    surgeon_name: str
    last_reported_pain: int = 2  # 0 to 10
    last_temp_f: float = 98.6
    wound_history: List[dict] = Field(default_factory=list)
