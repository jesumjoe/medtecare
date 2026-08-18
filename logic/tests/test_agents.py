import pytest
from logic.schemas.prediction import MLPrediction
from logic.schemas.diagnostic import DiagnosticResult
from logic.agents.graph import DiagnosticEngine, diagnostic_graph
from logic.integration import adapt_squad_a_prediction

def test_squad_a_adapter_conversion():
    squad_a_raw = {
        "device_id": "DEV-88401",
        "device_name": "Smart Infusion Pump System",
        "classification": "Active Infusion Equipment",
        "risk_class": "Class IIb",
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

    prediction = adapt_squad_a_prediction(squad_a_raw)
    assert prediction.equipment_id == "DEV-88401"
    assert prediction.equipment_type == "Smart Infusion Pump System"
    assert prediction.risk_score == 87.0
    assert prediction.predicted_failure == "medical-device future-event risk"
    assert len(prediction.important_features) == 2
    assert "previous_recalls" in prediction.important_features[0]

def test_diagnostic_engine_execution():
    engine = DiagnosticEngine()
    prediction = MLPrediction(
        device_id="DEV-88401",
        device_name="Smart Infusion Pump System",
        risk_score=87.0,
        predicted_failure="medical-device future-event risk",
        model_confidence=0.87,
        classification="Active Infusion Equipment",
        risk_class="Class IIb",
        previous_recalls=1,
        important_features=["previous_recalls (SHAP impact: +0.42)"]
    )

    result = engine.analyze(prediction)

    assert isinstance(result, DiagnosticResult)
    assert result.equipment_id == "DEV-88401"
    assert result.risk_score == 87.0
    assert result.maintenance_priority == "CRITICAL"
    assert result.requires_human_review is True
    assert len(result.recommended_actions) > 0
    assert len(result.evidence) > 0

    # Ensure evidence categorization contains MODEL_EVIDENCE
    model_ev = [e for e in result.evidence if e.type == "MODEL_EVIDENCE"]
    assert len(model_ev) > 0

def test_graph_direct_invocation():
    initial_state = {
        "device_id": "DEV-99202",
        "device_name": "High-Field MRI Scanner 3T",
        "risk_score": 72.0,
        "predicted_failure": "medical-device future-event risk",
        "model_confidence": 0.88,
        "risk_class": "Class III",
        "previous_events": 2
    }

    final_state = diagnostic_graph.invoke(initial_state)

    assert final_state["device_id"] == "DEV-99202"
    assert final_state["maintenance_priority"] in ["HIGH", "CRITICAL"]
    assert final_state["requires_human_review"] is True
