"""
Node 1: Validate ML Prediction Input.
"""

from typing import Dict, Any

def validate_prediction_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Validates Squad A ML prediction input or applies fallback values."""
    if not state.get("equipment_id"):
        state["equipment_id"] = "EQ-001"
    
    if not state.get("equipment_type"):
        state["equipment_type"] = "Industrial Machine"

    if state.get("risk_score") is None:
        state["risk_score"] = 75.0

    if not state.get("predicted_failure"):
        state["predicted_failure"] = "Elevated Mechanical Vibration & Thermal Spike"

    if not state.get("model_confidence"):
        state["model_confidence"] = 0.88

    return state
