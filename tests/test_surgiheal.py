import pytest
import os
from sample_data import (
    create_synthetic_incision_image,
    get_case_image_bytes,
    get_progression_image_bytes,
    SAMPLE_CASES
)
from models import WoundAnalysisResult, DischargeSummary, TriageAssessment
import ai_service


def test_synthetic_image_generation():
    img_normal = create_synthetic_incision_image("normal")
    assert isinstance(img_normal, bytes)
    assert len(img_normal) > 1000

    img_infection = create_synthetic_incision_image("infection")
    assert isinstance(img_infection, bytes)
    assert len(img_infection) > 1000


def test_realistic_case_images():
    for case_key in ["case_a", "case_custom"]:
        img_bytes = get_case_image_bytes(case_key)
        assert isinstance(img_bytes, bytes)
        assert len(img_bytes) > 10000
        # Verify file exists on disk
        img_path = SAMPLE_CASES[case_key]["image_path"]
        assert os.path.exists(img_path)


def test_progression_images():
    img_day1 = get_progression_image_bytes("day_1")
    assert isinstance(img_day1, bytes)
    assert len(img_day1) > 10000

    img_day14 = get_progression_image_bytes("day_14")
    assert isinstance(img_day14, bytes)
    assert len(img_day14) > 10000


def test_sample_cases_structure():
    assert "case_a" in SAMPLE_CASES
    assert "case_custom" in SAMPLE_CASES

    case_a = SAMPLE_CASES["case_a"]
    assert case_a["name"] == "Sarah Jenkins"
    assert isinstance(case_a["discharge"], DischargeSummary)
    assert isinstance(case_a["expected_analysis"], WoundAnalysisResult)

    case_custom = SAMPLE_CASES["case_custom"]
    assert case_custom["id"] == "PAT-USER"
    assert isinstance(case_custom["discharge"], DischargeSummary)


def test_ai_service_wound_analysis_normal():
    img = create_synthetic_incision_image("normal")
    result = ai_service.analyze_wound_image(
        image_bytes=img,
        patient_context={
            "procedure_name": "Total Knee Arthroplasty",
            "post_op_day": 4,
            "temperature_f": 98.6,
            "reported_pain": 2
        }
    )
    assert isinstance(result, WoundAnalysisResult)
    assert result.healing_status == "Normal / On Track"
    assert result.infection_risk_percentage < 30
    assert len(result.action_recommendations) > 0


def test_ai_service_wound_analysis_fever_infection():
    img = create_synthetic_incision_image("infection")
    result = ai_service.analyze_wound_image(
        image_bytes=img,
        patient_context={
            "procedure_name": "Laparoscopic Appendectomy",
            "post_op_day": 6,
            "temperature_f": 101.2,
            "reported_pain": 7
        }
    )
    assert isinstance(result, WoundAnalysisResult)
    assert "Urgent" in result.healing_status
    assert result.infection_risk_percentage > 60
    assert len(result.red_flags) > 0


def test_triage_chat_dvt_detection():
    assessment = ai_service.screen_symptoms_chat(
        user_query="My right calf is swollen, throbbing, and hot to touch. I also have slight shortness of breath.",
        patient_profile={"name": "Robert Chen", "post_op_day": 3, "procedure_name": "Hip Replacement"}
    )
    assert isinstance(assessment, TriageAssessment)
    assert "Emergency" in assessment.urgency_level
    assert "DVT" in assessment.suspected_condition or "Thrombosis" in assessment.suspected_condition
    assert any("911" in action or "emergency" in action.lower() for action in assessment.immediate_actions)


def test_triage_chat_routine():
    assessment = ai_service.screen_symptoms_chat(
        user_query="My incision feels slightly itchy around the staples.",
        patient_profile={"name": "Sarah", "post_op_day": 4, "procedure_name": "Knee Replacement"}
    )
    assert isinstance(assessment, TriageAssessment)
    assert "Routine" in assessment.urgency_level
