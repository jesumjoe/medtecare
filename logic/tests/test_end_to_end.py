import pytest
from logic.schemas.prediction import MLPrediction
from logic.schemas.diagnostic import DiagnosticResult
from logic.agents.graph import DiagnosticEngine
from logic.integration import adapt_squad_a_prediction


def test_full_vertical_slice_end_to_end():
    """Verifies end-to-end slice: Squad A Payload -> Adapter -> DiagnosticEngine -> LangGraph -> DiagnosticResult."""
    raw_squad_a_payload = {
        "device_id": "DEV-88401",
        "device_name": "Smart Infusion Pump System",
        "classification": "Active Infusion Equipment",
        "risk_class": "Class IIb",
        "country": "Germany",
        "manufacturer": "B. Braun Melsungen AG",
        "future_event_probability": 0.87,
        "prediction": 1,
        "risk_level": "HIGH",
        "model_confidence": 0.87,
        "previous_events": 3,
        "previous_recalls": 1,
        "previous_safety_notices": 2,
        "years_in_service": 4.5,
        "feature_drivers": [
            {"feature": "previous_recalls", "impact": 0.42},
            {"feature": "previous_safety_notices", "impact": 0.28}
        ]
    }

    prediction = adapt_squad_a_prediction(raw_squad_a_payload)
    engine = DiagnosticEngine()
    result = engine.analyze(prediction)

    assert isinstance(result, DiagnosticResult)
    assert result.equipment_id == "DEV-88401"
    assert result.equipment_type == "Smart Infusion Pump System"
    assert result.risk_score == 87.0
    assert result.predicted_failure == "medical-device future-event risk"
    assert result.maintenance_priority == "CRITICAL"
    assert result.requires_human_review is True
    assert len(result.probable_root_causes) > 0
    assert len(result.evidence) > 0
    assert len(result.recommended_actions) > 0
    
    # Verify strict safety recommendations (no physical component replacements like bearings/spindles)
    rec_titles = [a.title for a in result.recommended_actions]
    assert any("Safety" in t or "Notice" in t or "Monitoring" in t for t in rec_titles)
    assert not any("spindle" in t.lower() or "bearing" in t.lower() for t in rec_titles)
