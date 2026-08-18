import pytest
from logic.schemas.prediction import MLPrediction
from logic.schemas.diagnostic import DiagnosticResult
from logic.integration import adapt_squad_a_prediction
from logic.agents.graph import DiagnosticEngine
from logic.llm.diagnostic import LLMDiagnosticReasoner


def test_adapter_probability_scaling():
    payload = {
        "device_id": "DEV-101",
        "device_name": "Ventilator V-5",
        "future_event_probability": 0.42,
        "prediction": 0
    }
    pred = adapt_squad_a_prediction(payload)
    assert pred.risk_score == 42.0
    assert pred.predicted_failure == "medical-device future-event risk"


def test_model_evidence_preservation():
    reasoner = LLMDiagnosticReasoner()
    ctx = {
        "future_event_probability": 0.85,
        "classification": "Active Diagnostic Device",
        "risk_class": "Class III",
        "manufacturer": "MedTech OEM",
        "previous_recalls": 2,
        "previous_events": 5,
        "previous_safety_notices": 1,
        "years_in_service": 6.2
    }
    result = reasoner.synthesize_diagnosis(
        equipment_id="DEV-500",
        equipment_type="Defibrillator X",
        risk_score=85.0,
        predicted_failure="medical-device future-event risk",
        model_confidence=0.85,
        important_features=["previous_recalls (SHAP impact: +0.51)"],
        telemetry=[],
        retrieved_documents=[],
        historical_context=[],
        device_context=ctx
    )

    ev_types = [e.type for e in result.evidence]
    assert "MODEL_EVIDENCE" in ev_types
    assert "AI_INFERENCE" in ev_types

    # Ensure model evidence text preserves fields
    model_ev_descriptions = " ".join([e.description for e in result.evidence if e.type == "MODEL_EVIDENCE"])
    assert "85.0/100" in model_ev_descriptions
    assert "Class III" in model_ev_descriptions
    assert "MedTech OEM" in model_ev_descriptions
    assert "previous_recalls" in model_ev_descriptions


def test_insufficient_evidence_and_human_review():
    engine = DiagnosticEngine()
    prediction = MLPrediction(
        device_id="DEV-EMPTY",
        device_name="Unknown Device",
        risk_score=50.0,
        predicted_failure="medical-device future-event risk"
    )

    result = engine.analyze(prediction)
    assert result.requires_human_review is True
    assert isinstance(result.diagnosis, str)
    assert len(result.recommended_actions) > 0


def test_probabilistic_language_enforcement():
    reasoner = LLMDiagnosticReasoner()
    result = reasoner._generate_fallback_diagnosis(
        equipment_id="DEV-777",
        equipment_type="Infusion Pump",
        risk_score=90.0,
        predicted_failure="medical-device future-event risk",
        model_confidence=0.90,
        important_features=["previous_recalls"],
        telemetry=[],
        retrieved_documents=[],
        historical_context=[],
        evidence_list=[],
        ctx={"previous_recalls": 2, "years_in_service": 5.0}
    )

    assert "definitely fail" not in result.explanation.lower()
    assert "probabilistic" in result.explanation.lower() or "risk" in result.explanation.lower()
