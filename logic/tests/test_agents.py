import pytest
from logic.schemas.prediction import MLPrediction
from logic.schemas.diagnostic import DiagnosticResult
from logic.agents.graph import DiagnosticEngine, diagnostic_graph

def test_diagnostic_engine_execution():
    engine = DiagnosticEngine()
    prediction = MLPrediction(
        equipment_id="EQ-001",
        equipment_type="CNC Milling Machine",
        risk_score=87.0,
        predicted_failure="Spindle Bearing Wear",
        model_confidence=0.94,
        important_features=["Bearing Temperature", "Vibration RMS"]
    )

    result = engine.analyze(prediction)

    assert isinstance(result, DiagnosticResult)
    assert result.equipment_id == "EQ-001"
    assert result.risk_score == 87.0
    assert result.maintenance_priority == "CRITICAL"
    assert result.requires_human_review is True
    assert len(result.recommended_actions) > 0
    assert len(result.evidence) > 0

def test_graph_direct_invocation():
    initial_state = {
        "equipment_id": "EQ-002",
        "equipment_type": "Hydraulic Press",
        "risk_score": 72.0,
        "predicted_failure": "Fluid Viscosity Loss",
        "model_confidence": 0.88
    }

    final_state = diagnostic_graph.invoke(initial_state)

    assert final_state["equipment_id"] == "EQ-002"
    assert final_state["maintenance_priority"] == "HIGH"
    assert final_state["requires_human_review"] is True
