import pytest
from logic.schemas.prediction import MLPrediction
from logic.schemas.diagnostic import DiagnosticResult
from logic.agents.graph import DiagnosticEngine

def test_full_vertical_slice_end_to_end():
    """Verifies end-to-end slice: MLPrediction -> DiagnosticEngine -> LangGraph -> DiagnosticResult."""
    prediction = MLPrediction(
        equipment_id="EQ-001",
        equipment_type="CNC Milling Machine",
        risk_score=87.0,
        predicted_failure="Spindle Bearing Thermal Seizure",
        model_confidence=0.94,
        important_features=["Bearing Temperature", "Vibration RMS", "Spindle Load"]
    )

    engine = DiagnosticEngine()
    result = engine.analyze(prediction)

    assert isinstance(result, DiagnosticResult)
    assert result.equipment_id == "EQ-001"
    assert result.risk_score == 87.0
    assert result.predicted_failure == "Spindle Bearing Thermal Seizure"
    assert result.maintenance_priority == "CRITICAL"
    assert result.requires_human_review is True
    assert len(result.probable_root_causes) > 0
    assert len(result.evidence) > 0
    assert len(result.recommended_actions) > 0
    assert len(result.citations) > 0
